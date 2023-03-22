# GUI.py
import pygame
pygame.font.init()
from dokusan import generators


   
#This is a class that will be used to house the grid of the sudoku board
#I have chosen an object oriented approach as it allows both the grid and the squares to house their own attributes and methods
#This makes the project easier to interpret from an outside point of view as the methods within each are used
#To draw the grid and squares, along with solving the board
  
class Grid:


  def __init__(self, rows, cols, width, height, win):
    self.rows = rows
    self.cols = cols
    # initialises each square, 
    self.squares = [[Square(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
    self.width = width
    self.height = height
    self.model = None
    self.update_model()
    self.selected = None
    self.win = win

  sudokunumbers = [int(x) for x in str(generators.random_sudoku(avg_rank=50))]
#sudoku generator returns long string of numbers so this part breaks it down into a 2d list which the algorithm can interpret.
  list1 = []
  for j in range(9):
    list1.append(sudokunumbers[j])
  list2 = []
  for i in range(9):
    list2.append(sudokunumbers[i + 9])
  list3 = []
  for i in range(9):
    list3.append(sudokunumbers[i + 18])
  list4 = []
  for i in range(9):
    list4.append(sudokunumbers[i + 27])
  list5 = []
  for i in range(9):
    list5.append(sudokunumbers[i + 36])
  list6 = []
  for i in range(9):
    list6.append(sudokunumbers[i + 45])
  list7 = []
  for i in range(9):
    list7.append(sudokunumbers[i + 54])
  list8 = []
  for i in range(9):
    list8.append(sudokunumbers[i + 63])
  list9 = []
  for i in range(9):
    list9.append(sudokunumbers[i + 72])

  board = [list1, list2, list3, list4, list5, list6, list7, list8, list9]

  #used to update the board user can see with board used to see if inputs are valid
  def update_model(self):
    self.model = [[self.squares[i][j].value for j in range(self.cols)]
                  for i in range(self.rows)]
    
  #used to place numbers in squares
  def place(self, val):
    row, col = self.selected
    if self.squares[row][col].value == 0:
      self.squares[row][col].set(val)
      self.update_model()

      if valid(self.model, val, (row, col)) and self.solve():
        return True
      else:
        #if not valid sets back to 0
        self.squares[row][col].set(0)
        self.squares[row][col].set_temp(0)
        self.update_model()
        return False
        
  #sets temporary 'sketch' value in the visual board so users can attempt to solve board before inputting numbers
  #as if a user inputs a number, if it gets put on the board they know it is the correct number
  #whereas if it does not, then they know it is incorrect which could make the boards easily solvable
  #if user didn't want to try for themselves without using autosolver
  def sketch(self, val):
    row, col = self.selected
    self.squares[row][col].set_temp(val)
    
    # Draw Grid Lines
  def draw(self):
    gap = self.width / 9
    for i in range(self.rows + 1):
      #thickness varies to make the board easier to interpret, as the 3x3 boxes are clearly defined
      #every third line is thicker to illustrate this
      if i % 3 == 0 and i != 0:
        thick = 5
      else:
        thick = 2
      #parameters for drawing the line include the surface (win),the colour, the start position, the end position, and thickness)
      pygame.draw.line(self.win, (0, 0, 0), (0, i * gap),
                       (self.width, i * gap), thick)
      pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0),
                       (i * gap, self.height), thick)

    # Draw squares
    for i in range(self.rows):
      for j in range(self.cols):
        self.squares[i][j].draw(self.win)

  def select(self, row, col):
    # Deselects all other squares so new one can be selected
    if (row,col) == (10,10):
      for i in range(self.rows):
        for j in range(self.cols):
          self.squares[i][j].selected = False
          
    else: 
      for i in range(self.rows):
        for j in range(self.cols):
          self.squares[i][j].selected = False
      #selects new square
      self.squares[row][col].selected = True
      self.selected = (row, col)

  def clear(self):
    #deletes temperary value from seleced square
    row, col = self.selected
    if self.squares[row][col].value == 0:
      self.squares[row][col].set_temp(0)

  def click(self, pos):
    #parameter pos returns (x,y)
    #used to determine what box has been pressed (can't be off of the screen)
    if pos[0] < self.width and pos[1] < self.height:
      gap = self.width / 9
      x = pos[0] // gap
      y = pos[1] // gap
      #returns the index of square pressed as the x coordinate//the size of each box = index
      return (int(y), int(x))
    else:
      self.selected = None
      

  
  def solve(self):
    #autosolver
    #first step is to find first empty square
    find = find_empty(self.model)
    if not find:
      #if no empty squares, board is solved
      return True
    else:
      #splits find (which is two variables) into row variable and column variable
      row, col = find

    for i in range(1, 10):
      #checks number 1-9 to see if they're valid in given square using function valid()
      if valid(self.model, i, (row, col)):
        #if so, inputs valid number
        self.model[row][col] = i
        #checks to see if board is solved with new number
        if self.solve():
          return True
          #if not, changes value back to 0
        self.model[row][col] = 0

    return False

    
#function to show autosolver working visually, works same as solve() but draws each number
#tried on to board 
  def solve_gui(self):
    self.update_model()
    find = find_empty(self.model)
    if not find:
      return True
    else:
      row, col = find

    for i in range(1, 10):
      if valid(self.model, i, (row, col)):
        self.model[row][col] = i
        self.squares[row][col].set(i)
        self.squares[row][col].draw_change(self.win, True)
        self.update_model()
        pygame.display.update()
        pygame.time.delay(100)

        if self.solve_gui():
          return True

        self.model[row][col] = 0
        self.squares[row][col].set(0)
        self.update_model()
        self.squares[row][col].draw_change(self.win, False)
        pygame.display.update()
        pygame.time.delay(100)

    return False


#class for each square on the grid
class Square:
  #establishes that there are 9 rows, and 9 columns. 
  #also makes it easier to increase or decrease if I want to in future
  rows = 9
  cols = 9

  #initialises each square
  def __init__(self, value, row, col, width, height):
    self.value = value
    self.temp = 0
    self.row = row
    self.col = col
    self.width = width
    self.height = height
    self.selected = False

  #draws squares and values in squares
  def draw(self, win):
    fnt = pygame.font.SysFont("comicsans", 40)

    gap = self.width / 9
    x = self.col * gap
    y = self.row * gap

    if self.temp != 0 and self.value == 0:
      #creates variable for font including string, colour, font and thickness
      text = fnt.render(str(self.temp), 1, (128, 128, 128))
      #'blits' the text on to the square, positioning it                                                                                     centrally using the x and y coordinates found previously.
      win.blit(text, (x + 5, y + 5))
    elif not (self.value == 0):
      text = fnt.render(str(self.value), 1, (0, 0, 0))
      win.blit(text, (x + (gap / 2 - text.get_width() / 2), y +
                      (gap / 2 - text.get_height() / 2)))
    #makes selected square thicker with colour used in website pages
    if self.selected:
      pygame.draw.rect(win, (135,47,58), (x, y, gap, gap), 5)

  #updates the numbers when new number is placed in
  def draw_change(self, win, g=True):
    fnt = pygame.font.SysFont("comicsans", 40)

    gap = self.width / 9
    x = self.col * gap
    y = self.row * gap

    #draws white square over square being changed
    pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

    text = fnt.render(str(self.value), 1, (0, 0, 0))
    win.blit(text, (x + (gap / 2 - text.get_width() / 2), y +
                    (gap / 2 - text.get_height() / 2)))
    if g:
      #turns valid submissions green when autosolved
      pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 2)
    else:
      pygame.draw.rect(win, (0,0,0), (x, y, gap, gap), 1)

  def set(self, val):
    self.value = val

  def set_temp(self, val):
    self.temp = val

    
colour_inactive = pygame.Color('grey0')
colour_active = pygame.Color('firebrick1')
fnt = pygame.font.SysFont('', 25)
notice = pygame.font.SysFont('', 20)   

class emailBox:

    def __init__(self, x, y, w, h, text='' ):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colour_inactive
        self.text = text
        self.txt_surface = fnt.render('', True, self.color)
        self.active = False
        self.enterbutton = pygame.Rect(x+w+30,y,50,h)
      
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            elif self.enterbutton.collidepoint(event.pos):
                with open('emails.txt', 'a') as f:
                    f.write(self.text + '\n') 
                print(self.text)
                self.text = ''           
            else:
                self.active = False
                self.text = ''
            # Change the current color of the input box.
            self.color = colour_active if self.active else colour_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                  self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = fnt.render(self.text, True, colour_inactive)
                  
  


    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+7))
        win.blit(notice.render(("Enter email to receive updates on the game below!"), True, pygame.Color('black')), (self.rect.x, self.rect.y-20))
        # Blit the rect.
        pygame.draw.rect(win, self.color, self.rect, 2)
        pygame.draw.rect(win,"black", self.enterbutton, 2)
        win.blit(notice.render("Enter", True, pygame.Color('black')), (self.enterbutton.x + self.enterbutton.w/7, self.rect.y + self.rect.h/4))

          
def find_empty(bo):
  for i in range(len(bo)):
    for j in range(len(bo[0])):
      if bo[i][j] == 0:
        return (i, j)  # row, col

  return None
  
def valid(bo, num, pos):
  # Checks if value is valid across the row
  for i in range(len(bo[0])):
    if bo[pos[0]][i] == num and pos[1] != i:
      return False

  # Checks if value is valid across the column
  for i in range(len(bo)):
    if bo[i][pos[1]] == num and pos[0] != i:
      return False

  # Checks if value is valid within the 3x3 box
  box_x = pos[1] // 3
  box_y = pos[0] // 3

  for i in range(box_y * 3, box_y * 3 + 3):
    for j in range(box_x * 3, box_x * 3 + 3):
      if bo[i][j] == num and (i, j) != pos:
        return False

  return True

#redraws the window 
def redraw_window(win, board, emailBox):
  win.fill((255, 255, 255))

  # Draw grid and board
  board.draw()
  emailBox.draw(win)




#main function which combines the rest
def main():
  win = pygame.display.set_mode((540, 650))
  pygame.display.set_caption("Sudoku")
  board = Grid(9, 9, 540, 540, win)
  input_box1 = emailBox(10, 580, 300, 32)
  key = None
  run = True
  while run:

    #returns which button the user is pressing on their keyboard
    for event in pygame.event.get():    
      input_box1.handle_event(event)
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          key = 1
        if event.key == pygame.K_2:
          key = 2
        if event.key == pygame.K_3:
          key = 3
        if event.key == pygame.K_4:
          key = 4
        if event.key == pygame.K_5:
          key = 5
        if event.key == pygame.K_6:
          key = 6
        if event.key == pygame.K_7:
          key = 7
        if event.key == pygame.K_8:
          key = 8
        if event.key == pygame.K_9:
          key = 9
        if event.key == pygame.K_KP1:
          key = 1
        if event.key == pygame.K_KP2:
          key = 2
        if event.key == pygame.K_KP3:
          key = 3
        if event.key == pygame.K_KP4:
          key = 4
        if event.key == pygame.K_KP5:
          key = 5
        if event.key == pygame.K_KP6:
          key = 6
        if event.key == pygame.K_KP7:
          key = 7
        if event.key == pygame.K_KP8:
          key = 8
        if event.key == pygame.K_KP9:
          key = 9
        if event.key == pygame.K_DELETE:
          board.clear()
          key = None
#spacebar for autosolver
        if event.key == pygame.K_SPACE:
          board.solve_gui()
#return key for entering a number
        if event.key == pygame.K_RETURN:
          #if number inputted is valid, it gets placed if not the input is erased and key is set to none
          i, j = board.selected
          if board.squares[i][j].temp != 0:
            if not board.place(board.squares[i][j].temp):
              key = None


          
#gets position of mouse when clicked to determine the square clicked on
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        clicked = board.click(pos)
        if clicked:
          board.select(clicked[0], clicked[1])
          key = None
        else:
          board.select(10,10)
          key = None
          

    if board.selected and key != None:
      #if a square is selected and the key is not none, that key variable is inputted
      board.sketch(key)
      
#window must be updated with every loop
    redraw_window(win, board, input_box1)
    pygame.display.update()



main()
pygame.quit()

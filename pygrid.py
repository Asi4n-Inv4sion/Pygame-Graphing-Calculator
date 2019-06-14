# --------------------------------------------------------------------
# Program: Grid module for pygame
# Author: Leo Wang
# Date: April 12th
# Input: Input attributes for grid objects, and parameters
# for some methods
# Output: Creates 3 child classes of grid that have click
# detection, highlighting, and other methods.
# --------------------------------------------------------------------

import pygame
from abc import ABCMeta, abstractmethod

#pygame.init()

#screen = pygame.display.set_mode((400,400))

# parent class
class Grid(object):

    '''
    Attributes:
        width: width of the grid
        height: height of the grid
        rows: number of rows in the grid
        columns: number of columns in the grid
        x: x cord of the top left
        y: y cord of the top left
        cell_width: width of a single cell
        cell_height: height of a single cell
        font: font name and size
        font_colour: the colour of the font
    '''

    __metaclass__ = ABCMeta

    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=False):
        self.rect = rect
        self.rows = rows
        self.columns = columns
        self.font = font
        self.font_colour = font_colour
        self.text = text
        self.gap = gap
        self.outline = outline
        self.visible = visible
        # non-optional
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.cell_width = rect[2]/columns
        self.cell_height = rect[3]/rows

    @staticmethod
    def printText(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        textbox.center = (x, y)
        canvas.blit(theText, textbox)

    # draws the grid and text
    def drawGrid(self,screen,colour):
        if self.visible == True:
            font = pygame.font.SysFont(self.font[0],self.font[1])
            for r in range(self.rows):
                for c in range(self.columns):
                    pygame.draw.rect(screen,colour,(self.x+(self.cell_width)*c+self.gap,self.y+(self.cell_height)*r+self.gap,self.cell_width-self.gap*2,self.cell_height-self.gap*2),self.outline)
                    if r*self.columns+c < len(self.text):
                        self.printText(self.text[r*self.columns+c],font,screen,self.x+(self.cell_width)*c + self.cell_width/2,self.y+(self.cell_height)*r+self.cell_height/2)

    # returns what cell the x and y coords belong too
    def mouseOverCell(self,mouseX,mouseY):
        if self.x < mouseX < self.x+self.width and self.y < mouseY < self.y+self.height and self.visible == True:
            for r in range(self.rows):
                for c in range(self.columns):
                    if (self.x+(self.cell_width)*c+self.gap) < mouseX < (self.x+(self.cell_width)*c-self.gap)+self.cell_width and (self.y+(self.cell_height)*r+self.gap) < mouseY < (self.y+(self.cell_height)*r-self.gap) + self.cell_height:
                        # Returns the number cell the mouse is hovered over
                        return self.columns*r + c

    # highlight all given cells
    def highlightCells(self,screen,cell_list,colour):
        for x in cell_list:
            r = x // self.columns
            c = x % self.columns
            rect = (self.x+(self.cell_width)*c+self.gap,self.y+(self.cell_height)*r+self.gap,self.cell_width-self.gap*2,self.cell_height-self.gap*2)
            self.blit_alpha(screen,rect,colour,100)

    @staticmethod
    def blit_alpha(screen,rect,colour,alpha):
        s = pygame.Surface((rect[2],rect[3]))
        s.set_alpha(alpha)
        s.fill(colour)
        screen.blit(s,(rect[0],rect[1]))

    def highlightSelectedCell(self,screen):
        if self.selectedFunction != None:
            self.highlightCells(screen,[self.selectedFunction],(0,0,200))

    # returns the type of grid class
    @abstractmethod
    def gridType(self):
        pass

class Menu(Grid):

    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=True,growth=1):
        Grid.__init__(self,rect,rows,columns,outline,gap,font,font_colour,text,visible)
        self.growth = growth

    # creates an outline slightly bigger than the cell
    def growCell(self,screen,cell,colour):
        r = (cell // self.columns)
        c = (cell % self.columns)
        pygame.draw.rect(screen,colour,(self.x+(self.cell_width)*c+self.gap-self.growth, self.y+(self.cell_height)*r+self.gap-self.growth,self.cell_width-self.gap*2+self.growth*2,self.cell_height-self.gap*2+self.growth*2),self.growth)

    def gridType(self):
        return "Menu"

class WordList(Grid):

    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=True):
        Grid.__init__(self,rect,rows,columns,outline,gap,font,font_colour,text,visible)
        self.found_words = []

    # cross out the inputted cell with a line
    def crossOut(self,screen,cell,colour=(0,0,0),width=1):
        r = (cell // self.columns)
        c = (cell % self.columns)
        x = self.x+(self.cell_width)*c + self.gap
        y = self.y+(self.cell_height)*r + self.cell_height/2
        pygame.draw.line(screen,colour,(x,y),(x+self.cell_width-self.gap*3,y))

    # cross out all self.found_words
    def crossOutFoundWords(self,screen,colour=(0,0,0),width=1):
        for w in self.found_words:
            self.crossOut(screen,w,colour,width)

    # pass a list of words puts them in self.found_words
    def addFoundWords(self,wordList):
        for w in wordList:
            if w not in self.found_words:
                self.found_words.append(w)

    # checks if all the words are found
    def allWordsFound(self):
        if len(self.found_words) == len(self.text):
            return True
        else:
            return False

    def gridType(self):
        return "WordList"

class LetterGrid(Grid):

    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=True):
        Grid.__init__(self,rect,rows,columns,outline,gap,font,font_colour,text,visible)
        self.selected_letters = []
        self.cell_list = []
        self.found_letterCells = []
        self.found_words = []

    # blit a rectangle with optional alpha
    @staticmethod
    def blit_alpha(screen,rect,colour,alpha):
        s = pygame.Surface((rect[2],rect[3]))
        s.set_alpha(alpha)
        s.fill(colour)
        screen.blit(s,(rect[0],rect[1]))

    # highlight all cells in self.cell_list
    def highlightSelectedCells(self,screen,colour):
        if self.cell_list != None:
            self.highlightCells(screen,self.cell_list,colour)

    # highlight all cells in self.found_letterCells
    def highlightFoundCells(self,screen,colour):
        if self.found_letterCells != None:
            self.highlightCells(screen,self.found_letterCells,colour)

    # highlight cell method
    def highlightCells(self,screen,cell_list,colour):
        for x in cell_list:
            r = x // self.columns
            c = x % self.columns
            rect = (self.x+(self.cell_width)*c+self.gap,self.y+(self.cell_height)*r+self.gap,self.cell_width-self.gap*2,self.cell_height-self.gap*2)
            self.blit_alpha(screen,rect,colour,100)

    # adds a cell to self.cell_list if it follows wordsearch rules
    def selectCell(self,cell):
        if cell != None and cell not in self.cell_list:
            # first cell, position doesn't matter
            if self.cell_list == []:
                self.cell_list.append(cell)
                self.selected_letters.append(self.text[cell])
            # second cell, must be beside 1st one
            elif len(self.cell_list) == 1:
                if self.cell_list[0] - self.columns - 1 <= cell <= self.cell_list[0] - self.columns + 1 or self.cell_list[0] - 1 <= cell <= self.cell_list[0] + 1 or self.cell_list[0] + self.columns - 1 <= cell <= self.cell_list[0] + self.columns + 1:
                    self.cell_list.append(cell)
                    self.selected_letters.append(self.text[cell])
                else:
                    self.cell_list = []
                    self.selected_letters = []
            # after the 2nd one all the rest must follow the same line made by the 1st 2
            elif len(self.cell_list) > 1 and (cell == self.cell_list[-1] + (self.cell_list[1] - self.cell_list[0])):
                self.cell_list.append(cell)
                self.selected_letters.append(self.text[cell])
            elif len(self.cell_list) > 1 and (cell == self.cell_list[0] - (self.cell_list[1] - self.cell_list[0])):
                self.cell_list.insert(0,cell)
                self.selected_letters.insert(0,self.text[cell])
            else:
                self.cell_list = []
                self.selected_letters = []

    # remove a cell from self.cell_list
    def deselectCell(self,cell):
        if cell in self.cell_list:
            if self.cell_list.index(cell) == 0 or self.cell_list.index(cell) == len(self.cell_list) - 1:
                self.cell_list.remove(cell)
                self.selected_letters.remove(self.text[cell])

    # check if the current selected letters make any word passed in the wordList
    # allows the word to be spelt backwards
    def checkIfWord(self,wordList):
        if "".join(self.selected_letters) in wordList:
            self.found_words.append(wordList.index("".join(self.selected_letters)))
            for c in self.cell_list:
                if c not in self.found_letterCells:
                    self.found_letterCells.append(c)
            self.cell_list = []
            self.selected_letters = []
        elif ("".join(self.selected_letters)[::-1]) in wordList:
            self.found_words.append(wordList.index("".join(self.selected_letters)[::-1]))
            for c in self.cell_list:
                if c not in self.found_letterCells:
                    self.found_letterCells.append(c)
            self.cell_list = []
            self.selected_letters = []

    def gridType(self):
        return "LetterGrid"

'''grid = LetterGrid((100, 100, 200, 200),5,5,gap=1,font=(None,24),text=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y"],visible=True)

def redrawWin():
    screen.fill((255,255,255))
    grid.drawGrid(screen, (255,69,0))
    for c in crossedCells:
        grid.crossOut(screen,c)
    pygame.display.update()

crossedCells = []
Use = True
while Use:
    pygame.time.delay(10)
    redrawWin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Use = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if type(grid.mouseOverCell(mp[0], mp[1])) == int and grid.mouseOverCell(mp[0], mp[1]) < len(grid.text):
                print("you clicked on cell",grid.text[grid.mouseOverCell(mp[0], mp[1])])
                clicked_cell = grid.mouseOverCell(mp[0], mp[1])
                if clicked_cell not in crossedCells:
                    crossedCells.append(clicked_cell)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Use = False
pygame.quit()'''

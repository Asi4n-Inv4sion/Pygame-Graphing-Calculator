import pygame
from pygrid import Grid

pygame.init()


class functionList(Grid):
    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=True):
        Grid.__init__(self,rect,rows,columns,outline,gap,font,font_colour,text,visible)
        self.equations = []
        self.selectedFunction = None
        for i in range(rows):
            self.equations.append('')

    def equationAppend(self,symbol):
        if symbol != None and self.selectedFunction != None:
            if symbol == '÷':
                self.equations[self.selectedFunction] += '/'
            else:
                self.equations[self.selectedFunction] += symbol
            print(self.equations[self.selectedFunction])

    def selectFunc(self,cell):
        if cell != None:
            self.selectedFunction = cell

    def updateFunctions(self):
        self.text = self.equations[:]

    @staticmethod
    def printText(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        textbox.midleft = (x, y)
        canvas.blit(theText, textbox)

    # draws the grid and text
    def drawGrid(self,screen,colour):
        if self.visible == True:
            font = pygame.font.SysFont(self.font[0],self.font[1])
            for r in range(self.rows):
                for c in range(self.columns):
                    pygame.draw.rect(screen,colour,(self.x+(self.cell_width)*c+self.gap,self.y+(self.cell_height)*r+self.gap,self.cell_width-self.gap*2,self.cell_height-self.gap*2),self.outline)
                    if r*self.columns+c < len(self.text):
                        self.printText(self.text[r*self.columns+c],font,screen,self.x+(self.cell_width)*c + 10,self.y+(self.cell_height)*r+self.cell_height/2)

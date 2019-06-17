#--------------------------------------------------------------------------------
# GUI Class for Pygame Graph Calculator (Pymos)
# Leo Wang
# Creates the list of functions and moderates the input
# of symbols inputted into the functions
#--------------------------------------------------------------------------------

import pygame
from pygrid import Grid

pygame.init()

class functionList(Grid):
    def __init__(self,rect,rows,columns,outline=1,gap=0,font=(None,12),font_colour=(0,0,0),text=[],visible=True):
        Grid.__init__(self,rect,rows,columns,outline,gap,font,font_colour,text,visible)
        self.equations = []
        self.selectedFunction = None
        self.colours = [(255,0,0),(255,127,0),(255,255,0),(0,255,0),(108,180,238),(0,0,255),(75,0,130),(148,0,211)]
        for i in range(rows):
            self.equations.append('')

    # adds symbols into the selected function
    def equationAppend(self,symbol):
        if symbol != None and self.selectedFunction != None and len(self.equations[self.selectedFunction]) < 30:
            if symbol == '÷':
                self.equations[self.selectedFunction] += '/'
            elif symbol == 'a^2' and len(self.equations[self.selectedFunction]) < 29:
                self.equations[self.selectedFunction] += '^2'
            elif symbol == 'a^b' and len(self.equations[self.selectedFunction]) < 29:
                self.equations[self.selectedFunction] += '^('
            elif symbol == '√a' and len(self.equations[self.selectedFunction]) < 26:
                self.equations[self.selectedFunction] += 'sqrt('
            elif symbol == 'sin' or symbol == 'cos' or symbol == 'tan':
                if len(self.equations[self.selectedFunction]) < 28:
                    self.equations[self.selectedFunction] += symbol
            elif symbol != '←':
                self.equations[self.selectedFunction] += symbol
        # backspace symbol
        if symbol == '←' and self.selectedFunction != None:
            self.equations[self.selectedFunction] = self.equations[self.selectedFunction][:-1]

    # support for most keystrokes
    def equationKeyPress(self,key):
        if key == pygame.K_BACKSPACE:
            self.equationAppend('←')
        elif key == pygame.K_DELETE:
            if self.selectedFunction != None:
                self.equations[self.selectedFunction] = ''
        elif key in [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_EQUALS,pygame.K_MINUS,pygame.K_PERIOD,pygame.K_SLASH]:
            self.equationAppend(pygame.key.name(key))
        self.updateFunctions()

    # select a function by which cell it resides in
    def selectFunc(self,cell):
        if cell != None:
            self.selectedFunction = cell

    # update the text to show the equations
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

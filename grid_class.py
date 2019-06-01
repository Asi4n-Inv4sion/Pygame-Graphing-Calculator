# Pygame grid class for graphing calculator
import pygame
from abc import ABCMeta, abstractmethod
pygame.init()

class Grid(object):

    '''
    Attributes:
        x: x cord of the centre
        y: y cord of the centre
        width: width of an x value in pixels
        height: height of y value in pixels
        font: font name and size
        font_colour: the colour of the font
    '''

    __metaclass__ = ABCMeta

    def __init__(self,width,height,font=(None,12)):
        self.width = width
        self.height = height
        self.font = font
        # non-optional
        self.scale = 1

    @staticmethod
    def printText(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        textbox.center = (x, y)
        canvas.blit(theText, textbox)

    # draws the grid and text
    def drawGrid(self,screen):
        size = screen.get_size()
        font = pygame.font.SysFont(self.font[0],self.font[1])
        xChange = self.width
        yChange = self.height
        while xChange < size[0]//2:
            pygame.draw.line(screen,(127,127,127),(size[0]/2+xChange,0),(size[0]/2+xChange,size[1]),1)
            pygame.draw.line(screen,(127,127,127),(size[0]/2-xChange,0),(size[0]/2-xChange,size[1]),1)
            pygame.draw.line(screen,(127,127,127),(0,size[1]/2+yChange),(size[0],size[1]/2+yChange),1)
            pygame.draw.line(screen,(127,127,127),(0,size[1]/2-yChange),(size[0],size[1]/2-yChange),1)
            xChange += self.width
            yChange += self.height
        pygame.draw.line(screen,(0,0,0),(0,size[1]/2),(size[0],size[1]/2),2)
        pygame.draw.line(screen,(0,0,0),(size[0]/2,0),(size[0]/2,size[1]),2)

    # zoom in and out
    def zoom(self,mouse_get_pressed):
        multiplierSequenceList = [2,2,2.5]
        currentMultiplierIndex = 0
        if mouse_get_pressed[4] == True:
            self.scale *= multiplierSequenceList[currentMultiplierIndex]
            currentMultiplierIndex += 1
        elif mouse_get_pressed[3] == True:
            self.scale *= multiplierSequenceList[currentMultiplierIndex-1]
            currentMultiplierIndex -= 1
        if currentMultiplierIndex == -1:
            currentMultiplierIndex = 2
        elif currentMultiplierIndex == 3:
            currentMultiplierIndex = 0


def redrawWin():
    screen.fill((255,255,255))
    grid.drawGrid(screen)

    pygame.display.update()


screen = pygame.display.set_mode((400,400))
grid = Grid(20,20)
Use = True
while Use:
    pygame.time.delay(10)
    redrawWin()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Use = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Use = False
pygame.quit()

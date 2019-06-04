# Pygame grid class for graphing calculator
import pygame, math
from abc import ABCMeta, abstractmethod
pygame.init()

class Grid(object):

    '''
    Attributes:
        width: width of an x value in pixels
        height: height of y value in pixels
        font: font name and size of the numbers
        scale: zoom multiplier for the amount of pixels to represent 1 unit of measurement
        multiplierSequenceList: sequence to change the scale when zooming in or out
        currentMultiplierIndex: keeps track which index of the multiplierSequenceList to use next
        numOfDigits: keeps track of the number of digits to round
    '''

    __metaclass__ = ABCMeta

    def __init__(self,width,height,font=("monospace",12)):
        self.width = width
        self.height = height
        self.font = font
        # non-optional
        self.scale = 1
        self.multiplierSequenceList = [2.0,2.5,2.0]
        self.currentMultiplierIndex = 0
        self.numOfDigits = 0

    def printText(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        textbox.topright = (x, y)
        canvas.blit(theText, textbox)

    @staticmethod
    def printTextY(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        backgroundRect = theText.get_rect()
        textbox.center = (x-textbox[2]/2 - 2, y)
        backgroundRect.center = textbox.center
        background = pygame.draw.rect(canvas,(255,255,255),backgroundRect)
        canvas.blit(theText, textbox)

    @staticmethod
    def printTextX(text, font, canvas, x, y):
        theText = font.render(text, 1, (0,0,0))
        textbox = theText.get_rect()
        backgroundRect = theText.get_rect()
        textbox.center = (x, y+textbox[3]/2 + 2)
        backgroundRect.center = textbox.center
        background = pygame.draw.rect(canvas,(255,255,255),backgroundRect)
        canvas.blit(theText, textbox)

    # draws the grid and text
    def drawGrid(self,screen):
        size = screen.get_size()
        font = pygame.font.SysFont(self.font[0],self.font[1])
        xChange = self.width #* self.scale * 10 ^ self.magnitudeMultiplier
        yChange = self.height #* self.scale * 10 ^ self.magnitudeMultiplier

        while xChange < size[0]//2:
            if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
                for i in range(1,5):
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/5)*i),0),(int(size[0]/2+xChange-(self.width/5)*i),size[1]),1)
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/5)*i),0),(int(size[0]/2-xChange+(self.width/5)*i),size[1]),1)
            else:
                for i in range(1,4):
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/4)*i),0),(int(size[0]/2+xChange-(self.width/4)*i),size[1]),1)
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/4)*i),0),(int(size[0]/2-xChange+(self.width/4)*i),size[1]),1)
            #Grid.printTextTopLeft(str(xChange//(self.width * self.magnitudeMultiplier) * self.scale),font,screen,size[0]//2 + xChange+2,size[1]//2)
            #Grid.printTextTopLeft(str(xChange//(self.width * self.magnitudeMultiplier) * self.scale*-1),font,screen,size[0]//2 - xChange+2,size[1]//2)
            xChange += self.width #* self.scale

        if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
            for i in range(1,5):
                pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/5)*i),0),(int(size[0]/2+xChange-(self.width/5)*i),size[1]),1)
                pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/5)*i),0),(int(size[0]/2-xChange+(self.width/5)*i),size[1]),1)
        else:
            for i in range(1,4):
                pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/4)*i),0),(int(size[0]/2+xChange-(self.width/4)*i),size[1]),1)
                pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/4)*i),0),(int(size[0]/2-xChange+(self.width/4)*i),size[1]),1)

        while yChange < size[1]//2:
            if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
                for i in range(1,5):
                    pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2+yChange-(self.height/5)*i)),(size[0],int(size[1]/2+yChange-(self.height/5)*i)),1)
                    pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2-yChange+(self.height/5)*i)),(size[0],int(size[1]/2-yChange+(self.height/5)*i)),1)
            else:
                for i in range(1,4):
                    pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2+yChange-(self.height/4)*i)),(size[0],int(size[1]/2+yChange-(self.height/4)*i)),1)
                    pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2-yChange+(self.height/4)*i)),(size[0],int(size[1]/2-yChange+(self.height/4)*i)),1)

            #Grid.printTextTopLeft(str(int(yChange//(self.height * self.magnitudeMultiplier) * self.scale)),font,screen,size[0//2]+2,size[1] - yChange)
            yChange += self.height #* self.scale

        if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
            for i in range(1,5):
                pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2+yChange-(self.height/5)*i)),(size[0],int(size[1]/2+yChange-(self.height/5)*i)),1)
                pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2-yChange+(self.height/5)*i)),(size[0],int(size[1]/2-yChange+(self.height/5)*i)),1)
        else:
            for i in range(1,4):
                pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2+yChange-(self.height/4)*i)),(size[0],int(size[1]/2+yChange-(self.height/4)*i)),1)
                pygame.draw.line(screen,(230,230,230),(0,int(size[1]/2-yChange+(self.height/4)*i)),(size[0],int(size[1]/2-yChange+(self.height/4)*i)),1)

        xChange = 0
        yChange = 0

        while yChange < size[1]//2:
            pygame.draw.line(screen,(127,127,127),(0,size[1]/2+yChange),(size[0],size[1]/2+yChange),1)
            pygame.draw.line(screen,(127,127,127),(0,size[1]/2-yChange),(size[0],size[1]/2-yChange),1)
            if (yChange // self.height) * self.scale >= 1:
                self.printTextY(str(int((yChange // self.height) * self.scale)),font,screen,size[0]//2,size[1]/2-yChange)
                self.printTextY(str(int((yChange // self.height) * self.scale * -1)),font,screen,size[0]//2,size[1]/2+yChange)
            elif yChange != 0:
                self.printTextY(str(((yChange // self.height) * self.scale)/1),font,screen,size[0]//2,size[1]/2-yChange)
                self.printTextY(str(((yChange // self.height) * self.scale * -1)/1),font,screen,size[0]//2,size[1]/2+yChange)
            yChange += self.height

        while xChange < size[0]//2:
            pygame.draw.line(screen,(127,127,127),(size[0]/2+xChange,0),(size[0]/2+xChange,size[1]),1)
            pygame.draw.line(screen,(127,127,127),(size[0]/2-xChange,0),(size[0]/2-xChange,size[1]),1)
            xChange += self.width

        Grid.printText('0',font,screen,size[0]//2-2,size[1]//2+2)

        pygame.draw.line(screen,(0,0,0),(0,size[1]/2),(size[0],size[1]/2),2)
        pygame.draw.line(screen,(0,0,0),(size[0]/2,0),(size[0]/2,size[1]),2)


    # zoom in and out
    def zoom(self,zoomDirection):
        # zoom out
        if zoomDirection == "out":
            self.scale *= self.multiplierSequenceList[self.currentMultiplierIndex]
            self.currentMultiplierIndex += 1
        # zoom in
        elif zoomDirection == "in":
            self.scale /= self.multiplierSequenceList[self.currentMultiplierIndex-1]
            self.currentMultiplierIndex -= 1
        else:
            raise SyntaxError('zoom direction should be "in" or "out"')

        if self.currentMultiplierIndex == -1:
            self.currentMultiplierIndex = 2
            if self.scale < 1:
                self.numOfDigits += 1
            else:
                self.numOfDigits -= 1
        elif self.currentMultiplierIndex == 3:
            self.currentMultiplierIndex = 0
            if self.scale < 1:
                self.numOfDigits -= 1
            else:
                self.numOfDigits += 1
        print(self.scale)


def redrawWin():
    screen.fill((255,255,255))
    grid.drawGrid(screen)

    pygame.display.update()


screen = pygame.display.set_mode((800,800))
grid = Grid(60,60)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                grid.zoom('in')
            if event.button == 5:
                grid.zoom('out')
pygame.quit()

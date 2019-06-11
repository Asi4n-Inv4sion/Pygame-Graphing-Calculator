# Pygame grid class for graphing calculator
import pygame, math
from abc import ABCMeta, abstractmethod
from float_rounder import *
pygame.init()

class CalcGrid(object):

    '''
    Attributes:
        width: width of an x value in pixels
        height: height of y value in pixels
        font: font name and size of the numbers
        scale: zoom multiplier for the amount of pixels to represent 1 unit of measurement
        multiplierSequenceList: sequence to change the scale when zooming in or out
        currentMultiplierIndex: keeps track which index of the multiplierSequenceList to use next
    '''

    __metaclass__ = ABCMeta

    def __init__(self,width,height,font=("monospace",12)):
        self.width = width
        self.height = height
        self.font = font
        # non-optional
        self.scale = 1
        self.multiplierSequenceList = [2,2.5,2]
        self.currentMultiplierIndex = 0

    @staticmethod
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
    def drawGrid(self,screen,sizex,sizey,tx,ty):
        '''
        sizex: the width of the displayed graph in pixels
        sizey: the height of the displayed graph in pixels
        tx: translation of the graph right in pixels
        ty: translation of the graph down in pixels
        '''
        size = (sizex,sizey)
        font = pygame.font.SysFont(self.font[0],self.font[1])
        xChange = self.width
        yChange = self.height

        while xChange < size[0]//2:
            if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
                for i in range(1,5):
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/5)*i)+tx,ty),(int(size[0]/2+xChange-(self.width/5)*i)+tx,size[1]+ty))
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/5)*i)+tx,ty),(int(size[0]/2-xChange+(self.width/5)*i)+tx,size[1]+ty))
            else:
                for i in range(1,4):
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/4)*i)+tx,ty),(int(size[0]/2+xChange-(self.width/4)*i)+tx,size[1]+ty))
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/4)*i)+tx,ty),(int(size[0]/2-xChange+(self.width/4)*i)+tx,size[1]+ty))

            xChange += self.width

        if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
            for i in range(1,5):
                if int(size[0]/2+xChange-(self.width/5)*i) > size[0]//2:
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/5)*i)+tx,ty),(int(size[0]/2+xChange-(self.width/5)*i)+tx,size[1]+ty))
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/5)*i)+tx,ty),(int(size[0]/2-xChange+(self.width/5)*i)+tx,size[1]+ty))
        else:
            for i in range(1,4):
                if int(size[0]/2+xChange-(self.width/4)*i) > size[0]//2:
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2+xChange-(self.width/4)*i)+tx,ty),(int(size[0]/2+xChange-(self.width/4)*i)+tx,size[1]+ty))
                    pygame.draw.line(screen,(230,230,230),(int(size[0]/2-xChange+(self.width/4)*i)+tx,ty),(int(size[0]/2-xChange+(self.width/4)*i)+tx,size[1]+ty))

        while yChange < size[1]//2:
            if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
                for i in range(1,5):
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2+yChange-(self.height/5)*i)),(size[0]+tx,ty+int(size[1]/2+yChange-(self.height/5)*i)))
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2-yChange+(self.height/5)*i)),(size[0]+tx,ty+int(size[1]/2-yChange+(self.height/5)*i)))
            else:
                for i in range(1,4):
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2+yChange-(self.height/4)*i)),(size[0]+tx,ty+int(size[1]/2+yChange-(self.height/4)*i)))
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2-yChange+(self.height/4)*i)),(size[0]+tx,ty+int(size[1]/2-yChange+(self.height/4)*i)))

            yChange += self.height

        if self.multiplierSequenceList[self.currentMultiplierIndex] == 2.0:
            for i in range(1,5):
                if int(size[1]/2+yChange-(self.height/5)*i) < size[1]:
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2+yChange-(self.height/5)*i)),(size[0]+tx,ty+int(size[1]/2+yChange-(self.height/5)*i)))
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2-yChange+(self.height/5)*i)),(size[0]+tx,ty+int(size[1]/2-yChange+(self.height/5)*i)))
        else:
            for i in range(1,4):
                if int(size[1]/2+yChange-(self.height/4)*i) < size[1]:
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2+yChange-(self.height/4)*i)),(size[0]+tx,ty+int(size[1]/2+yChange-(self.height/4)*i)))
                    pygame.draw.line(screen,(230,230,230),(tx,ty+int(size[1]/2-yChange+(self.height/4)*i)),(size[0]+tx,ty+int(size[1]/2-yChange+(self.height/4)*i)))

        xChange = 0
        yChange = 0

        while yChange < size[1]//2:
            pygame.draw.line(screen,(127,127,127),(tx,ty+size[1]/2+yChange),(size[0]+tx,ty+size[1]/2+yChange),1)
            pygame.draw.line(screen,(127,127,127),(tx,ty+size[1]/2-yChange),(size[0]+tx,ty+size[1]/2-yChange),1)
            if ((yChange // self.width) * self.scale) == int((yChange // self.width) * self.scale) and yChange != 0:
                if self.scale >= 1000000:
                    self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale))[0]+'e'+str(len(str(self.scale))-1),font,screen,size[0]//2+tx,size[1]/2-yChange+ty)
                    self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale)*-1)[0:2]+'e'+str(len(str(self.scale))-1),font,screen,size[0]//2+tx,size[1]/2+yChange+ty)
                else:
                    self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale)),font,screen,size[0]//2+tx,size[1]/2-yChange+ty)
                    self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale)*-1),font,screen,size[0]//2+tx,size[1]/2+yChange+ty)
            elif yChange != 0:
                self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale)),font,screen,size[0]//2+tx,size[1]/2-yChange+ty)
                self.printTextY(str(multiplyByFloat1(yChange // self.height, self.scale)*-1),font,screen,size[0]//2+tx,size[1]/2+yChange+ty)
            yChange += self.height

        while xChange < size[0]//2:
            pygame.draw.line(screen,(127,127,127),(size[0]/2+xChange+tx,ty),(size[0]/2+xChange+tx,size[1]+ty),1)
            pygame.draw.line(screen,(127,127,127),(size[0]/2-xChange+tx,ty),(size[0]/2-xChange+tx,size[1]+ty),1)
            if ((xChange // self.width) * self.scale) == int((xChange // self.width) * self.scale) and xChange != 0:
                if self.scale >= 1000000:
                    self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale))[0]+'e'+str(len(str(self.scale))-1),font,screen,size[0]/2+xChange+tx,ty+size[1]/2)
                    self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale)*-1)[0:2]+'e'+str(len(str(self.scale))-1),font,screen,size[0]/2-xChange+tx,ty+size[1]/2)
                else:
                    self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale)),font,screen,size[0]/2+xChange+tx,ty+size[1]/2)
                    self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale)*-1),font,screen,size[0]/2-xChange+tx,ty+size[1]/2)
            elif xChange != 0:
                self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale)),font,screen,size[0]/2+xChange+tx,ty+size[1]/2)
                self.printTextX(str(multiplyByFloat1(xChange // self.width, self.scale)*-1),font,screen,size[0]/2-xChange+tx,ty+size[1]/2)
            xChange += self.width

        Grid.printText('0',font,screen,size[0]//2-2+tx,size[1]//2+2+ty)

        pygame.draw.line(screen,(0,0,0),(tx,ty+size[1]/2),(size[0]+tx,ty+size[1]/2),2)
        pygame.draw.line(screen,(0,0,0),(size[0]/2+tx,ty),(size[0]/2+tx,ty+size[1]),2)


    # zoom in and out
    def zoom(self,zoomDirection):
        # zoom out
        if zoomDirection == "out" and self.scale < 10**21:
            #self.scale *= self.multiplierSequenceList[self.currentMultiplierIndex]
            self.scale = multiplyByFloat1(self.scale,self.multiplierSequenceList[self.currentMultiplierIndex])
            self.currentMultiplierIndex += 1

        # zoom in
        elif zoomDirection == "in" and self.scale > 10**-10:
            #self.scale /= self.multiplierSequenceList[self.currentMultiplierIndex-1]
            self.scale = multiplyByFloat1(self.scale,1/self.multiplierSequenceList[self.currentMultiplierIndex-1])
            self.currentMultiplierIndex -= 1

        if self.currentMultiplierIndex == -1:
            self.currentMultiplierIndex = 2
        elif self.currentMultiplierIndex == 3:
            self.currentMultiplierIndex = 0

'''def redrawWin():
    screen.fill((255,255,255))
    grid.drawGrid(screen,1096,600,270,0)

    pygame.display.update()


screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN)
grid = CalcGrid(70,70)
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
pygame.quit()'''

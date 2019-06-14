from grid_class import *
from GUI_class import *
from pygrid import *

import pygame

pymos = pygame.image.load('sowsep_logo.png')

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def redrawWin():
    screen.fill((255,255,255))
    #grid.drawGrid(screen,infoObject.current_w*0.8,infoObject.current_h*0.8,infoObject.current_w*0.2,0)

    grid.drawGrid(screen,WIDTH*0.75,HEIGHT*0.8,WIDTH*0.25,0)

    screen.blit(pymos,(6,6))

    funcList.drawGrid(screen,(0,0,0))
    keypad.drawGrid(screen,(0,0,0))
    operationpad.drawGrid(screen,(0,0,0))
    trigfunc.drawGrid(screen,(0,0,0))
    expofunc.drawGrid(screen,(0,0,0))

    funcList.highlightSelectedCell(screen)
    pygame.draw.line(screen,(97,178,66),(0.25*WIDTH-2,0),(0.25*WIDTH-2,0.8*HEIGHT),3)
    pygame.draw.line(screen,(97,178,66),(0,0.8*HEIGHT+2),(WIDTH,0.8*HEIGHT+2),3)
    pygame.display.update()

# grids
grid = CalcGrid(70,70)
funcList = functionList((1,60,0.25*WIDTH-5,0.8*HEIGHT-60),8,1,1,1,('monospace',16))
keypad = Grid((WIDTH//2-0.1*WIDTH,0.8*HEIGHT+5,0.2*WIDTH,0.2*HEIGHT-5),4,3,1,2,('monospace',18),(0,0,0),['7','8','9','4','5','6','1','2','3','0','.','='],True)
operationpad = Grid((WIDTH//2+0.1*WIDTH,0.8*HEIGHT+5,0.05*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['+','-','*','÷'],True)
trigfunc = Grid((WIDTH//2+0.15*WIDTH,0.8*HEIGHT+5,0.07*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['sin','cos','tan','←'],True)
expofunc = Grid((WIDTH//2-0.17*WIDTH,0.8*HEIGHT+5,0.07*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['a^2','a^3','a^b','√a'],True)

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
            if event.key == pygame.K_BACKSPACE:
                funcList.equationAppend('←')
                funcList.updateFunctions()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if 0.25 * WIDTH < mp[0] < WIDTH and mp[1] < 0.8*HEIGHT:
                if event.button == 4:
                    grid.zoom('in')
                if event.button == 5:
                    grid.zoom('out')
            if event.button == 1:
                funcList.selectFunc(funcList.mouseOverCell(mp[0],mp[1]))
                if keypad.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(keypad.text[keypad.mouseOverCell(mp[0],mp[1])])
                elif operationpad.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(operationpad.text[operationpad.mouseOverCell(mp[0],mp[1])])
                elif trigfunc.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(trigfunc.text[trigfunc.mouseOverCell(mp[0],mp[1])])
                elif expofunc.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(expofunc.text[expofunc.mouseOverCell(mp[0],mp[1])])
                elif funcList.mouseOverCell(mp[0],mp[1]) == None:
                    funcList.selectedFunction = None
                funcList.updateFunctions()
pygame.quit()

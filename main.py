#--------------------------------------------------------------------------------
# Graphing Calculator for Pygame
# Julian and Leo
# User can input functions using the printed buttons or using their keyboard
# for most functions
# Given eight inputboxes to define variables or create functions
#--------------------------------------------------------------------------------

from grid_class import *
from GUI_class import *
from pygrid import *
from analyze import *
import pygame

pymos = pygame.image.load('sowsep_logo.png')
pygame.init()
WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH,HEIGHT))
functions = []
radOrDeg = "rad"
boxesUsed = []

def getPoints(e,width,scale):
    p = []
    for x in range(-width//2,width//2):#equation variable changes depending on the graph being drawn
        y = Calculate(e[:],[],0,x/70*scale,radOrDeg)
        if y != None:
            y *= 70/scale

        #If the equation has division by 0 at a point, use None as a point
        if type(y) != float and type(y) != int:
            p.append(None)
            if x == -width//2:
                p.append(None)
        else:
            #If too big or small, set a limit. Won't work if too big
            if y >= 10**8 or y <= -(10**8):
                y = y//abs(y)*(10**8)
            #Add the point to a list
            else:
                p.append((x,y))
                if x == -width//2:
                    p.append((x,y))
    return p

def drawFunction(p,xcord,ycord,width,height):
    for i in range(len(p)-1):
        if p[i] != None and p[i+1] != None:
            pygame.draw.line(screen,(0,0,255),(xcord+width/2+p[i][0],ycord+height/2-p[i][1]),(xcord+width/2+p[i+1][0],ycord+height/2-p[i+1][1]),3)

#Draws any vertical lines passed
def drawVertical(v,xcord,ycord,width,height,scale):
    pygame.draw.line(screen,(200,0,200),(xcord+width//2+v*70/scale,ycord),(xcord+width//2+v*70/scale,ycord+height),3)
        
def redrawWin():
    global functions,verticals
    screen.fill((255,255,255))
    #grid.drawGrid(screen,infoObject.current_w*0.8,infoObject.current_h*0.8,infoObject.current_w*0.2,0)
    grid.drawGrid(screen,WIDTH*0.75,HEIGHT*0.8,WIDTH*0.25,0)

    #Draws function(s)
    for f in range(len(functions)):
        drawFunction(functions[f],round(WIDTH*0.25),0,round(WIDTH*0.75),round(HEIGHT*0.8))
    for v in verticals:
        drawVertical(v,round(WIDTH*0.25),0,round(WIDTH*0.75),round(HEIGHT*0.8),grid.scale)
    pygame.draw.rect(screen,(255,255,255),(WIDTH*0.25,HEIGHT*0.8,WIDTH*0.75,HEIGHT*0.2))#Covers up the function if it exits the graph
    pygame.draw.rect(screen,(255,255,255),(0,0,WIDTH*0.25,HEIGHT*0.8))#Covers up the function if it exits the graph

    #Drawing keyboard sections
    funcList.drawGrid(screen,(0,0,0))
    for f in keyboard:
        f.drawGrid(screen,(0,0,0))

    """
    keypad.drawGrid(screen,(0,0,0))
    operationpad.drawGrid(screen,(0,0,0))
    trigfunc.drawGrid(screen,(0,0,0))
    expofunc.drawGrid(screen,(0,0,0))
    miscfunc.drawGrid(screen,(0,0,0))
    variables.drawGrid(screen,(0,0,0))"""

    #Drawing extra GUI
    screen.blit(pymos,(6,6))
    funcList.highlightSelectedCell(screen)
    angleMode.highlightCells(screen,[angleMode.text.index(radOrDeg)],(30,30,30))
    pygame.draw.line(screen,(97,178,66),(0.25*WIDTH-2,0),(0.25*WIDTH-2,0.8*HEIGHT),3)
    pygame.draw.line(screen,(97,178,66),(0,0.8*HEIGHT+2),(WIDTH,0.8*HEIGHT+2),3)
    pygame.display.update()

def getFunctions():
    global boxesUsed
    funcs = []
    for f in funcList.equations:
        funcs.append(list(f))
    boxesUsed = [i for i,f in enumerate(funcs) if len(f) > 0]
    funcs = [Initialize(f) for f in funcs if len(f) > 0]
    return [getPoints(f,round(WIDTH*0.75),grid.scale) for f in funcs if type(f) == list and len(f) > 0]

# keyboard grids
grid = CalcGrid(70,70)
funcList = functionList((1,60,0.25*WIDTH-5,0.8*HEIGHT-60),8,1,1,1,('monospace',16))
keypad = Grid((WIDTH//2-0.1*WIDTH,0.8*HEIGHT+5,0.2*WIDTH,0.2*HEIGHT-5),4,3,1,2,('monospace',18),(0,0,0),['7','8','9','4','5','6','1','2','3','0','.','='],True)
operationpad = Grid((WIDTH//2+0.1*WIDTH,0.8*HEIGHT+5,0.05*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['+','-','*','÷'],True)
trigfunc = Grid((WIDTH//2+0.15*WIDTH,0.8*HEIGHT+5,0.07*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['sin','cos','tan','←'],True)
expofunc = Grid((WIDTH//2-0.17*WIDTH,0.8*HEIGHT+5,0.07*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['a^2','a^b','√a','π'],True)
miscfunc = Grid((WIDTH//2-0.24*WIDTH,0.8*HEIGHT+5,0.07*WIDTH,0.2*HEIGHT-5),4,1,1,2,('monospace',18),(0,0,0),['(',')','x','y'],True)
variables = Grid((3,0.8*HEIGHT+5,0.25*WIDTH,0.2*HEIGHT-5),4,6,1,2,('monospace',18),(0,0,0),['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','z'],True)
angleMode = Grid((WIDTH//2+0.22*WIDTH,0.8*HEIGHT+5,0.1*WIDTH,0.05*HEIGHT-2),1,2,1,2,('monospace',18),(0,0,0),['deg','rad'],True)
keyboard = [keypad,operationpad,trigfunc,expofunc,miscfunc,variables,angleMode]

tick = 0
Use = True
while Use:
    pygame.time.delay(20)
    #every half a second or so, the equations are tested for mistakes and added to the functions list if they make sense
    if tick % 15 == 0:
        del verticals[:] #resets vertical lines
        customVars.clear()#resets customVars in case they were deleted
        functions = getFunctions() #gets the points for each function
    redrawWin()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Use = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Use = False
            else:
                funcList.equationKeyPress(event.key)
        '''
        if event.key == pygame.K_LEFT:
            grid.hTranslation += 70
        if event.key == pygame.K_RIGHT:
            grid.hTranslation -= 70
        if event.key == pygame.K_UP:
            grid.vTranslation -= 70
        if event.key == pygame.K_DOWN:
            grid.vTranslation += 70
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if 0.25 * WIDTH < mp[0] < WIDTH and mp[1] < 0.8*HEIGHT:
                if event.button == 4:
                    grid.zoom('in')
                    functions = getFunctions()
                if event.button == 5:
                    grid.zoom('out')
                    functions = getFunctions()
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
                elif miscfunc.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(miscfunc.text[miscfunc.mouseOverCell(mp[0],mp[1])])
                elif variables.mouseOverCell(mp[0],mp[1]) != None:
                    funcList.equationAppend(variables.text[variables.mouseOverCell(mp[0],mp[1])])
                elif funcList.mouseOverCell(mp[0],mp[1]) == None:
                    funcList.selectedFunction = None
                if angleMode.mouseOverCell(mp[0],mp[1]) != None:
                    radOrDeg = angleMode.text[angleMode.mouseOverCell(mp[0],mp[1])]
                funcList.updateFunctions()
    tick += 1
pygame.quit()

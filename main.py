#--------------------------------------------------------------------------------
# Graphing Calculator for Pygame
# Julian and Leo
# User can input functions using the printed buttons or using their keyboard
# for most symbols
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
colours = []
boxesWithFunctions = []

# Julian
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

# Julian
def drawFunction(p,xcord,ycord,width,height,colour,i):
    #draws each function created
    for i in range(len(p)-1):
        if p[i] != None and p[i+1] != None:
            pygame.draw.line(screen,colour,(xcord+width/2+p[i][0],round(ycord+height/2-p[i][1])),(xcord+width/2+p[i+1][0],round(ycord+height/2-p[i+1][1])),3)

# Draws any vertical lines passed
# Julian
def drawVertical(v,xcord,ycord,width,height,scale):
    pygame.draw.line(screen,(200,0,200),(xcord+width//2+v*70/scale,ycord),(xcord+width//2+v*70/scale,ycord+height),3)

# labels the colour of a box to correspond to the colour of the function
# Julian
def drawFuncColours(screen,x,y,colours,boxesUsed):
    for i in range(len(colours)):
        if i in boxesUsed:
            pygame.draw.circle(screen,colours[i],(x,y+64*i),5)

def redrawWin():
    global functions,verticals
    screen.fill((255,255,255))
    #grid.drawGrid(screen,infoObject.current_w*0.8,infoObject.current_h*0.8,infoObject.current_w*0.2,0)
    grid.drawGrid(screen,WIDTH*0.75,HEIGHT*0.8,WIDTH*0.25,0)

    #Draws function(s)
    for f in range(len(functions)):
        drawFunction(functions[f],round(WIDTH*0.25),0,round(WIDTH*0.75),round(HEIGHT*0.8),colours[f],f)
    for v in verticals:
        drawVertical(v,round(WIDTH*0.25),0,round(WIDTH*0.75),round(HEIGHT*0.8),grid.scale)
    pygame.draw.rect(screen,(255,255,255),(WIDTH*0.25,HEIGHT*0.8,WIDTH*0.75,HEIGHT*0.2))#Covers up the function if it exits the graph
    pygame.draw.rect(screen,(255,255,255),(0,0,WIDTH*0.25,HEIGHT*0.8))#Covers up the function if it exits the graph

    #for c in range(len(colours)):
    #    pygame.draw.circle(screen,colours[c],(300,int(73+c*64.5)),6)
    
    #Drawing keyboard sections
    funcList.drawGrid(screen,(0,0,0))
    for f in keyboard:
        f.drawGrid(screen,(0,0,0))

    #Drawing extra GUI
    screen.blit(pymos,(6,6))
    drawFuncColours(screen,300,73,funcList.colours,boxesWithFunctions)#draws colour circles for functions
    printText('Sowsep™',pygame.font.SysFont('consolas',40),screen,150,33)
    funcList.highlightSelectedCell(screen)
    angleMode.highlightCells(screen,[angleMode.text.index(radOrDeg)],(25,25,25))
    pygame.draw.line(screen,(97,178,66),(0.25*WIDTH-2,0),(0.25*WIDTH-2,0.8*HEIGHT),3)
    pygame.draw.line(screen,(97,178,66),(0,0.8*HEIGHT+2),(WIDTH,0.8*HEIGHT+2),3)
    pygame.display.update()

# Julian
def getFunctions():
    global boxesUsed,colours,boxesWithFunctions
    funcs = []
    for f in funcList.equations:
        funcs.append(list(f))
    #A list of gui function boxes with something written in them
    boxesUsed = [i for i,f in enumerate(funcs) if len(f) > 0]
    #A lst of indexes for the gui function boxes with a function in them
    boxesWithFunctions = [i for i,f in enumerate(funcs) if (len(f) == 1 and f[0] == "x")or (len(f) > 1 and (f[1] != "=" or f[0:2] == ['y','=']))]
    #The colours for the functions
    colours = [funcList.colours[i] for i in boxesWithFunctions]
    #Creates a list of each function intitialized
    funcs = [Initialize(f) for f in funcs if len(f) > 0]
    #returns a master list of nested lists with points for each solvable function
    return [getPoints(f,round(WIDTH*0.75),grid.scale) for f in funcs if type(f) == list and len(f) > 0]

# saves, loads, or deleted functions from a text file
# Leo
def fileFunc(f,mode):
    if mode == 'save':
        funcfile = open(f,'w')
        funcfile.writelines('\n'.join(funcList.equations))
        funcfile.close()
    elif mode == 'load':
        funcfile = open(f,'r')
        funcList.equations = [line.strip() for line in funcfile.readlines()]
        funcfile.close()
    elif mode == 'delete':
        funcfile = open(f,'w')
        funcfile.writelines('')
        funcfile.close()

#The good old print text function
def printText(text, font, canvas, x, y):
    theText = font.render(text, 1, (0,0,0))
    textbox = theText.get_rect()
    textbox.center = (x, y)
    canvas.blit(theText, textbox)

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
filebuttons = Grid((WIDTH//2+0.22*WIDTH,0.85*HEIGHT+2,0.2*WIDTH,0.15*HEIGHT-2),3,1,1,2,('monospace',18),(0,0,0),['Save Functions','Load Functions','Delete Saved Functions'],True)
keyboard = [keypad,operationpad,trigfunc,expofunc,miscfunc,variables,angleMode,filebuttons]

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
                # detect if any keyboard key is pressed
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
                if filebuttons.mouseOverCell(mp[0],mp[1]) != None:
                    if filebuttons.mouseOverCell(mp[0],mp[1]) == 0:
                        fileFunc('saved_functions.txt','save')
                    elif filebuttons.mouseOverCell(mp[0],mp[1]) == 1:
                        fileFunc('saved_functions.txt','load')
                    elif filebuttons.mouseOverCell(mp[0],mp[1]) == 2:
                        fileFunc('saved_functions.txt','delete')
                #updates the functions in case they were changed (backspace, etc)
                funcList.updateFunctions()
    tick += 1
pygame.quit()

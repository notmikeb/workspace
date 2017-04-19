# 15-112 Term Project

# https://www.youtube.com/watch?v=uuUbdluqSiE
# Peter Pak + ppak + B
######################################################################
# Imports
######################################################################
from __future__ import with_statement
from tkSimpleDialog import*
from tkMessageBox import*
from contextlib import*
from threading import*
from winsound import*
from Tkinter import*
from decimal import*
from random import*
from ctypes import*
from copy import*
from math import*
from sys import*
import os
######################################################################
# EventBasedAnimationClass taken from the notes
######################################################################
class EventBasedAnimationClass(object): #Runs the program, and is again from
    def onKeyPressed(self, event): pass #the notes in class
    def onTimerFired(self): pass
    def redrawAll(self): pass
    def initAnimation(self): pass
    def __init__(self, width, height):
        (self.width, self.height, self.timerDelay)=(width, height,250)
    def onKeyPressedWrap(self, event): #Wrapper function for Keyboard presses
        self.onKeyPressed(event),self.redrawAll()
    def onTimerFiredWrap(self): #Wrapper function for Timer functions 
        if(self.timerDelay == None):return #Turns off timer
        self.onTimerFired(),self.redrawAll() 
        self.canvas.after(self.timerDelay, self.onTimerFiredWrap)         
    def run(self):# create the root and the canvas
        self.root = Tk() #Tkinter root function
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(),self.initAnimation()#setup events 
        #self.root.bind("<Key>", lambda event: self.onKeyPressedWrap(event))
        self.onTimerFiredWrap(),self.root.mainloop()

######################################################################
#Main Class
######################################################################
class Main(EventBasedAnimationClass):
    
    @ classmethod #creates a function so that it returns a color
    def rgb(self, red, green, blue):return "#%02x%02x%02x" % (red, green, blue)
    
    def __init__(self): #[X][Y],[0][1] = old,[2][3] = new
        super(Main,self).__init__(1600,900)
        self.buttonLocations(), self.functionsAI(),self.functionsFile()
        self.defaultGrid()
        self.gameMode = None
        (self.midX, self.midY) = (self.width/2, self.height/2)
        (self.degrees, self.zoom, self.time, self.score) = (91, 1, 0, 0)
        self.verticesRight = self.verticesBackwards = self.verticesLeft = None
        self.oldMouseMoveX = self.oldMouseMoveY = self.verticesForwards = None
        (self.speed, self.look) =  (2, 0)
        self.pause = self.start = self.edgeAdjust = False
        (self.weaponMidX, self.weaponMidY) = (self.midX+350, self.midY+250)
        (self.row, self.col, self.area) = (len(self.grid),len(self.grid[1]),20)
        (self.gridX,self.gridY,self.midBox)=(self.row/2,self.col/2,self.area/2)
        self.gridXY,self.boxXY=[self.gridX,self.gridY]*2,[self.midBox]*4
        self.cubeRunnerMultiplier = 1
        self.skinColor, self.skinStipple = "blue", "gray75"
        self.fill = self.oldFill = "white"
        self.outline = "green"

    def defaultGrid(self):#The defualt Grid When no file is present
        self.grid = ([[2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,0,2],
                    [2,0,0,2,0,2,0,0,2],
                    [2,0,2,0,0,0,2,0,2],
                    [2,0,0,0,0,0,0,0,2],
                    [2,0,2,0,0,0,2,0,2],
                    [2,0,0,2,0,2,0,0,2],
                    [2,0,0,0,0,0,0,0,2],
                    [2,2,2,2,2,2,2,2,2]])

    def functionsFile(self):
        self.folder = "Grid Maps"
        self.initialFileSetup()

    def functionsAI(self):
        self.frontAI = self.backAI = self.leftAI = self.rightAI = None
        self.gridAI = None
        self.coordinatesAI = []
        self.directionAI = "forwards"
        self.speedAI = 0.10
        self.equipedWeapon = None

    def buttonLocations(self):#locations of the buttons on the start screen
        (self.topLeftGrid, self.bottomRightGrid) = (550,200),(1050,800)
        (self.topLeftCubeRun,self.bottomRightCubeRun)=(1100,250),(1500,350)
        (self.topLeftHelp,self.bottomRightHelp)=(1100,450),(1500,550)
        (self.topLeftOptions,self.bottomRightOptions)=(1100,650),(1500,750)
        (self.topLeftGridRun,self.bottomRightGridRun)=(100,250),(500,350)
        (self.topLeftGridHunt,self.bottomRightGridHunt)=(100,450),(500,550)
        (self.topLeftGridEdit,self.bottomRightGridEdit)=(100,650),(500,750)
        self.startScreenMouseX = self.startScreenMouseY = None
        self.gridEditMouseX = self.gridEditMouseY = None

    def restart(self): #restarts the game when tab is pressed
        if(self.gameMode == "CubeRunner"):self.__init__()
        (self.gameMode, self.start) = (None, False)
        self.initAnimation(),self.functionsAI()
        (self.degrees, self.zoom, self.time, self.score) = (91, 1, 0, 0)
        (self.row, self.col, self.area) = (len(self.grid),len(self.grid[1]),20)
        (self.gridX,self.gridY,self.midBox)=(self.row/2,self.col/2,self.area/2)
        self.verticesRight = self.verticesBackwards = self.verticesLeft = None
        self.oldMouseMoveX = self.oldMouseMoveY = self.verticesForwards = None
        (self.speed, self.look) =  (2, 0)
        self.pause = self.start = self.edgeAdjust = False
        (self.weaponMidX, self.weaponMidY) = (self.midX+350, self.midY+250)
        self.gridXY,self.boxXY=[self.gridX,self.gridY]*2,[self.midBox]*4
        for row in xrange(self.row):
            for col in xrange(self.col):
                if(self.grid[row][col] == 1): self.grid[row][col] = 0
        self.redrawAll()        
        
    def options(self):#user adjustable features
        if(self.gridAI == None):self.gridAI = (1,self.col/2)
        (self.sensitivityX, self.sensitivityY) = (50,50)
        self.fov = 50

    ##################################################################
    #File Functions taken from the notes and modified
    ##################################################################
    def readFile(self, location):#called by self.runFileFunctions()
        #opens and reads files
        with open(location, "rt") as fin:
            return fin.read()

    def writeFile(self, location):#called by self.runFileFunctions()
        #creates new files
        with open(location, "wt") as fout:
            fout.write(repr(self.grid))

    def initialFileSetup(self):#called by self.__init__()
        if(not os.path.exists(self.folder)):
            os.makedirs(self.folder)
            assert(os.path.exists(self.folder))

    def onTimerFired(self):self.time+=1
        
    def initAnimation(self):#binds other functions into animation
        if(self.start == True and self.gameMode not in["GridEdit","Options"]):
            self.root.config(cursor = "none")#Thanks stackoverflow
        elif(self.start==False):self.root.config(cursor = "")
        self.root.title("Grid") #Thanks stackoverflow
        self.root.attributes("-fullscreen", True) #Thanks stackoverflow
        self.root.bind("<KeyPress>",lambda event:self.onKeyPress(event))
        self.root.bind("<KeyRelease>",lambda event:self.onKeyRelease(event))
        self.root.bind("<Motion>",lambda event:self.onMouseMoved(event))
        self.root.bind("<ButtonPress-1>",lambda event: #Thanks stackoverflow
                       self.onMouseLeftPress(event))
        self.root.bind("<ButtonPress-3>",lambda event: #Thanks stackoverflow
                       self.onMouseRightPress(event))
        self.root.bind("<ButtonRelease-3>",lambda event: #Thanks stackoverflow
                       self.onMouseRightRelease(event))

    def onMouseMoved(self, event):#called by mouse movements
        if(self.start == False or self.gameMode == "GridEdit"):        
            (self.startScreenMouseX,self.startScreenMouseY) = (event.x,event.y)
        elif(self.start == True):
            if(self.gameMode in["GridHunt","GridTest"]):self.headMovement(event)

    def headMovement(self,event): #called by self.onMouseMoved
        # "windll.user32.SetCursorPos(self.midX,self.midY)" was modified
        # from https://www.daniweb.com/software-development/python/threads
        #/194446/tkinter-set-mouse-position
        if(self.oldMouseMoveX == self.oldMouseMoveY == None):
            self.oldMouseMoveX,self.oldMouseMoveY=(event.x,event.y)
        if(self.edgeAdjust == False):#tracks the user's head movement
            oldDegrees = preDegrees = self.degrees
            oldLook = preLook = self.look
        if(0 < event.x < self.width-10 and 0 < event.y < self.height-10 and
            self.edgeAdjust == False):
            (self.mouseMoveX, self.mouseMoveY) = (event.x, event.y)
            if(self.mouseMoveX == self.width or self.mouseMoveX == 0):pass
            preLook+=(self.sensitivityY)/25*(self.oldMouseMoveY-self.mouseMoveY)
            preDegrees -= ((Decimal(self.sensitivityX)/Decimal(100))*
                            (self.oldMouseMoveX-self.mouseMoveX))
            self.oldMouseMoveX = self.mouseMoveX
            self.oldMouseMoveY = self.mouseMoveY
            if(abs(preLook - oldLook) > 10):self.look = preLook
            if(abs(preDegrees - oldDegrees) > 5):self.degrees = preDegrees
        elif(self.midX -100 <= event.x <= self.midX +100 and
            self.mouseMoveY-20<= event.y <=self.mouseMoveY +20):
            self.edgeAdjust = False
        else:
            windll.user32.SetCursorPos(self.midX,self.mouseMoveY)
            self.edgeAdjust = True #Taken from the internet

    def onMouseLeftPress(self, event):
        (mouseX, mouseY) = (event.x, event.y)
        if(self.start == False):self.testButtons(event)
        if(self.start == True):
            if(self.gameMode == "GridHunt"):
                if(self.equipedWeapon == "shotgun"):self.createPlayer("shotgun")
            elif(self.gameMode == "GridEdit"):
                (self.gridEditMouseX, self.gridEditMouseY) = (mouseX, mouseY)

    def testButtons(self, event): #Test to see if the buttons are pressed
        (mouseX, mouseY) = (event.x, event.y)
        if(self.topLeftGridRun[0]<=mouseX<=self.bottomRightGridRun[0] and
            self.topLeftGridRun[1]<=mouseY<=self.bottomRightGridRun[1]):
            self.gameMode = "GridTest"
        elif(self.topLeftGridHunt[0]<=mouseX<=self.bottomRightGridHunt[0]
        and self.topLeftGridHunt[1]<=mouseY<=self.bottomRightGridHunt[1]):
            self.gameMode = "GridHunt"
        elif(self.topLeftGridEdit[0]<=mouseX<=self.bottomRightGridEdit[0]
        and self.topLeftGridEdit[1]<=mouseY<=self.bottomRightGridEdit[1]):
            self.gameMode = "GridEdit"
        elif(self.topLeftHelp[0]<=mouseX<=self.bottomRightHelp[0] and
            self.topLeftHelp[1]<=mouseY<=self.bottomRightHelp[1]):
            self.gameMode = "Help"
        elif(self.topLeftOptions[0]<=mouseX<=self.bottomRightOptions[0] and
            self.topLeftOptions[1]<=mouseY<=self.bottomRightOptions[1]):
            self.gameMode = "Options"
        elif(self.topLeftCubeRun[0]<=mouseX<=self.bottomRightCubeRun[0] and
            self.topLeftCubeRun[1]<=mouseY<=self.bottomRightCubeRun[1]):
            self.gameMode = "CubeRunner"
            self.gridY = self.row-2
            self.gridXY=[self.gridX,self.gridY]*2
        if(self.gameMode != None):self.startGame()
            
    def onMouseLeftRelease(self, event):pass

    def onMouseRightPress(self, event):self.zoom = 2
        
    def onMouseRightRelease(self, event):self.zoom = 1

    def onKeyPress(self, event): #called by the Key Presses
        if(self.start == True):
            if(self.gameMode in["GridHunt","GridTest"]):self.gridMovement(event)
            elif(self.gameMode == "CubeRunner"):self.cubeRunnerMovement(event)
            elif(self.gameMode == "GridEdit"):self.gridEditKeys(event)
        if(event.keysym == "Tab"):
            self.canvas.delete(ALL)
            self.timerDelay = 1 
            self.restart()
        if(event.keysym == "Escape"):self.root.destroy()

    def gridEditKeys(self, event):
        if(event.keysym == "s"):
            fileName = self.savePrompt()
            path = self.folder + os.sep + fileName
            self.writeFile(path)
        if(event.keysym == "c"):
            self.grid = []
            for row in xrange(self.row):self.grid += [[0]*self.col]
        if(event.keysym == "r"):self.resizePrompt()
            
    def savePrompt(self):# Help from dialogs-demo2.py and dialogs-demo1.py
        fileName = str(askstring("Save as", "Please name file"))
        return fileName

    def resizePrompt(self):# Help from dialogs-demo2.py and dialogs-demo1.py
        self.row = self.col = int(askstring("Resize", "Rows and Columns"))
        self.grid = []
        for row in xrange(self.row):self.grid += [[0]*self.col]

    def cubeRunnerMovement(self, event):
        if(event.keysym == "a"):  #strafe left
            Grid(self.grid, self.gridXY, self.boxXY,self.degrees,
                self.speed).cubeMove("left")
        if(event.keysym == "d"): #strafe right
            Grid(self.grid, self.gridXY, self.boxXY,self.degrees,
                self.speed).cubeMove("right")
        if(event.keysym == "v"):self.fill = ""

    def gridMovement(self, event):
        if(event.keysym == "Shift_L"): #sprint forward
            Grid(self.grid, self.gridXY,self.boxXY,self.degrees,
                 self.speed*3).move("forward")
        if(event.keysym == "w"): #move forward
            Grid(self.grid, self.gridXY,self.boxXY,self.degrees,
                self.speed).move("forward")
        if(event.keysym == "s"): #move backward
            Grid(self.grid, self.gridXY,self.boxXY,self.degrees,
                self.speed).move("back") 
        if(event.keysym == "a"):  #strafe left
            Grid(self.grid, self.gridXY, self.boxXY,self.degrees,
                self.speed).move("left")
        if(event.keysym == "d"): #strafe right
            Grid(self.grid, self.gridXY, self.boxXY,self.degrees,
                self.speed).move("right")
        if(event.keysym == "Left"):self.degrees -= 5
        if(event.keysym == "Right"):self.degrees += 5
        if(event.keysym == "v"):self.fill = ""
        if(event.keysym == "Up"):self.look += 10
        if(event.keysym == "Down"):self.look -= 10

    def onKeyRelease(self, event):
        if(self.pause == False):
            if(event.keysym == "v"):self.fill = self.oldFill

######################################################################
#redrawAll Functions
######################################################################

    def redrawAll(self): #called by self.run() in EventBasedAnimationClass
        if(self.start == False):self.startScreen()
        elif(self.pause == False):
            if(self.gameMode != "Options"):self.timerDelay = 10
            if(self.gameMode == "GridTest"):self.runGridTest()
            elif(self.gameMode == "GridHunt"):self.runGridHunt()
            elif(self.gameMode == "GridEdit"):self.runGridEdit()
            elif(self.gameMode == "CubeRunner"):self.runCubeRunner()
            elif(self.gameMode == "Help"):self.runHelpScreen()
            elif(self.gameMode == "Options"):self.runOptions()
            
    def startGame(self):
        (self.start, self.degrees, self.fill) = (True, 91, self.oldFill)
        self.options(),self.initAnimation()

    def runGridTest(self):#called by self.redrawAll()
        self.canvas.delete(ALL)
        self.gridAI = None
        (self.weaponMidX, self.weaponMidY) = (self.midX, self.midY)
        self.drawHorizon(), self.createGrid()#draws the background
        self.drawGrid(), self.drawPoint() #draws the mini-map
                
    def runGridHunt(self):#called by self.redrawAll()
        self.canvas.delete(ALL)
        self.options()
        self.equipedWeapon = "shotgun"
        self.drawHorizon(), self.createGrid()#draws the background
        self.createPlayer(None)
        self.drawGrid(), self.drawPoint() #draws the mini-map
        self.drawHUD("black")

    ##################################################################
    #GridEdit
    ##################################################################

    def runGridEdit(self):#called by self.redrawAll()
        self.canvas.delete(ALL)
        self.drawGridEdit()

    def drawGridEdit(self):#draws the board
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="white")
        instructions = """INSTRUCTIONS\n\nPress "s" to save grid
Press "c" to clear grid\nPress "r" to resize grid\nClick on boxes to change type
Black boxes are empty space\nColored boxes are walls\n\nPress TAB to EXIT"""
        self.canvas.create_text(self.midX, self.midY/4, text = "Grid Edit",
                                font = "Arial 60 bold")
        self.canvas.create_text(self.midX/2.5, self.midY,
        text = instructions, font = "Arial 30 bold")
        for row in xrange(self.row):
            for col in xrange(self.col):
                self.drawBoxEdit(row, col)
        
    def drawBoxEdit(self, row, col):#called by self.drawGridEdit()
        #draws each box in the grid
        (stipple, area, width) = ("gray50", self.area *2, 1)
        if(self.grid[row][col]==1):color,stipple=Main.rgb(250,250,0),"gray50"
        elif(self.grid[row][col]==2):color = self.oldFill, #blue
        else:color = Main.rgb(0,0,0) #black
        left = (col*area+self.midX)
        top = (row*area+self.midY-(self.row*area)/2)
        right = (col*area+self.midX+area)
        bottom = (row*area+self.midY-(self.row*area)/2+area)
        if(left < self.startScreenMouseX < right and 
           top < self.startScreenMouseY < bottom):(stipple,width) = (None,5)
        if(left < self.gridEditMouseX < right and 
           top < self.gridEditMouseY < bottom):
            if(self.grid[row][col] == 0):self.grid[row][col] = 2
            elif(self.grid[row][col] == 2):self.grid[row][col] = 0
            self.gridEditMouseX = self.gridEditMouseY = None
        self.canvas.create_rectangle(left,top,right,bottom,
            fill = color, stipple = stipple, width = width)

    ##################################################################
    #CubeRunner
    ##################################################################

    def runCubeRunner(self):#called by self.redrawAll()
        self.canvas.delete(ALL)
        for col in xrange(self.col):self.grid[self.row-1][col] = 0
        legal=Grid(self.grid, self.gridXY,self.boxXY,self.degrees,
            self.speed*self.cubeRunnerMultiplier).cubeMove("forward")
        if(legal[0] == False):self.pause = True
        if(legal[1] == True):self.shiftGrid()
        self.gridAI = None
        self.drawDarkHorizon(),self.createGrid()
        self.score += (Decimal(self.time)*Decimal(self.cubeRunnerMultiplier)/
                       Decimal(100))
        self.drawGrid(), self.drawPoint(), self.drawHUD("green")
        if(self.pause == True):self.drawGameOver()

    def shiftGrid(self):
        for row in xrange(self.row-2,1,-1):
            self.grid[row] = deepcopy(self.grid[row-1])
        self.grid[1] = self.grid[0]
        block = []
        emptyRow = randint(0,1)
        if(emptyRow == 0):
            for blocks in xrange(2):
                block.append(randint(0,self.col-1))
        for col in xrange(1,self.col-1):
            if(col in block):self.grid[0][col] = 2
            else:self.grid[0][col] = 0
            self.grid[0][0] = self.grid[0][self.col-1] = 2

    def drawGameOver(self):
        endScreenText = "Score: %d\nPress Tab to exit to menu" % self.score
        self.canvas.create_rectangle(0,0,self.width,self.height,fill = "green",
                                     stipple = "gray12")
        self.canvas.create_text(self.midX,self.midY,text=endScreenText,
                                font="Arial 60 bold")

    ##################################################################
    #HelpScreen
    ##################################################################

    def runHelpScreen(self):
        self.canvas.delete(ALL)
        self.drawHelpScreen()

    ##################################################################
    #Options
    ##################################################################

    def runOptions(self):
        self.canvas.delete(ALL)
        self.timerDelay = 1000
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="white")
        self.canvas.create_text(self.midX, self.midY/4, text = "Options",
                                font = "Arial 60 bold")
        self.bindOptionButtons(),self.buttonsOptions(),self.buttonTitles()

    def buttonTitles(self):
        self.canvas.create_text(self.midX/4,self.midY/2+200,
                    text="Color Adjustment", font ="Arial 30 bold")
        self.canvas.create_text(self.midX/4,self.midY/2,
                    text="Map Import", font ="Arial 30 bold")
        self.canvas.create_text(self.midX*3/4,self.midY/2,
                    text="Cube Runner Settings", font ="Arial 30 bold")

    def buttonsOptions(self):
        self.canvas.create_window(self.midX/4, self.midY/2 + 100,
                                  window = self.importMapButton)
        self.canvas.create_window(self.midX/4, self.midY/2 + 300,
                                  window = self.changeSkinColor)
        self.canvas.create_window(self.midX/4, self.midY/2 + 400,
                                  window = self.changeSkinStipple)
        self.canvas.create_window(self.midX/4, self.midY/2 + 500,
                                  window = self.changeWallColor)
        self.canvas.create_window(self.midX/4, self.midY/2 + 600,
                                  window = self.changeOutlineColor)
        self.canvas.create_window(self.midX*3/4, self.midY/2 + 100,
                                  window = self.easy)
        self.canvas.create_window(self.midX*3/4, self.midY/2 + 200,
                                  window = self.medium)
        self.canvas.create_window(self.midX*3/4, self.midY/2 + 300,
                                  window = self.hard)
        self.canvas.create_window(self.midX*3/4, self.midY/2 + 400,
                                  window = self.veryHard)
        
    def bindOptionButtons(self):#taken from button-demo3.py
        self.easy = Button(self.canvas, text = "Easy",
                    font = "Arial 20 bold",command = self.setEasy)
        self.medium = Button(self.canvas, text = "Medium",
                    font = "Arial 20 bold",command = self.setMedium)
        self.hard = Button(self.canvas, text = "Hard",
                    font = "Arial 20 bold",command = self.setHard)
        self.veryHard = Button(self.canvas, text = "Very Hard",
                    font = "Arial 20 bold",command = self.setVeryHard)
        self.importMapButton = Button(self.canvas, text = "Import Grid Map",
                    font = "Arial 20 bold",command = self.importMap)
        self.changeWallColor = Button(self.canvas, text = "Change Wall Color",
                    font = "Arial 20 bold",command = self.changeWallColors)
        self.changeOutlineColor = Button(self.canvas, text = "Change Line Color"
                    ,font = "Arial 20 bold",command = self.changeLineColor)
        self.changeSkinColor = Button(self.canvas, text = "Change Skin Color",
                    font = "Arial 20 bold",command = self.changePlayerColor)
        self.changeSkinStipple=Button(self.canvas,text="Change Skin Stipple",
                    font = "Arial 20 bold",command = self.changePlayerStipple)

    def setEasy(self):
        self.cubeRunnerMultiplier = 0.5
        showinfo("Difficulty Reset", "Cube Runner Difficulty set to Easy")

    def setMedium(self):
        self.cubeRunnerMultiplier = 1
        showinfo("Difficulty Reset", "Cube Runner Difficulty set to Medium")

    def setHard(self):
        self.cubeRunnerMultiplier = 1.5
        showinfo("Difficulty Reset", "Cube Runner Difficulty set to Hard")

    def setVeryHard(self):
        self.cubeRunnerMultiplier = 2
        showinfo("Difficulty Reset", "Cube Runner Difficulty set to Very Hard")

    def importMap(self):
        fileName = str(askstring("Open", "Please name the file to import"))
        path = self.folder + os.sep + fileName
        try:
            self.grid = eval(self.readFile(path))
            showinfo("Load Success!", "'%s' Loaded"%(fileName))           
        except:showerror("Load Failure!", "'%s' does not exist"%(fileName))

    def changeWallColors(self):
        color = str(askstring("Color",
                              "Please state the color to change walls to"))
        try:
            self.fill = color
            self.canvas.create_rectangle(0,0,0,0,fill = color)
            showinfo("Load Success!", "The walls are now %s"%(color))
            self.oldFill = color
        except:
            showerror("Load Failure!", "Invalid color name")
            self.fill = self.oldFill

    def changeLineColor(self):
        color = str(askstring("Color",
                            "Please state the color to change lines to"))
        try:
            (outlineOld, self.outline) = (self.outline, color)
            self.canvas.create_rectangle(0,0,0,0,fill = color)
            showinfo("Load Success!", "The lines are now %s"%(color))
        except:
            showerror("Load Failure!", "Invalid color name")
            self.outline = outlineOld

    def changePlayerColor(self):
        color=str(askstring("Color","Please state the color to change skin to"))
        try:
            (skinOld, self.skinColor) = (self.skinColor, color)
            self.canvas.create_rectangle(0,0,0,0,fill = color)
            showinfo("Load Success!", "The lines are now %s"%(color))
        except:
            showerror("Load Failure!", "Invalid color name")
            self.skinColor = skinOld

    def changePlayerStipple(self):
        stipple = str(askstring("Color",
        "Please state either 'gray12', 'gray25', 'gray50', 'gray75', or None"))
        if(stipple in ['gray12', 'gray25', 'gray50', 'gray75', "None"]):
            if(stipple == "None"):stipple = None
            self.skinStipple = stipple
            showinfo("Load Success!","The player's stipple is now %s"%(stipple))
        else:showerror("Load Failure!", "Invalid color name")           
        
######################################################################
#Start Screen Functions
######################################################################

    def startScreen(self):
        self.fill = ""
        self.degrees += 5
        self.drawStartScreen()

    def drawHelpScreen(self):#Draws the Help Screen
        helpLeft = """MOVEMENT
Press "w" to move forwards\nPress "a" to move left\nPress "s" to move backwards
Press "d" to move right\nHold "Shift" to sprint forwards\n\nLOOK
Hold "v" for X-ray vision\nUse arrow keys or mouse to look around
Press Left Mouse Button to shoot\nHold Right Mouse Button to zoom in"""
        helpRight = """CUBE RUNNER
Press "a" to move left\nPress "d" to move right\nHold "v" for X-ray vision\n
EXIT\nPress Escape Key to quit program\nPress Tab Key to quit game
\nPRESS TAB TO EXIT"""
        self.canvas.create_rectangle(0,0,self.width,self.height,fill = "white")
        self.canvas.create_text(self.midX, self.midY/4, text = "Help",
                                font = "Arial 60 bold")
        self.canvas.create_text(self.midX/2, self.midY, text = helpLeft,
                                font="Arial 30 bold")
        self.canvas.create_text(self.midX/2 + self.midX, self.midY,
                                text = helpRight, font="Arial 30 bold")        

    def drawStartScreen(self):
        title = "Tkinter 3D Engine Demo"
        self.canvas.create_rectangle(0,0,self.width,self.height,fill = "white")
        self.drawStartHorizon(self.topLeftGrid, self.bottomRightGrid)
        self.createGrid()
        self.drawScreenEdge()
        self.canvas.create_text(self.midX, self.midY/4, text = title,
                                font = "Arial 40 bold")
        self.drawCubeRunnerButton(),self.drawHelpButton(),
        self.drawGridButton(),self.drawGridHuntButton(),
        self.drawGridEditButton(),self.drawOptionsButton()
        
    def drawStartHorizon(self, topLeft, bottomRight):
        darkSky, darkGround = Main.rgb(200,200,200), Main.rgb(50,50,50)
        self.canvas.create_rectangle(topLeft,bottomRight[0],
        (topLeft[1] + bottomRight[1])/2,fill = darkSky, width = 0)
        self.canvas.create_rectangle(topLeft[0],(topLeft[1]+bottomRight[1])/2,
                                     bottomRight,fill = darkGround, width = 0)

    def drawScreenEdge(self):
        self.canvas.create_rectangle(0,0,self.topLeftGrid[0],self.height,
                                     fill = "white",width = 0)
        self.canvas.create_rectangle(0,0,self.width,self.topLeftGrid[1],
                                     fill = "white",width = 0)
        self.canvas.create_rectangle(0,self.bottomRightGrid[1],self.width,
                                     self.height,fill = "white",width = 0)
        self.canvas.create_rectangle(self.bottomRightGrid[0],
        self.topLeftGrid[1]/2,self.width,self.height,fill = "white",width = 0)

    ##################################################################
    #Buttons
    ##################################################################

    def drawHelpButton(self):
        if(self.topLeftHelp[0]<=self.startScreenMouseX<=self.bottomRightHelp[0]
           and self.topLeftHelp[1]<=self.startScreenMouseY<=
           self.bottomRightHelp[1]):change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftHelp,self.bottomRightHelp
                                ,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text((self.bottomRightHelp[0]+self.topLeftHelp[0])/2,
        (self.bottomRightHelp[1]+self.topLeftHelp[1])/2,
         text = "Help", font = "Arial 40 bold")
                                 
    def drawCubeRunnerButton(self):
        if(self.topLeftCubeRun[0] <= self.startScreenMouseX <=
           self.bottomRightCubeRun[0] and self.topLeftCubeRun[1] <=
           self.startScreenMouseY <= self.bottomRightCubeRun[1]):
            change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftCubeRun,self.bottomRightCubeRun
                                ,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text(
        (self.bottomRightCubeRun[0]+self.topLeftCubeRun[0])/2,
        (self.bottomRightCubeRun[1]+self.topLeftCubeRun[1])/2,
        text = "Cube Runner", font = "Arial 40 bold")

    def drawOptionsButton(self):
        if(self.topLeftOptions[0] <= self.startScreenMouseX <=
           self.bottomRightOptions[0] and self.topLeftOptions[1] <=
           self.startScreenMouseY <= self.bottomRightOptions[1]):
            change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftOptions,self.bottomRightOptions
                                ,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text(
        (self.bottomRightOptions[0]+self.topLeftOptions[0])/2,
        (self.bottomRightOptions[1]+self.topLeftOptions[1])/2,
        text = "Options", font = "Arial 40 bold")

    def drawGridButton(self):
        if(self.topLeftGridRun[0] <= self.startScreenMouseX <=
           self.bottomRightGridRun[0] and self.topLeftGridRun[1] <=
           self.startScreenMouseY <= self.bottomRightGridRun[1]):
            change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftGridRun,self.bottomRightGridRun
                                ,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text(
        (self.bottomRightGridRun[0]+self.topLeftGridRun[0])/2,
        (self.bottomRightGridRun[1]+self.topLeftGridRun[1])/2,
        text = "Grid Test", font = "Arial 40 bold")

    def drawGridHuntButton(self):
        if(self.topLeftGridHunt[0] <= self.startScreenMouseX <=
           self.bottomRightGridHunt[0] and self.topLeftGridHunt[1] <=
           self.startScreenMouseY <= self.bottomRightGridHunt[1]):
            change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftGridHunt,
        self.bottomRightGridHunt,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text(
        (self.bottomRightGridHunt[0]+self.topLeftGridHunt[0])/2,
        (self.bottomRightGridHunt[1]+self.topLeftGridHunt[1])/2,
        text = "Grid Hunt", font = "Arial 40 bold")

    def drawGridEditButton(self):
        if(self.topLeftGridEdit[0] <= self.startScreenMouseX <=
           self.bottomRightGridEdit[0] and self.topLeftGridEdit[1] <=
           self.startScreenMouseY <= self.bottomRightGridEdit[1]):
            change = "gray12"
        else:change = None
        self.canvas.create_rectangle(self.topLeftGridEdit,
        self.bottomRightGridEdit,fill = "gray", width = 10, stipple = change)
        self.canvas.create_text(
        (self.bottomRightGridEdit[0]+self.topLeftGridEdit[0])/2,
        (self.bottomRightGridEdit[1]+self.topLeftGridEdit[1])/2,
        text = "Grid Edit", font = "Arial 40 bold")

######################################################################
#Player Functions
######################################################################
            
    def createPlayer(self,fired):
        self.drawArms()
        (topLeft, bottomRight) = self.drawCrosshairs()
        if(fired == "shotgun"):
            self.drawShotgunBlast()
            self.fireShotgun(topLeft, bottomRight)
        if(self.equipedWeapon == "shotgun"):self.drawShotgun()
        if(self.zoom > 1):self.drawReticle()
        

    def fireShotgun(self, topLeft, bottomRight):
        for side in [self.frontAI, self.backAI, self.leftAI, self.rightAI]:
            if(side != None):
                if (side[0][0] >= (topLeft[0] and bottomRight[0]) >= side[1][0]
               and side[0][1] >= (topLeft[1] and bottomRight[1]) >= side[1][1]):
                    self.score+=1
                    self.deathAI()
                if(topLeft[0] <= (side[0][0] or side[1][0]) <= bottomRight[0]
               and topLeft[1] <= (side[0][1] or side[1][1]) <= bottomRight[1]):
                    self.score+=1
                    self.deathAI()
    ##################################################################
    #Drawing Functions
    ##################################################################

        ##################################################################
        #Player Functions
        ##################################################################
    def drawCrosshairs(self): #draws the crosshairs on the screen
        distance = 50/self.zoom**2 - (self.zoom-1)*100
        self.canvas.create_rectangle((self.midX - 100 -distance, self.midY - 2),
        (self.midX-125-distance,self.midY+2),
        fill = "white",width = 1,stipple ="gray12") #left
        self.canvas.create_rectangle((self.midX + 100 +distance, self.midY - 2),
        (self.midX + 125+distance, self.midY + 2),
        fill = "white",width = 1,stipple ="gray12") #right
        self.canvas.create_rectangle((self.midX -2, self.midY - 100-distance),
        (self.midX + 2, self.midY - 125-distance),
        fill = "white",width = 1,stipple ="gray12") #top
        self.canvas.create_rectangle((self.midX -2, self.midY + 100+distance),
        (self.midX + 2, self.midY + 125+distance),
        fill = "white",width = 1,stipple ="gray12") #bottom
        topLeft = (self.midX-125-distance, self.midY - 125-distance)
        bottomRight = (self.midX + 125+distance, self.midY + 125+distance)
        return topLeft, bottomRight

    def drawArms(self): #draws the arms
        (handX, handY, ads) = (self.weaponMidX,self.weaponMidY,125*self.zoom)
        bottomLeft,topRight = (0,self.midY+self.height),(handX-ads, handY)
        bottomRight,topLeft = (handX, handY+ads),(-self.midX,self.height)
        self.drawPolygon(topLeft, bottomLeft, bottomRight, topRight,
                         self.skinColor,"black", 5,self.skinStipple) #Left Hand
        bottomRight,topLeft=(self.width,self.midY+self.height),(handX+ads,handY)
        bottomLeft,topRight=(self.midX+self.width,self.height),(handX,handY+ads)
        if(self.zoom == 1):
            self.drawPolygon(topLeft, bottomLeft, bottomRight, topRight,
                         self.skinColor,"black", 5,self.skinStipple) #Right Hand

    def drawShotgun(self): #Draws the shotgun for the player
        color = Main.rgb(15,15,15)
        if(self.zoom != 1):
            topLeft = (self.midX-50,self.midY+50)
            bottomLeft = (self.midX-500,self.midY+450)
            bottomRight = (self.midX+500,self.midY+450)
            topRight = (self.midX+50,self.midY+50)
            self.drawPolygon(topLeft, bottomLeft, bottomRight, topRight,
                             color,"black", 5, None)
        elif(self.zoom == 1):
            topLeft = (self.midX-50+200,self.midY+50)
            topRight = (self.midX+50+200,self.midY+50)
            bottomLeft = (self.midX-500+800,self.midY+450)
            bottomRight = (self.midX+500+500,self.midY+450)
            self.drawPolygon(topLeft, bottomLeft, bottomRight, topRight,
                             color,"black", 5, None)
            topRight, bottomRight = topLeft, bottomLeft
            topLeft = (topRight[0],self.midY+100)
            bottomLeft = (self.midX-500+800,self.midY+800)
            self.drawPolygon(topLeft, bottomLeft, bottomRight, topRight,
                             color,"black", 5, None)
            
    def drawShotgunBlast(self):
        if(self.zoom == 1):
            self.canvas.create_oval(self.midX+50,self.midY-50,
            self.midX+300+100,self.midY+50+150,fill = "yellow",width=0)
            self.canvas.create_oval(self.midX+100,self.midY,
            self.midX+300+50,self.midY+50+100,fill = "white",width = 0)
        if(self.zoom != 1):
            self.canvas.create_oval(self.midX-200,self.midY-100,
            self.midX+200,self.midY+300,fill = "yellow",width = 0)
            self.canvas.create_oval(self.midX-100,self.midY,
            self.midX+100,self.midY+200,fill = "white",width = 0)

    def drawReticle(self):#creates the zoom reticle
        (midX, midY, area, adjust) = (self.midX, self.midY, self.area,190)
        topLeft = (midX + 8*area, midY - 6*area),(midX+6*area,midY-8*area)
        topRight = (midX - 6*area, midY - 8*area),(midX-8*area,midY-6*area)
        bottom = (midX-8*area,midY+8*area),(midX + 8*area, midY + 8*area)
        self.drawPolygon((topLeft[0][0],topLeft[0][1]),(topRight[1][0],
        topRight[1][1]),topRight[0],topLeft[1],"green","green",5,"gray25")
        self.drawPolygon((topLeft[0][0]-25,topLeft[0][1]),
        (topLeft[0][0],topLeft[0][1]),(topLeft[0][0],bottom[0][1]),
        (topLeft[0][0]-25,bottom[0][1]-25),"green","green",5,"gray25")
        self.drawPolygon((topRight[1][0]+25,topRight[1][1]),#left side
        (topRight[1][0],topRight[1][1]),(topRight[1][0],bottom[1][1]),
        (topRight[1][0]+25,bottom[1][1]-25),"green","green",5,"gray25")
        self.canvas.create_line(topRight[1][0]+25,bottom[1][1]-25,
        topLeft[0][0]-25,bottom[0][1]-25,fill="green",width=5)
        self.canvas.create_polygon(topLeft,topRight,bottom,
        fill = "blue", outline = "green", width = 5, stipple="gray12")
        self.canvas.create_oval(midX-area,midY-area,midX+area,midY+area,
                                fill = "",outline = "red", width = 5)
        self.canvas.create_oval(midX-area/8,midY-area/8,midX+area/8,midY+area/8,
                    fill = "red",outline = "red",width = 5,stipple="gray12")

    def drawPolygon(self, topLeft, bottomLeft, bottomRight, topRight, fillColor,
                    outlineColor, size, stippleType):
        self.canvas.create_polygon(topLeft, bottomLeft, bottomRight, topRight,
        fill = fillColor, outline=outlineColor,width=size,stipple=stippleType)

######################################################################
#Map and AI Functions
######################################################################

    def deathAI(self):
        validSpawn = False
        while(validSpawn == False):
            spawnX, spawnY = randint(0,self.row-1), randint(0,self.col-1)
            if(self.grid[spawnX][spawnY] == 0): 
                self.gridAI = (spawnX,spawnY)
                validSpawn = True
        self.coordinatesAI = []

        
    def createGrid(self): #called by self.redrawAll()
        self.verticesForwards = Vertices().forwards(self.gridAI,self.grid,
                            self.directionAI,self.coordinatesAI)[0]
        self.verticesBackwards = self.verticesForwards[::-1]#reverses list
        self.verticesLeft = Vertices().left(self.gridAI,self.grid,
                            self.directionAI,self.coordinatesAI)[0]
        self.verticesRight = self.verticesLeft[::-1]#reverses list
        if(2 in self.grid):
            self.gridAI = Vertices().forwards(self.gridAI,self.grid,
                                self.directionAI,self.coordinatesAI)[1]
            self.directionAI =Vertices().forwards(self.gridAI,self.grid,
                                self.directionAI,self.coordinatesAI)[2]
        degrees = (self.degrees +1080) %360
        if(45 <=degrees<135):self.createHalfGrid(self.verticesForwards)
        elif(135<=degrees<225):self.createHalfGrid(self.verticesRight)
        elif(225<=degrees<315):
            self.createHalfGrid(self.verticesBackwards)
        elif(315<=degrees<360 or 0<=degrees<45):
            self.createHalfGrid(self.verticesLeft)

    def createHalfGrid(self, direction):
        degrees = (self.degrees +1080) %360
        for index in direction:#Calculates only half the map
            if(self.grid[index[0][2]][index[0][3]] == 2): drawType = "wall"
            elif((index[0][2],index[0][3]) == self.gridAI): drawType = "AI"
            if((45 <= degrees < 135 and index[0][2]-2  < self.gridXY[1]) or
                (135<= degrees < 225 and index[0][3]+2 > self.gridXY[0]) or
                (225<= degrees < 315 and index[0][2]+2 > self.gridXY[1]) or
                ((315<=degrees < 360)or(0 <= degrees < 45))and index[0][3]-2 
                < self.gridXY[0]):self.createBox(index, drawType)
        

    def createBox(self, coor, drawType): #called by self.createMap()
        #determines the type of map that is mades i.e. transparent or solid
        frontLeft,frontRight,backLeft,backRight=coor[0],coor[1],coor[2],coor[3]
        self.location = Point(self.gridXY,self.boxXY).location() #finds location
        if(self.fill == "" and drawType == "wall"):
            self.transparent(frontLeft, frontRight, backLeft, backRight)
        elif(drawType == "wall"):
            self.solid(frontLeft, frontRight, backLeft, backRight)
        elif(drawType == "AI"):
            (front, back, left, right) = self.transparent(frontLeft, frontRight,
                                                          backLeft, backRight)
            (self.frontAI, self.backAI, self.leftAI, self.rightAI) = (front,
                                                            back, left, right)

    ##################################################################
    #Transparent Enviroment Functions
    ##################################################################

    def transparent(self, frontLeft, frontRight, backLeft, backRight):
        #called by self.createBox
        front = self.createWalls(frontLeft,frontRight,"front") #front face
        back = self.createWalls(backLeft,backRight,"back") #back face
        left = self.createWalls(frontLeft, backLeft,"left") #left face
        right = self.createWalls(frontRight, backRight,"right") #right face
        return front, back, left, right
        
    ##################################################################
    #Solid Enviroment Functions
    ##################################################################
        
    def solid(self, frontLeft, frontRight, backLeft, backRight):
        #called by self.createBox
        degrees = (self.degrees +1080) %360
        if(frontLeft[2]in[0,self.row-1] and frontLeft[3]in[0,self.col-1]):pass
        else:
            if(frontLeft[2] == 0):
                self.createWalls(frontLeft, frontRight, "front")
            elif(frontLeft[2] == self.row-1):
                self.createWalls(backLeft,backRight,"back")
            elif(frontLeft[3] == 0):
                self.createWalls(frontRight, backRight,"right")
            elif(frontLeft[3] == self.col-1):
                self.createWalls(frontLeft, backLeft,"left")
            elif(45 <= degrees < 135 and self.gridXY[1] >= frontLeft[2]+1):
                self.faceForward(frontLeft, frontRight, backLeft, backRight)
            elif(135 <= degrees < 225 and self.gridXY[0] <= frontLeft[3]+1):
                self.faceLeft(frontLeft, frontRight, backLeft, backRight)
            elif(225 <= degrees < 315 and self.gridXY[1] <= frontLeft[2]+1):
                self.faceRight(frontLeft, frontRight, backLeft, backRight)
            elif((315 <= degrees < 360)or(0 <= degrees < 45)and
                self.gridXY[0] >= frontLeft[3]+1):
                self.faceBackward(frontLeft, frontRight, backLeft, backRight)            

    def faceForward(self, frontLeft, frontRight, backLeft, backRight):
        if(self.gridXY[0] == frontLeft [3]):
            self.createWalls(frontLeft,frontRight,"front") #front face
        if(self.gridXY[0] > frontLeft [3]):
            self.createWalls(frontLeft,frontRight,"front") #front face
            self.createWalls(frontRight, backRight,"right") #right face
        if(self.gridXY[0] < frontLeft [3]):
            self.createWalls(frontLeft,frontRight,"front") #front face
            self.createWalls(frontLeft, backLeft,"left") #left face

    def faceLeft(self, frontLeft, frontRight, backLeft, backRight):
        if(self.gridXY[1] == frontLeft [2]):
            self.createWalls(frontLeft, backLeft,"left") #right face
        if(self.gridXY[1] > frontLeft [2]):
            self.createWalls(frontLeft, backLeft,"left") #right face
            self.createWalls(frontLeft,frontRight,"front") #front face
        if(self.gridXY[1] < frontLeft [2]):
            self.createWalls(frontLeft, backLeft,"left") #right face
            self.createWalls(backLeft,backRight,"back") #back face

    def faceRight(self, frontLeft, frontRight, backLeft, backRight):
        if(self.gridXY[0] == frontLeft [3]):
            self.createWalls(backLeft,backRight,"back") #back face
        if(self.gridXY[0] > frontLeft [3]):
            self.createWalls(backLeft,backRight,"back") #back face
            self.createWalls(frontRight, backRight,"right") #right face
        if(self.gridXY[0] < frontLeft [3]):
            self.createWalls(backLeft,backRight,"back") #back face
            self.createWalls(frontLeft, backLeft,"left") #left face

    def faceBackward(self, frontLeft, frontRight, backLeft, backRight):
        if(self.gridXY[1] == frontLeft [2]):
            self.createWalls(frontRight, backRight,"right") #right face
        if(self.gridXY[1] > frontLeft [2]):
            self.createWalls(frontRight, backRight,"right") #right face
            self.createWalls(frontLeft,frontRight,"front") #front face
        if(self.gridXY[1] < frontLeft [2]):
            self.createWalls(frontRight, backRight,"right") #right face
            self.createWalls(backLeft,backRight,"back") #back face

    ##################################################################
    #Coordinate Functions
    ##################################################################

    def createWalls(self, left, right, side):
        (adjustX, adjustY) = self.locationAdjust()
        degrees = (self.degrees +1080) %360
        xLeft = left[0] - self.location[0] + adjustX
        yLeft = left[1] - self.location[1] + adjustY
        xRight = right[0] - self.location[0] + adjustX
        yRight = right[1] - self.location[1] + adjustY
        if((((315 <= degrees < 360)or(0 <= degrees < 45))and yLeft<0 and
            yRight<0)or(45 <= degrees < 135 and xLeft > 0 and xRight > 0)
            or(135<= degrees < 225 and yLeft > 0 and yRight > 0)
            or(225<= degrees < 315 and xLeft < 0 and xRight < 0)):
            if(yLeft != 0 and yRight != 0):
                leftTan = Decimal(xLeft)/Decimal(yLeft)
                rightTan = Decimal(xRight)/Decimal(yRight)
            else:
                leftTan = Decimal(xLeft)/Decimal(1)
                rightTan = Decimal(xRight)/Decimal(1)
            leftAng, rightAng = (atan(leftTan), atan(rightTan))
            leftHypotenuse = (xLeft**2 + yLeft**2)**0.5
            rightHypotenuse = (xRight**2 + yRight**2)**0.5
            (topLeft,bottomRight)=self.coordinateAlgorithm(left,right, leftAng,
                                rightAng, side,leftHypotenuse, rightHypotenuse)
            return topLeft, bottomRight

    def locationAdjust(self):#allow the player to see all the walls
        (degrees, adjust) = ((self.degrees +1080) %360, 15)
        if(0 <= degrees < 45): (adjustX, adjustY) = (0,-adjust)
        if(45 <= degrees < 90): (adjustX, adjustY) = (+adjust,0)
        if(90 <= degrees < 135): (adjustX, adjustY) = (+adjust,0)
        if(135 <= degrees < 180): (adjustX, adjustY) = (0,+adjust)
        if(180 <= degrees < 225): (adjustX, adjustY) = (0,+adjust)
        if(225 <= degrees < 270): (adjustX, adjustY) = (-adjust,0)
        if(270 <= degrees < 315): (adjustX, adjustY) = (-adjust,0)
        if(315 <= degrees < 360): (adjustX, adjustY) = (0,-adjust)
        return adjustX, adjustY

    def coordinateAlgorithm(self, left, right, leftAng, rightAng, side,
        leftHypotenuse, rightHypotenuse):#called by self.createWalls
        xLeft = leftHypotenuse * (sin(radians(-self.degrees + 90) - leftAng))
        yLeft = leftHypotenuse*(cos(radians(self.degrees + 90) + leftAng))
        xRight = rightHypotenuse*(sin(radians(-self.degrees + 90) - rightAng))
        yRight = rightHypotenuse*(cos(radians(self.degrees + 90) + rightAng))
        topLeft = self.coordinateConversion(right,xRight, yRight, +1, side)
        bottomLeft = self.coordinateConversion(right,xRight, yRight, -1, side)
        bottomRight = self.coordinateConversion(left,xLeft, yLeft, -1, side)
        topRight = self.coordinateConversion(left, xLeft, yLeft, +1, side)
        if(abs(xLeft) < self.area and abs(xRight) < self.area):pass
        else:
            if(self.grid[left[2]][left[3]] == 2):
                self.drawWall(topLeft, bottomLeft, bottomRight, topRight)
            else:self.drawAI(topLeft, bottomLeft, bottomRight, topRight)
        return topLeft, bottomRight

    def coordinateConversion(self, corner, xDist, yDist, constant, side):
        #called by self.coordinateAlgortihm()
        if(self.start == False):
            midY = (self.topLeftGrid[1] + self.bottomRightGrid[1])/2
            midX = (self.topLeftGrid[0] + self.bottomRightGrid[0])/2
            self.fov = 15
        else:(midX, midY) = (self.midX, self.midY)
        degrees = (self.degrees +1080) %360
        scaleX = (self.zoom*self.fov * 2**0.25 * self.area)/(xDist)
        #the next portion converts 3D coordinates into 2D
        if(((xDist <= -self.area and side in["front", "back"]) or
            (xDist <= self.area and side in["front", "back"]))and
            (45<=degrees<=135 or 225<=degrees<=315)):
            xCoordinate = midX + scaleX * (yDist)
            if(self.grid[corner[2]][corner[3]] == 2):
                yCoordinate = (midY + -scaleX * self.area/2*constant
                                + self.look)
            else:
                yCoordinate = (midY + -scaleX * self.area/4*constant
                                + self.look)
        else:
            xCoordinate = midX + scaleX * (yDist)
            if(self.grid[corner[2]][corner[3]] == 2):
                yCoordinate = (midY + scaleX * self.area/2*constant
                                + self.look)
            else:
                yCoordinate = (midY + scaleX * self.area/4*constant
                                + self.look)
        return xCoordinate, yCoordinate
        
    ##################################################################
    #Drawing Functions
    ##################################################################

    def drawWall(self, topLeft, bottomLeft, bottomRight, topRight):
        if(self.fill == ""):
            self.canvas.create_polygon(topLeft, bottomLeft, bottomRight,
            topRight,fill = self.fill, outline = self.outline, width=5)
        else:
            self.canvas.create_polygon(topLeft, bottomLeft, bottomRight,
            topRight,fill = self.fill, outline="black",width=1,stipple="")

    def drawAI(self, topLeft, bottomLeft, bottomRight, topRight):
        self.canvas.create_polygon(topLeft, bottomLeft, bottomRight, topRight,
                fill = "red", outline="blue",width=1,stipple="gray75")
        
    def drawHorizon(self):
        darkSky, darkGround = Main.rgb(200,200,200), Main.rgb(50,50,50)
        self.canvas.create_rectangle(0,0,self.width,self.midY+self.look, #sky
                                     fill = darkSky,width = 0)
        self.canvas.create_rectangle(0,self.midY+self.look,self.width, #ground
                            self.height, fill= darkGround,width = 0)

    def drawDarkHorizon(self):
        self.canvas.create_rectangle(0,0,self.width,self.height, #sky
                                     fill = "black",width = 0)

    def drawHUD(self, color):
        self.canvas.create_text(self.width-self.area,self.area, anchor = E,
        text="Score: %d"%(self.score),font="Arial 20 bold",
        fill = color)

    def drawGrid(self):#called by self.redrawAll()
        #draws the board
        self.grid = Grid(self.grid,self.gridXY,self.boxXY,
                         self.degrees,self.speed).createGrid()
        for row in xrange(self.row):
            for col in xrange(self.col):self.drawBox(row, col)
        
    def drawBox(self, row, col):#called by self.drawGrid()
        #draws each box in the grid
        stipple = "gray50"
        if(self.grid[row][col]==1):color,stipple=Main.rgb(250,250,0),"gray50"
        elif(self.grid[row][col]==2):color = self.oldFill, #blue
        elif((row+1,col) == self.gridAI and self.fill ==""):color = "red"
        #elif(self.grid[row][col]==0):color = Main.rgb(0,0,0) #black
        else:color = Main.rgb(0,0,0) #black
        self.canvas.create_rectangle((col*self.area),(row*self.area),
        (col*self.area+self.area),(row*self.area+self.area),fill = color,
        stipple = stipple)

    def drawPoint(self):#called by self.redrawAll()
        #draws the point on the grid
        self.canvas.create_line( #tail
        (self.gridXY[2]*self.area+self.boxXY[2]+10*cos(radians(self.degrees))),
        (self.gridXY[3]*self.area+self.boxXY[3]+10*sin(radians(self.degrees))),
        (self.gridXY[2]*self.area+self.boxXY[2]),
        (self.gridXY[3]*self.area+self.boxXY[3]),
        fill = "black")
        self.canvas.create_oval((self.gridXY[2]*self.area+self.boxXY[2]-2),
        (self.gridXY[3]*self.area+self.boxXY[3]-2),
        (self.gridXY[2]*self.area+self.boxXY[2]+2),
        (self.gridXY[3]*self.area+self.boxXY[3]+2),
        fill = "red") #head
        pointerX = self.gridXY[2]*self.area+self.boxXY[2]
        pointerY = self.gridXY[3]*self.area+self.boxXY[3]

######################################################################
#Vertices Class
######################################################################
#Finds the coordinates of all the vertices in the box
class Vertices(Main):#called by self.createMap() in Main class

    def forwards(self, gridAI, grid, directAI, coorAI):#creates list of vertices
        self.plane, self.gridAI, self.coordinatesAI = [], gridAI, coorAI
        self.directionAI, self.grid = directAI, grid
        for row in xrange(self.row):#for all values of 2 in self.grid
            for col in xrange(self.col):#find the coordinates of the vertices
                if(self.grid[row][col] == 2 or (row,col) == self.gridAI):
                    self.plane+=[self.wallLocation(row,col)]
        return self.plane, self.gridAI, self.directionAI

    def left(self, gridAI, grid, directAI, coorAI):#creates a list of vertices 
        self.plane, self.gridAI, self.coordinatesAI = [], gridAI, coorAI
        self.directionAI, self.grid = directAI, grid
        for col in xrange(self.col):#for all values of 2 in self.grid
            for row in xrange(self.row):#find the coordinates of the vertices
                if(self.grid[row][col] == 2 or (row,col) == self.gridAI):
                    self.plane+=[self.wallLocation(row,col)]
        return self.plane, self.gridAI, self.directionAI
        
    def wallLocation(self, row, col):#called by self.left() or forwards()
        coordinateList = []
        if(self.grid[row][col] == 2):drawType = "wall"
        elif((row,col) == self.gridAI):drawType = "AI"
        #print drawType
        for face in ["front","back"]:
            for side in ["left","right"]:
                if(drawType == "wall"):
                    coordinateList.append(self.coordinate(face, side, row, col))
                elif(drawType == "AI"): 
                    if(len(self.coordinatesAI)<4):
                        coordinateList.append(self.coordinateAI
                                              (face,side,row,col))
                        self.coordinatesAI.append(self.coordinateAI
                                              (face,side,row,col))
                    else:
                        coordinateList.append(self.coordinateAIDirection
                                              (face,side,row,col))
        return coordinateList

    def coordinateAI(self, face, side, row, col):
        (midX, midY) = ((self.col*self.area)/2,(self.row*self.area)/2)
        size = self.area/4
        if(face=="front"and side=="left"):adjustX, adjustY = 3*size,size
        if(face=="front"and side=="right"):adjustX = adjustY = 3*size
        if(face=="back"and side=="left"):adjustX = adjustY = size
        if(face=="back"and side=="right"):adjustX, adjustY = size, 3*size
        planeX = -(row*self.area) + midY - adjustX
        planeY = +(col*self.area) - midX + adjustY    
        vertex = (planeX, planeY, row, col)
        return vertex

    def coordinateAIDirection(self, face, side, row, col):
        if(face == "front" and side == "left"): index = 0
        elif(face == "front" and side == "right"): index = 1
        elif(face == "back" and side == "left"): index = 2
        elif(face == "back" and side == "right"): index = 3
        adjustX = self.coordinatesAI[index][0]
        adjustY = self.coordinatesAI[index][1]
        if(self.directionAI == "forwards"):
            adjustX = self.coordinatesAI[index][0] - self.speedAI
        elif(self.directionAI == "backwards"):
            adjustX = self.coordinatesAI[index][0] + self.speedAI
        elif(self.directionAI == "left"):
            adjustY = self.coordinatesAI[index][1] - self.speedAI
        elif(self.directionAI == "right"):
            adjustY = self.coordinatesAI[index][1] + self.speedAI
        centers = self.centerAI(row, col, self.directionAI)
        if(centers[0] == True): #test if legal
            self.coordinatesAI[index] = (adjustX, adjustY)
            centers = self.centerAI(row, col, self.directionAI)
            self.gridAI = (centers[2],centers[1])
        else:
            adjustX = self.coordinatesAI[index][0]
            adjustY = self.coordinatesAI[index][1]
            self.coordinatesAI = []
            Main().deathAI()
        return (adjustX, adjustY, row, col)

    def centerAI(self, row, col, direction):
        averageX = averageY = 0
        (boxXYAI, halfArea) = ([None,None], self.area/2)
        if(direction == "forwards"):
            (degrees, boxXYAI[0], boxXYAI[1]) = (90, -halfArea, 0)
        elif(direction == "backwards"):
            (degrees, boxXYAI[0], boxXYAI[1]) = (270, halfArea, 0)
        elif(direction == "left"):
            (degrees, boxXYAI[0], boxXYAI[1]) = (0, 0, -halfArea)
        elif(direction == "right"):
            (degrees, boxXYAI[0], boxXYAI[1]) = (180, 0, halfArea)
        for index in self.coordinatesAI:
            averageX += index[0]
            averageY += index[1]
        (newRow,newCol)=Point(None,None).inverseLocation(averageX/4,averageY/4)
        gridXYAI = (newRow,newCol)
        return self.legalAI(gridXYAI),newRow, newCol

    def legalAI(self,gridXY):
        if(self.grid[gridXY[0]][gridXY[1]] == 2):return False
        return True
        

    def coordinate(self, face, side, row, col):#called by self.wallLocation()
        (midX, midY) = ((self.col*self.area)/2,(self.row*self.area)/2)
        if(face=="front"and side=="left"):(adjustX, adjustY) = (self.area, 0)
        if(face=="front"and side=="right"):adjustX, adjustY=self.area,self.area
        if(face=="back"and side=="left"):(adjustX, adjustY) = (0, 0)
        if(face=="back"and side=="right"):(adjustX, adjustY) = (0, self.area)
        planeX = -(row*self.area) + midY - adjustX
        planeY = +(col*self.area) - midX + adjustY
        vertex = (planeX, planeY, row, col)
        return vertex

######################################################################
#Point Class
######################################################################
#uses the grids and box points to create plane with new coordinates 
class Point(Main):#called by self.onKeyPressed() in Main class
    def __init__(self, gridXY, boxXY):
        super(Point, self).__init__()
        (self.gridXY, self.boxXY) = (gridXY, boxXY)
        if(gridXY != None and boxXY != None):
            (self.planeX, self.planeY) = self.location()

    def location(self):
        (gridX, gridY) = (self.gridXY[2], self.gridXY[3])
        (midX, midY) = ((self.col*self.area)/2,(self.row*self.area)/2)
        planeX = -(gridY*self.area) + midY - self.boxXY[3]
        planeY = +(gridX*self.area) - midX + self.boxXY[2]
        return planeX, planeY

    def inverseLocation(self, planeX, planeY):
        (midX, midY) = ((self.col*self.area)/2,(self.row*self.area)/2)
        gridX = int(round((planeY + midX)/self.area))
        gridY = -int(round((planeX - midY)/self.area))
        return gridX, gridY
    
######################################################################
#Grid Class
######################################################################
#creates a grid based list not based on coordinates or pixels
#Grid class will track the player and his movement and will stop when
#the player runs to the edge by taking in a list of the surrounding area
class Grid(Main):
    def __init__(self,grid,gridXY,boxXY,degree,speed):
        super(Grid,self).__init__()
        self.grid, self.gridXY, self.boxXY = grid, gridXY, boxXY
        self.degrees, self.speed = degree, speed

    def cubeMove(self,direction):# special move function for cuberunner
        if(direction == "forward"):self.boxXY[3] -= self.speed
        elif(direction == "left"):self.boxXY[2] -= self.speed
        elif(direction == "right"):self.boxXY[2] += self.speed
        return self.cubeMovement()

    def cubeMovement(self):
        #changes the grid list when the point leaves a grid
        shift = False
        if(0 >= self.boxXY[2]): #left side
            self.boxXY[2] = self.area-abs(self.boxXY[2])
            self.gridXY[2]= self.gridXY[2] - 1
        if(0 >= self.boxXY[3]): #top side
            self.boxXY[3] = self.area-abs(self.boxXY[3])
            shift = True
        if(self.area <= self.boxXY[2]): #right side
            self.boxXY[2] = self.area-abs(self.boxXY[2])
            self.gridXY[2] = self.gridXY[2] + 1
        legal = self.edgeLegal() #checks if the point is in the grid
        self.createGrid()
        (self.gridXY[0], self.gridXY[1]) = (self.gridXY[2], self.gridXY[3])
        (self.boxXY[0], self.boxXY[1]) = (self.boxXY[2], self.boxXY[3])
        return legal, shift
        
    def move(self, direction): #called by self.onKeyPressed() from Main class
        if(direction == "forward"):
            self.boxXY[2] -= self.speed * cos(radians(self.degrees))
            self.boxXY[3] -= self.speed * sin(radians(self.degrees))
        elif(direction == "back"):
            self.boxXY[2] += self.speed * cos(radians(self.degrees))
            self.boxXY[3] += self.speed * sin(radians(self.degrees))
        elif(direction == "left"):
            self.boxXY[2] += self.speed * cos(radians(self.degrees) + pi/2)
            self.boxXY[3] += self.speed * sin(radians(self.degrees) + pi/2)
        elif(direction == "right"):
            self.boxXY[2] += self.speed * cos(radians(self.degrees) - pi/2)
            self.boxXY[3] += self.speed * sin(radians(self.degrees) - pi/2)
        self.movement() #calls the movement function

    def movement(self): #called by self.move()
        #changes the grid list when the point leaves a grid
        if(0 >= self.boxXY[2]): #left side
            self.boxXY[2] = self.area-abs(self.boxXY[2])
            self.gridXY[2]= self.gridXY[2] - 1
        if(0 >= self.boxXY[3]): #top side
            self.boxXY[3] = self.area-abs(self.boxXY[3])
            self.gridXY[3] = self.gridXY[3] - 1
        if(self.area <= self.boxXY[2]): #right side
            self.boxXY[2] = self.area-abs(self.boxXY[2])
            self.gridXY[2] = self.gridXY[2] + 1
        if(self.area <= self.boxXY[3]): #bottom side
            self.boxXY[3] = self.area-abs(self.boxXY[3])
            self.gridXY[3] = self.gridXY[3] + 1
        self.edgeLegal() #checks if the point is in the grid
        self.createGrid()
        (self.gridXY[0], self.gridXY[1]) = (self.gridXY[2], self.gridXY[3])
        (self.boxXY[0], self.boxXY[1]) = (self.boxXY[2], self.boxXY[3])

    def edgeLegal(self): #called by self.movement()
        #checks if the player move is legal i.e. running into a wall
        legal = True
        if(self.gridXY[2] < 0 or self.gridXY[3] < 0 or self.gridXY[2] >
           self.col - 1 or self.gridXY[3] > self.row - 1):legal=self.notLegal()
        if(self.grid[self.gridXY[3]][self.gridXY[2]] == 2):legal=self.notLegal()
        if(self.boxXY[2] < 5 and
           self.grid[self.gridXY[3]][self.gridXY[2]-1]==2):legal=self.notLegal()
        if(self.boxXY[3] < 5 and
           self.grid[self.gridXY[3]-1][self.gridXY[2]]==2):legal=self.notLegal()
        if(self.boxXY[2] > self.area - 5 and
           self.grid[self.gridXY[3]][self.gridXY[2]+1]==2):legal=self.notLegal()
        if(self.boxXY[3] > self.area - 5 and
           self.grid[self.gridXY[3]+1][self.gridXY[2]]==2):legal=self.notLegal()
        return legal                
            
    def notLegal(self): #called by self.edgeLegal()
        (self.boxXY[2], self.boxXY[3]) = (self.boxXY[0], self.boxXY[1])
        (self.gridXY[2], self.gridXY[3]) = (self.gridXY[0], self.gridXY[1])
        return False

    def createGrid(self):#called by self.drawGrid() from Main class
        #resets the grid and highlights the location of the player
        self.grid[self.gridXY[1]][self.gridXY[0]] = 0
        self.grid[self.gridXY[3]][self.gridXY[2]] = 1
        return self.grid
Main().run()

#Test Functions
"""([[2,2,2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,2,0,2,0,2,0,2,0,2],
                    [2,0,0,2,0,2,0,2,0,0,2],
                    [2,0,2,0,2,0,2,0,2,0,2],
                    [2,0,0,2,0,0,0,2,0,0,2],
                    [2,0,2,0,2,0,2,0,2,0,2],
                    [2,0,0,2,0,2,0,2,0,0,2],
                    [2,0,2,0,2,0,2,0,2,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,2,2,2,2,2,2,2,2,2,2]])""" #11x11 grid with pillars
"""([[2,2,2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,2],
                    [2,2,2,2,2,2,2,2,2,2,2]])""" #11x11 grid without pillars
"""([[2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,2,2],
                    [2,0,2,2,0,0,0,0,2],
                    [2,0,2,2,0,0,2,0,2],
                    [2,0,0,2,0,0,0,0,2],
                    [2,2,0,0,0,2,0,0,2],
                    [2,0,0,2,0,0,0,2,2],
                    [2,0,0,0,0,0,0,0,2],
                    [2,2,2,2,2,2,2,2,2]])""" #9x9 grid with some pillars

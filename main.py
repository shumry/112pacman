# events-example0.py
# Barebones timer, mouse, and keyboard events
import copy, random
from tkinter import *
import heapq
from TPClasses import Ghost, AIPlayer
from Astar import AStar, Cell
from tkinter.font import Font

####################################
# customize these functions
####################################
# 0 - Walkable Space with RegularSeed
# 1 - Wall
# 2 - Ghost Spawn point
# 3 - Null Space
# 4 - SuperSeed
# 5 - Gate
#print


#game states
# 0 is start screen
# 1 is regular play
# 2 is pause
# 3 is help screen
# 5 is with AI Co-op
# 7 is with AI
# 8 is death animation
# 9 is game over
# 11 AI game over

def init(data):
    
    data.originalBlockList =[
    [1,1,1,1,1,1,1,1,3,1,7,1,3,1,1,1,1,1,1,1,1,1],
    [1,0,0,4,0,0,0,1,3,1,0,1,3,1,0,0,4,1,0,0,0,1],
    [1,0,1,1,0,1,0,1,3,1,0,1,3,1,0,1,0,0,0,1,0,1],
    [1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1], #6
    [1,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,2,1,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,5,2,1,0,1,1,1,0,1,1,1,0,1], #mid(10)
    [1,0,0,0,0,1,0,0,0,1,2,1,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1], #15
    [1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,1,0,1,0,1,3,1,0,1,3,1,0,1,0,0,0,1,0,1],
    [1,0,0,4,0,0,0,1,3,1,0,1,3,1,0,0,4,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,3,1,7,1,3,1,1,1,1,1,1,1,1,1]]
    
    
    data.level = 1
    
    data.blockList = copy.deepcopy(data.originalBlockList)
    
    data.displayPacManSize =150
    data.ghostDisplayRadius = 40 #radius
    data.ghostSpace = 280
    data.playerDyingSize = 359
    data.heightGhostTranslation = 35
    data.ghostDisplayList = ["cyan", "red", "pink", "orange"]
    
    #grid information
    data.walkableList = [0,4,9,7]
    data.aiWalkableList = [0,4,9,7]
    data.ghostWalkableList = [0,2,4,5,7]
    data.ghostHome = set([2,5])
    data.seedSet = set([0,4])
    data.warpDict = {(0,10):(18,10), (18,10):(0,10)} #, (4,4):(16,20), (16,20):(4,4)}
    
    data.blockSize = 24
    data.gateSize = 10
    data.wallWidth = data.blockSize//3
    data.marginX = (data.width - (data.blockSize * len(data.blockList)))//2
    data.marginY = (data.height - (data.blockSize * len(data.blockList[0])))//2

    #player start
    data.playerRad = data.blockSize//2 - 3
    data.xStart = data.marginX + (9.5*data.blockSize)
    data.yStart = data.marginY + (16.5*data.blockSize)
    data.playerX = data.xStart
    data.playerY = data.yStart
    data.playerFace = "Left"
    data.playerNextFace = "Left"
    data.playerSpeed= 8
    data.mouthMovementCount = 45
    data.mouthVariability = 8
    data.drawPlayerDirection = 270
    
    #AI stuff
    #self, startX, startY, speed, size, colour, faceDirection)
    data.aiStartX = data.marginX + (9.5*data.blockSize)
    data.aiStartY = data.marginY + (16.5*data.blockSize)
    data.aiSpeed = 6
    data.aiSize = data.blockSize//2 - 3
    data.aiColour = "grey"
    data.aifaceDirection = "Left"
    data.ai = AIPlayer(data.aiStartX, data.aiStartY, data.aiSpeed, data.aiSize, data.aiColour, data.aifaceDirection)
    
    
    #seeds information
    data.seedList = copy.deepcopy(data.blockList)
    data.seedSize = 2
    data.superSeedSize = 4
    
    data.score = 0
    data.gameState = 0
    data.collisionAllowance = data.playerRad//5
    
    #time stuff
    data.timerCount = 0
    data.timePerLevel = 300 #seconds
    data.timeElapsed = 0
    data.timeDisplay = data.timePerLevel
    data.ghostCountdown = 11 - data.level
    
    #ghost stuff
    data.ghostSpeed = 4
    ghost1startX = data.marginX + (9.5*data.blockSize)
    ghost1startY = data.marginY + (10.5*data.blockSize)
    data.ghostSize = data.playerRad
    #self, positionX, positionY, speed, size, colour, movePattern, faceDirection)
    data.ghost1 = Ghost(ghost1startX, ghost1startY, data.ghostSpeed, data.ghostSize, "red", "Smart", "Up")
    
    ghost2startX = data.marginX + (9.5*data.blockSize)
    ghost2startY = data.marginY + (9.5*data.blockSize)
    data.ghost2 = Ghost(ghost2startX, ghost2startY, data.ghostSpeed, data.ghostSize, "pink", "Easy", "Up")
    
    ghost3startX = data.marginX + (8.5*data.blockSize)
    ghost3startY = data.marginY + (10.5*data.blockSize)
    data.ghost3 = Ghost(ghost3startX, ghost3startY, data.ghostSpeed, data.ghostSize, "cyan", None, "Left")

    ghost4startX = data.marginX + (10.5*data.blockSize)
    ghost4startY = data.marginY + (10.5*data.blockSize)
    data.ghost4 = Ghost(ghost3startX, ghost3startY, data.ghostSpeed, data.ghostSize, "orange", None, "Right")
        
    data.ghost1X = data.ghost1.getGhostX()
    data.ghost1Y = data.ghost1.getGhostY()
    data.ghostList = [data.ghost1, data.ghost2, data.ghost3, data.ghost4]
    
    data.ghostRespawnX = 9
    data.ghostRespawnY = 10
    
    data.ghostSquares = []
    
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.gameState == 0:
        if event.keysym=="c" or event.keysym=="C":
            data.gameState = 1
        if event.keysym=="h" or event.keysym=="H":
            data.gameState = 3
        if event.keysym=="d":
            data.gameState = 7
            
    elif data.gameState == 1:  
        if event.keysym=="p" or event.keysym=="P":
            data.gameState = 2
        
        if event.keysym=="c" or event.keysym=="C":
            data.gameState = 5
        
        #data.timerCount +=1
        if event.keysym=="Right" :
            data.playerNextFace = "Right"
        elif event.keysym=="Left" :
            data.playerNextFace = "Left"
        elif event.keysym=="Up" :
            data.playerNextFace = "Up"
        elif event.keysym=="Down" :
            data.playerNextFace = "Down"  
            
    elif data.gameState ==2:
        if event.keysym=="p" or event.keysym=="P":
            data.gameState = 1
                    
    elif data.gameState == 3:
        if event.keysym=="c" or event.keysym=="C":
            data.gameState = 1
        if event.keysym=="b" or event.keysym=="B":
            data.gameState = 0
    
    elif data.gameState == 5:  
        if event.keysym=="p" or event.keysym=="P":
            data.gameState = 2
        
        #data.timerCount +=1
        if event.keysym=="Right" :
            data.playerNextFace = "Right"
        elif event.keysym=="Left" :
            data.playerNextFace = "Left"
        elif event.keysym=="Up" :
            data.playerNextFace = "Up"
        elif event.keysym=="Down" :
            data.playerNextFace = "Down" 
    
    elif data.gameState ==7:
        if event.keysym == "q":
            data.gameState = 0
            init(data)
    
    elif data.gameState == 9:
        if event.keysym=="r"or event.keysym=="R":
            data.score = 0
            data.blockList = copy.deepcopy(data.originalBlockList)
            init(data)
            data.gameState = 0
            
    elif data.gameState == 11:
        if event.keysym=="r"or event.keysym=="R":
            data.score = 0
            data.blockList = copy.deepcopy(data.originalBlockList)
            init(data)
            data.gameState = 0  
        pass

def timerFired(data):
    data.timeLeft = data.timePerLevel - data.timeElapsed  #data.timePerLevel - 
    data.timeDisplay = str(int(data.timeLeft))
    
    if data.gameState == 1:
        #print(data.timerDelay)
        data.timeElapsed += 0.1
        #print(data.timeElapsed)
        data.timerCount +=1
        warp(data)
    #data.playerFace = data.playerNextFace
        if mustStop(data, data.playerFace):
            #print("Stop")
            stopPlayer(data)
            
        if isLegalTurn(data, data.playerNextFace):
            data.playerFace = data.playerNextFace
        
        else:
            data.playerFace == data.playerFace
    
        if mustStop(data, data.playerFace):
            movePlayer(data, True)

        else:
            data.mouthMovementCount +=1
            movePlayer(data)
        
        updateScore(data)
        #updateState(data)
        for ghost in data.ghostList:
            ghost.warp(data)
            #print(ghost.colour)
            ghost.checkStop(data)
            
            if ghost.centeredGhost(data, ghost.dir):
                #print(ghost.colour, "ghost is centered", ghost.x, ghost.y)
                ghost.moveGhostWithTurning(data)
                
                if ghost.dir == "Up":
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y - ghost.speed - data.marginY)// data.blockSize)
                    
                elif ghost.dir == "Down":
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y + ghost.speed - data.marginY)// data.blockSize)
                
                elif ghost.dir == "Left":
                    i = int(((ghost.x - ghost.speed - data.marginX)// data.blockSize))
                    j = int((ghost.y- data.marginY)// data.blockSize)
                    
                elif ghost.dir == "Right":
                    i = int(((ghost.x + ghost.speed - data.marginX)// data.blockSize))
                    j = int((ghost.y - data.marginY)// data.blockSize)
                    
                else:
                    #print(" the else case under tinerFired Centered ghost is being used")
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y  - data.marginY)// data.blockSize)
                
                try:
                    if not (data.blockList[i][j] in data.ghostWalkableList):
                        ghost.dir = "Stop"
                        #print ("STOP")
                        
                    else:
                        #("moving ghost under timerFired, centered ghost, post direction update")
                        ghost.moveGhost(data)
                
                except:
                    ghost.dir = "Stop"
                    
            else:
                i = int(((ghost.x - data.marginX)// data.blockSize))
                j = int((ghost.y - data.marginY)// data.blockSize)
                if not (data.blockList[i][j] in data.ghostWalkableList):
                    ghost.dir = "Stop"
                    #print ("STOP")
                #print(ghost.colour, "ghost is not centered", ghost.x, ghost.y)
                ghost.moveGhostToNextBlock(data)
                
            #print(ghost.colour, ghost.x, ghost.y)
            ghost.updateIJ
            
        updateGhostSquares(data)
        collisionCheck(data)
        ghostRespawnCheck(data)
        
    if data.gameState == 5:
        data.timeElapsed += 0.1
        #print(data.timeElapsed)
        data.timerCount +=1
        warp(data)
    #data.playerFace = data.playerNextFace
        if mustStop(data, data.playerFace):
            #print("Stop")
            stopPlayer(data)
            
        if isLegalTurn(data, data.playerNextFace):
            data.playerFace = data.playerNextFace
        
        else:
            data.playerFace == data.playerFace
    
        if mustStop(data, data.playerFace):
            movePlayer(data, True)

        else:
            data.mouthMovementCount +=1
            movePlayer(data)
        
        updateScore(data)
        #updateState(data)
        for ghost in data.ghostList:
            ghost.warp(data)
            #print(ghost.colour)
            ghost.checkStop(data)
            
            if ghost.centeredGhost(data, ghost.dir):
                #print(ghost.colour, "ghost is centered", ghost.x, ghost.y)
                ghost.moveGhostWithTurning(data)
                
                if ghost.dir == "Up":
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y - ghost.speed - data.marginY)// data.blockSize)
                    
                elif ghost.dir == "Down":
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y + ghost.speed - data.marginY)// data.blockSize)
                
                elif ghost.dir == "Left":
                    i = int(((ghost.x - ghost.speed - data.marginX)// data.blockSize))
                    j = int((ghost.y- data.marginY)// data.blockSize)
                    
                elif ghost.dir == "Right":
                    i = int(((ghost.x + ghost.speed - data.marginX)// data.blockSize))
                    j = int((ghost.y - data.marginY)// data.blockSize)
                    
                else:
                    #print(" the else case under tinerFired Centered ghost is being used")
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y  - data.marginY)// data.blockSize)
                
                try:
                    if not (data.blockList[i][j] in data.ghostWalkableList):
                        ghost.dir = "Stop"
                        #print ("STOP")
                        
                    else:
                        #("moving ghost under timerFired, centered ghost, post direction update")
                        ghost.moveGhost(data)
                
                except:
                    ghost.dir = "Stop"
                    
            else:
                i = int(((ghost.x - data.marginX)// data.blockSize))
                j = int((ghost.y - data.marginY)// data.blockSize)
                if not (data.blockList[i][j] in data.ghostWalkableList):
                    ghost.dir = "Stop"
                    #print ("STOP")
                #print(ghost.colour, "ghost is not centered", ghost.x, ghost.y)
                ghost.moveGhostToNextBlock(data)
                
            #print(ghost.colour, ghost.x, ghost.y)
            ghost.updateIJ
            
        updateGhostSquares(data)
        collisionCheck(data)
        ghostRespawnCheck(data)
        
        if data.ai.switch == True:
            data.mouthMovementCount +=1
            data.ai.move(data)
            data.ai.updateScore(data)
            data.ai.checkCollisions(data)
            
            for ghost in data.ghostList:
                ghost.warp(data)
                #print(ghost.colour)
                ghost.checkStop(data)
                
                
                if ghost.centeredGhost(data, ghost.dir):
                    #print(ghost.colour, "ghost is centered", ghost.x, ghost.y)
                    ghost.moveGhostWithTurning(data)
                    
                    if ghost.dir == "Up":
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y - ghost.speed - data.marginY)// data.blockSize)
                        
                    elif ghost.dir == "Down":
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y + ghost.speed - data.marginY)// data.blockSize)
                    
                    elif ghost.dir == "Left":
                        i = int(((ghost.x - ghost.speed - data.marginX)// data.blockSize))
                        j = int((ghost.y- data.marginY)// data.blockSize)
                        
                    elif ghost.dir == "Right":
                        i = int(((ghost.x + ghost.speed - data.marginX)// data.blockSize))
                        j = int((ghost.y - data.marginY)// data.blockSize)
                        
                    else:
                        #print(" the else case under tinerFired Centered ghost is being used")
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y  - data.marginY)// data.blockSize)
                    
                    try:
                        if not (data.blockList[i][j] in data.ghostWalkableList):
                            ghost.dir = "Stop"
                            #print ("STOP")
                            
                        else:
                            #("moving ghost under timerFired, centered ghost, post direction update")
                            ghost.moveGhost(data)
                    
                    except:
                        ghost.dir = "Stop"
                        
                else:
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y - data.marginY)// data.blockSize)
                    if not (data.blockList[i][j] in data.ghostWalkableList):
                        ghost.dir = "Stop"
                        #print ("STOP")
                    #print(ghost.colour, "ghost is not centered", ghost.x, ghost.y)
                    ghost.moveGhostToNextBlock(data)
                    
                #print(ghost.colour, ghost.x, ghost.y)
                ghost.updateIJ
                
            updateGhostSquares(data)
            ghostRespawnCheck(data)
            
    if data.gameState == 7:
        if data.ai.switch == True:
            data.timeElapsed += 0.1
            #print(data.timeElapsed)
            data.timerCount +=1
            data.mouthMovementCount +=1
            data.ai.move(data)
            data.ai.updateScore(data)
            data.ai.checkCollisions(data)
            
            for ghost in data.ghostList:
                ghost.warp(data)
                #print(ghost.colour)
                ghost.checkStop(data)
                
                
                if ghost.centeredGhost(data, ghost.dir):
                    #print(ghost.colour, "ghost is centered", ghost.x, ghost.y)
                    ghost.moveGhostWithTurning(data)
                    
                    if ghost.dir == "Up":
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y - ghost.speed - data.marginY)// data.blockSize)
                        
                    elif ghost.dir == "Down":
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y + ghost.speed - data.marginY)// data.blockSize)
                    
                    elif ghost.dir == "Left":
                        i = int(((ghost.x - ghost.speed - data.marginX)// data.blockSize))
                        j = int((ghost.y- data.marginY)// data.blockSize)
                        
                    elif ghost.dir == "Right":
                        i = int(((ghost.x + ghost.speed - data.marginX)// data.blockSize))
                        j = int((ghost.y - data.marginY)// data.blockSize)
                        
                    else:
                        #print(" the else case under tinerFired Centered ghost is being used")
                        i = int(((ghost.x - data.marginX)// data.blockSize))
                        j = int((ghost.y  - data.marginY)// data.blockSize)
                    
                    try:
                        if not (data.blockList[i][j] in data.ghostWalkableList):
                            ghost.dir = "Stop"
                            #print ("STOP")
                            
                        else:
                            #("moving ghost under timerFired, centered ghost, post direction update")
                            ghost.moveGhost(data)
                    
                    except:
                        ghost.dir = "Stop"
                        
                else:
                    i = int(((ghost.x - data.marginX)// data.blockSize))
                    j = int((ghost.y - data.marginY)// data.blockSize)
                    if not (data.blockList[i][j] in data.ghostWalkableList):
                        ghost.dir = "Stop"
                        #print ("STOP")
                    #print(ghost.colour, "ghost is not centered", ghost.x, ghost.y)
                    ghost.moveGhostToNextBlock(data)
                    
                #print(ghost.colour, ghost.x, ghost.y)
                ghost.updateIJ
                
            updateGhostSquares(data)
            ghostRespawnCheck(data)
        else:
            data.gameState = 11
        
    if data.gameState == 8:
        data.playerDyingSize -=10
        if data.playerDyingSize <= 0:
            data.gameState = 9
            
        
        
def updateGhostSquares(data):
    data.ghostSquares = []
    for ghost in data.ghostList:
        if ghost.state == "normal":
            coordinates = (ghost.i,ghost.j)
            data.ghostSquares.append(coordinates)
    
def ghostRespawnCheck(data):
    for ghost in data.ghostList:
        if ghost.state == "eyes":
            i = int((ghost.x - data.marginX)// data.blockSize)
            j = int((ghost.y - data.marginY)//data.blockSize)
            if i==data.ghostRespawnX and j==data.ghostRespawnY:
                ghost.setState(data, "normal")
    pass
    
def stopPlayer(data):
    if mustStop(data, data.playerFace):
        data.playerX += 0
        data.playerY += 0

def collisionCheck(data):
    collisionBounds = data.playerRad + data.ghostSize - data.collisionAllowance
    for ghost in data.ghostList:
        gX = ghost.getGhostX()
        gY = ghost.getGhostY()
        xDif = (data.playerX-gX)
        yDif = (data.playerY-gY)
        hypDif = (xDif**2 + yDif**2)**0.5
        if (hypDif <collisionBounds):
            #print(ghost.getState())
            if ghost.getState() == "normal":
                #game ends /loses a life
                #play audio
                data.gameState = 8
                
            elif ghost.getState() == "edible":
                #score increases
                data.score += 200
                #ghostStateChanges
                ghost.setState(data, "eyes")
            
            elif ghost.getState() == "eyes":
                pass
    
    #print("the ai is at" , data.ai.x, data.ai.y)
    
    xAiDif = (data.playerX-data.ai.x)
    yAiDif =(data.playerY-data.ai.y)
    
    hypAiDif = (xAiDif**2 + yAiDif**2)**0.5
    
    if (hypAiDif <= collisionBounds):
        print("SWITCH")
        data.ai.switch = True

    pass

    
def movePlayer(data, stop = False):
    if stop == True:
        data.playerX+=0
        data.playerY+=0
        
    else:
        if data.playerFace == "Down":
            data.playerY+=data.playerSpeed
            
        elif data.playerFace =="Up":
                data.playerY-=data.playerSpeed
                
        elif data.playerFace == "Left":
                data.playerX-=data.playerSpeed
                    
        elif data.playerFace == "Right":
                data.playerX+=data.playerSpeed
            
def warp(data):
    i = int(((data.playerX - data.marginX)// data.blockSize))
    j = int((data.playerY - data.marginY)// data.blockSize)
    
    if (i,j) in data.warpDict:
        (newI, newJ) = data.warpDict[(i,j)]
        if i<newI:
            if data.playerFace == "Left":
                data.playerX = data.marginX + data.blockSize * (newI+0.5)
                data.playerY = data.marginY + data.blockSize * (newJ+0.5)
        elif i>newI:
            if data.playerFace == "Right":
                data.playerX = data.marginX + data.blockSize * (newI+0.5)
                data.playerY = data.marginY + data.blockSize * (newJ+0.5)
        
            
    #elif i > (len(data.blockList)-1):
     #   data.playerX = data.marginX

def isLegalTurn(data, dir):
    #checks if its centered
    if not centered(data, data.playerX, data.playerY):
        return False
    
    else:
        #convert position to location on board
        board = copy.deepcopy(data.blockList)
        i = int(((data.playerX - data.marginX)// data.blockSize))
        j = int((data.playerY - data.marginY)// data.blockSize)
        
        if dir=="Up":
            return board[i][j-1] in data.walkableList
            
        elif dir=="Down":
            return board[i][j+1] in data.walkableList
        
        elif dir=="Left":
            return board[i-1][j] in data.walkableList
        
        elif dir=="Right":
            if i >= 18 and j==10:
                return True
            else:
                return board[i+1][j] in data.walkableList
            
        #check if next location is Legal (return true if it is, false if not)
        pass

def centered(data, x, y):
    testX = (x-data.marginX - data.blockSize//2) / data.blockSize
    testY = (y-data.marginY - data.blockSize//2) / data.blockSize
    
    if int(testX) ==testX  and int(testY)==testY:
        return True
    return False

def mustStop(data, dir):
    if centered(data, data.playerX, data.playerY):        
        board = data.blockList
        if dir=="Up":
            immediateI = int((data.playerX -data.marginX) // data.blockSize)
            immediateJ = int(((data.playerY-data.playerRad) - data.marginY)//data.blockSize)
            nextI = int((data.playerX -data.marginX) // data.blockSize)
            nextJ = int(((data.playerY-data.playerRad-data.playerSpeed) - data.marginY)//data.blockSize)
            i = nextI
            j= nextJ
            iJ = immediateJ
            #print(nextI, nextJ)
            if i>len(board) or j>len(board[0]) or i<0 or j<0 or iJ<0:
                return True
            
            elif (i,j) in data.warpDict:
                    return False
                    
            else:
                return not(board[nextI][nextJ] in data.walkableList)
                
            
            """i = int((data.playerX - data.marginX )// data.blockSize)
            j = int((data.playerY - data.marginY- data.blockSize//2)//data.blockSize) 
            
            if i>len(board) or j> len(board[0]) or i<=0 or j<=0:
                if (i,j) in data.warpDict:
                    return False
                else:
                    return True
            print(i,j)
            return board[i][j-1] not in data.walkableList"""
            
        elif dir=="Down":
            i = int((data.playerX - data.marginX)// data.blockSize)
            j = int((data.playerY - data.marginY + data.blockSize//2)//data.blockSize) -1
            #print(i,j)
            if i>len(board) or j> len(board[0]) or i<=0 or j<=0:
                if (i,j) in data.warpDict:
                    return False
                else:
                    return True
            
            return board[i][j+1] not in data.walkableList
        
        elif dir=="Left":
            i = int((data.playerX - data.marginX - data.blockSize//2)// data.blockSize) 
            j = int((data.playerY - data.marginY)//data.blockSize)
            #print(i,j)
            
            if i>len(board) or j> len(board[0]) or i<=0 or j<=0:
                if (i,j) in data.warpDict:
                    return False
                else:
                    
                    return True
            return board[i-1][j] not in data.walkableList
        
        elif dir=="Right":
            i = int((data.playerX - data.marginX + data.blockSize//2)// data.blockSize) -1
            j = int((data.playerY - data.marginY)//data.blockSize)
            #print(i,j)
            if (i>=len(board)-1) or (j>=len(board[0])-1) or (i<=0) or (j<=0):
                if (i,j) in data.warpDict:
                    return False
                    
                else:
                    return True
            else:
                
                return board[i+1][j] not in data.walkableList
    

def updateScore(data):
    emptyCount = 0
    i = int(((data.playerX - data.marginX)// data.blockSize))
    j = int((data.playerY - data.marginY)// data.blockSize)
    if i<=18:
        if data.seedList[i][j] == 0:
            data.score+=10
            data.seedList[i][j] = 9
        
        elif data.seedList[i][j] == 4:
            data.score+=10
            data.seedList[i][j] = 9
            for ghost in data.ghostList:
                if ghost.state == "normal":
                    ghost.setState(data, "edible")
                    
        
        for k in range(len(data.seedList)):
            if 0 in data.seedList[k]:
                continue
            else:
                emptyCount += 1
        
        if emptyCount == len(data.seedList):
            data.level+=1
            newLevel = data.level
            score = data.score
            init(data)
            data.level = newLevel
            data.score = score
            data.gameState = 1

def redrawAll(canvas, data):
    if data.gameState == 0:
        drawStart(canvas, data)
    
    elif data.gameState ==1 or data.gameState ==2 :
        drawBoard(canvas, data)
        drawSeeds(canvas, data, data.seedList)
        drawPlayer(canvas, data, data.playerX, data.playerY)
        drawGhosts(canvas, data)
        drawBorders(canvas, data)
        drawDetails(canvas, data)
    
    if data.gameState == 3:
        drawInstructions(canvas, data)
        
    if data.gameState == 5:
        
        drawBoard(canvas, data)
        drawSeeds(canvas, data, data.seedList)
        drawGhosts(canvas, data)
        drawBorders(canvas, data)
        drawDetails(canvas, data)
        data.ai.draw(canvas, data)
        drawPlayer(canvas, data, data.playerX, data.playerY)
    
    if data.gameState == 7:
        
        drawBoard(canvas, data)
        drawSeeds(canvas, data, data.seedList)
        drawGhosts(canvas, data)
        drawBorders(canvas, data)
        drawDetails(canvas, data)
        data.ai.draw(canvas, data)
        
    if data.gameState == 8:
        drawBoard(canvas, data)
        drawSeeds(canvas, data, data.seedList)
        #drawGhosts(canvas, data)
        drawBorders(canvas, data)
        drawDetails(canvas, data)
        drawDyingPlayer(canvas, data)
        
        
    
    if data.gameState == 9:
        drawGameOverDisplay(canvas,data)
    
    if data.gameState == 11:
        drawGameOverDisplay(canvas,data)
        

    pass

def drawDyingPlayer(canvas, data):
    x = data.playerX
    y = data.playerY
    r = data.playerRad
    canvas.create_arc(x-r, y-r, x+r, y+r, style = PIESLICE, start = data.drawPlayerDirection, extent = data.playerDyingSize, fill="yellow")

def drawStart(canvas, data):
    #drawBoard(canvas, data)
    #drawSeeds(canvas, data, data.seedList)
    #drawPlayer(canvas, data, data.playerX, data.playerY)
    #drawGhosts(canvas, data)
    drawBorders(canvas, data)
    drawStartDisplay(canvas,data)
    drawGhostDisplay(canvas, data)
    

def drawStartDisplay(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")
    canvas.create_text(data.width//2, 6*data.height//8 - data.marginY//2, text = "Press C to insert coin!", anchor = "center", fill = "Yellow", font =("Arial" , 50))
    canvas.create_text(data.width//2, 3*data.height//4 + data.marginY//5, text = "Press H for how-to-play!", anchor = "center", fill = "Yellow", font =("Arial" , 20))
    canvas.create_text(data.width//2, 7*data.height//8 - data.marginY//5, text = "Press D for a demo!", anchor = "center", fill = "Yellow", font =("Arial" , 20))
    canvas.create_text(data.width//2, data.height//3 , text = "PA    MAN", anchor = "center", fill = "Yellow", font =("Arial Bold" , 150))
    
    canvas.create_arc(data.width//2 + 10-data.displayPacManSize, data.height//2 - 40 - data.displayPacManSize, data.width//2 + 10, data.height//2 -40, style = PIESLICE, start = 40, extent = 280, fill="yellow")
    
    
def drawGhostDisplay(canvas, data):
    for i in range(len(data.ghostDisplayList)):
        j = i-2 + 0.2
        fillColour = data.ghostDisplayList[i]
        
        canvas.create_arc(data.width//2 + (data.ghostSpace//2*j) , data.height//2 + data.heightGhostTranslation - data.ghostDisplayRadius,  data.width//2 + data.ghostSpace//2*j + (2* data.ghostDisplayRadius), data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius +2, style = PIESLICE, start = 0, extent = 180, fill = fillColour, outline = fillColour)
        canvas.create_polygon(data.width//2 + data.ghostSpace//2*j, data.height//2 + data.heightGhostTranslation, #point 1
        data.width//2 + data.ghostSpace//2*j, data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius,     #point2
        data.width//2 + data.ghostSpace//2*j + data.ghostDisplayRadius//2, data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius//2, #point3
        data.width//2 + data.ghostSpace//2*j + data.ghostDisplayRadius, data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius, #point4
        data.width//2 + data.ghostSpace//2*j + (3*data.ghostDisplayRadius//2), data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius//2, #point 5
        data.width//2 + data.ghostSpace//2*j + (2*data.ghostDisplayRadius), data.height//2 + data.heightGhostTranslation + data.ghostDisplayRadius, #point6
        data.width//2 + data.ghostSpace//2*j + (2*data.ghostDisplayRadius),data.height//2 + data.heightGhostTranslation, fill = fillColour, outline = fillColour)
        
    
def drawInstructions(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")
    canvas.create_text(data.marginX, data.marginY, text = "INSTRUCTIONS", fill = "yellow", anchor = "nw", font =("Arial Bold" , 50))
    canvas.create_text(data.marginX, data.marginY, text = '\n\n\n\n - Use the arrow keys to guide pacman around the maze! \n\n - Eat up those yellow dots and avoid those pesky ghosts! \n\n - If you eat a power pill, you\'ll be able to eat  ghosts! \n\n - The more you eat per pill, the higher your score! \n\n - Eat up all the seeds and you can level up! \n\n\n\n BEWARE! You need to eat all the dots before time runs out! \n\n \t (Warp tunnels will help you with this!)', fill = "yellow", anchor = "nw", font =("Arcade" , 18))
    canvas.create_text(data.marginX + 30, data.height - data.marginY, text = "press 'b' to go back", fill = "yellow", anchor = "sw", font =("Helvetica" , 20))
    
    
    canvas.create_text(data.width-data.marginX - 30, data.height - data.marginY, text = "press 'c' to insert coin", fill = "yellow", anchor = "se", font =("Helvetica" , 20))
    
    canvas.create_polygon(data.marginX +6, data.height - data.marginY-12, data.marginX+22,data.height - data.marginY - 5, data.marginX+22,data.height - data.marginY-19, fill = "yellow")
    
    canvas.create_polygon(data.width - data.marginX - 6, data.height - data.marginY-12, data.width -data.marginX -22,data.height - data.marginY - 5,data.width- data.marginX-22,data.height - data.marginY-19, fill = "yellow")
    
    
def drawGhosts(canvas, data):
    for ghost in data.ghostList:
        ghost.draw(canvas)

def drawBorders(canvas, data):
    canvas.create_rectangle(0,0, data.marginX, data.height, fill = "black")
    canvas.create_rectangle(0,0, data.width, data.marginY, fill = "black")
    canvas.create_rectangle(data.width - data.marginX,0,data.width, data.height, fill = "black")
    canvas.create_rectangle(0,data.height - data.marginY, data.width, data.height, fill = "black")

def drawBoard(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")
    board = copy.deepcopy(data.blockList)
    
    for i in range(len(board)):
        xPos = data.marginX + (data.blockSize*i) + data.blockSize//2
        for j in range(len(board[0])):
            yPos = data.marginY + (data.blockSize*j) + data.blockSize//2
            
            if board[i][j] == 1:
                colour = "blue"
                drawBlock(canvas, data, board[i][j], xPos, yPos, colour)
            
            elif board[i][j] == 5:
                colour = "brown"
                drawGate(canvas, data, board[i][j], xPos, yPos, colour)
            else:
                colour = "black"
                drawBlock(canvas, data, board[i][j], xPos, yPos, colour)
                
    pass

def drawBlock(canvas, data, val, x, y, colour):
    w = data.blockSize//2
    canvas.create_rectangle(x-w,y-w,x+w,y+w, fill=colour, width=0)

def drawGate(canvas, data, val, x, y, colour):
    w = data.blockSize//2
    g = data.gateSize//2
    canvas.create_rectangle(x-w,y-g,x+w,y+g, fill=colour, width=0)
    
def drawPlayer(canvas, data, x, y):
    playerDrawCount = data.mouthMovementCount % data.mouthVariability
    if playerDrawCount >= (data.mouthVariability//2):
        playerDrawCount = (data.mouthVariability-1)-playerDrawCount
        
    playerMouthSize = 359 - playerDrawCount* 25
    
    if data.playerFace == "Up":
        data.drawPlayerDirection = 270 - playerMouthSize//2
        
    elif data.playerFace == "Down":
        data.drawPlayerDirection = 90 - playerMouthSize//2
    
    elif data.playerFace == "Left":
        data.drawPlayerDirection = 0 - playerMouthSize//2
    
    elif data.playerFace == "Right":
        data.drawPlayerDirection = 180 - playerMouthSize//2
        
    r = data.playerRad
    
    canvas.create_arc(x-r, y-r, x+r, y+r, style = PIESLICE, start = data.drawPlayerDirection, extent = playerMouthSize, fill="yellow")
    
    """for player in data.playersList:
        player.draw(data)"""

def drawSeeds(canvas, data, seedList):
    s = data.seedSize
    ss = data.superSeedSize
    
    for i in range(len(seedList)):
        xPos = data.marginX + (data.blockSize*i) + data.blockSize//2
        
        for j in range(len(seedList[0])):
            yPos = data.marginY + (data.blockSize*j) + data.blockSize//2
            
            if data.seedList[i][j]==0:
                canvas.create_oval(xPos-s, yPos - s, xPos +s, yPos+s, fill = "yellow")
            elif data.seedList[i][j]==4:
                canvas.create_oval(xPos-ss, yPos - ss, xPos +ss, yPos+ss, fill = "yellow")    

def drawDetails(canvas, data):
    #score
    if data.gameState == 7:
        scoreDisplay = str(data.ai.score)
        
    else:
        scoreDisplay = str(data.score+ data.ai.score)
    canvas.create_text(data.width//2, data.marginY//2, text ="Score = " +scoreDisplay, anchor = "center", fill = "yellow")
    
    #time
    canvas.create_text(data.width - data.marginX, data.marginY//2, text ="Countdown: " + str(data.timeDisplay), anchor = "e", fill = "yellow")
    
    #lives
    """canvas.create_text(data.width - data.marginX, data.marginY, text ="Countdown: " + str(data.timerCount), anchor = "e", fill = "yellow")"""
    
    #levels

def drawGameOverDisplay(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")
    canvas.create_text(data.width//2, data.height//2, text = "Game Over", fill = "yellow", anchor = "center", font = ("Arial", 50))
    canvas.create_text(data.width//2, 2*data.height//3, text = "Your Score: " + str(data.score+data.ai.score), fill = "yellow", anchor = "center", font = ("Arial", 30),)
    canvas.create_text(data.width//2, 3*data.height//4, text = "Press 'r' to play again", fill = "yellow", anchor = "center", font = ("Arial", 20))
    
    
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1300, 700)
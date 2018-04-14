import random, copy
from Astar import AStar, Cell
from tkinter import *
from TPaicode import aiAStar, Cell

class AIPlayer(object):
    def __init__(self, startX, startY, speed, size, colour, faceDirection):
        self.x = startX
        self.y = startY
        self.speed = speed
        self.size = size
        self.r = size
        self.dir = faceDirection
        self.colour = colour
        self.score = 0
        self.personality = "Smart"
        self.eyeColour = "green"
        self.switch = True
        pass
    
    def move(self, data):
        if self.isCentered(data):
            self.updateDirection(data)
            self.directMove(data)

        else:
            self.moveAIToNextBlock(data)
            pass
    
    def isCentered(self, data):
        x = self.x
        y = self.y
        
        testX = (x-data.marginX - data.blockSize/2) / data.blockSize
        testY = (y-data.marginY - data.blockSize/2) / data.blockSize
        
        return ((int(testX) == testX) and (int(testY) == testY))
    
    def pathHasGhost(self, data, dir):
        if dir == "Up":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)-2
            if (i, j) in data.ghostSquares and (data.blockList[i][j+1] in data.ghostWalkablelist):
                return True
            else:
                if (i, j+1) in data.ghostSquares:
                    return True
            
        elif dir == "Down":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)+2
            if (i, j) in data.ghostSquares and (data.blockList[i][j-1] in data.ghostWalkablelist):
                return True
            else:
                if (i, j-1) in data.ghostSquares:
                    return True
                
        elif dir == "Left":
            i = int(((self.x - data.marginX)// data.blockSize))-2
            j = int((self.y - data.marginY)// data.blockSize)
            if (i, j) in data.ghostSquares and (data.blockList[i+1][j] in data.ghostWalkablelist):
                return True
            else:
                if (i+1, j) in data.ghostSquares:
                    return True
                    
        elif dir == "Right":
            i = int(((self.x - data.marginX)// data.blockSize)) +2
            j = int((self.y - data.marginY)// data.blockSize)
            if (i, j) in data.ghostSquares and (data.blockList[i-1][j] in data.ghostWalkablelist):
                return True
            else:
                if (i-1, j) in data.ghostSquares:
                    return True
            
    def updateDirection(self, data):
        possMoves = ["Up", "Down", "Left", "Right"]
        dir = self.dir
        board = (data.seedList)
        x = int(((self.x - data.marginX)// data.blockSize))
        y = int((self.y - data.marginY)// data.blockSize)
        portals = data.warpDict
        iterateMoveList=copy.deepcopy(possMoves)
        
        
        for move in (iterateMoveList):
            if (self.isLegal(data, board, move)==False) or (self.pathHasGhost(data, move)==True):
                possMoves.remove(move)
        
        if len(possMoves)==0:
            self.dir = "Stop"

        else:
            if self.personality == "Easy":
                self.dir = self.followEasy(data, possMoves)
            
            elif self.personality == "Smart":
                startI = int(((self.x - data.marginX)// data.blockSize))
                startJ = int((self.y - data.marginY)// data.blockSize)
                
                bestLen = 2*len(data.seedList[0])
                pathFound = False
                bestTurn = None
                
                for i in range(1, 2*len(data.seedList[0])):
                    
                    for j in range(0,i):
                        k = i-j
                        
                        if (x-j>=0 and y-k>=0 and board[x-j][y-k] in data.seedSet):
                                newI = x-j
                                newJ = y-k
                                
                                newTurn = aiAStar(data, startI,startJ, newI, newJ, portals, True)
                                nextDir = newTurn.solve()
                                
                                if nextDir != None and (nextDir in possMoves):
                                    pathFound = True
                                    if newTurn.getPathLen() < bestLen:
                                        bestLen = newTurn.pathLen
                                        bestTurn = nextDir
                                
                        if (x+k<len(board) and y-j>=0):
                            if board[x+k][y-j] in data.seedSet:
                                newI = x+k
                                newJ = y-j
                                
                                newTurn = aiAStar(data, startI,startJ, newI, newJ, portals, True)
                                nextDir = newTurn.solve()
                                
                                if nextDir != None and (nextDir in possMoves):
                                    pathFound = True
                                    if newTurn.getPathLen() <=bestLen:
                                        bestLen = newTurn.pathLen
                                        bestTurn = nextDir

                        if (x-k>=0 and y-j>=0):
                            if board[x-k][y-j] in data.seedSet :
                                newI = x-k
                                newJ = y-j
                                
                                newTurn = aiAStar(data, startI,startJ, newI, newJ, portals, True)
                                nextDir = newTurn.solve()
                                
                                if nextDir != None and (nextDir in possMoves):
                                    pathFound = True
                                    if newTurn.getPathLen() < bestLen:
                                        bestLen = newTurn.pathLen
                                        bestTurn = nextDir
                            
                        if (x-j>=0 and y+k<len(board[0])):
                            if board[x-j][y+k] in data.seedSet:
                                newI = x-j
                                newJ = y+k
                                
                                newTurn = aiAStar(data, startI,startJ, newI, newJ, portals, True)
                                nextDir = newTurn.solve()
                                
                                if nextDir != None and (nextDir in possMoves):
                                    pathFound = True
                                    if newTurn.getPathLen()<bestLen:
                                        bestLen = newTurn.pathLen
                                        bestTurn = nextDir
                            
                        if (x+j<len(board) and y+k<len(board[0])):
                            if board[x+j][y+k] in data.seedSet:
                                newI = x+j
                                newJ = y+k
                                newTurn = aiAStar(data, startI,startJ, newI, newJ, portals, True)
                                nextDir = newTurn.solve()
                                if nextDir != None and (nextDir in possMoves):
                                    pathFound = True
                                    if newTurn.getPathLen() <=bestLen:
                                        bestLen = newTurn.pathLen
                                        bestTurn = nextDir
                        
                        if pathFound == True:
                            self.dir =  bestTurn
                            break
                        
                        if pathFound == True:
                            self.dir =  bestTurn
                            break
                            
                    else:
                        #print(self.dir, "AI dir")
                        continue
                    #print(self.dir, "AI dir")
                    break
 
            
            
            elif self.personality == "Scared":
                self.dir = self.runAwayEasy(data, possMoves)
                
            elif self.personality == "Home":
                print("randomizing eyes")
                if self.originalPersonality == "Smart":
                    print("randomizing eyes")
                    #startI = int(((self.x - data.marginX)// data.blockSize))
                    startJ = int((self.y - data.marginY)// data.blockSize)
                    
                    endI = data.ghostRespawnX
                    endJ = data.ghostRespawnY
                    
                    newTurn = AStar(data, startI,startJ, endI, endJ, data.warpDict, False)
                    nextDir = newTurn.solve()
                    
                    if nextDir == None:
                        randLen = random.randint(0,len(possMoves)-1)
                        self.dir = possMoves[randLen]
                    
                    self.dir = nextDir
                    
                else:
                    randLen = random.randint(0,len(possMoves)-1)
                    self.dir = possMoves[randLen]

            else:
                randLen = random.randint(0,len(possMoves)-1)
                self.dir = possMoves[randLen]
    
    
    
    def warp(self, data):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if (i, j) in data.warpDict:
            self.updateDirection
            (nextI, nextJ) = data.warpDict[(i,j)]
            if (nextI, nextJ) == (0,10):
                nextI+=1
                if self.dir == "Up":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                    
                elif self.dir == "Down":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                
                elif self.dir == "Left":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                    
                elif self.dir == "Right":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                
                else:
                    pass
                    
                self.dir = "Right"
            elif (nextI, nextJ) == (18,10):
                nextI-=1
                if self.dir == "Up":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                    
                elif self.dir == "Down":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                
                elif self.dir == "Left":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                    
                elif self.dir == "Right":
                    self.x = data.marginX + (data.blockSize*(nextI+0.5))
                    self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                
                else:
                    pass
                self.dir = "Left"
            
        else:
            pass
    
    def directMove(self, data):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        board = data.blockList
        
        if (self.isLegal(data, data.blockList, self.dir)==False):
            self.dir == "Stop"
        
        if ((i,j) in data.warpDict):
            self.warp(data)
            
        if self.dir == "Down":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y +self.speed- data.marginY)// data.blockSize)
            
            if board[i][j] in data.aiWalkableList:
                self.y+=self.speed
            else:
                self.updateDirection(data)
            
        elif self.dir == "Up":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y -self.speed- data.marginY)// data.blockSize)
            
            if board[i][j] in data.aiWalkableList:
                self.y-=self.speed
            else:
                self.updateDirection(data)
                
        elif self.dir == "Left":
            i = int(((self.x - self.speed - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)
            
            if board[i][j] in data.aiWalkableList:
                self.x -= self.speed
            else:
                pass

        elif self.dir == "Right":
            i = int(((self.x + self.speed - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)

            
            if board[i+1][j] in data.aiWalkableList:
                
                self.x += self.speed
                
            else:
                
                self.updateDirection(data)
                
                pass
        
        elif self.dir == "Stop":
            self.x, self.y = self.x, self.y
            
            
    def isLegal(self, data, board, move, haveWarped = True):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if move=="Up":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.aiWalkableList)
            else:
                if i>= len(data.blockList) or i<=0 or j<=0 or j>=len(data.blockList[0]):
                    return False
                else:
                    return (board[i][j-1]  in data.aiWalkableList)

        elif move=="Down":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.aiWalkableList)
            else:
                if i>= len(data.blockList) or j>= len(data.blockList[0])-1 or i<=0 or j<=0:
                    return False
             
                return (board[i][j+1]  in data.aiWalkableList)

        elif move=="Left":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.aiWalkableList)
                
            else:
                if i<=0 or i>=len(data.blockList) or  j> len(data.blockList[0]) or j<=0:
                    return False
                    
                return (board[i-1][j]  in data.aiWalkableList)
            
        elif move=="Right":
            
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.aiWalkableList)
            else:
                if i>= len(data.blockList)-1 or j>=len(data.blockList[0]) or j<=0 or i<=0:
                    return False
                else:
                    return (board[i+1][j] in data.aiWalkableList)
    
    
    def moveAIToNextBlock(self, data):
        
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if self.dir == "Stop":
            
            if self.state == "normal":
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
            else:
                
                self.x = (data.ghostRespawnX * data.blockSize)+ data.marginX + (data.blockSize//2)
                self.y = (data.ghostRespawnY * data.blockSize) + data.marginY + (data.blockSize//2)
            
        

        if self.dir == "Up":
            try:
                if data.blockList[i][j-1] in data.aiWalkableList:
                    if self.y-self.speed >= ((j-1)*data.blockSize + data.marginY):
                        self.y -=self.speed
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                    else:
                        self.y= ((j-1)*data.blockSize) + data.marginY+ (data.blockSize//2)
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                else:
                    if self.y-self.speed >= ((j-1)*data.blockSize + data.marginY):
                        self.y -= self.speed
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                    else:
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
                self.updateDirection(data)
                
        elif self.dir == "Down":
            try:
                if data.blockList[i][j+1] in data.aiWalkableList:
                    if self.y+self.speed <= ((j+1)*data.blockSize) + data.marginY:
                        self.y +=self.speed
                        self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                    else:
                        self.y= ((j+1)*data.blockSize) + data.marginY + (data.blockSize//2)
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                else:
                    if self.y+self.speed <= ((j+1)*data.blockSize) + data.marginY:
                        self.y +=self.speed
                        self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                        
                    else:
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
                self.updateDirection(data)
                                    
        elif self.dir == "Left":
            try:
                if data.blockList[i-1][j] in data.aiWalkableList:
                    if self.x-self.speed >= ((i-1)*data.blockSize) + data.marginX:
                        self.x -=self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    else:
                        self.x= ((i-1)*data.blockSize) + data.marginX
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                else:
                    if self.x-self.speed > ((i-1)*data.blockSize) + data.marginX:
                        
                        self.x -= self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    
                    else:
                        
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                self.updateDirection(data)   
                
        elif self.dir == "Right":
            try:
                if data.blockList[i+1][j] in data.aiWalkableList:
                    if self.x+self.speed <= ((i+1)*data.blockSize) + data.marginX:
                        self.x +=self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    else:
                        self.x= ((i+1)*data.blockSize) + data.marginX+ (data.blockSize//2)
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                else:
                    if self.x+self.speed < ((i+1)*data.blockSize) + data.marginX:
                      
                        self.x += self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                        
                    else:
                        
                        self.x= ((i)*data.blockSize) + data.marginX+ (data.blockSize//2)
                        self.updateDirection(data)
                
            except:
                self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                self.updateDirection(data)
    
    
    def updateScore(self,data):
        emptyCount = 0
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if i<=18 and j<=21:
            if data.seedList[i][j] == 0:
                self.score+=10
                data.seedList[i][j] = 9
            
            elif data.seedList[i][j] == 4:
                self.score+=10
                data.seedList[i][j] = 9
                for ghost in data.ghostList:
                    if ghost.state == "normal":
                        pass
                        ghost.setState(data, "edible")
            
            for k in range(len(data.seedList)):
                if 0 in data.seedList[k]:
                    continue
                else:
                    emptyCount += 1
            
            if emptyCount == len(data.seedList):
                data.level+=1
        
    def checkCollisions(self, data):
        collisionBounds = self.size +data.ghostSize- data.collisionAllowance
        for ghost in data.ghostList:
            gX = ghost.getGhostX()
            gY = ghost.getGhostY()
            xDif = (self.x-gX)
            yDif = (self.y-gY)
            hypDif = (xDif**2 + yDif**2)**0.5
            if (hypDif <collisionBounds):
                if ghost.getState() == "normal":
                
                    self.switch = False
                    
                elif ghost.getState() == "edible":
                    
                    self.score += 200
                    ghost.setState(data, "eyes")
                
                elif ghost.getState() == "eyes":
                    pass
        pass


    def draw(self, canvas, data):
        r = self.size

        playerDrawCount = data.mouthMovementCount % data.mouthVariability
        if playerDrawCount >= (data.mouthVariability//2):
            playerDrawCount = (data.mouthVariability-1)-playerDrawCount
            
        playerMouthSize = 359 - playerDrawCount* 25
        
        if self.dir == "Up":
            data.drawPlayerDirection = 270 - playerMouthSize//2
            
        elif self.dir == "Down":
            data.drawPlayerDirection = 90 - playerMouthSize//2
        
        elif self.dir == "Left":
            data.drawPlayerDirection = 0 - playerMouthSize//2
        
        elif self.dir == "Right":
            data.drawPlayerDirection = 180 - playerMouthSize//2
        

        r = data.playerRad
        x = self.x
        y = self.y
        
        canvas.create_arc(x-r, y-r, x+r, y+r, style = PIESLICE, start = data.drawPlayerDirection, extent = playerMouthSize, fill=self.colour)
        canvas.create_oval(x-r//2, y-r//2, x+r//5, y+r//5, fill=self.eyeColour)
        



class Ghost(object):
    moves = ["Up", "Down", "Left", "Right"]
    moveList = []
    edibleSpeed = 4
    edibleColour = "blue"
    eyesColour = "white"
    eyesSpeed = 8
    
    def __init__(self, positionX, positionY, speed, size, colour, personality, faceDirection):
        self.x = positionX
        self.y = positionY
        self.originalSpeed = speed
        self.speed = speed
        self.dir = faceDirection
        self.size = size
        self.originalColour = colour
        self.colour = colour
        self.speed = speed
        self.dir = faceDirection
        self.originalPersonality = personality
        self.personality = personality
        self.state = "normal"
        
        self.i = 0
        self.j = 0
    
    def __repr__(self):
        return ("%s" % (self.state))
    
    def updateIJ(self):
        self.i = int(((self.x - data.marginX)// data.blockSize))
        self.j = int((self.y +self.speed- data.marginY)// data.blockSize)
    
    
    def setState(self, data, newState):
        self.state = newState
        if self.state == "normal":
            self.colour = self.originalColour
            self.speed = self.originalSpeed
            self.personality = self.originalPersonality
            
        elif self.state == "edible":
            self.colour = Ghost.edibleColour
            self.speed = Ghost.edibleSpeed
            self.personality = "Scared"
            if self.centeredGhost(data, self.dir):
                self.dir = "Stop"
            else:
                self.moveGhostToNextBlock(data)
                self.dir = "Stop"
            
        elif self.state == "eyes":
            self.colour = Ghost.eyesColour
            self.speed = Ghost.eyesSpeed
            self.personality = "Home"
            if self.centeredGhost(data, self.dir):
                self.dir = "Stop"
                
            else:
                self.moveGhostToNextBlock(data)
                self.dir = "Stop"
    
    def getState(self):
        return self.state
    
    def getGhostX(self):
        return self.x
    
    def getGhostY(self):
        return self.y
    
    def moveGhost(self, data):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        board = data.blockList
        
        if (self.isLegal(data, data.blockList, self.dir)==False):
            self.dir == "Stop"
        
        if ((i,j) in data.warpDict):
            self.warp(data)
            
        if self.dir == "Down":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y +self.speed- data.marginY)// data.blockSize)
            
            if board[i][j] in data.ghostWalkableList:
                self.y+=self.speed
            else:
                self.updateDirection(data)
            
        elif self.dir == "Up":
            i = int(((self.x - data.marginX)// data.blockSize))
            j = int((self.y -self.speed- data.marginY)// data.blockSize)
            
            if board[i][j] in data.ghostWalkableList:
                self.y-=self.speed
            else:
                self.updateDirection(data)
                
        elif self.dir == "Left":
            i = int(((self.x - self.speed - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)
            
            if board[i][j] in data.ghostWalkableList:
                self.x -= self.speed
            else:
                self.updateDirection(data)

        elif self.dir == "Right":
            i = int(((self.x + self.speed - data.marginX)// data.blockSize))
            j = int((self.y - data.marginY)// data.blockSize)
            
            if board[i][j] in data.ghostWalkableList:
                self.x += self.speed
                
            else:
            
                self.x += self.speed
                self.updateDirection(data)
        
        elif self.dir == "Stop":
            self.x, self.y = self.x, self.y
        
    def moveGhostToNextBlock(self, data):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if self.dir == "Stop":
            if self.state == "normal":
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
            else:
                self.x = (data.ghostRespawnX * data.blockSize)+ data.marginX + (data.blockSize//2)
                self.y = (data.ghostRespawnY * data.blockSize) + data.marginY + (data.blockSize//2)
            
        

        if self.dir == "Up":
            try:
                if data.blockList[i][j-1] in data.ghostWalkableList:
                    if self.y-self.speed >= ((j-1)*data.blockSize + data.marginY):
                        self.y -=self.speed
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                    else:
                        self.y= ((j-1)*data.blockSize) + data.marginY+ (data.blockSize//2)
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                else:
                    if self.y-self.speed >= ((j-1)*data.blockSize + data.marginY):
                        self.y -= self.speed
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                    else:
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
                self.updateDirection(data)
                
        elif self.dir == "Down":
            try:
                if data.blockList[i][j+1] in data.ghostWalkableList:
                    if self.y+self.speed <= ((j+1)*data.blockSize) + data.marginY:
                        self.y +=self.speed
                        self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                    else:
                        self.y= ((j+1)*data.blockSize) + data.marginY + (data.blockSize//2)
                        self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                else:
                    if self.y+self.speed <= ((j+1)*data.blockSize) + data.marginY:
                        self.y +=self.speed
                        self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                        
                    else:
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX + (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY + (data.blockSize//2)
                self.updateDirection(data)
                                    
        elif self.dir == "Left":
            try:
                if data.blockList[i-1][j] in data.ghostWalkableList:
                    if self.x-self.speed >= ((i-1)*data.blockSize) + data.marginX:
                        self.x -=self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    else:
                        self.x= ((i-1)*data.blockSize) + data.marginX
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                else:
                    if self.x-self.speed > ((i-1)*data.blockSize) + data.marginX:
                        self.x -= self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    else:
                        self.updateDirection(data)
            except:
                self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                self.updateDirection(data)   
                
        elif self.dir == "Right":
            try:
                if data.blockList[i+1][j] in data.ghostWalkableList:
                    if self.x+self.speed <= ((i+1)*data.blockSize) + data.marginX:
                        self.x +=self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                    else:
                        self.x= ((i+1)*data.blockSize) + data.marginX+ (data.blockSize//2)
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                else:
                    if self.x+self.speed < ((i+1)*data.blockSize) + data.marginX:
                        
                        self.x += self.speed
                        self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                        
                    else:
                        self.updateDirection(data)
                
            except:
                self.x = (i*data.blockSize) + data.marginX+ (data.blockSize//2)
                self.y = (j*data.blockSize) + data.marginY+ (data.blockSize//2)
                self.updateDirection(data)
        
        
    def draw(self, canvas):
        x = self.x
        y = self.y
        s = self.size

        if self.originalPersonality == "Easy":
            canvas.create_polygon(x, y-(2*s), x+s//2, y, x-s//2, y,  fill = "gray")
            
        elif self.originalPersonality == "Smart":
            canvas.create_polygon(x-s, y-(2*s), x-(s//2), y, x+(s//2), y,x+s, y-(2*s), x, y-s//2 , fill = "gray")
        
        canvas.create_arc(x-s , y-s,  x + s, y+s , style = PIESLICE, start = 0, extent = 180, fill = self.colour, outline = self.colour)
        
        canvas.create_polygon(x-s, y, #point 1
        x-s, y+s,     #point2
        x-(s//2), y+s//2, #point3
        x, y+s, #point4
        x+(s//2), y+(s//2), #point 5
        x+s, y+s, #point6
        s+x,y,
        fill = self.colour, outline = self.colour)
        
        
        
        
    def moveGhostWithTurning(self,data):
        self.updateDirection(data)
        pass
    
    def checkStop(self, data):
        iterateMoveList = ["Up", "Down", "Left", "Right"]
        possMoves = ["Up", "Down", "Left", "Right"]
        
        if self.dir == "Stop":
            for move in (iterateMoveList):
                if not self.isLegal(data, data.blockList, move):
                    possMoves.remove(move)
    
            if len(possMoves)==0:
                print("no poss move")
                pass
                
            else:
                print(self.colour, "checkstop, move with turning")
                self.moveGhostWithTurning(data)
        else:
            pass
    
    def updateDirection(self, data):
        possMoves = ["Up", "Down", "Left", "Right"]
        dir = self.dir
        if dir=="Up":
            complement = "Down"
            possMoves.remove("Down")
            
        elif dir=="Down":
            complement = "Up"
            possMoves.remove("Up")
        
        elif dir=="Left":
            complement="Right"
            possMoves.remove("Right")
            
        elif dir=="Right":
            complement="Left"
            possMoves.remove("Left")
        
        elif dir == "Stop":
            complement = "Stop"
            
        
        board = (data.blockList)
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        iterateMoveList=copy.deepcopy(possMoves)
        
        for move in (iterateMoveList):
            if not self.isLegal(data, board, move):
                possMoves.remove(move)

        if len(possMoves)==0:
            if self.isLegal(data, board, complement):
                self.dir = complement
            else:
                self.dir = "Stop"
        
        elif len(possMoves)==1:
            self.dir = possMoves[0]
        
        else:
            if self.personality == "Easy":
                self.dir = self.followEasy(data, possMoves)
            
            elif self.personality == "Smart":
                startI = int(((self.x - data.marginX)// data.blockSize))
                startJ = int((self.y - data.marginY)// data.blockSize)
                endI = int(((data.playerX - data.marginX)// data.blockSize))
                endJ = int((data.playerY - data.marginY)// data.blockSize)
                portals = data.warpDict
                
                
                newTurn = AStar(data, startI,startJ, endI, endJ, portals, True)
                nextDir = newTurn.solve()
                if nextDir == None:
                    self.dir = self.dir
                self.dir = nextDir
            
            elif self.personality == "Scared":
                self.dir = self.runAwayEasy(data, possMoves)
                
            elif self.personality == "Home":
                if self.originalPersonality == "Smart":
                    startI = int(((self.x - data.marginX)// data.blockSize))
                    startJ = int((self.y - data.marginY)// data.blockSize)
                    
                    endI = data.ghostRespawnX
                    endJ = data.ghostRespawnY
                    
                    newTurn = AStar(data, startI,startJ, endI, endJ, data.warpDict, False)
                    nextDir = newTurn.solve()
                    
                    if nextDir == None:
                        randLen = random.randint(0,len(possMoves)-1)
                        self.dir = possMoves[randLen]
                    
                    self.dir = nextDir
                    
                else:
                    randLen = random.randint(0,len(possMoves)-1)
                    self.dir = possMoves[randLen]

            else:
                randLen = random.randint(0,len(possMoves)-1)
                self.dir = possMoves[randLen]
        
    def isLegal(self, data, board, move, haveWarped = True):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if move=="Up":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.ghostWalkableList)
            else:
                if i>= len(data.blockList) or i<=0 or j<=0 or j>=len(data.blockList[0]):
                    return False
                else:
                    return (board[i][j-1]  in data.ghostWalkableList)

        elif move=="Down":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.ghostWalkableList)
            else:
                if i>= len(data.blockList) or j>= len(data.blockList[0])-1 or i<=0 or j<=0:
                    return False
                
                return (board[i][j+1]  in data.ghostWalkableList)

        elif move=="Left":
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.ghostWalkableList)
                
                
            else:
                if i<=0 or i>=len(data.blockList) or  j> len(data.blockList[0]) or j<=0:
                    return False

                return (board[i-1][j]  in data.ghostWalkableList)
            
        elif move=="Right":
            print(i,j)
            if (i,j) in data.warpDict and self.dir==move:
                (warpOutX, warpOutY) = data.warpDict[i,j]
                return (board[warpOutX][warpOutY] in data.ghostWalkableList)
            else:
                if i>= len(data.blockList)-1 or j>=len(data.blockList[0]) or j<=0 or i<=0:
                    return False
                else:
                    return (board[i+1][j] in data.ghostWalkableList)
        
    
    def centeredGhost(self, data, dir):
        x = self.x
        y = self.y
        
        testX = (x-data.marginX - data.blockSize/2) / data.blockSize
        testY = (y-data.marginY - data.blockSize/2) / data.blockSize
        
        return (int(testX) == testX) and (int(testY) == testY)
    
    def warp(self, data):
        i = int(((self.x - data.marginX)// data.blockSize))
        j = int((self.y - data.marginY)// data.blockSize)
        
        if (i, j) in data.warpDict:
            (nextI, nextJ) = data.warpDict[(i,j)]
            
            
            if self.dir == "Up":
                self.x = data.marginX + (data.blockSize*(nextI+0.5))
                self.y = data.marginY + (data.blockSize*(nextJ-1.5))
                
                
            elif self.dir == "Down":
                self.x = data.marginX + (data.blockSize*(nextI+0.5))
                self.y = data.marginY + (data.blockSize*(nextJ+1.5))
            
            elif self.dir == "Left":
                self.x = data.marginX + (data.blockSize*(nextI-1.5))
                self.y = data.marginY + (data.blockSize*(nextJ+0.5))
                
            elif self.dir == "Right":
                self.x = data.marginX + (data.blockSize*(nextI+1.5))
                self.y = data.marginY + (data.blockSize*(nextJ+0.5))
            
            else:
                pass
        else:
            #There is no warp
            pass
            
    
    def followEasy(self, data, moveList):
        def narrow(moveList, gX, gY, pX, pY):
            recList = []
            if ("Up" in moveList) and pY<gY:
                recList.append("Up")
            if ("Down" in moveList) and pY>gY:
                recList.append("Down")
            if ("Left" in moveList) and pX<gX:
                recList.append("Left")
            if ("Right" in moveList) and pX>gX:
                recList.append("Right")
            return recList
            
        bestHVal = data.width *data.height
        bestMove = "Up" #does not matter
        pX = data.playerX
        pY = data.playerY
        gX = self.x
        gY = self.y
        
        newMoveList = narrow(moveList, gX, gY, pX, pY)
        if len(newMoveList) == 0:
            return moveList[0]
        
        elif len(newMoveList) == 1:
            return newMoveList[0]
        
        else:
            if data.playerFace in newMoveList:
                return data.playerFace
            
            else:    
                move = newMoveList[0]
                if data.playerFace==move:
                    return move
                    
                else:
                    if move == "Up" or move =="Down":
                        dX = abs(gX-pX)
                        dY = abs(gY-pY)
                        if dX<dY:
                            return move
                        else:
                            if "Left" in newMoveList:
                                return "Left"
                            else:
                                return "Right"
                                
                                
    def runAwayEasy(self, data, moveList):
        def narrow(moveList, gX, gY, pX, pY):
            recList = []
            if ("Up" in moveList) and pY>gY:
                recList.append("Up")
            if ("Down" in moveList) and pY<gY:
                recList.append("Down")
            if ("Left" in moveList) and pX>gX:
                recList.append("Left")
            if ("Right" in moveList) and pX<gX:
                recList.append("Right")
            return recList
            
        bestHVal = data.width *data.height
        bestMove = "Stop" #does not matter
        pX = data.playerX
        pY = data.playerY
        gX = self.x
        gY = self.y
        
        newMoveList = narrow(moveList, gX, gY, pX, pY)
        if len(newMoveList) == 0:
            return moveList[0]
        
        elif len(newMoveList) == 1:
            return newMoveList[0]
        
        else:
            if data.playerFace in newMoveList:
                if self.isLegal(data, data.blockList, data.playerFace):
                    print("with javier")
                    return data.playerFace
                else:
                    return "Stop"
            
            else:    
                move = newMoveList[0]
                if data.playerFace==move:
                    if self.isLegal(data, data.blockList, move):
                        return move
                    
                else:
                    if move == "Up" or move =="Down":
                        dX = abs(gX-pX)
                        dY = abs(gY-pY)
                        
                        if dX>dY and self.isLegal(data, data.blockList, move):
                            return move
                        
                            
                        elif dX<=dY:
                            if ("Left" in newMoveList) and self.isLegal(data, data.blockList, "Left"):
                                print("Left is valid")
                                return "Left"
                            else:
                                return "Right"
        

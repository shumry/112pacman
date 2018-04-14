import heapq
import copy

class Struct(object): pass
data = Struct()


class Cell(object):
    def __init__(self, x, y, reachable):
        
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __repr__(self):
        return str((self.x,self.y))
    
    def __lt__(self, other):
        return self.f<other.f

class aiAStar(object):
    def __init__(self, data, startX, startY, endX, endY, portals, portalCheck):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.startX = startX
        self.startY = startY
        self.gridHeight = len(data.blockList[0])
        self.gridWidth = len(data.blockList)
        #print (data.ghostWalkableList)
        for i in range(self.gridWidth):
            for j in range(self.gridHeight):
                if (data.blockList[i][j] in data.aiWalkableList) and ((i,j)not in data.ghostSquares):
                    reachable = True
                else:
                    reachable = False
                self.cells.append(Cell(i, j, reachable))
                
        self.start = self.getCell(startX, startY)
        self.end = self.getCell(endX, endY)
        self.portals = portals
        self.portalCheck = portalCheck
        self.consideredPortal = False
        self.pathLen = None


    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def getCell(self, x, y):
        #print(self.gridWidth)
        return self.cells[(x * self.gridHeight) + y]

    def get_adjacent_cells(self, cell):
        cells = []
        
        if (cell.x,cell.y) in self.portals:
            (leadingX,leadingY)=self.portals[(cell.x,cell.y)]
            self.consideredPortal = True
            
            cells.append(self.getCell(leadingX,leadingY))
        
        if cell.x < self.gridWidth-1:
            cells.append(self.getCell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.getCell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.getCell(cell.x-1, cell.y))
            
        if cell.y < self.gridHeight-1:
            cells.append(self.getCell(cell.x, cell.y+1))
         
         #checks for warping  
        return cells
    
    def get_path(self, startCell=None, endCell=None, fromPortal = False):
        if startCell == None:
            startCell = self.start
        if endCell == None:
            endCell = self.end
            
        cell = endCell
        #print (cell)
        path = [(cell.x, cell.y)]
        while cell.parent is not startCell:
            try:
                cell = cell.parent
                #print(cell.x,cell.y)
                path.append((cell.x, cell.y))
            except:
                return None
        if fromPortal == True:
            path.append(startCell)
        path.reverse()
        return path
        

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
        
    def getLengthNoPortal(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                try:
                    return (len(self.get_path()), self.get_path())
                except:
                    return None
            
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and (adj_cell not in self.closed):
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))
            
    def getLength(self, startCell, endCell, fromPortal=False):
        openedCells = []
        heapq.heapify(openedCells)
        closedCells = set()
        cells = self.cells

        
        heapq.heappush(openedCells, (startCell.f, startCell))
    
        while len(openedCells):
            
            f, cellTest = heapq.heappop(openedCells)
            closedCells.add(cellTest)
            if cellTest is endCell:
                return (len(self.get_path(startCell, endCell, fromPortal)),self.get_path(startCell, endCell, fromPortal))
            
            adj_cells = self.get_adjacent_cells(cellTest)
            #print(adj_cells)
            for adj_cell in adj_cells:
                if adj_cell.reachable and (not(adj_cell in closedCells)):
                    if (adj_cell.f, adj_cell) in openedCells:
                        if adj_cell.g > cellTest.g + 10:
                            self.update_cell(adj_cell, cellTest)
                    else:
                        self.update_cell(adj_cell, cellTest)
                        # add adj cell to open list
                        heapq.heappush(openedCells, (adj_cell.f, adj_cell))
        return 999
    
        
    def solve(self):
        if self.portalCheck == False:
            try:
                self.pathLen = len(noPortalPath)
                (noPortalLength, noPortalPath) = self.getLengthNoPortal()
                
            except:
                return None
                
            (newX, newY) =noPortalPath[0]
                #print(noPortalPath)
                
            if newX- self.startX == 0:
                if newY - self.startY == 1:
                    return "Down"
                elif newY - self.startY == -1:
                    return "Up"
                    
            elif newY - self.startY == 0:
                if newX - self.startX == 1:
                    return "Right"
                elif newX- self.startX == -1:
                    return "Left"           
        
        (noPortalLength, noPortalPath) = self.getLengthNoPortal()
        bestPathLen = len(self.cells) + 1
        bestPortalExit = None
        bestPortalEntry = None
        bestToPortalPath = []
        bestFromPortalPath = []
        
        if self.portalCheck == True and (self.consideredPortal==False) and (len(self.portals)>0):
            #iterates through portals
            for (portalX, portalY) in self.portals:
                entryPortal = self.getCell(portalX, portalY)
                (exitX, exitY) = self.portals[(portalX, portalY)]
                exitPortal = self.getCell(exitX,exitY)
                (toPortalLength, toPortalPath) = self.getLength(self.start, entryPortal)


                if toPortalLength >= noPortalLength:
                    break
                    
                (fromPortalLength, fromPortalPath) = self.getLength(exitPortal,self.end, fromPortal = True)
                
                if fromPortalLength >= noPortalLength:
                    break
                
                newPathLen = (toPortalLength + fromPortalLength + 1)
                
                if newPathLen < bestPathLen:
                    bestPathLen = newPathLen
                    bestPortalEntry = entryPortal
                    bestPortalExit = exitPortal
                    bestToPortalPath = toPortalPath
                    bestFromPortalPath = fromPortalPath
                    
            if bestPathLen <= noPortalLength:
                self.pathLen = bestPathLen
                (newX, newY) =bestToPortalPath[0]
                if newX- self.startX == 0:
                    if newY - self.startY == 1:
                        return "Down"
                    elif newY - self.startY == -1:
                        return "Up"
                    
                elif newY - self.startY == 0:
                    if newX - self.startX == 1:
                        return "Right"
                    elif newX- self.startX == -1:
                        return "Left"    
                
            else:
                (newX, newY) =noPortalPath[0]
                self.pathLen = len(noPortalPath)
                if newX- self.startX == 0:
                    if newY - self.startY == 1:
                        return "Down"
                    elif newY - self.startY == -1:
                        return "Up"
                    
                elif newY - self.startY == 0:
                    if newX - self.startX == 1:
                        return "Right"
                    elif newX- self.startX == -1:
                        return "Left" 
        else:
            (newX, newY) =noPortalPath[0]
            self.pathLen = len(noPortalPath)
            if newX- self.startX == 0:
                if newY - self.startY == 1:
                    return "Down"
                elif newY - self.startY == -1:
                    return "Up"
                    
            elif newY - self.startY == 0:
                if newX - self.startX == 1:
                    return "Right"
                elif newX- self.startX == -1:
                    return "Left" 
                    
    def getPathLen(self):
        return self.pathLen

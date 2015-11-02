#Corie Bain
#Student Number 1436514
#MAC ID: bainc2
#COMP SCI 1XA3 Final Project
#Perfect Maze

from time import * #To make the maze more visually appealing, in addition to painting the path, time was used to simulate walking.
                   #The time call was used to slow the execution of the painting of the path and simulate a walking effect.
                   #The implementation of the time import can be found on line 225 in my code. 

from random import *
from graphics import *
                    
import sys         #The Algorithm was implemented recursively. The recursive depth in python is 1000 by default.
                   #When a maze of size 70 is drawn, there is 70*70=4900 cells involved and the recursive depth in python is easily
                   #exceeded. The solution was to import sys and use the sys.setrecursionlimit(n) function to break that barrier. The implementation of the import can
                   #be found on line 81 of my code.

                   #******NOTE***************************************************************************************************#:
                   #Time and sys were not used to actually create the maze, they were used to enhance it.
                   #Removing the time import and its call will give a less visually appealing static painting of the path.
                   #Removing the sys import and its call will make the user unable to draw an extremely huge maze such as 70.
                   #Even if both these imports and their calls are removed, the maze is still fully functional.
                   #*****NOTE****************************************************************************************************#


"""
This program creates a perfect N by N maze.

After the program is ran, the START CELL will be printed,
followed by the MAZE KEY CELL, and the EXIT CELL.
Next, the PATH TO KEY will be printed, follwed by the PATH FROM KEY TO EXIT,
then the ENTIRE PATH FROM START TO KEY, AND KEY TO EXIT.

The Start point is coloured Red.
The Exit Point is coloured White.
The Key is initially coloured Blue.
Yellow Indicates the initial path taken before the key is found, and up to the key. The key is coloured yellow after it is found.
Violet represents the path taken from the key to the exit, after the key is found.
After the key is found and the exit is reached, "Solved Maze" will be displayed at the exit point and it will be coloured purple.


"""

print()
print()
print("                         {0}".format("This program creates a perfect N by N maze. "))
print()
print("Yellow Indicates the initial path taken before the key is found, and up to the key. The key is coloured yellow after it is found.")
print()
print("Violet represents the path taken from the key to the exit, after the key is found.")
print()
print("Maze Solved is displayed at the exit after the key is found and taken there.")
print()

class MyStack:
    """
    This Class contains methods that perform operations on the Cell Stack.
    """

    def push(self,item,S):
        S.append(item)
    def pop(self,S):
        return S.pop()
    def isEmpty(self,S):
        return len(S) == 0
    def size(self,S):
        return len(S)



    
class maze:
    '''
    Contains methods for building a N by N perfect Maze.
    '''
    def __init__(self,N):  #Self,N
        self.State=True         #MEANING YOU HAVE THE KEY
        self.Path=[[1,1]]       #Used with the explore algorithm, Initial cell [1,1] must be marked as visited.
        self.FootPrints=[]      #Used with the explore algorithm to keep track of where you have been.
        #self.KeyPath=[]    
        self.track=MyStack()  #Creates an instance of the myStack class.     
        #self.N=eval(input("Enter N Value: "))
        self.N=N
        self.TotalCells=self.N*self.N  #REMEMBER TO USE SIZE         
        self.CellStack=[]   #Important Array#3 #At the very start [1,1] is not added here because technically you have not walked over to this location.    
        choose=[]                                                 #This is to choose a random start        
        while True:
            for i in range(0,self.N+2):
                    for j in range(0,self.N+2):
                            k=[i,j]
                            choose.append(k)
            randir=randrange(1,len(choose))
            self.CurrentCell=choose[randir]
            if self.CurrentCell[0]!=0 and self.CurrentCell[0]!=self.N+1 \
               and self.CurrentCell[1]!=0 and self.CurrentCell[1]!=self.N+1:break  #Used to make sure your start is not outside the grid
        self.PreserveStart=self.CurrentCell #Preserves the initial starting point.      
        self.VisitedCoord=[self.CurrentCell] #Important Array#2 #At the very start [1,1] is added to the places you have been.        
        self.VisitedCells=0
        self.North = [[  True for x in range(0,(self.N)+2)] for y in range(0,(self.N)+2)  ]  #Truth grids for every location.
        self.South = [[  True for x in range(0,(self.N)+2)] for y in range(0,(self.N)+2)  ]
        self.East = [[  True for x in range(0,(self.N)+2)] for y in range(0,(self.N)+2)  ]
        self.West = [[  True for x in range(0,(self.N)+2)] for y in range(0,(self.N)+2)  ]
        


    def main(self):
        """
        This is the brain method that calls other methods where necessary.
        """
        sys.setrecursionlimit(2**20)#10**8)
        self.result=self.Breakwalls()  #IS THE INITIAL RESULT OF THE MAZE. THE INITIAL LIST STARTING FROM A RANDOM POINT AND ENDING WHEN ALL CELLS VISITED.
        if self.CurrentCell==[1,1]:     #[1,1] is already taken as the start of explore 
            self.CurrentCell=[1,randrange(2,self.N+1)]
        self.MazeKey=self.GenerateKey() ##Generates a mazekey
        print("Start: ", [1,1])
        print("MazeKey: ", self.MazeKey)
        print("Exit: ", self.CurrentCell)
        self.Objectives()  #Things to do in the maze, find key, find exit.
        print("Path to key: ", self.ExploreKey)  #Path to the Key
        print()
        print("Path from key to exit: ", self.ExploreExit)
        print()
        print("Entire Path from Start to Key, and Key to Exit: ", self.EntirePath)        
        self.drawmaze()


    def Objectives(self):
        """
        This method handles finding the Key and then finding the Exit. 
        """
        self.ExploreKey=self.Explore(1,1)     #FINDS THE KEY INEFFICIENTLY
        self.Path=self.ExploreKey             #Updates the key path to the new inefficient list
        self.ExploreKey=self.Efficient()      #FINDS THE KEY EFFICIENTLY
        self.KeyPath=self.ExploreKey          #AT THIS POINT THE KEY IS FOUND EFFICIENTLY
       
        
        self.Path=[[self.keyx,self.keyy]]          #REFRESHES THE PATH AND STARTS FROM THE KEY CELL SO EXPLORE EXIT CAN TAKE OVER.
        self.FootPrints=[]
        
        self.ExploreExit=self.Explore(self.keyx,self.keyy)   #EXPLORES THE EXIT STARTING FROM THE KEYCELL
        self.Path=self.ExploreExit
        self.ExploreExit=self.Efficient()
        self.ExitPath=self.ExploreExit
       
        self.EntirePath=(self.KeyPath)+(self.ExitPath[1:])
        
        
        
    def GenerateKey(self):
        """
        This method generates the Key.
        """
        while True:                            
            rand=randrange(0,len(self.result))
            self.MazeKey=self.result[rand]
            if self.MazeKey!=self.CurrentCell and self.MazeKey!=[1,1]:break    #Makes sure the key doesnt overlap with the exit.
        self.keyx=self.MazeKey[0]
        self.keyy=self.MazeKey[1]
        return self.MazeKey
        



     
    def drawmaze(self):
        """
        This method handles the drawing of the Maze.
        """
        win=GraphWin("Perfect Maze",600,600)  
        win.setBackground("White")
        scale=600/self.N  #Used to generalize the size difference for the input of larger numbers. The background resolution/ grid size, N

        x1=scale
        y1=0
        x2=scale
        y2=scale

        ##VERTICAL LINES ####
        for i in range(self.N,0,-1):
            for j in range(1,self.N):
                if self.East[j][i]: #If East is true, draw a line.
                    
                    line=Line(Point(x1,y1),Point(x2,y2)) #lines | |
                    line.setFill("red")
                    line.draw(win)
                x1+=scale   #Increment causes |->|
                x2+=scale   #Increment causes |->|
            y1+=scale  #Used to draw two more
            y2+=scale  #of the same spaced lines further down.
            x1=scale   #Reset
            x2=scale   #Reset


        ##HORIZONTAL LINES##
        x1=0
        y1=scale
        x2=scale
        y2=scale


        for i in range(self.N,1,-1):
            for j in range(1,self.N+1):
                if self.South[j][i]:  #If South is true, draw a line.
                    
                    line=Line(Point(x1,y1),Point(x2,y2))
                    line.setFill("red")
                    line.draw(win)
                x1+=scale
                x2+=scale
            y1+=scale
            y2+=scale
            x1=0
            x2=scale

        const=scale//5 #Very useful const which helps in placing circles on grid.
        x=scale//2
        y=600-scale//2
        #radius=(scale-(4*scale//self.N))/2
        radius=scale//2-(const)
        start=Point(x,y)  #START POINT HERE 
        circ=Circle(start,radius)
        circ.setFill("Red")
        label=Text(start,"Start")
        label.setFill("Black")
        circ.draw(win)
        label.draw(win)
        #print(self.CurrentCell)
        #Using the current cell from the finished algorithm(last place visited), a circle can be placed at that point.
        endpointx=(self.CurrentCell[0]-1)*scale +scale//2  ####MAKING END POINT X
        endpointy=600-(self.CurrentCell[1]-1)*scale-scale//2 ####MAKING END POINT Y
        endpoint=Point(endpointx,endpointy)
        circ2=Circle(endpoint,radius)
        circ2.setFill("White")
        label2=Text(endpoint,"End")
        circ2.draw(win)
        label2.draw(win)
        
        ###############CREATE KEY########################
        
        
        keypointx=(self.MazeKey[0]-1)*scale +scale//2  ####MAKING END POINT X
        keypointy=600-(self.MazeKey[1]-1)*scale-scale//2 ####MAKING END POINT Y
        keypoint=Point(keypointx,keypointy)
        circ3=Circle(keypoint,radius)
        circ3.setFill("Blue")
        label3=Text(keypoint,"Key")
        circ3.draw(win)
        label3.draw(win)
        pathcol="Yellow"
##

        
        for i in range(1,len(self.EntirePath)): 
            pathpointx=(self.EntirePath[i][0]-1)*scale +scale//2  ####MAKING END POINT X
            pathpointy=600-(self.EntirePath[i][1]-1)*scale-scale//2 ####MAKING END POINT Y
            pathpoint=Point(pathpointx,pathpointy)
            drawpath=Circle(pathpoint,radius)
            drawpath.setFill(pathcol)
            if self.EntirePath[i]==self.KeyPath[-1]:
                pathcol="Violet"
            label4=Text(keypoint,"Key")
            label4.draw(win)    
            drawpath.draw(win)
            drawpath.setWidth(1)
            sleep(0.1)
        
                #drawpath.draw(win)
                
        label5=Text(endpoint,"Maze Solved ")
        label5.draw(win)
        circ4=Circle(start,radius)
        circ4.setFill("Red")
        circ4.draw(win)        
        label6=Text(start,"Start ")
        label6.draw(win)  

    def Explore(self,x,y):
        """
        This method handles exploring the maze from the start point,
        finding the Key, and then finding the Exit.
        """
        if [x,y]==self.MazeKey and self.State:
            self.State=False
            return self.Path

        if [x,y]==self.CurrentCell and not self.State:
            return self.Path
       
        if not self.North[x][y]  and [x,y+1] not in self.Path:  #If false and not in the explore path so far.
            self.track.push([x,y],self.FootPrints)
            self.track.push([x,y+1],self.Path)
            return self.Explore(x,y+1)
            
        elif not self.East[x][y] and [x+1,y] not in self.Path:
            self.track.push([x,y],self.FootPrints)
            self.track.push([x+1,y],self.Path)
            return self.Explore(x+1,y)
            
        elif not self.South[x][y] and [x,y-1] not in self.Path:
            self.track.push([x,y],self.FootPrints)
            self.track.push([x,y-1],self.Path)
            return self.Explore(x,y-1)

        elif not self.West[x][y] and [x-1,y] not in self.Path:
            self.track.push([x,y],self.FootPrints)
            self.track.push([x-1,y],self.Path)
            return self.Explore(x-1,y)
        else:
            prev=self.track.pop(self.FootPrints)
            x=prev[0]
            y=prev[1]
            self.track.push(prev,self.Path)
            return self.Explore(x,y)
                
    def Efficient(self):  #CLEANS THE INEFFICIENT PATH AND MAKES IT EFFICIENT
        """
        Cleans the inefficient paths taken by eliminating useless routes.
        Returns the most efficient path that can be taken. 
        """
        self.efficient=[]
        for i in range(len(self.Path)):
           #print(self.efficient)
           self.efficient.append(self.Path[i])
           if self.Path[i] in self.efficient[:-1]:
               #print(self.efficient)
               ind=self.efficient.index(self.Path[i])
               self.efficient=self.efficient[:ind+1]
               #n+=1
        return self.efficient  #Creates the most efficient path 
               

        
    def Breakwalls(self):
        """
        This method is used to construct the maze. An intital cell is chosen at
        random and the algorithm stops when all cells have been visited.
        At the end a perfect N by N maze has been generated.
        """
        
        
        if len(self.VisitedCoord)==self.TotalCells:  #Base case for the recursive call.
            
            return self.VisitedCoord                 #When base case is hit, returns the list of all the visited cells. [[x,y],[x,y],[x,y],[x,y]]
        xval=self.CurrentCell[0]  #Breaks Current Cell up, xval is the x value 
        yval=self.CurrentCell[1]  #yval is the y value
        
        
        if    (yval+1==self.N+1 or [xval,yval+1] in self.VisitedCoord) and (yval-1==0 or [xval,yval-1] in self.VisitedCoord) \
               and (xval+1==self.N+1 or [xval+1,yval] in self.VisitedCoord) and (xval-1==0 or [xval-1,yval] in self.VisitedCoord):  #If the Cell is surrounded
                                                                                                                                    #and can't move 
            self.CurrentCell=self.track.pop(self.CellStack)  #Pop the last coord from the cell stack and make that current cell.
            #print("Current: ", self.CurrentCell)
            return self.Breakwalls()  #Recursive call to Breakwalls 
            
        self.track.push(self.CurrentCell,self.CellStack)  #If cell not surrounded push the current cell onto the cellstack and begin looking for a neighbour 
        while True:                                       #Remember Cell stack is where you out your foot down.
            Directions=["North","South","East","West"]
            randir=randrange(0,len(Directions))
            dir=Directions[randir]   #Choose a random direction 
            #print(dir,yval+1,self.CurrentCell,self.VisitedCoord)
            
            if dir== "North" and yval+1<self.N+1 and [xval,yval+1] not in self.VisitedCoord: #if direction and not out of bounds. Self.N+ is the border.
                self.North[xval][yval]=self.South[xval][yval+1] = False                      #if less than that, you are within the border        
                yval+=1;break                
            elif dir =="South" and yval-1>0 and [xval,yval-1] not in self.VisitedCoord:     #in the southern part, 0 is the border.if >0, within actual maze.
                self.South[xval][yval]=self.North[xval][yval-1] = False                
                yval-=1;break                
            elif dir =="East" and xval+1 <self.N+1 and [xval+1,yval] not in self.VisitedCoord:
                self.East[xval][yval]=self.West[xval+1][yval] = False
                xval+=1;break                
            elif dir =="West" and xval-1 > 0 and [xval-1,yval] not in self.VisitedCoord:
                self.West[xval][yval]=self.East[xval-1][yval] =False
                xval-=1;break

        #Above chooses a random direction and if condition checks out, breaks the wall by setting it to false and increments/decrements the respective value
        #to reflect N/S/E/W.
        self.CurrentCell=[xval,yval] #xval/yval was incremented so the new value remains, all thats left is to make the current cell that new coord.
        
        self.track.push(self.CurrentCell,self.VisitedCoord)  #The new current cell is now pushed onto the visited coordinates stack 
    
        return self.Breakwalls()   ##Recursive call on the current cell. Everything happens again on that new coordinate.     

                
      


mazesize = eval(input("Enter maze size: "))
z=maze(mazesize)
z.main()
print()
hold=input("Press Enter to Exit: ")#Used to halt after drawn 











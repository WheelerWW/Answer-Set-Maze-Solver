
from tkinter import *
from os import system

#Initializes one list for each direction a wall can be in relative to each cell.
#Also initializes a list where the Solver's Path will be fed into.
topWalls=[]
rightWalls=[]
bottomWalls=[]
leftWalls=[]



#Opens the file which contains data for the maze and all its walls, then feeds it into four different lists.
with open ("MazeMeta.txt") as f:
    for line in f:
        (t,r,b,l)=line.split(",")
        topWalls.append(t)
        rightWalls.append(r)
        bottomWalls.append(b)
        leftWalls.append(l)


#Creates a simple window and canvas for the GUI.
#The window is not resizeable, as all assets are assigned to specific locations using bit-mapping.
class MazeGUI:
    def __init__(self):
        self.window=Tk()
        self.window.title('Maze Solver')
        self.window.resizable(width=FALSE,height=FALSE)
        self.canvas=Canvas(self.window, width=720, height=600, background='white')
        self.canvas.pack()

        

#Each cell has an (x,y) coordinate and four values, each of which correspond to the direction a wall may be in.
#The "self.xxxLine" statements are used later to draw lines around the cell.
class Cell:
    def __init__(self, X, Y, T, R, B, L):
        self.x=X
        self.y=Y
        self.top=int(T)
        self.right=int(R)
        self.bottom=int(B)
        self.left=int(L)
        
        self.topLine=0      #These are used later
        self.rightLine=0    #in the draw function
        self.bottomLine=0
        self.leftLine=0


#Three buttons are made, each of which calls a different function or method.
#Each button is formatted in pretty much the same way, but they are given different x-coordinates in the "create_window" method.
def makeLayout(mGUI, cellArray):
    
    #The solve button runs the Navigate function.  However, Navigate requires the GUI itself as an input, as well as
    #a current cell, the cell map, and a path to the end cell.  The functions "findCurrent" and "makeFile" generate a current cell
    #and pathway to the end cell respectively.
    solveButton=Button(mGUI.window, text="Solve", justify=CENTER, command=lambda : Navigate(mGUI, findCurrent(mGUI, cellArray), cellArray, makeFile(mGUI)))
    solveButton.configure(width=10, fg='black', bg='cyan', activebackground="#33B5E5", relief=FLAT) #I honestly don't know why "command=lambda" is necessary.  It just is.
    solveButton_window=mGUI.canvas.create_window(100, 550, anchor=NW, window=solveButton)

    #Clear is pretty self-explanatory.  It is used to wipe away any highlighting used in the path generation.
    clearButton=Button(mGUI.window, text="Clear", justify=CENTER, command=lambda : ClearMaze(mGUI, cellArray))
    clearButton.configure(width=10, fg='black', bg='cyan', activebackground="#33B5E5", relief=FLAT)
    clearButton_window=mGUI.canvas.create_window(250, 550, anchor=NW, window=clearButton)

    #Quit is even more self-explanatory.
    quitButton=Button(mGUI.window, text="Quit", justify=CENTER, command=mGUI.window.destroy)
    quitButton.configure(width=10, fg='black', bg='cyan', activebackground="#33B5E5", relief=FLAT)
    quitButton_window=mGUI.canvas.create_window(400, 550, anchor=NW, window=quitButton)

    
    #Two entry windows are created, one for the start cell and one for the end cell.
    #Each entry is given an explanatory label.
    mGUI.sEntry=Entry(mGUI.window, width=20, bd=4)
    mGUI.sEntry_window=mGUI.canvas.create_window(570, 200, anchor=NW, window=mGUI.sEntry)
    mGUI.sLabel=Label(mGUI.window, width=12, text="Start Point (x,y)")
    mGUI.sLabel_window=mGUI.canvas.create_window(590, 179, anchor=NW, window=mGUI.sLabel)

    mGUI.eEntry=Entry(mGUI.window, width=20, bd=4)
    mGUI.eEntry_window=mGUI.canvas.create_window(570, 300, anchor=NW, window=mGUI.eEntry)
    mGUI.eLabel=Label(mGUI.window, width=12, text="End Point (x,y)")
    mGUI.eLabel_window=mGUI.canvas.create_window(590, 279, anchor=NW, window=mGUI.eLabel)

    #This particular label is used to direct the user to create valid input.
    mGUI.fLabel=Label(mGUI.window, width=16, justify=CENTER, bg='white', relief=SUNKEN, text="Please enter the \nstart and end points \nin the format 'x,y' \nwith no parentheses.", font='8')
    mGUI.fLabel_window=mGUI.canvas.create_window(560, 380, anchor=NW, window=mGUI.fLabel)
    


#Takes a cell, which has a set width and height of ~40 pixels, and draws a line on each side of the cell so long as
#the cell has a 0 value for it's wall (indicating the program cannot navigate past it, and hence that there is a wall).
def draw(cell, mGUI):
    X=(cell.x*40)+20
    Y=(cell.y*40)+20

    #These if statements generate the numbers which border the maze.  They help indicate what the (x,y) coordinate positions of a given cell are.
    if cell.x==0:
        mGUI.sLabel=Label(mGUI.window, height=1, width=2, bg='white', text=str(cell.y), font='8')
        mGUI.sLabel_window=mGUI.canvas.create_window(X, Y+10, anchor=NW, window=mGUI.sLabel)
        return
    elif cell.y==0:
        mGUI.sLabel=Label(mGUI.window, height=1, width=2, bg='white', text=str(cell.x), font='8')
        mGUI.sLabel_window=mGUI.canvas.create_window(X+10, Y, anchor=NW, window=mGUI.sLabel)
        return

    if cell.top==False:
        cell.topLine=mGUI.canvas.create_line(X, Y, X+40, Y, fill='black', width=2)        #draw top line
    if cell.right==False:
        cell.rightLine=mGUI.canvas.create_line(X+40, Y, X+40 , Y+40, fill='black', width=2) #draw right line
    if cell.bottom==False:
        cell.bottomLine=mGUI.canvas.create_line(X, Y+40, X+40, Y+40, fill='black', width=2) #draw bottom line
    if cell.left==False:
        cell.leftLine=mGUI.canvas.create_line(X, Y, X, Y+40, fill='black', width=2)       #draw left line
    
#Takes the start and end cells provided by the user and makes sure that they are within a valid range and contain valid input.
#If not, a nonviable cell is returned, which notifies Navigate (the function that uses findCurrent) that the rest of the function is defunct.
def findCurrent(mGUI, cellArray):
    try:
        mGUI.sValue=mGUI.sEntry.get()
        mGUI.eValue=mGUI.eEntry.get()
        (xStart, yStart)=mGUI.sValue.split(",")
        (xEnd, yEnd)=mGUI.eValue.split(",")

        if int(xStart) not in range(1,13) or int(yStart) not in range(1,13) or int(xEnd) not in range(1,13) or int(yEnd) not in range(1,13):
            return cellArray[0][0]
    except:
        return cellArray[0][0]
    return cellArray[int(xStart)][int(yStart)]

#Takes the start and end cells provided by the user and makes sure that they are within a valid range and contain valid input.  Yes, this is a repeat of findCurrent.
#It was too much of a hassle to refactor my code after I got it working.  I understand it's bad coding practicum to have redundent code.  Slap my wrist.       
def makeFile(mGUI):
    newPath=[]
    try:
        mGUI.sValue=mGUI.sEntry.get()
        mGUI.eValue=mGUI.eEntry.get()
        (xStart, yStart)=mGUI.sValue.split(",")
        (xEnd, yEnd)=mGUI.eValue.split(",")

        if int(xStart) not in range(1,13) or int(yStart) not in range(1,13) or int(xEnd) not in range(1,13) or int(yEnd) not in range(1,13):
            messagebox.showinfo('Error','One or more of the numbers entered were not in the correct range.  Please try again.')
            return newPath
    except:
        messagebox.showinfo('Error','One or more of the values entered were in the wrong format.  Please try again.')
        return newPath

#Makes a handler which opens up a file, then writes the start and end cells into it in ASP format. 
    handler=open('MazeStartEnd.txt','w')
    handler.write('holds(current('+mGUI.sValue+'),0).\n')
    handler.write('goal(T):- holds(current('+mGUI.eValue+'),T), step(T).')
    handler.close()
    print('\nholds(current('+mGUI.sValue+'),0).')
    print('goal(T):- holds(current('+mGUI.eValue+'),T), step(T).')

    #Opens the Output file, wipes it, then closes it.
    handler=open('SolverData.txt','w')
    handler.write('')
    handler.close()
    
    system("clingo.exe MazeASPSolver.txt MazeStartEnd.txt > SolverData.txt")    #System call

    #Opens the output file and reads through each line.  Just before the term "SATISFIABLE" is the list of "occurs" statements which I need.
    #I took "doesOccur" and made it save the line just before "line", so that when line==SATISFIABLE, doesOccur equals the occurs statements.
    #That value is then saved into "occurs" and is parsed into newPath, which is a list.
    with open ("SolverData.txt") as f:
        for line in f:
            if "SATISFIABLE" in line:
                occurs=doesOccur
            doesOccur=line
    newPath=[]
    newPath=occurs.split()
    index=0
    for x in newPath:
        print (newPath[index])
        index=index+1
    return newPath

#Takes the start cell generated by "findCurrent" and the path generated by "makeFile" as inputs.
#Moves through each step of the path and highlights each movement made.  Start and end cells are yellow.  Other cells along the path are cyan.
def Navigate(mGUI, cell, cellArray, path):
    if cell==cellArray[0][0]:
        return
        
    X=(cell.x*40)+20
    Y=(cell.y*40)+20
    mGUI.canvas.create_rectangle(X+1 ,Y+1, X+39, Y+39, fill='yellow', outline='')

    for i in path:
        if "move_east" in i:
            cell=cellArray[cell.x+1][cell.y]
        if "move_south" in i:
            cell=cellArray[cell.x][cell.y+1]
        if "move_west" in i:
            cell=cellArray[cell.x-1][cell.y]
        if "move_north" in i:
            cell=cellArray[cell.x][cell.y-1]
        highlight(cell, mGUI)
        
    X=(cell.x*40)+20
    Y=(cell.y*40)+20    
    mGUI.canvas.create_rectangle(X+1 ,Y+1, X+39, Y+39, fill='yellow', outline='')

#Colors cells cyan if they are along the path.
def highlight(cell, mGUI):
    X=(cell.x*40)+20
    Y=(cell.y*40)+20
    mGUI.canvas.create_rectangle(X+1 ,Y+1, X+39, Y+39, fill='cyan', outline='')
    
#Moves through each cell along the maze.  Calls "Clear" on each cell.
def ClearMaze(mGUI, cellArray):
    for x in range(0,13):
        for y in range(0,13):
            Clear(cellArray[x][y],mGUI)
    
#Replaces any highlighting with the color white, effectively returning the maze to normal.
def Clear(cell, mGUI):
    X=(cell.x*40)+20
    Y=(cell.y*40)+20
    mGUI.canvas.create_rectangle(X+1 ,Y+1, X+39, Y+39, fill='white', outline='')



# Main Line
MazeGUI=MazeGUI()
Map=[[[] for x in range(0,13)] for r in range(0,13)]    #Initializing a 2d array
Index=0
for x in range(0,13):
    for y in range(0,13):
        if x==0 or y==0:                    #If x==0 or y==0, do not fill the cells with values for the walls.  These cells are
            newCell=Cell(x, y, 1, 1, 1, 1)  #only used to create numbers along the border to indicate x,y coordinate values.
            Map[x][y]=newCell
            draw(Map[x][y],MazeGUI)
            MazeGUI.window.update()
            
        else:   #Likewise, these cells are filled with the values from the MazeMeta.txt file.
            newCell=Cell(x, y, topWalls[Index], rightWalls[Index], bottomWalls[Index], leftWalls[Index])
            Index=Index+1
            Map[x][y]=newCell
            draw(Map[x][y],MazeGUI)
            MazeGUI.window.update()

makeLayout(MazeGUI, Map)        #Generates GUI







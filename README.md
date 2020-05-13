# Answer-Set-Maze-Solver
A program which uses answer set programming with Clingo to solve a maze generated in Python. Also utilizes a Python GUI for visualization.

This program is a maze solver which utilizes Answer Sets (to solve the maze) and TKinter Python (to get user input and generate the GUI).This program is fairly simple to use.  Just do the following:

1. Type in a start cell and an end cell in the entry fields on the right hand side of the window.  Please make sure they are within x,y format. Also, please be sure that the values you enter are within the range of 1-12.  There is a reminder in the program window if you forget.

2. Click the 'Solve' Button.  The start and end cells that you chose should light up yellow, while any cells along the path to those cells will light up cyan.

3. Click the 'Clear' Button to reset the map.  Enter new values into the entry fields to try again.

4. Click quit when you are ready to exit the program.
	
The files necessary for this program to work are as follows:

1. The MazeSolverGUI.py, which is the TKinter Python code for this program.

2. The MazeASPSolver.txt, which is an Answer Set Program that solves the maze then sends output to the Python GUI.
	
3. MazeMeta.txt, which contains all of the data values necessary to generate the maze into the GUI.

4. MazeStartEnd.txt, which is where the start and end points are saved and then compiled with the ASP Solver.

5. SolverData.txt, which is where the Solver sends its output.  This file is then read by the python program and used to navigate the maze within the GUI.
	
	Also necessary is a Clingo executable within the active directory.
	
	

	
*NOTE*
For whatever reason, my Answer Set Program cannot properly solve mazes of length 4 or lower.  I have tested it extensively to see what the problem might be, and I have found nothing.
It is rather irritating.  However, it is definitely a problem in the ASP, not the Python.  I have tried hard-coding length 3 mazes into the ASP, and the Answer Sets still make no sense.  Given that this is the first Answer Set Program I have ever made, I imagine there may well be an error in my constraints that is causing these strange bugs.
Be prepared to see mazes that move through walls, somehow have 8 or more moves, move backwards, or move from one side of the maze to the other Pacman-style when doing sufficiently small mazes.  (I honestly don't even understand that last one).  
I have constraints to prevent all of these possibilities.  I do not know why they are ineffective at such small maze lengths.

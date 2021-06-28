'''
A program to solve the hyper sudoku puzzle using the backtracking algorithm.
The heuristics used are the Minimum Remaining Value and degree heuristics.
'''

import random
import copy

#Function to read input from file and set up board and domains of the variables
def readFile():
    fileName = input("Input file name to read from: ")
    file = open(fileName)
    #Set up board as a double dimensional array
    initialBoard = [[int(num) for num in row.strip().split(" ")] for row in file]
    #Domains of unassigned variables are stored in a dictionary with
    #the key being a tuple containing the row and column
    domains = {}
    for row in range(9):
        for col in range(9):
            if not initialBoard[row][col]:
                #All domains initially contain all 9 possible numbers
                domains[row,col] = set(range(1,10))
    return initialBoard, domains

#Forward checking to reduce domains of variables constrained by assigned variables
def forwardChecking(board, domains):
    for row in range(9):
        for col in range(9):
            if board[row][col]:
                updateNeighbors(row,col, board, domains)
    
    #If any of the domains has a length of 0, the board is not solvable and the
    #program exits
    for i in domains:
        if len(domains[i]) == 0:
            print("Not solvable")
            exit()

#A function to check if the puzzle has been solved
#I multiply all the numbers on the board and if the result is 0, that means there
#are unassigned variables remaining
def isSolved(board):
    mult = 1
    for row in board:
        for num in row:
            mult*=num
    return mult

#Function to check if a new value is consistent with its neighbors
def consistent(newVar, value, board):
    for neighbor in neighbors(newVar):
        #If any of the neighbors has the same value, return False
        if board[neighbor[0]][neighbor[1]] == value:
            return False
    return True

#Function that implements backtracking algorithm to solve puzzle
def solve(board, domains):
    #Base case: If it is solved, return True
    if isSolved(board):
        return True
    
    #If there are no valid variables left, backtrack
    if sum([len(domains[i]) for i in domains]) == 0:
        return
    
    #Select next variable based on MRV and degree heuristics
    newVar = selectNextVariable(board, domains)
    #Sort the values in ascending order (ORDER-DOMAIN-VALUES function)
    toIterate = sorted(domains[newVar])
    del domains[newVar] #Remove variable from domain once selected
    for value in toIterate: #Iterate over domain of selected variable
        if consistent(newVar, value, board): #Check for consistency
            board[newVar[0]][newVar[1]] = value #If consistent, assign the value
            oldDomains = copy.deepcopy(domains) #Save state of domain in case of backtracking
            updateNeighbors(newVar[0], newVar[1], board, domains) #Update domains of neighbors
            if solve(board, domains): #Recurse
                return True #If call returns True, the solution has been reached already
            board[newVar[0]][newVar[1]] = 0 #If not, set the variable to 0 and backtrack
            domains = oldDomains #Reset the state of the domains
    return False #If function reaches this, the puzzle is unsolvable

#Function to determine neighbors of a variable
def neighbors(variable):
    row = variable[0]
    col = variable[1]
    neighbors = [] #list to keep track of all the neighbors

    #Constraint 1: Check for all horizontal neighbors
    for j in range(9):
        if j != col:
            neighbors.append((row, j))
    
    #Constraint 2: Check for all vertical neighbors
    for i in range(9):
        if i != row:
            neighbors.append((i, col))
    
    #Constraint 3: Check for all neighbors in the same block as variable
    blockRowStart = row - (row % 3)
    blockColStart = col - (col % 3)
    for i in range(blockRowStart, blockRowStart + 3):
        for j in range(blockColStart, blockColStart + 3):
            if i != row and j != col:
                neighbors.append((i,j))

    #Constraint 4: If variable is in a hyperblock, add those neighbors to the list
    if row in [1,2,3,5,6,7] and col in [1,2,3,5,6,7]:
        if row <= 3:
            rowStart = 1
        else:
            rowStart = 5
        
        if col <= 3:
            colStart = 1
        else:
            colStart = 5 
        for i in range(rowStart, rowStart + 3):
            for j in range(colStart, colStart + 3):
                if i != row and j != col:
                    neighbors.append((i, j))
    return neighbors #Return list

#Function to update domains of neighbors based on value of given variable
def updateNeighbors(row, col,board, domains):
    for neighbor in neighbors((row,col)):
        if neighbor in domains:
            domains[neighbor].discard(board[row][col])

#Function to calculate number of assigned neighbors of a variable
def calculateDegree(variable, board):
    count = 0
    for neighbor in neighbors(variable):
        if board[neighbor[0]][neighbor[1]]:
            count += 1
    return count

#Function to select the next variable based on MRV and degree heuristics
def selectNextVariable(board, domains):
    #Populate list using MRV
    minDomain = 9
    for i in domains:
        if board[i[0]][i[1]] == 0 and (0 < len(domains[i]) < minDomain):
            minDomain = len(domains[i])
    possibleVariables = [i for i in domains if board[i[0]][i[1]] == 0 and len(domains[i]) == minDomain]

    #Shorten list using degree heuristic
    maxDegree = 0
    for variable in possibleVariables:
        count = calculateDegree(variable, board)
        if count > maxDegree:
            maxDegree = count

    for variable in possibleVariables:
        if calculateDegree(variable, board) != maxDegree:
            possibleVariables.remove(variable)

    #Randomly select variable from the remaining list
    ind = random.randint(0,len(possibleVariables)-1)
    return possibleVariables[ind]

#Function to print solved puzzle to file
def printOutput(board):
    fileName = input("Input file name to write to: ")
    file = open(fileName, "w")
    file.write("\n".join(" ".join(str(i) for i in row) for row in board))
        
def main():
    board, domains = readFile() #Take input
    forwardChecking(board, domains) #Run forward checking
    if not solve(board, domains): #Solve puzzle
        print("Not Solvable :(") #Print error if puzzle is not solvable
        return
    print("Success!")
    printOutput(board)

main()
from csp import *
from p3_aux import *


def getVariables(puzzle):
    variables = []
    rows, cols = len(puzzle), len(puzzle[0])
    for x in range(rows):
        for y in range(cols):
            if type(puzzle[x][y]) == int:
                varName= "V_%d_%d" % (x, y)
                if varName not in variables:
                    variables.append(varName)
            else:
                neighbors= getNeighbors(x, y, rows, cols)
                for j in neighbors:
                    if type(puzzle[j[0]][j[1]]) == int:
                        varName= "V_%d_%d" % (x, y)
                        if varName not in variables:
                            variables.append(varName)
    variables = sorted(variables)
    return variables


def getNeighbors(x, y, rows, cols):
    neighbors = []
    if x - 1 >= 0:
        neighbors.append((x-1, y))
    if x + 1 < rows:
        neighbors.append((x+1, y))
    if y - 1 >= 0:
        neighbors.append((x, y-1))
    if y + 1 < cols:
        neighbors.append((x, y+1))
    if x - 1 >= 0 and y - 1 >= 0:
        neighbors.append((x-1, y-1))
    if x - 1 >= 0 and y + 1 < cols:
        neighbors.append((x-1, y+1))
    if x + 1 < rows and y - 1 >= 0:
        neighbors.append((x+1, y-1))
    if x + 1 < rows and y + 1 < cols:
        neighbors.append((x+1, y+1))
    return neighbors


puzzle = [[1, 2, '#', '#', '#'],
          [1, '#', '#', '#', 2],
          ['#', '#', '#', 4, '#'],
          ['#', '#', 2, '#', 3],
          [2, 2, '#', 2, '#']]

print(getVariables(puzzle))


def minesweeper_CSP(puzzle):
    variables = getVariables(puzzle)
    return minesweeper_CSP(puzzle)

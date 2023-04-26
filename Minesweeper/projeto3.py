from csp import *
from p3_aux import *


def getVariables(puzzle):
    variables = []
    rows, cols = len(puzzle), len(puzzle[0])
    for x in range(rows):
        for y in range(cols):
            if type(puzzle[x][y]) == int:
                varName = "V_%d_%d" % (x, y)
                if varName not in variables:
                    variables.append(varName)
            else:
                neighbors = getNeighbors(x, y, rows, cols)
                for j in neighbors:
                    if type(puzzle[j[0]][j[1]]) == int:
                        varName = "V_%d_%d" % (x, y)
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


def defineDomains(puzzle):
    domain = {}
    variaveis = getVariables(puzzle)
    rows, cols = len(puzzle), len(puzzle[0])
    for var in variaveis:
        varParsed = int(var.split('_')[1]), int(var.split('_')[2])
        if puzzle[varParsed[1]][varParsed[0]] == "#":
            domain[var] = [0, 1]
        else:
            neighbors = getNeighbors(varParsed[1], varParsed[0], rows, cols)
            espacosVazios = 0
            numBombas = int(puzzle[varParsed[1]][varParsed[0]])
            lst = []
            for x in neighbors:
                if puzzle[x[0]][x[1]] == "#":
                    espacosVazios += 1
            for x in range(espacosVazios-1, -1, -1):
                lst.append(x)
            res=[]
            for comb in itertools.combinations(lst, numBombas):
                newLst = [0] * espacosVazios
                for x in comb:
                    newLst[x] = 1
                res.append(tuple(newLst))
            domain[var]=res

    return domain


puzzle = [[1, 2, '#', '#', '#'],
          [1, '#', '#', '#', 2],
          ['#', '#', '#', 4, '#'],
          ['#', '#', 2, '#', 3],
          [2, 2, '#', 2, '#']]

print(defineDomains(puzzle))


def minesweeper_CSP(puzzle):
    # Definir Variáveis
    variables = getVariables(puzzle)
    # Definir Domínios
    domains = defineDomains(puzzle)


    return CSP(variables, domains, neighbors ,constraints)


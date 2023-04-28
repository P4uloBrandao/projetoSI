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


def show_domains(domains):
    result = []
    for key in domains:
        result.append((key, domains[key]))
    return result


def getNeighbors(x, y, rows, cols):
    neighbors = []
    if y - 1 >= 0:
        neighbors.append((x, y-1))
    if x + 1 < rows and y - 1 >= 0:
        neighbors.append((x+1, y-1))
    if x + 1 < rows:
        neighbors.append((x+1, y))
    if x + 1 < rows and y + 1 < cols:
        neighbors.append((x+1, y+1))
    if y + 1 < cols:
        neighbors.append((x, y+1))
    if x - 1 >= 0 and y + 1 < cols:
        neighbors.append((x-1, y+1))
    if x - 1 >= 0:
        neighbors.append((x-1, y))

    if x - 1 >= 0 and y - 1 >= 0:
        neighbors.append((x-1, y-1))
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
            res = []
            for comb in itertools.combinations(lst, numBombas):
                newLst = [0] * espacosVazios
                for x in comb:
                    newLst[x] = 1
                res.append(tuple(newLst))
            domain[var] = sorted(res)

    return domain


def defineConstraint(A, a, B, b):
    if type(a) == int:
        positianA = (int(A.split('_')[1]), int(A.split('_')[2]))
        positianB = (int(B.split('_')[1]), int(B.split('_')[2]))
        neighbors = getNeighbors(
            positianB[1], positianB[0], len(puzzle), len(puzzle[0]))
        vazios = []
        for pos in range(len(neighbors)):
            if puzzle[neighbors[pos][1]][neighbors[pos][0]] == "#":
                vazios.append(neighbors[pos])
        for x in range(len(vazios)):
            if vazios[x] == positianA:
                if len(b) >= x+1:
                    return a == b[x]

    if type(b) == int:
        positianA = (int(A.split('_')[1]), int(A.split('_')[2]))
        positianB = (int(B.split('_')[1]), int(B.split('_')[2]))
        neighbors = getNeighbors(
            positianA[1], positianA[0], len(puzzle), len(puzzle[0]))
        vazios = []
        for pos in range(len(neighbors)):
            if puzzle[neighbors[pos][1]][neighbors[pos][0]] == "#":
                vazios.append(pos)
        for x in range(len(vazios)):
            if vazios[x] == positianB:
                if len(a) >= x+1:
                    return a[x] == b
    return a == b


# puzzle = [[1, 2, '#', '#', '#'],
#           [1, '#', '#', '#', 2],
#           ['#', '#', '#', 4, '#'],
#           ['#', '#', 2, '#', 3],
#           [2, 2, '#', 2, '#']]


def minesweeper_CSP(puzzle):
    # Definir Variáveis
    variables = getVariables(puzzle)
    # Definir Domínios
    domains = defineDomains(puzzle)
    # Definir Vizinhos
    neighbors = {}
    for var in variables:
        varParsed = int(var.split('_')[1]), int(var.split('_')[2])
        neighbors[var] = []

        if type(puzzle[varParsed[1]][varParsed[0]]) == int:
            for x in getNeighbors(varParsed[0], varParsed[1], len(puzzle), len(puzzle[0])):
                if puzzle[x[1]][x[0]] == "#":
                    neighbors[var].append("V_%d_%d" % (x[0], x[1]))
            neighbors[var] = sorted(neighbors[var])
        else:
            for x in getNeighbors(varParsed[0], varParsed[1], len(puzzle)-1, len(puzzle[0])-1):
                if type(puzzle[x[1]][x[0]]) == int:
                    neighbors[var].append("V_%d_%d" % (x[0], x[1]))
            neighbors[var] = sorted(neighbors[var])
    print(neighbors["V_4_1"])
    
    return CSP(variables, domains, neighbors, defineConstraint)



puzzle = [[1, 2, '#', '#', '#', '#', '#'],
            [1, '#', '#', '#', 2, '#', '#'],
            ['#', '#', '#', 4, '#', '#', '#'],
            ['#', '#', 2, '#', 3, '#', '#'],
            [2, 2, '#', 2, '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#', '#']]
xxx = minesweeper_CSP(puzzle)
grafo = xxx.neighbors

from csp import *
from p3_aux import *
import numpy as np

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
            for x in range(espacosVazios):
                lst.append(0)
            
            for k in range(numBombas):
                lst[k] = 1
            res = (sorted(set(itertools.permutations(lst))))
            # domain[var]=res
            domain[var] = sorted(res)

    return domain


def show_domains(dic):
    r=[]
    for chave in dic:
        r.append((chave,dic[chave]))
    return r

def find_positions(puzzle):
    puzzle = np.array(puzzle)
    puzzle = puzzle.transpose()

    dic = {}
    rows, cols = len(puzzle), len(puzzle[0])
    number_positions = []
    hastag_positions = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            #print("(I: " + str(i) + ", J: " + str(j) + ")" + str(puzzle[i][j]))
            varName = "V_%d_%d" % (i, j)
            lista = []
            if puzzle[i][j] != '#':
                #number_positions.append((i,j))
                k = getNeighbors(i, j, rows, cols)
                for x in k:
                    varName1 = "V_%d_%d" % (x[0], x[1])
                    if puzzle[x[0]][x[1]] == '#':
                        
                        lista.append(varName1)
                if len(lista) > 0:
                    dic[varName] = sorted(lista)
            else:
                #hastag_positions.append((i,j))
                #number_positions.append((i,j))
                k = getNeighbors(i, j, rows, cols)
                for x in k:
                    posicao = puzzle[x[0]][x[1]]
                    varName1 = "V_%d_%d" % (x[0], x[1])
                    if puzzle[x[0]][x[1]] != '#':
                        
                        lista.append(varName1)
                if len(lista) > 0:
                    dic[varName] = sorted(lista)


    return dic

def name_find_positions(puzzle):
    find_positions(puzzle)

def updateVariables(neighbors):
    vars = []
    for var in neighbors:
        if var not in vars:
            vars.append(var)
    return vars
    
def updateDomains(neighbors, domains):
    removeKeys = []
    for d in domains:
        if d not in neighbors:
            removeKeys.append(d)
    for r in removeKeys:
        domains.pop(r)
    return domains

def minesweeper_CSP(puzzle):
    # Definir Variáveis
    variables = getVariables(puzzle)

    # Definir Domínios
    #domains = defineDomains(puzzle)
    
    # Definir Vizinhos
    neighbors = find_positions(puzzle)

    variables = updateVariables(neighbors)

    #domains = updateDomains(neighbors, domains)

    # Definir Restrições
    constraints = {}

    return CSP(variables, None, neighbors ,None)


puzzle=[[1, 2, '#', '#', '#'],
[1,'#','#','#',2],
['#','#','#',4,'#'],
['#','#',2,'#',3],
[2,2,'#',2,'#'],
['#','#','#',4,'#'],
['#','#',2,'#',3],
['#','#','#','#','#']]
xxx= minesweeper_CSP(puzzle)
#print(xxx.variables)
#print(xxx.domains)
#print(xxx.neighbors)

#print(show_domains(xxx.domains))

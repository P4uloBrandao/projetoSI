from searchPlus import *
from p2_aux import *


class GridProblem(Problem):
    def __init__(self, initial, goal, obstacles=()):
        self.initial = initial
        self.goal = goal
        self.obstacles = set(obstacles) - {initial, goal}
        self.pacman = initial
        pacmanX, pacmanY = self.pacman
        pastilhaX, pastilhaY = self.goal

        if pacmanX < pastilhaX:
            minX = pacmanX - 1
            maxX = pastilhaX

        elif pacmanX > pastilhaX:
            minX = pastilhaX
            maxX = pacmanX + 1

        else:
            minX = pacmanX - 1
            maxX = pacmanX + 1

        if pacmanY < pastilhaY:
            minY = pacmanY - 1
            maxY = pastilhaY

        elif pacmanY > pastilhaY:
            minY = pastilhaY
            maxY = pacmanY + 1

        else:
            minY = pacmanY - 1
            maxY = pacmanY + 1

        lista = []
        for j in range(minY, maxY+1):  # range devia conter apenas o self.pacman e a self.goal
            add = []
            for i in range(minX, maxX+1):  # range devia conter apenas o self.pacman e a self.goal
                add.append((i, j))
            lista.append(add)
        self.expanded = lista

    directions = {"N": (0, -1), "S": (0, +1), "W": (-1, 0),
                  "E": (1,  0)}  # ortogonais

    def result(self, state, action):
        "Tanto as acções como os estados são representados por pares (x,y)."
        (x, y) = state
        (dx, dy) = self.directions[action]
        return (x+dx, y+dy)

    def actions(self, state):
        """Podes move-te para uma célula em qualquer das direcções para uma casa
           que não seja obstáculo."""
        x, y = state
        return [act for act in self.directions.keys() if (x+self.directions[act][0], y+self.directions[act][1]) not in self.obstacles]

    def goal_test(self, state):
        return state == self.goal

    def manhatan_goal(self, no):
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        return manhatan(no.state, self.goal)

    def addObstacle(self, obstacle):
        self.obstacles.add(obstacle)

    def showOutput(self, path=[]):
        output = ""
        for y in self.expanded:
            ch = ""
            for x in range(len(y)):
                if self.pacman == y[x]:
                    ch += '@ '
                elif self.goal == y[x]:
                    ch += '* '
                elif y[x] in self.obstacles:
                    ch += '# '
                elif y[x] in path:
                    ch += '+ '
                else:
                    ch += '. '
            output += ch + "\n"
        print(output)


def aroundPacman(pacman):
    return [(pacman[0]+i, pacman[1]+j)
            for i in range(-1, 2) for j in range(-1, 2)]


def obstaclesAround(pacman, obstacles):
    arround_pacman = aroundPacman(pacman)
    res = []
    for i in arround_pacman:
        if i in obstacles:
            res.append(i)
    return res


def pathCount(pacman, iteracao):
    path = [pacman]
    for x in iteracao:
        if x == 'N':
            pacman = (pacman[0], pacman[1]-1)
            path.append(pacman)
        elif x == 'S':
            pacman = (pacman[0], pacman[1]+1)
            path.append(pacman)
        elif x == 'W':
            pacman = (pacman[0]-1, pacman[1])
            path.append(pacman)
        elif x == 'E':
            pacman = (pacman[0]+1, pacman[1])
            path.append(pacman)
    return path


def planeia_online(pacman, pastilha, obstaculos):

    aroundObstacles = obstaclesAround(pacman, obstaculos)
    iteracao = 0

    gridProblem = GridProblem(
        initial=pacman, obstacles=aroundObstacles, goal=pastilha)

    res_astar = astar_search(gridProblem, gridProblem.manhatan_goal).solution()

    acabou = False

    print("MUNDO")
    display(pacman, pastilha, fronteira | l | c, path=[])

    print("\nMODELO")
    #  faz modelo é o mundo cortado em que é mostrado o pacman e a pastilha
    # em cada iteração irá mostrar o plano gerado pelo astar_search
    gridProblem.showOutput(path=[])

    while not acabou:
        path = []
        iteracao += 1
        print("\nITERAÇÃO " + str(iteracao))
        res_astar = astar_search(
            gridProblem, gridProblem.manhatan_goal).solution()
        print(str(res_astar) + "\n")
        path = pathCount(pacman, res_astar)
        for x in range(1, len(path)):
            if path[x] in obstaculos:
                del path[x:]
                gridProblem.pacman = path[x-1]
                break
            else:
                gridProblem.pacman = path[x]
                aroundPac = aroundPacman(gridProblem.pacman)
                for i in aroundPac:
                    if i in obstaculos and i not in gridProblem.obstacles:
                        gridProblem.addObstacle(i)
                    model = gridProblem.expanded
                    if i[1] > len(model):
                        model.append([])
                    for x in range(1, len(model)+1):
                        if i[1] == x and i not in model[x-1]:
                            model[x-1].append(i)
                            gridProblem.expanded = model

        gridProblem.showOutput(path=path)

        if gridProblem.pacman == gridProblem.goal:
            acabou = True


pacman = (1, 2)
pastilha = (3, 6)
l = line(2, 2, 1, 0, 6)
c = line(2, 3, 0, 1, 4)
fronteira = quadro(0, 0, 10)
obstaculos = fronteira | l | c
planeia_online(pacman, pastilha, obstaculos)

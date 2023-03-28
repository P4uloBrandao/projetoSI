from searchPlus import *
from p2_aux import *


class GridProblem(Problem):
    def __init__(self, initial, goal, obstacles=()):
        self.initial = initial
        self.goal = goal
        self.obstacles = set(obstacles)
        self.expanded = set()

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
        actions = []
        for action in self.directions:
            dx, dy = self.directions[action]
            if (x+dx, y+dy) not in self.obstacles:
                actions.append(action)
        return actions
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


def steps(pacman, iteracao):
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

    acabou = False

    print("MUNDO")
    display(pacman, pastilha, fronteira | l | c, path=[])

    print("\nMODELO")
    #  faz modelo é o mundo cortado em que é mostrado o pacman e a pastilha
    # em cada iteração irá mostrar o plano gerado pelo astar_search
    display(gridProblem.initial, gridProblem.goal, gridProblem.obstacles)

    while not acabou:
        path = []
        iteracao += 1
        print("\nITERAÇÃO " + str(iteracao))
        res_astar = astar_search(
            gridProblem, gridProblem.manhatan_goal).solution()
        print(str(res_astar) + "\n")
        path = steps(gridProblem.initial, res_astar)
        for x in range(1, len(path)):
            if path[x] in obstaculos:
                del path[x:]
                gridProblem.initial = path[x-1]
                break
            else:
                gridProblem.initial = path[x]
                aroundPac = aroundPacman(gridProblem.initial)
                for i in aroundPac:
                    if i in obstaculos and i not in gridProblem.obstacles:
                        gridProblem.addObstacle(i)
                            
        display(gridProblem.initial, gridProblem.goal, gridProblem.obstacles, path=path)

        if gridProblem.initial == gridProblem.goal:
            acabou = True


# Exemplo 3 

pacman=(1,1)
pastilha=(3,3)
l = line(2,2,1,0,6)
c = line(2,3,0,1,4)
fronteira = quadro(0,0,10)
obstaculos=fronteira | l | c
# atacar o planeamento repetido
planeia_online(pacman,pastilha,obstaculos)

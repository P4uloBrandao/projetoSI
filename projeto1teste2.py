from searchPlus import *
from p2_aux import *

class GridProblem(Problem):
    def __init__(self, initial, goal, obstacles=()):
        self.initial = initial
        self.goal = goal
        self.obstacles = set(obstacles)
        self.expanded = 0
        self.expandedMoment=0

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
        self.expanded += 1
        self.expandedMoment += 1
        return actions

    def goal_test(self, state):
        return state == self.goal


    def manhatan_goal(self, node):
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        manhatan(no.state, self.goal)

    def adaptative_heuristic(self, node):
        """Calcula a diferença entre a distância atual do estado à meta e a distância estimada
        pela heurística. Essa diferença é armazenada em um novo atributo, adaptative_heuristic."""
        distance_to_goal = self.manhattan_distance(node.state, self.goal)
        return distance_to_goal - node.f

    def value(self, state):
        """Retorna a distância do estado atual à meta."""
        return self.manhattan_distance(state, self.goal)

    def f(self, node):
        """Calcula a função de avaliação do A*, que é a soma da distância
        do nó à meta (dada pela função value) e da adaptação da heurística
        (dada pela função adaptative_heuristic)."""
        return self.value(node.state) + self.adaptative_heuristic(node)

    def add_obstacle(self, obstacle):
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

def planeia_adaptativo_online(pacman, pastilha, obstaculos):
    aroundObstacles = obstaclesAround(pacman, obstaculos)
    iteracao = 0

    gridProblem = GridProblem(
        initial=pacman, obstacles=aroundObstacles, goal=pastilha)

    acabou = False

    print("MUNDO")
    display(pacman, pastilha, obstaculos, path=[])

    print("MODELO")
    display(gridProblem.initial, gridProblem.goal, gridProblem.obstacles)

    while not acabou:
        path = []
        iteracao += 1
        print("ITERAÇÃO: " + str(iteracao))
        gridProblem.expandedMoment = 0
        res_astar = astar_search(gridProblem, gridProblem.manhatan_goal).solution()
        print(str(res_astar))
        print("Expandidos " + str(gridProblem.expandedMoment))
        
        # calculo da heuristica adaptativa
        for i in range(len(res_astar)):
            state = gridProblem.result(gridProblem.initial, res_astar[i])
            g_val = i+1
            h_val = gridProblem.manhatan_goal(Node(state, None, None, g_val, None))
            f_diff = h_val - g_val
            if state in gridProblem.obstacles:
                continue
            if state not in gridProblem._closed and state not in gridProblem._opened:
                gridProblem._opened.add(state)
                gridProblem.g[state] = g_val
                gridProblem.h[state] = h_val
                gridProblem.f[state] = g_val + h_val + f_diff
            elif state in gridProblem._opened and g_val < gridProblem.g[state]:
                gridProblem.g[state] = g_val
                gridProblem.h[state] = h_val
                gridProblem.f[state] = g_val + h_val + f_diff
                gridProblem._opened.update(state)
            elif state in gridProblem._closed and g_val < gridProblem.g[state]:
                gridProblem.g[state] = g_val
                gridProblem.h[state] = h_val
                gridProblem.f[state] = g_val + h_val + f_diff
                gridProblem._closed.remove(state)
                gridProblem._opened.add(state)
        
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
    print("FIM: total de expandidos: " + str(gridProblem.expanded))

l = line(2,2,1,0,6)
c = line(2,3,0,1,4)
fronteira = quadro(0,0,10)
pacman=(1,1)
pastilha=(3,3)
paredes=fronteira | c | l
# atacar o planeamento repetido
planeia_adaptativo_online(pacman,pastilha,paredes)
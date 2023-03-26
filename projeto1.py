from searchPlus import * 
from p2_aux import *



class GridProblem(Problem):
    def __init__(self, initial, goal, obstacles=()):
        self.initial=initial
        self.goal=goal 
        self.obstacles=set(obstacles) - {initial, goal}
 

    directions = {"N":(0, -1), "S":(0, +1), "W":(-1, 0), "E":(1,  0)}  # ortogonais
                  
    def result(self, state, action): 
        "Tanto as acções como os estados são representados por pares (x,y)."
        (x,y) = state
        (dx,dy) = self.directions[action]
        return (x+dx,y+dy) 
    
    def actions(self, state):
        """Podes move-te para uma célula em qualquer das direcções para uma casa 
           que não seja obstáculo."""
        x, y = state
        return [act for act in self.directions.keys() if (x+self.directions[act][0],y+self.directions[act][1]) not in self.obstacles]

    def goal_test(self, state):
        return state == self.goal

    def manhatan_goal(self,no) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        return manhatan(no.state,self.goal)

pacman=(1,2)
pastilha=(3,6)
l = line(2,2,1,0,6)
c = line(2,3,0,1,4)
fronteira = quadro(0,0,10)
obstaculos=fronteira | l | c
g = GridProblem(initial=(1,1), obstacles=fronteira | l | c,goal=(3,3))

#display(pacman, pastilha, fronteira | l | c,path=[])

def display_modelo(pacman,pastilha,obstaculos,path=[]):
    """ print the state please"""
    pacmanX,pacmanY=pacman
    osXs={x for (x,_) in obstaculos | {pastilha, pacman}}
    minX=min(osXs)
    maxX=max(osXs)
    osYs={y for (_,y) in obstaculos | {pastilha, pacman}}
    minY=min(osYs)
    maxY=max(osYs)
    output=""
    arround_pacman = [(pacmanX+i,pacmanY+j) for i in range(-1,2) for j in range(-1,2)]
    for j in range(minY,pastilha[1]+1): # range devia conter apenas o pacman e a pastilha
        for i in range(minX,pastilha[0]+2): # range devia conter apenas o pacman e a pastilha
            if pacman ==(i,j):
                ch = '@'
            elif pastilha==(i,j):
                ch = "*"
            elif (i,j) in obstaculos and (i,j) in  arround_pacman :
                ch = "#"
            elif (i,j) in path:
                ch = '+'
            else:
                ch = "."
            output += ch + " "
        output += "\n"
    print(output)

display_modelo(pacman, pastilha, fronteira | l | c,path=[])


def planeia_online(pacman, pastilha, obstaculos):
    
    print("MUNDO")
    display(pacman, pastilha, fronteira | l | c,path=[])

    print("\nMODELO")
    #  faz modelo é o mundo cortado em que é mostrado o pacman e a pastilha
    # em cada iteração irá mostrar o plano gerado pelo astar_search 


    print("\nIteração: " + str(0))
    print(action())
    print("Expandidos: " + str(0))
    # bem como o número de estados expandidos o novo modelo do mundo com a sua nova posição e as marcas das posições por onde andou.
    #o ciclo termina quando o Pacman chega à pastilha


    print("\nFim: total de expandidos: " + str(0))
    #No final deve indicar o total de expandidos acumulados ao longo dos vários planeamentos.

res_astar = astar_search(g,g.manhatan_goal)
print(res_astar.solution())
print('Custo =',res_astar)


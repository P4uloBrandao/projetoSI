from copy import *
from random import *

class EstadoOuri:
    
    def __init__(self,tabuleiro=None,n=12, to_move="Um"):
        self.n = n
        self.tabuleiro = [4]*12 # atenção à numeração Um joga de 0 a 5, Outro de 6 a 11
        self.sacoUm=0
        self.sacoOutro=0 #todas as pedras estao no tabuleiro
        self.to_move=to_move
        self.passa=False #serve para ver se o jogo pode terminar esvaziando o tabuleiro
        self.cuidadoCiclo=False
        
    def copy_me(self):
        """Generate a clone of myself"""
        clone=EstadoOuri(n=self.n, to_move=self.to_move)
        clone.tabuleiro=deepcopy(self.tabuleiro)
        clone.sacoUm= self.sacoUm
        clone.sacoOutro = self.sacoOutro
        clone.passa=self.passa
        clone.cuidadoCiclo = self.cuidadoCiclo
        return clone 

    def proximo(self,i):
        return (i+1)%self.n

    def anterior(self,i):
        return (i-1)%self.n

    def souUmEstadoPequeno(self):
        return sum(self.tabuleiro[:self.n//2]) == 0 \
               or sum(self.tabuleiro[self.n//2:self.n]) == 0 \
               or (sum(self.tabuleiro[:self.n//2]) < 5 and sum(self.tabuleiro) < 9) \
               or (sum(self.tabuleiro) < 31 and self.tabuleiro[:self.n//2]==self.tabuleiro[self.n//2:])
               # não é pequeno mas é um potencial ciclo

    def terminou (self):
        "Usado para o display, se um jogo terminou não há next player."
        "estes testes são usados em ourtos sítios, são flags assinaladas"
        return sum(self.tabuleiro)==0 \
               or self.sacoUm>self.n*4//2 \
               or self.sacoOutro>self.n*4//2\
               or (self.passa and self.naohajogada()) \
               or self.cuidadoCiclo
               
    def cicloDetectado(self):
        self.cuidadoCiclo = True
        self.despeja()

        

    def naohajogada(self):
        if self.to_move=="Um" and sum(self.tabuleiro[:self.n//2])!=0:
            return all([self.tabuleiro[i]<self.n//2-i for i in range(0,self.n//2)])
        else:
            return all([self.tabuleiro[i]<self.n-i for i in range(self.n//2, self.n)]) 
            
    def despeja(self): # o jogo vai terminar sem 25, vamos despejar nos sacos
        self.sacoUm += sum(self.tabuleiro[:self.n//2])
        self.sacoOutro += sum(self.tabuleiro[self.n//2:self.n])
        self.tabuleiro=[0]*self.n

    def display(self):
        """Display the state"""
        print("SacoOutro= ", self.sacoOutro) 
        print("+"+"----"*(self.n//2))
        print("|",end="")
        for k in self.tabuleiro[::-1][:self.n//2]:
            print("{0:2d} ".format(k), end="|")
        print()
        print("|", end="")
        for k in self.tabuleiro[:self.n//2]:
            print("{0:2d} ".format(k), end="|")
        print()
        print("+"+"----"*(self.n//2))
        print("SacoUm= ", self.sacoUm)         
        if not self.terminou():
            print('--NEXT PLAYER:',self.to_move)

    
                    
from jogos import *

##########class jogo_BT(Game):
class JogoOuri(Game):
    """Play Ouri on an 2 x 6 board, with Um (first player) playing first (1--6) and
    Outro playing 7--12: internal coordinates go 0--11, of course
    """
    
    def __init__(self):
        self.initial= EstadoOuri()
        self.estadosPequenos=[] # lista de tabuleiros para o joga11 testar ciclos
        
    def actions(self, state):
        "Legal moves for Um and Outro"
        if state.to_move=="Um":
            jogadas = [x for x in range(0, state.n//2) if state.tabuleiro[x]>1] #regra 2
            # vamos ver se deixamos o adversário com peças (regra 4)
            tabuleiros = list(map(lambda x: self.result(state,x), jogadas))
            jogadas = [jogadas[i] for i in range(len(jogadas)) if sum(tabuleiros[i].tabuleiro[state.n//2:state.n])!=0]
            # se não há jogadas válidas, vamos ver se só sobram 1s (ultima linha regra 2)
            if jogadas ==[]:
                jogadas = [x for x in range(0, state.n//2) if state.tabuleiro[x]>0] #ultima linha regra2
            # e mais uma vez temos de retirar as jogadas que deixam o adv a seco
            tabuleiros = list(map(lambda x: self.result(state,x), jogadas))
            jogadas = [jogadas[i] for i in range(len(jogadas)) if sum(tabuleiros[i].tabuleiro[state.n//2:state.n])!=0]
            
        else:
            jogadas = [x for x in range(state.n//2, state.n) if state.tabuleiro[x]>1] #regra2
            # vamos ver se deixamos o adversário com peças (regra 4)
            tabuleiros = list(map(lambda x: self.result(state,x), jogadas))
            jogadas = [jogadas[i] for i in range(len(jogadas)) if sum(tabuleiros[i].tabuleiro[:state.n//2])!=0]
            # se não há jogadas válidas, vamos ver se só sobram 1s (ultima linha regra 2)
            if jogadas ==[]:
                jogadas = [x for x in range(state.n//2, state.n) if state.tabuleiro[x]>0] #ultima linha regra2
            # e mais uma vez temos de retirar as jogadas que deixam o adv a seco
            tabuleiros = list(map(lambda x: self.result(state,x), jogadas))
            jogadas = [jogadas[i] for i in range(len(jogadas)) if sum(tabuleiros[i].tabuleiro[:state.n//2])!=0]
        return jogadas if jogadas != [] else ["passa"] #ainda para a regra 4, alinea b, para forçar o adversário a jogar novamente


    def result(self, state, move):
        ss=state.copy_me()
        ss.to_move = "Um" if state.to_move == "Outro" else "Outro"
        if move == "passa" and state.naohajogada(): # o jogo termina a seguir
            ss.passa = True
            ss.despeja()
            return ss
        if move == "passa": # aqui não termina, há jogadas possíveis
            ss. passa=True
            return ss
        # vamos espalhar as pedras
        pedras = ss.tabuleiro[move] 
        ss.tabuleiro[move]=0
        buraco = move
        while pedras > 0:
            buraco=ss.proximo(buraco)
            if buraco != move:
                ss.tabuleiro[buraco] += 1
                pedras -= 1
        ## já distribuimos as pedras        
        ## agora vamos às capturas
        if state.to_move=="Um":
            while buraco in range(ss.n//2, ss.n) and ss.tabuleiro[buraco] in [2,3]:
                ss.sacoUm += ss.tabuleiro[buraco]
                ss.tabuleiro[buraco]=0
                buraco = ss.anterior(buraco)            
        else:
            while buraco in range(ss.n//2) and ss.tabuleiro[buraco] in [2,3]:
                ss.sacoOutro += ss.tabuleiro[buraco]
                ss.tabuleiro[buraco]=0
                buraco = ss.anterior(buraco)
        return ss

    def addEstadoPequeno(self, state):
        self.estadosPequenos.append(state.tabuleiro)

    def estamosEmCiclo(self,state):
        return state.tabuleiro in self.estadosPequenos

    def utility(self, state, player):
        """Return always the score."""
        if player == "Um":
            return state.sacoUm
        else:
            return state.sacoOutro

    def terminal_test(self, state):
        "A state is terminal if the whites reached line 7 or some black reached line 0."
        " the state knows, there may be no more W or B"
        return state.terminou()

    def executa(self, estado, listaJogadas):
        "executa varias jogadas sobre um estado dado"
        "devolve o estado final "
        s = estado
        for j in listaJogadas:
            s = self.result(s, j)
        return s

    def display(self, state):
        state.display()



from jogar import *
from La_Ouri import *
from jogos import *


#### def kibir

def func_aval_1111(s,p):
    """valoriza ter mais peças do que o adversário"""
    if s.terminou():
        if p == "Um":
            if s.sacoUm>24:
                return 100
            elif s.sacoOutro >24:
                return -100
            else:
                return 0
        else:
            if s.sacoOutro >24:
                return 100
            elif s.sacoUm>24:
                return -100
            else:
                return 0
    if p == "Um":
        return s.sacoUm+sum(s.tabuleiro[:s.n//2])# - sum(s.tabuleiro[s.n//2:])
    else:
        return s.sacoOutro+sum(s.tabuleiro[s.n//2:])# - sum(s.tabuleiro[:s.n//2])

jogadorOuri_Kibir4 = JogadorAlfaBeta("Kibir4", 4 ,func_aval_1111)

######## abaixo estão jogadores para ajudar a explorar o jogo e as vossas opções


######jogadores simples: humanos perguntam a jogada de entre as possíveis e
# Bacoco escolhe aleatóriamente 
# simplório escolhe a primeira das acções disponíveis
### isto serve para testarem as vossas heurísticas e jogadores

def pergunta(game, state):
    game.display(state)
    print("Jogadas possiveis: ", game.actions(state))
    return int(input(state.to_move+",  qual a jogada? "))
    
humano1 = Jogador("Pessoa1", pergunta)
humano2 = Jogador("Pessoa2", pergunta)

def bacoco(game, state):
    return choice(game.actions(state))

def simplorio(g,s):
    return g.actions(s)[0]

bacoco1 = Jogador("Bacoco1", bacoco)

bacoco2 = Jogador("Bacoco2", bacoco)

simplorio1 = Jogador("Simplorio1", simplorio)
simplorio2 = Jogador("Simplorio2", simplorio)

todos_jogadores = [bacoco1, bacoco2, simplorio1, simplorio2, jogadorOuri_Kibir4]



###### Para testes descomentar isto a seguir

#faz_campeonato(JogoOuri(), todos_jogadores, 1)


#### este serve para testar os dois jogadores abaixo com 2x50 jogos

vit = 0
for _ in range(500):
    ((a,b),x,n)= joga11(JogoOuri(),simplorio2, jogadorOuri_Kibir4)
    vit += n<24
    vit += 0.5*(n==24)
    ((a,b),x,n)= joga11(JogoOuri(), jogadorOuri_Kibir4, simplorio2)
    vit += n>24
    vit += 0.5*(n==24)
    print(".", end="")

print("alcacer kibir ganhou "+str(vit)+ "de 1000 jogos")
##
##

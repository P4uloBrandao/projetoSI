from jogar import *
from La_Ouri import *
from jogos import *

def h(s,p):
    """Heurística simples que valoriza os tabuleiros do adversario com 1 e 2 peças
    """
    if p == "Um":
        return len([j for j in range(s.n//2,s.n) if s.tabuleiro[j] in [1,2]])
    else:
        return len([j for j in range(s.n//2) if s.tabuleiro[j] in [1,2]])
            
Atacama0 = JogadorAlfaBeta("Atacama0", 0, h)
Atacama1 = JogadorAlfaBeta("Atacama1", 1, h)
Atacama2 = JogadorAlfaBeta("Atacama2", 2, h)
Atacama3 = JogadorAlfaBeta("Atacama3", 3, h)
Atacama4 = JogadorAlfaBeta("Atacama4", 4, h)


def hh (s, p):
    """heuristica simples que valoriza as casas que não são 1 nem 2 do nosso lado"""
    if p == "Um":
        return len([j for j in range(s.n//2) if s.tabuleiro[j] not in [1,2]])
    else:
        return len([j for j in range(s.n//2, s.n) if s.tabuleiro[j] not in [1,2]])
    
Frontispicia0 = JogadorAlfaBeta("Frontispicia0", 0, hh)
Frontispicia1 = JogadorAlfaBeta("Frontispicia1", 1, hh)
Frontispicia2 = JogadorAlfaBeta("Frontispicia2", 2, hh)
Frontispicia3 = JogadorAlfaBeta("Frontispicia3", 3, hh)
Frontispicia4 = JogadorAlfaBeta("Frontispicia4", 4, hh)


def maiscontas(s,p):
    """valoriza ter mais peças do que o adversário"""
    if p == "Um":
        return sum(s.tabuleiro[:s.n//2]) - sum(s.tabuleiro[s.n//2:])
    else:
        return sum(s.tabuleiro[s.n//2:]) - sum(s.tabuleiro[:s.n//2])

Babilonitti0 = JogadorAlfaBeta("Babilonitti0", 0, maiscontas)
Babilonitti1 = JogadorAlfaBeta("Babilonitti1", 1, maiscontas)
Babilonitti2 = JogadorAlfaBeta("Babilonitti2", 2, maiscontas)
Babilonitti3 = JogadorAlfaBeta("Babilonitti3", 3, maiscontas)
Babilonitti4 = JogadorAlfaBeta("Babilonitti4", 4, maiscontas)

    

contas_alvosatc_alvosdef1 = JogadorAlfaBeta("MaisContas++", 1,
                                            lambda s,p: 3*h(s,p)+3*hh(s,p)+maiscontas(s,p))






#### def kibir

def func_aval_1111(s,p):
    """valoriza ter mais peças do que o adversário"""
    if s.terminou():
        if p == "Um":
            if s.sacoUm>24:
                return 100
            elif s.sacoOutro >24:
                return -100
#            else:
#                return 0
        else:
            if s.sacoOutro >24:
                return 100
            elif s.sacoUm>24:
                return -100
#            else:
#                return 0
    if p == "Um":
        return sum(s.tabuleiro[:s.n//2]) - sum(s.tabuleiro[s.n//2:])
    else:
        return sum(s.tabuleiro[s.n//2:]) - sum(s.tabuleiro[:s.n//2])
def func_aval_1112(s,p):
    """valoriza ter mais peças do que o adversário"""
    if p == "Um":
        return sum(s.tabuleiro[:s.n//2]) - sum(s.tabuleiro[s.n//2:])
    else:
        return sum(s.tabuleiro[s.n//2:]) - sum(s.tabuleiro[:s.n//2])

    
jogadorOuri_kibir3 = JogadorAlfaBeta("Kibir3", 4 ,func_aval_1112)
jogadorOuri_kibir4 = JogadorAlfaBeta("Kibir4", 4 ,func_aval_1111)


######jogadores simples: humanos perguntam a jogada de entre as possíveis e Bacoco escolhe aleatóriamente 
        
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

todos_jogadores = [simplorio1, Atacama1, Atacama2,
                   Atacama3, Atacama4, Babilonitti0,
                   Babilonitti1, Babilonitti2, Babilonitti3,
                   Babilonitti4, Frontispicia0, Frontispicia1, Frontispicia2,
                   Frontispicia3, Frontispicia4, bacoco2, contas_alvosatc_alvosdef1, jogadorOuri_kibir3, jogadorOuri_kibir4]


alguns_jogadores = [Babilonitti4, Babilonitti3, Babilonitti2, jogadorOuri_kibir3, Atacama4, jogadorOuri_kibir4]


###### Para testes descomentar isto a seguir

#faz_campeonato(JogoOuri(), alguns_jogadores, 10)
vitkibir = 0
for _ in range(50):
    ((a,b),x,n)= joga11(JogoOuri(),jogadorOuri_kibir3, jogadorOuri_kibir4)
    vitkibir += n<24
    vitkibir += 0.5*(n==24)
    ((a,b),x,n)= joga11(JogoOuri(), jogadorOuri_kibir4, jogadorOuri_kibir3)
    vitkibir += n>24
    vitkibir += 0.5*(n==24)

print("kibir ganhou "+str(vitkibir)+ "de 100 jogos")


#jogo = joga11(JogoOuri(),simplorio1, simplorio2)
#mostraJogo(JogoOuri(),jogo,True,True)

##for i in range(33):
##    print("jogo", i, "-------")
##    ((a,b),c,d) = joga11(JogoOuri(), Atacama2 , bacoco2)
##    print("TERMINEI JOGO", i)
###    print("jogadas =", c, "resultado do Um= ", d)
##    print("estadofinal")
##    JogoOuri().executa(JogoOuri().initial,c).display()
##    #input()
    

#umjogo = joga11(JogoOuri(), humano1, humano2)



# CombinaÃ§Ã£o de caracterÃ­sticas
def linear_combination(state,player,weights,features):
    if weights == []:
        return 0
    else:
        return weights[0]*features[0](state,player) + linear_combination(state,player,weights[1:],features[1:])

def linear_combiner(state,player,weights,features):
    return linear_combination(state,player,weights,features)


def linear_func(weights,features):
    return lambda state, player: linear_combiner(state,player,weights,features)


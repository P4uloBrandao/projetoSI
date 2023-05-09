##Versão 2 Maio 2023

        
from random import *
import sys

##################################
# Classe Jogador 

class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun
    def display(self):
        print(self.nome+" ")


# Classe JogadorAlfaBeta 

class JogadorAlfaBeta(Jogador):
    def __init__(self, nome, depth,fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)
    def display(self):
        print(self.nome+" ")


from jogos import *

##########  para ser independente dos jogos deveria devolver um método em string ou um atributo
def joga11(game, jog1, jog2):
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve uma lista de jogadas e o resultado >25 se Um ganha <24 se Outro ganha
    estado=game.initial
    proxjog = jog1
    lista_jogadas=[]
    while not game.terminal_test(estado):
##        if len(lista_jogadas)>500: ### usado para no debug detectar ciclos infinitos
##            estado.display()       ### situações de jogo pouco prováveis mas que podem ocorrer
##            input("mais de 500 jogadas")         
        jogada = proxjog.fun(game, estado)
        estado=game.result(estado,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
        ## aqui detectamos os ciclos, guardamos estados suspeitos
        ## específico do Ouri
        ## e interrompemos o jogo se se repetirem
        if estado.souUmEstadoPequeno():
            if game.estamosEmCiclo(estado):
                estado.cicloDetectado()
            else:
                game.addEstadoPequeno(estado)
    return ((jog1.nome,jog2.nome),lista_jogadas, game.utility(estado,"Um"))

# from func_timeout import func_timeout, FunctionTimedOut

# def joga11com_timeout(game,jog1, jog2, nsec):
#     ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
#     ### devolve uma lista de jogadas e o resultado >24 se Um ganha <24 se Outro ganha
#     estado=game.initial
#     proxjog = jog1
#     lista_jogadas=[]
#     while not game.terminal_test(estado):
#         try:
#             ReturnedValue = func_timeout(nsec, proxjog.fun, args=(game, estado))
#         except FunctionTimedOut:
#             print("pim!", proxjog.nome)
#             ReturnedValue = None    
#         jogada = ReturnedValue
#         if jogada == None:
#             return ((jog1.nome,jog2.nome),lista_jogadas, -1 if proxjog==jog1 else 1)
#         else:
#             estado=game.result(estado,jogada)
#             lista_jogadas.append(jogada)
#             proxjog = jog2 if proxjog == jog1 else jog1
#             ## detecção de ciclos, específica do Ouri
#             if estado.souUmEstadoPequeno():
#                 if game.estamosEmCiclo(estado):
#                     estado.cicloDetectado()
#                 else:
#                     game.addEstadoPequeno(estado)
#     return ((jog1.nome,jog2.nome),lista_jogadas, game.utility(estado,"Um"))

def jogaNN(game, listaJog, listaAdv, nsec=1):
    ### devolve uma lista de tuplos da forma ((j1, j2), lista de jogadas, score_do_Um)
    lista_jogos=[]
    j=0
    for jog in listaJog:
        for adv in listaAdv:
            if jog != adv:
                j +=1
                res = joga11(game, jog, adv)#, nsec)
                lista_jogos.append(res)
                ((a,b),_,d) = res
                print(j,jog.nome, adv.nome,  "--vencedor="+a if d>24 else "--vencedor="+b if d<24 else "----empate")
    return lista_jogos

def jogaNNSemPrint(game, listaJog, listaAdv, nsec=1):
    ### devolve uma lista de tuplos da forma ((j1, j2), lista de jogadas, score_do_Um)
    lista_jogos=[]
    j=0
    for jog in listaJog:
        for adv in listaAdv:
            if jog != adv:
                j +=1
                res = joga11(game, jog, adv)#, nsec)
                lista_jogos.append(res)
                ((a,b),_,d) = res
    return lista_jogos

def jogaNN2(game, listaJog, listaAdv, nsec=1):
    ### devolve uma lista de tuplos da forma ((j1, j2), lista de jogadas, score_do_Um)
    lista_jogos=[]
    j=0
    contador=0
    for jog in listaJog:
        for adv in listaAdv:
            if jog != adv:
                j +=1
                res = joga11(game, jog, adv)#, nsec)
                lista_jogos.append(res)
                ((a,b),_,d) = res
                # print(j,jog.nome, adv.nome,  "--vencedor="+a if d>24 else "--vencedor="+b if d<24 else "----empate")
                if a== "Jogador56":
                    if d > 24:
                        contador+= 1
                    else:
                        contador+= 0
                elif b == "Jogardor56":
                    if d < 24:
                        contador+= 1
                    else:
                        contador+= 0
                else:
                    contador+= 0
    return contador




# -----------------  Mostra os jogos


def mostraJogo(game, logjog, verbose = False, step_by_step=False):
    (jogs,listajog,score)=logjog
    print(jogs[0],'vs',jogs[1])
    estado=game.initial
    for jog in listajog:
        if verbose:
            game.display(estado)
        if step_by_step:
            input()
        estado=game.result(estado,jog)
        if verbose:
            print()
            print("--> ", jog)
            print()
    if verbose:
        game.display(estado)
    print("Empate" if game.utility(estado,"Um") == 24 else \
          "Ganha o Um" if game.utility(estado,"Um") > 24 else "Ganha o Outro")


#### função para fazer campeonatos e construir a tabela final


######## Funções para jogar e fazer torneios
def faz_campeonato(jogo, listaJogadores, nsec=1):
    ### faz todos os jogos com timeout de nsec por jogada
    campeonato = jogaNN(jogo, listaJogadores, listaJogadores, nsec)
    ### ignora as jogadas e contabiliza quem ganhou
    resultado_jogos = [(a,b,n) for ((a,b),x,n) in campeonato]
    tabela = dict([(jog.nome, 0) for jog in listaJogadores])
    for jogo in resultado_jogos:
        if jogo[2] >24:
            tabela[jogo[0]] += 1
        elif jogo[2] < 24:
            tabela[jogo[1]] += 1
        else:
            tabela[jogo[0]] += 0.5
            tabela[jogo[1]] += 0.5
    classificacao = list(tabela.items())
    classificacao.sort(key=lambda p: -p[1])
    print("JOGADOR      ", "     PONTOS")
    for jog in classificacao:
        print('{:20}'.format(jog[0]), '{:>4}'.format(jog[1]))

def faz_campeonatoHard(jogo, listaJogadores, nsec=1):
    ### faz todos os jogos com timeout de nsec por jogada
    campeonato = jogaNNSemPrint(jogo, listaJogadores, listaJogadores, nsec)
    ### ignora as jogadas e contabiliza quem ganhou
    resultado_jogos = [(a,b,n) for ((a,b),x,n) in campeonato]
    tabela = dict([(jog.nome, 0) for jog in listaJogadores])
    for jogo in resultado_jogos:
        if jogo[2] >24:
            tabela[jogo[0]] += 1
        elif jogo[2] < 24:
            tabela[jogo[1]] += 1
        else:
            tabela[jogo[0]] += 0.5
            tabela[jogo[1]] += 0.5
    classificacao = list(tabela.items())
    classificacao.sort(key=lambda p: -p[1])
    for jog in classificacao:
        if jog[0] == "Jogador56":
            if int(jog[1])>=2:
                return 1
    return 0

    




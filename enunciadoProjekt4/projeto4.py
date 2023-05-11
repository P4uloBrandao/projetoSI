# Grupo 56
from jogar import *
from La_Ouri import *
from kibir import *


def func_aval_1111(s, p):
    """valoriza ter mais peças do que o adversário"""
    if s.terminou():
        if p == "Um":
            if s.sacoUm > 24:
                return 100
            elif s.sacoOutro > 24:
                return -100
            else:
                return 0
        else:
            if s.sacoOutro > 24:
                return 100
            elif s.sacoUm > 24:
                return -100
            else:
                return 0
    if p == "Um":
        # - sum(s.tabuleiro[s.n//2:])
        return s.sacoUm+sum(s.tabuleiro[:s.n//2])
    else:
        # - sum(s.tabuleiro[:s.n//2])
        return s.sacoOutro+sum(s.tabuleiro[s.n//2:])


def func_aval_56(s, p):

    def contaBoasJogadas(tabuleiro, p):
        contador = 0
        validator = True
        if p == "Um":
            jog = tabuleiro[:len(tabuleiro)//2]
            op = tabuleiro[len(tabuleiro)//2:]
        else:
            jog = tabuleiro[len(tabuleiro)//2:]
            op = tabuleiro[:len(tabuleiro)//2]
        for x in jog:
            if x > 1:
                validator = False
        tamJog = len(jog)
        if not validator:
            for x in range(tamJog):
                if jog[x] > 1:

                    casasAndar = int(jog[x]) % len(tabuleiro)
                    x += 1
                    if (casasAndar + x > tamJog):
                        casasAndar -= (tamJog - x)
                        casasAndar= casasAndar%(tamJog) 
                        if op[casasAndar-1] + 1 == 3 or op[casasAndar-1] + 1 == 2:
                            contador += 1
        else:
            if jog[len(jog)-1] == 1:
                if op[0]+1 == 2 or op[0]+1 == 3:
                    contador += 1
        return contador

    def contarSequencias(lista):
        contador = 0
        pontos = 0
        for i in range(len(lista)-1):
            if lista[i] == 1 or lista[i] == 2:
                if lista[i+1] == lista[i]:
                    contador += 1
                else:
                    if contador > 0:
                        pontos += contador+1
                    contador = 0
            else:
                if contador > 0:
                    pontos += contador+1
                contador = 0
        if contador > 0:
            pontos += contador+1
        return pontos / (len(lista)//2)

    if s.terminou():
        if p == "Um":
            if s.sacoUm > 24:
                return 100
            elif s.sacoOutro > 24:
                return -100
            else:
                return 0
        else:
            if s.sacoOutro > 24:
                return 100
            elif s.sacoUm > 24:
                return -100
            else:
                return 0
    if p == "Um":
        pecasJog = s.sacoUm+sum(s.tabuleiro[:s.n//2])
        contagemOp = contarSequencias(s.tabuleiro[s.n//2:]) - contarSequencias(s.tabuleiro[:s.n//2])
        pontJogadas = contaBoasJogadas(s.tabuleiro, "Um") - contaBoasJogadas(s.tabuleiro, "Outro")
    else:
        pecasJog = s.sacoOutro+sum(s.tabuleiro[s.n//2:])
        contagemOp = contarSequencias(s.tabuleiro[:s.n//2]) - contarSequencias(s.tabuleiro[s.n//2:])
        pontJogadas = contaBoasJogadas(s.tabuleiro, "Outro") - contaBoasJogadas(s.tabuleiro, "Um")

    if contagemOp<0:
        contagemOp=0
    pontuacaoJog = round((pecasJog/25)*50)
    pontuacaoJog += round((contagemOp/(s.n//2))*25)
    pontuacaoJog+= round((pontJogadas/6)*10)

    # Limita a pontuação entre 0 e 100.
    return max(0, min(100, pontuacaoJog))


jogadorOuri_56 = JogadorAlfaBeta("Jogador56", 4, func_aval_56)

jogadores = todos_jogadores + [jogadorOuri_56]
contador=0
tamanhoComp= 10
# for x in range(tamanhoComp):
#         campeonato = faz_campeonatoHard(JogoOuri(), jogadores, 1)

#         contador +=campeonato
# print(str(round((contador/tamanhoComp)*100))+"%")

# for x in range(3):
faz_campeonato(JogoOuri(), jogadores, 1)
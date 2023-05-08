# Grupo 56
from jogar import *
from La_Ouri import *

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


def func_aval_56(s, p):

    def contarSequencias(lista):
        contador = 0
        res = 0
        for i in range(len(lista)-1):
            if lista[i] == 1 or lista[i] == 2:
                if lista[i+1] == lista[i]:
                    contador += 1
                else:
                    if contador > 0:
                        res += contador+1
                    contador = 0
            else:
                if contador > 0:
                    res += contador+1
                contador = 0
        if contador > 0:
            res += contador+1
        return res

    if s.terminou():
        if p == "Um":
            return 100 if s.sacoUm > s.sacoOutro else 0
        else:
            return 100 if s.sacoOutro > s.sacoUm else 0

    # Se ainda não terminou, a pontuação é calculada com base no número de pedras no tabuleiro.
    # if p == "Um":
    #     pedras_jogador = sum(s.tabuleiro[:6])
    #     pedras_oponente = sum(s.tabuleiro[6:])
    # else:
    #     pedras_jogador = sum(s.tabuleiro[6:])
    #     pedras_oponente = sum(s.tabuleiro[:6])

    if p == "Um":
        sacoJog = s.sacoUm
        contagemOp = contarSequencias(s.tabuleiro[6:])

    else:
        sacoJog = s.sacoOutro
        contagemOp = contarSequencias(s.tabuleiro[:6])
    pontuacaoJog = round((sacoJog/25)*50)
    pontuacaoJog += round((contagemOp/6)*25)

    # Limita a pontuação entre 0 e 100.
    return max(0, min(100, pontuacaoJog))


jogadorOuri_56 = JogadorAlfaBeta("Jogador56", 4, func_aval_56)
jogadorOuri_Kibir4 = JogadorAlfaBeta("Kibir4", 4, func_aval_1111)

jogadores = [jogadorOuri_56, jogadorOuri_Kibir4]
for x in range (3):
    faz_campeonato(JogoOuri(), jogadores, 1)


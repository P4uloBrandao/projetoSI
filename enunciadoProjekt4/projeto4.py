# Grupo 56
from jogar import *
from La_Ouri import *
from jogos import *
from kibir import *
from jogadoresOuri import *

def func_aval_56(s, p):
    """
    Avalia um estado do jogo Ouri para o jogador atual.
    
    Args:
        s (EstadoOuri): O estado atual do jogo.
        p (str): O jogador atual ("Um" ou "Outro").
    
    Returns:
        A pontuação do estado, um valor entre 0 e 100.
    """
    if s.terminou():
        # Se o jogo terminou, a pontuação é baseada nos sacos de cada jogador.
        if p == "Um":
            return 100 if s.sacoUm > s.sacoOutro else 0
        else:
            return 100 if s.sacoOutro > s.sacoUm else 0
    
    # Se ainda não terminou, a pontuação é calculada com base no número de pedras no tabuleiro.
    if p == "Um":
        pedras_jogador = sum(s.tabuleiro[:6])
        pedras_oponente = sum(s.tabuleiro[6:])
    else:
        pedras_jogador = sum(s.tabuleiro[6:])
        pedras_oponente = sum(s.tabuleiro[:6])
    
    pontuacao = 50 + (pedras_jogador - pedras_oponente) * 5
    
    # Limita a pontuação entre 0 e 100.
    return max(0, min(100, pontuacao))

jogadorOuri_56 = JogadorAlfaBeta("Jogador56", 4 ,func_aval_56)
jogadorOuri_Kibir4 = JogadorAlfaBeta("Kibir4", 4 ,func_aval_1111)

jogadores = [jogadorOuri_56, jogadorOuri_Kibir4]
faz_campeonato(JogoOuri(), jogadores, 1)
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


tabuleiro = [11,9,7,5,2,2     ,1,1,1,1,1,1]
print(contaBoasJogadas(tabuleiro, "Um"))

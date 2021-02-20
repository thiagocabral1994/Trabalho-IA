from queue import LifoQueue
from copy import deepcopy

tabuleiro = [
            [1,2,3,4,5,6],
            [0,0,0,3,0,5],
            [0,0,0,0,0,0],
            [6,0,0,5,0,4],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]

labels = [
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]]
        ]

def updateLabels(labels: list, n: int, lin_col: tuple):
    # Verifica a regra da Horizontal
    for col in range(len(labels)):
        # Verifica se o número existe na mesma linha
        if n in labels[lin_col[0]][col]:
            labels[lin_col[0]][col].remove(n)

    # Verifica a regra da Vertical
    for lin in range(len(labels)):
        # Verifica se o número existe na mesma coluna
        if n in labels[lin][lin_col[1]]:
            labels[lin][lin_col[1]].remove(n)

    #Verifica a regra das diagonais principais
    if lin_col[0] == lin_col[1]:
        for i in range(6):
            if n in labels[i][i]:
                labels[i][i].remove(n)
    if lin_col[0] == 5 - lin_col[1]:
        for i in range(6):
            if n in labels[i][5 - i]:
                labels[i][5-i].remove(n)

def existe(tabuleiro: list, n: int, lin_col: tuple) -> tuple:
    """Valida se o atual estado respeita a regra do Lógica Grega

    :param tabuleiro: matriz do tabuleiro
    :type tabuleiro: list
    :param n: valor no Campo
    :type n: int
    :param lin_col: posição no tabuleiro (linha, coluna)
    :type lin_col: tuple
    :returns: tuple com a coordenada válida ou vazio
    :rtype: tuple
    """

    # Verifica a regra da Horizontal
    for col in range(len(tabuleiro)):
        # Verifica se o número existe na mesma linha
        if tabuleiro[lin_col[0]][col] == n:
            return (lin_col[0], col)

    # Verifica a regra da Vertical
    for lin in range(len(tabuleiro)):
        # Verifica se o número existe na mesma coluna
        if tabuleiro[lin][lin_col[1]] == n:
            return (lin, lin_col[1])

    #Verifica a regra das diagonais principais
    if lin_col[0] == lin_col[1]:
        for i in range(6):
            if tabuleiro[i][i] == n:
                return (i, i)
    if lin_col[0] == 5 - lin_col[1]:
        for i in range(6):
            if tabuleiro[i][5 - i] == n:
                return (i, 5 - i)

    # Retorna vazio, indicando que é uma posição válida para inserção
    return ()

def printMatrix(tabuleiro: list):
    for row in tabuleiro:
        print(row)

def checkLen(slot: tuple) -> int:
    return len(slot[1])

def initListaLabels(tabuleiro: list) -> list:
    labels = [
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]],
            [[],[],[],[],[],[]]
        ]
    # Inicializando a matriz de label
    fila = []
    for i in range(6):
        for j in range(6):
            if tabuleiro[i][j] != 0:
                labels[i][j] = []
            else:
                for value in range(1,7):
                    if existe(tabuleiro, value, (i,j)) == ():
                        labels[i][j].append(value)
                fila.append(((i,j), labels[i][j]))
    return fila


def gulosa(tabuleiro: list) -> bool:
    passos = 0
    # Declaração da Fila
    fila = LifoQueue()
    # Insere na fila o estado inicial do tabuleiro
    fila.put(deepcopy(tabuleiro))
    # Repete a busca até a fila esvaziar
    while not fila.empty():
        # Verifica se o usuário interrompeu a busca no GUI
        if not False: #Trocar self.__kill por False
            # Pega próximo elemento da fila
            tabuleiro = fila.get()
            filaLabel = initListaLabels(tabuleiro)
            filaLabel.sort(key = checkLen)
            print(filaLabel)
            print()
            if not filaLabel:
                break
            # Pega o próximo estado seguindo a estratégia
            # de controle
            pos = (filaLabel[0])[0]
            # Varre possíveis do tabuleiro
            for n in (filaLabel[0])[1]:
                # Escreve valor válido no tabuleiro
                tabuleiro[pos[0]][pos[1]] = n
                # Adiciona cópia do tabuleiro na fila
                fila.put(deepcopy(tabuleiro))
                passos += 1
        # Caso o usuário tenha interrompido a busca no GUI, 
        # esvaziar fila
        else:
            fila = LifoQueue()
            break
    printMatrix(tabuleiro)
    print(passos," estados")

gulosa(tabuleiro)
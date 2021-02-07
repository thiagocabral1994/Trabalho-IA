"""
# Classe de busca para resolução da Lógica Grega por IA
#
# Autores:
# Data: 16/01/2021
"""
import threading
import time
import queue
import copy

class Busca:

    """Classe de busca (Backtracking, Busca em Largura, ADA)

    :param tabuleiro: intância de tabuleiro (default None)
    :type tabuleiro: Tabuleiro
    :param delay: tempo de delay (default = 0.0)
    :type delay: float
    """
    def __init__(self, tabuleiro=None, delay: float = 0.0):
        self.tabuleiro = tabuleiro
        self.__delay = delay / 1000
        self.__proxPos = self.estrategia1
        self.__e = threading.Event()
        self.__kill = False
        self.__e.set()

    @property
    def proxPos(self) -> float:
        """getProxPos()"""
        return self.__proxPos

    @proxPos.setter
    def proxPos(self, proxPos):
        """getProxPos(proxPos)

        :param proxPos: função da estratégia de controle
        :type delay: function
        """
        if proxPos == 1:
            self.__proxPos = self.estrategia1
        elif proxPos == 2:
            self.__proxPos = self.estrategia2

    @property
    def delay(self) -> float:
        """getDelay()"""
        return self.__delay

    @delay.setter
    def delay(self, delay: float):
        """setDelay(delay)

        :param delay: delay em 1/1000 segundos
        :type delay: float
        """
        self.__delay = delay / 1000

    @property
    def e(self):
        """getE()"""
        return self.__e.is_set()

    @e.setter
    def e(self, set: bool):
        """e property (setter)

        :param set: status do set
        :type set: bool
        """
        if set:
            self.__e.set()
        else:
            self.__e.clear()

    @property
    def kill(self):
        """isKilled()"""
        return self.__kill

    @kill.setter
    def kill(self, kill: bool):
        """setKill(kill)

        :param kill: True ou False
        :type kill: bool
        """
        self.__kill = kill

    def solve(self, tabuleiro: list) -> bool:
        """Backtracking para botão random do painel

        :param board: matriz representativa do tabuleiro da Lógica Grega
        :type board: list
        :returns: True se solucionado, False caso contrário
        :rtype: bool
        """
        pos = self.proxPos(tabuleiro)
        if not pos:
            return True
        for n in range(1, 7):
            if not self.existe(tabuleiro, n, pos):
                tabuleiro[pos[0]][pos[1]] = n
                if self.solve(tabuleiro):
                    return True
                tabuleiro[pos[0]][pos[1]] = 0
        return False
    
    def backtracking(self) -> bool:
        """Resolve a Lógica Grega por Backtracking (AutoSolver (tabuleiro state change))

        :returns: True se solucionou e False se não possui solução
        :rtype: bool
        """
        if not self.__kill:
            # Pega próximo estado
            pos = self.proxPos(self.tabuleiro.tabuleiro)
            # Verifica se é válido
            if not pos:
                return True
            # Varre todos os 6 possíveis números
            for n in range(1, 7):
                # Verifica se o número é válido de acordo com a regra do Lógica Grega
                if not self.existe(self.tabuleiro.tabuleiro, n, pos):
                    # pausa/retoma
                    # self.__e.wait()
                    # muda o estado do tabuleiro
                    self.tabuleiro.setCampo(n, (pos[0], pos[1]))
                    self.tabuleiro.tabuleiro[pos[0]][pos[1]] = n
                    # Implementa delay
                    time.sleep(self.__delay)
                    # continua a próxima iteração
                    if self.backtracking():
                        return True
                    elif not self.__kill:
                        # pausa/retoma
                        # self.__e.wait()
                        # backtracking
                        # muda o estado do tabuleiro
                        self.tabuleiro.setCampo(0, (pos[0], pos[1]))
                        self.tabuleiro.tabuleiro[pos[0]][pos[1]] = 0
            # delay (backtracking)
            time.sleep(self.__delay)
            # retorna solução inválida
            return False

    def largura(self):
        """Resolve a Lógica Grega por Busca em Largura

        :returns: True se solucionou e False se não tem solução
        """
        fila = queue.Queue()
        fila.put(copy.deepcopy(self.tabuleiro.tabuleiro))
        while not fila.empty():
            self.tabuleiro.setTabuleiro(fila.get())
            pos = self.proxPos(self.tabuleiro.tabuleiro)
            # Verifica se é válido
            if not pos:
                continue
            # Varre possíveis valores
            for n in range(1, 7):
                # Verifica se existe
                if not self.existe(self.tabuleiro.tabuleiro, n, pos):
                    # Seta valor
                    self.tabuleiro.setCampo(n, (pos[0], pos[1]))
                    self.tabuleiro.tabuleiro[pos[0]][pos[1]] = n
                    fila.put(copy.deepcopy(self.tabuleiro.tabuleiro))
                    time.sleep(self.__delay)
        self.__e.clear()

    def gulosa(self) -> bool:
        # [INSERIR BUSCA GULOSA AQUI]
        print("Soon: Busca Gulosa")
        pass

    def ida_estrela(self) -> bool:
        # [INSERIR BUSCA IDA* AQUI]
        print("Soon: Busca IDA*")
        pass

    def estrategia1(self, tabuleiro: list) -> tuple:
        """Pega o próximo estado não mapeado da Esquerda pra Direita, Cima para Baixo.

        :param tabuleiro: matriz que representa o tabuleiro
        :type tabuleiro: list
        :returns: próximo estado não usado ou vazio
        :rtype: tuple
        """
        for lin in range(6):
            for col in range(6):
                if tabuleiro[lin][col] == 0:
                    return (lin, col)
        # Quando mapeia tudo, retorna vazio.
        return ()

    def estrategia2(self, tabuleiro: list) -> tuple:
        """Pega o próximo estado não mapeado da Direita pra Esquerda, Baixo para Cima.

        :param tabuleiro: matriz que representa o tabuleiro
        :type tabuleiro: list
        :returns: próximo estado não usado ou vazio
        :rtype: tuple
        """
        for lin in range(6):
            for col in range(6):
                if tabuleiro[5-lin][5-col] == 0:
                    return (5-lin, 5-col)
        # Quando mapeia tudo, retorna vazio.
        return ()

    def existe(self, tabuleiro: list, n: int, lin_col: tuple) -> tuple:
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

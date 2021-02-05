"""
# Classe Gerador para gerar novos boards
#
# Autores:
# Data: 16/01/2021
"""
from random import randint

# Importação local
from busca.busca import Busca

class Gerador:

    """Gerador"""
    def __init__(self):
        self.__busca = Busca()
    
    @property
    def QTD_PREENCHIDOS(self):
        """Quantidade"""
        return 11

    def gerarDefault(self) -> list:
        """Gera o estado inicial padrão
        :returns: board padrão
        :rtype: list
        """
        return [
            [1,2,3,4,5,6],
            [0,0,0,3,0,5],
            [0,0,0,0,0,0],
            [6,0,0,5,0,4],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]

    def gerarRandom(self) -> list:
        """Gera um novo board de Lógica Grega válido
        :returns: novo board
        :rtype: list
        """
        # fill random position with random value
        grid = [[0 for lin in range(6)] for col in range(6)]
        grid[randint(0, 5)][randint(0, 5)] = randint(1, 6)
        # Lista de posições randomizadas
        posRan = []
        # Marca as posições do estado inicial
        cont = 0
        while cont <= self.QTD_PREENCHIDOS:
            # Sorteia uma nova coordenada
            lin, col = randint(0, 5), randint(0, 5)
            # Verifica se já foi mapeada
            if (lin, col) not in posRan:
                posRan.append((lin, col))
                cont += 1
        # Soluciona por uma busca padrão
        self.__busca.solve(grid)
        # aplica a solução 
        grid2 = [[] for i in range(6)]
        for lin in range(6):
            for col in range(6):
                # Marca no tabuleiro novo se (lin, col) forem as coordenadas marcadas
                if (lin, col) in posRan:
                    grid2[lin].append(grid[lin][col])
                else:
                    grid2[lin].append(0)
        return grid2

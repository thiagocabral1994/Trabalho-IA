"""
# Classe Tabuleiro para a renderização do puzzle
#
# Autores:
# Data: 16/01/2021
"""
import pygame

# local import
from base.base import GUIBase
from busca.busca import Busca


class Tabuleiro(GUIBase):

    """Construtor do Tabuleiro

    :param tabuleiro: matriz com a representação da Lógica Grega
    :type tabuleiro: list
    :param tamanho: tamno em pixels (largura, altura)
    :type tamanho: tuple
    :param tela: Tela pygame
    :type tela: pygame.Surface
    """
    def __init__(self, tamanho: tuple, tabuleiro: list, tela: pygame.Surface):
        super().__init__((tamanho[1], tamanho[1], tamanho[0] - tamanho[1]), tela)
        self.__tabuleiro = tabuleiro
        self.__busca = Busca(self)
        # lista 
        self.__campos = [
            [
                Campo(
                    self.__tabuleiro[col][lin],
                    (lin, col),
                    (self.tamanho[0], self.tamanho[2]),
                    self.tela,
                    True if self.__tabuleiro[col][lin] == 0 else False,
                )
                for lin in range(6)
            ]
            for col in range(6)
        ]

    @property
    def campos(self) -> list:
        """getCampos()"""
        return self.__campos

    """Renderiza todos os campos com valor atualizado"""
    def update_campos(self):
        for lin in range(6):
            for col in range(6):
                self.__campos[lin][col].valor = self.__tabuleiro[lin][col]

    @property
    def tabuleiro(self) -> list:
        """getTabuleiro()"""
        return self.__tabuleiro

    @tabuleiro.setter
    def tabuleiro(self, tabuleiro: list):
        """setTabuleiro(list)
    
        :param tabuleiro: matriz com os valores do tabuleiro da lógica grega
        :type tabuleiro: list
        """
        self.__tabuleiro = tabuleiro
        # reinicia os campos
        self.__campos = [
            [
                Campo(
                    self.__tabuleiro[col][lin],
                    (lin, col),
                    (self.tamanho[0], self.tamanho[2]),
                    self.tela,
                    True if self.__tabuleiro[col][lin] == 0 else False,
                )
                for lin in range(6)
            ]
            for col in range(6)
        ]

    @property
    def finalizado(self):
        """Verifica se o tabuleiro foi preenchido

        :returns: True se não tiver mais campos preenchidos. False caso contrário
        :rtype: bool
        """
        return not self.__busca.nextpos(self.tabuleiro)

    def setCampo(self, valor: int, pos: tuple):
        """Define o valor novo do Campo, através de sua coordenada e o valor novo

        :param valor: novo falor
        :type valor: int
        :param pos: posição na matriz
        :type pos: tuple
        """
        self.__campos[pos[0]][pos[1]].valor = valor

    def desenhar(self):
        """Desenha o tabuleiro na tela"""
        # Renderiza os 36 campos
        for lin in range(6):
            # iterate over all columns
            for col in range(6):
                # desenhar Campo valor
                self.__campos[col][lin].desenhar()

        # Renderiza o grid
        # Define o tamanho do espacamento entre campos
        espaco = self.tamanho[0] // 6
        # Desenha 7 linhas na Horizontal e Vertical
        for r in range(7):
            # Peso da linha
            peso = 1
            # Desenho na Horizontal (tela, (cor), (pos_inicial), (pos_final), tam_linha)
            pygame.draw.line(
                self.tela,
                (128,128,128),
                (self.tamanho[2], r * espaco),
                (self.tamanho[0] + self.tamanho[2], r * espaco),
                peso,
            )
            # Desenho na Vertical (tela, (cor), (pos_inicial), (pos_final), tam_linha)
            pygame.draw.line(
                self.tela,
                (128,128,128),
                (r * espaco + self.tamanho[2], 0),
                (r * espaco + self.tamanho[2], self.tamanho[1]),
                peso,
            )

class Campo(GUIBase):

    """Quadrado do tabulerio 6x6

    :param valor: valor preenchido no campo
    :type valor: int
    :param pos: posição no tabuleiro (lin, col)
    :type pos: tuple
    :param largura: largura da tela e offset à esquerda (largura, offset)
    :type largura: tuple
    :param tela: Tela pygame
    :type tela: pygame.Surface
    :param alteravel: é um campo de estado inicial?
    :type alteravel: bool
    """
    def __init__(
        self,
        valor: int,
        pos: tuple,
        pos_largura: tuple,
        tela: pygame.Surface,
        alteravel: bool,
    ):
        super().__init__(0, tela)
        self.__valor = valor
        self.__pos = pos
        self.__pos_largura = pos_largura
        self.__alteravel = alteravel

    @property
    def alteravel(self):
        """isAlteravel()"""
        return self.__alteravel

    @property
    def valor(self) -> int:
        """getValor()"""
        return self.__valor

    @valor.setter
    def valor(self, valor: int):
        """setValor(valor)

        :param valor: valor a ser inserido
        :type valor: int
        """
        if self.__alteravel:
            self.__valor = valor

    def desenhar(self):
        """Desenha o Campo"""
        # Define o espaco dividido entre os campos
        espaco = self.__pos_largura[0] // 6
        # Define a posição real na tela
        lin, col = self.__pos[0] * espaco + self.__pos_largura[1], self.__pos[1] * espaco
        # Colore campos
        sqtamanho = self.__pos_largura[0] // 6
        if not self.__alteravel:
            rgb = (240, 248, 255)
        else:
            rgb = (255, 255, 255)
        pygame.draw.rect(self.tela, rgb, ((lin, col), (sqtamanho, sqtamanho)))
            
        # Verifica se o campo já possui algum valor
        if self.__valor != 0:
            fonte = pygame.font.Font("./assets/Rubik-font/seguisym.ttf", 38)
            # Cria objeto
            letra_grega = ""
            rgb = (128,128,128)
            if self.__valor == 1:
                letra_grega = "\u03A3"
                rgb = (255, 65, 54)
            elif self.__valor == 2:
                letra_grega = "\u039E"
                rgb = (177, 13, 201)
            elif self.__valor == 3:
                letra_grega = "\u039B"
                rgb = (255, 220, 0)
            elif self.__valor == 4:
                letra_grega = "\u03A9"
                rgb = (133, 20, 75)
            elif self.__valor == 5:
                letra_grega = "\u03F4"
                rgb = (17, 17, 17)
            elif self.__valor == 6:
                letra_grega = "\u03C8"
                rgb = (127, 219, 255)
            v = fonte.render(letra_grega, 1, rgb)
            # Desenha na tela
            self.tela.blit(
                v,
                (
                    int(lin + ((espaco / 2) - (v.get_width() / 2))),
                    int(col + ((espaco / 2) - (v.get_height() / 2))),
                ),
            )

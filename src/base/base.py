"""
# Classe base para renderização do GUI (Graphic User Interface)
#
# Autores:
# Data: 16/01/2021
"""
import pygame

class GUIBase:

    """Construtor do GUIBase
    :param tamanho: dimensões da tela
    :type tamanho: tuple
    :param tela: janela pygame
    :type tela: pygame.Surface
    """
    def __init__(self, tamanho: tuple, tela: pygame.Surface):
        self.__tamanho = tamanho
        self.__tela = tela

    @property
    def tamanho(self):
        """getTamanho()"""
        return self.__tamanho

    @property
    def tela(self):
        """getTela()"""
        return self.__tela

    def draw(self):
        """Desenhar"""
        pass

    def _type(self, txt: str, rgb: tuple, pos: tuple, tamFonte: int):
        """Escreve uma string na tela

        :param txt: texto a ser desenhado
        :type txt: str
        :param rgb: cor do texto
        :type rgb: tuple
        :param pos: posição do desenho
        :type pos: tuple
        :param tamFonte: tamanho da fonte
        :type tamFonte: int
        """
        # cria uma fonte
        font = pygame.font.Font("./assets/Rubik-font/DalekPinpointBold.ttf", tamFonte)
        # renderiza a fonte com um texto
        v = font.render(txt, 1, rgb)
        # escreve na tela
        self.__tela.blit(v, pos)
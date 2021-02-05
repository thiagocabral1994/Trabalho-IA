# -*- coding: UTF-8 -*-
"""
# Classe Principal do Trabalho
#
# Autores:
# Data: 16/01/2021
"""
import pygame

from gui.gui import GUI

if __name__ == "__main__":
    # Inicia as importações dos módulos do pygame
    pygame.init()
    # Inicia o loop do GUI
    gui = GUI()
    gui.loop()
    # Finaliza todos os módulos do pygame
    pygame.quit()

"""
# Classe GUI para Lógica Grega
#
# Autores:
# Data: 16/01/2021
"""
import pygame, time

# Importações locais
from models.tabuleiro import Tabuleiro
from models.painel_lateral import PainelLateral
from busca.busca import Busca
from generator.gerador import Gerador


class GUI:

    """Construtor do GUI"""
    def __init__(self):
        # Define o tamanho da janela
        self.__tamanho_tela = (750, 540)
        self.__tela = pygame.display.set_mode(self.__tamanho_tela[:2])

        # Ícone
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
        self.__gerador = Gerador()
        self.__tabuleiro = self.__gerador.gerarDefault()

        # Cria o tabuleiro
        self.__tabuleiro_model = Tabuleiro(self.__tamanho_tela, self.__tabuleiro, self.__tela)

        # Cria o objeto Busca
        self.__busca = Busca(self.__tabuleiro_model, 250)

        # Cria o painel
        self.__painel_lateral = PainelLateral(self.__busca, self.__tamanho_tela, self.__tela)

        # Título da janela
        pygame.display.set_caption("Lógica Grega")

    """Recarrega a tela atualizada"""
    def __refresh(self):
        # define o plano de fundo como preto
        self.__tela.fill((240, 248, 255))
        # recarrega o quadro
        self.__tabuleiro_model.desenhar()
        # recarrega painel lateral
        self.__painel_lateral.desenhar()
        # atualiza tela
        pygame.display.update()
        # reseta o estilo dos botões
        # reseta os botões de busca
        for b in self.__painel_lateral.auto_busca.botoes:
            b.reset
        # reseta os botões de opção
        for b in self.__painel_lateral.opcoes.botoes:
            b.reset

    """Loop do Pygame"""
    def loop(self):
        jump_mode = False
        # loop principal
        while True:
            # evento
            for e in pygame.event.get():
                # fechar janela
                if e.type == pygame.QUIT:
                    return
                # evento em clicar nos botões
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.__auto_busca_botoes_mouse()
                    self.__opcoes_botoes_mouse()
            # atualiza tela
            self.__refresh()

    """Eventos de busca"""
    def __auto_busca_botoes_mouse(self):
        # Pos mouse
        p = pygame.mouse.get_pos()
        for b in self.__painel_lateral.auto_busca.botoes:
            # verifica se está no range do botão
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                # chama evento de click
                self.__painel_lateral.auto_busca.mark(b)
                b.click()

    """Eventos de opcoes"""
    def __opcoes_botoes_mouse(self):
        p = pygame.mouse.get_pos()
        s = True
        for b in self.__painel_lateral.opcoes.botoes:
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                if b.label_botao == "random" or b.label_botao == "default":
                    s = b.click((self.__tabuleiro_model,))
                else:
                    s = b.click()
        if not s:
            print("Puzzle Impossível")

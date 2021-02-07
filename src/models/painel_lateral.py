"""
# Classe Painel Lateral com as opções de menu
#
# Autores:
# Data: 16/01/2021
"""
import pygame, time

# importação local
from base.base import GUIBase
from busca.threads import Threads
from generator.gerador import Gerador

class PainelLateral(GUIBase):

    """Painel Lateral

    :param busca: objeto de busca
    :type busca: Busca
    :param tamanho: tela tamanho (width height)
    :type tamanho: tuple
    :param tela: pygame tela
    :type tela: pygame.Surface
    """
    def __init__(self, busca, tamanho: tuple, tela: pygame.Surface):
        super().__init__((tamanho[0] - tamanho[1], tamanho[1]), tela)
        self.auto_busca = AutoBusca(busca, self.tamanho, self.tela)
        self.opcoes = Opcoes(busca, self.tamanho, self.tela)

    def desenhar(self):
        """desenhar the left panel on the tela"""
        w = 3
        # desenhar retângulo (quadro)
        pygame.draw.rect(
            self.tela, (128,128,128), ((0, 0), (self.tamanho[0], self.tamanho[1])), w
        )
        # print Lógica Grega
        pygame.draw.rect(
            self.tela,
            (128,128,128),
            ((0, 0), (self.tamanho[0], self.tamanho[1] // 9)),
            w // 3,
        )
        self._type("Lógica Grega", (128, 128, 128), (14, 14), 30)
        # desenhar auto solver control panel
        self.auto_busca.desenhar()
        # desenhar option panel (solve, select, reset, generate)
        self.opcoes.desenhar()


class AutoBusca(GUIBase):

    """Painel de controle para opções de busca

    :param busca: objeto de busca
    :type busca: Busca
    :param tamanho: tamanho da tela (largura, altura)
    :type tamanho: tuple
    :param tela: Tela pygame
    :type tela: pygame.Surface
    """
    def __init__(self, busca, tamanho: tuple, tela: pygame.Surface):
        super().__init__((tamanho[0], tamanho[1] // 6), tela)
        self.__threads = Threads()
        self.__busca = busca

        # Cria os botões de controle
        tamanhoControle = (self.tamanho[0] - self.tamanho[0] // 2 - 35, self.tamanho[1] // 3)
        self.__botoes = [
            Botao(*i, tamanhoControle, self.tela)
            for i in (
                #(self.iniciar_backtracking, (), (-14, 8), "backtracking", 10, (30, 120)),
                (self.iniciar_largura, (), (-11, 4), "largura", 16, (30, 120)),
                (self.iniciar_gulosa, (), (-8, 4), "gulosa", 16, (110, 120)),
                (self.iniciar_IDA_estrela, (), (5, 4), "IDA*", 16, (30, 170)),
                (self.parar, (), (-2, 4), "parar", 16, (110, 170)),
            )
        ]
        # Criar botões de delay
        delayTamanho = (self.tamanho[0] - self.tamanho[0] // 2 - 45, self.tamanho[1] // 4)
        self.__botoes.extend(
            [
                Botao(*i, delayTamanho, self.tela, 1)
                for i in (
                    (self.set_delay, (1000), (5, 0), "1.0", 16, (40, 245)),
                    (self.set_delay, (500), (5, 0), "0.5", 16, (40, 273)),
                    (self.set_delay, (750), (0, 0), "0.75", 16, (115, 245)),
                    (self.set_delay, (250), (0, 0), "0.25", 16, (115, 273)),
                    (self.set_delay, (100), (0, 0), "0.10", 16, (40, 301)),
                    (self.set_delay, (0.000000001), (10, 0), "0", 16, (115, 301)),
                )
            ]
        )
        for botao in self.botoes:
            if botao.label_botao == "0.25":
                botao.marked = True
                break
        self.__ultimo_delay = 250

    @property
    def delay(self) -> float:
        """getDelay()"""
        return self.__busca.delay

    def set_delay(self, valor: float):
        """delay property (setter)

        :param valor: delay
        :type valor: float
        """
        self.__ultimo_delay = valor
        self.__busca.delay = valor

    @property
    def botoes(self):
        """getBotoes()"""   
        return self.__botoes

    def iniciar(self, func):
        """Mata as buscas a ser realizada"""
        self.parar()
        self.__busca.delay = self.__ultimo_delay
        self.reiniciar()

        """Inicia algoritmo de busca"""
        self.__busca.kill = False
        self.__busca.e = True
        self.__threads.start(func)


    def iniciar_backtracking(self):
        """Busca BackTracking"""
        self.iniciar(self.__busca.backtracking)
    
    def iniciar_largura(self):
        """Busca BackTracking"""
        self.iniciar(self.__busca.largura)

    def iniciar_gulosa(self):
        """Busca BackTracking"""
        self.iniciar(self.__busca.gulosa)

    def iniciar_IDA_estrela(self):
        """Busca BackTracking"""
        self.iniciar(self.__busca.ida_estrela)

    def parar(self):
        """Mata a busca a ser realizada"""
        self.__busca.delay = 0
        self.__busca.kill = True
        self.__busca.e = False
        self.__threads.parar()
    
    def reiniciar(self) -> bool:
        """Limpa o tabuleiro para o último estado inicial gerado"""
        for lin in range(6):
            for col in range(6):
                if self.__busca.tabuleiro.campos[lin][col].alteravel:
                    # Reseta todos os alteráveis para 0
                    self.__busca.tabuleiro.tabuleiro[lin][col] = 0
        # update squares
        self.__busca.tabuleiro.update_campos()
        return True

    def mark(self, b):
        """Evento de marcação no clique

        :param args: botao a ser marcado
        :type args: Botao
        """
        for botao in self.botoes:
            if botao == b:
                pass
            elif botao.grupo == b.grupo:
                botao.marked = False
        b.marked = True

    def desenhar(self):
        """Renderizar o campo de busca"""
        # Desenhar o quadro principal
        # Definir grossura da linha
        peso = 1
        # Desenhar quadro
        pygame.draw.rect(
            self.tela,
            (128, 128, 128),
            ((0, 0), (self.tamanho[0], 350)),
            #((0, self.tamanho[1] * 2), (self.tamanho[0], self.tamanho[1] * 3)),
            peso,
        )
        # Definir Título do Quadro
        self._type(
            "Algoritmo de Busca",
            (128, 128, 128),
            (5, 75),
            #(self.tamanho[0] // 6 + 10, self.tamanho[1] * 2.15),
            21,
        )
        # Definir Título das opções de delay
        self._type(
            "Delay (segundos)", (128, 128, 128), 
            (35, 210),
            #(self.tamanho[0] // 3, self.tamanho[1] * 4), 
            18
        )
        # Desenhar os botões
        for b in self.__botoes:
            b.desenhar()

class Opcoes(GUIBase):

    """Classe opcoes

    :param busca: objeto de busca
    :type busca: Busca
    :param tamanho: tamanho da tela (largura, altura)
    :type tamanho: tuple
    :param tela: tela pygame
    :type tela: pygame.Surface
    """

    def __init__(self, busca, tamanho: tuple, tela: pygame.Surface):
        super().__init__((tamanho[0], tamanho[1] // 6), tela)
        self.__busca = busca
        self.__gerador = Gerador()
        # Cria os botões
        tamanhoOpcoes = (self.tamanho[0] - self.tamanho[0] // 2 - 35, self.tamanho[1] // 3)
        self.__botoes = [
            Botao(*i, tamanhoOpcoes, self.tela)
            for i in (
                (self.reiniciar, (), (0, 4), "reset", 16, (30, 400)),
                (self.gerarNovo, (), (-10, 4), "random", 16, (110, 400)),
                (self.gerarDefault, (), (-8, 4), "default", 16, (30, 450))
            )
        ]

        self.__botoes.extend(
            [
                Botao(*i, tamanhoOpcoes, self.tela, 1)
                for i in (
                    (self.setStrat1, (), (-8, 4), "strat 1", 16, (30, 500)),
                    (self.setStrat2, (), (-8, 4), "strat 2", 16, (110, 500))
                )
            ]
        )
        for botao in self.botoes:
            if botao.label_botao == "strat 1":
                botao.marked = True
                break

    @property
    def botoes(self):
        """getBotoes()"""
        return self.__botoes

    def gerarNovo(self, tabuleiro: list) -> bool:
        """Gera um estado inicial novo e randomizado

        :param tabuleiro: tabuleiro de lógica grega
        :type tabuleiro: list
        """
        tabuleiro.tabuleiro = self.__gerador.gerarRandom()
        return True

    def gerarDefault(self, tabuleiro: list) -> bool:
        """Gera um estado inicial novo e randomizado

        :param tabuleiro: tabuleiro de lógica grega
        :type tabuleiro: list
        """
        tabuleiro.tabuleiro = self.__gerador.gerarDefault()
        return True

    def reiniciar(self) -> bool:
        """Limpa o tabuleiro para o último estado inicial gerado"""
        for lin in range(6):
            for col in range(6):
                if self.__busca.tabuleiro.campos[lin][col].alteravel:
                    # Reseta todos os alteráveis para 0
                    self.__busca.tabuleiro.tabuleiro[lin][col] = 0
        # update squares
        self.__busca.tabuleiro.update_campos()
        return True
    
    def setStrat1(self) -> bool:
        if not self.__busca.e: 
            self.mark(self.botoes[3])
            self.__busca.proxPos = 1
            return True
        return False

    def setStrat2(self) -> bool:
        if not self.__busca.e: 
            self.__busca.proxPos = 2
            self.mark(self.botoes[4])
            return True
        return False
    
    def mark(self, b):
        """Evento de marcação no clique

        :param args: botao a ser marcado
        :type args: Botao
        """
        for botao in self.botoes:
            if botao == b:
                pass
            elif botao.grupo == b.grupo:
                botao.marked = False
        b.marked = True

    def desenhar(self):
        """Desenhar quadro de opções"""
        # Título
        self._type("Opções", (128, 128, 128), (70, 355), 22)
        # desenhar botoes
        for b in self.__botoes:
            b.desenhar()


class Botao(GUIBase):

    """Classe de criação de Botão

    :param alvo: função alvo que será iniciada com o clique
    :type alvo: function
    :param _args: argumentos da função
    :type _args: tuple
    :param s: offset (esquerda, topo)
    :type s: tuple
    :param label_botao: texto do botão
    :type label_botao: str
    :param tamanhoFonte: tamanho do label_botao
    :type tamanhoFonte: int
    :param pos: posição (lin, col)
    :type pos: tuple
    :param tamanho: tamanho da tela (largura, altura)
    :type tamanho: tuple
    :param tela: tela pygame
    :type tela: pygame.Surface
    """
    def __init__(
        self,
        alvo,
        _args: tuple,
        s: tuple,
        label_botao: str,
        tamanhoFonte: int,
        pos: tuple,
        tamanho: tuple,
        tela: pygame.Surface,
        grupo: int = 0
    ):
        super().__init__(tamanho, tela)
        self.__pos = pos
        self.__label_botao = label_botao
        self.__tamanhoFonte = tamanhoFonte
        self.__alvo = alvo
        self.__args = _args
        self.__preenchimento = (0, 0, 0)
        self.__marked = False
        self.__peso = 1
        self.__s = s
        self.__grupo = grupo
        self.__click_range = (
            range(self.__pos[0], self.__pos[0] + self.tamanho[0] + 1),
            range(self.__pos[1], self.__pos[1] + self.tamanho[1] + 1),
        )

    @property
    def label_botao(self):    
        """getLabelBotao()"""
        return self.__label_botao

    @property
    def marked(self):    
        """isMarked()"""
        return self.__marked

    @marked.setter
    def marked(self, valor: bool):    
        """setMarked(valor)"""
        self.__marked = valor

    @property
    def grupo(self):    
        """getGrupo()"""
        return self.__grupo

    @grupo.setter
    def grupo(self, valor: int):    
        """setGrupo(valor)"""
        self.__grupo = valor

    @property
    def click_range(self):
        """getClickRange()"""
        return self.__click_range

    @property
    def reset(self):
        """Reseta o estilo do botão"""
        self.__preenchimento = (0, 0, 0)
        self.__peso = 1

    def click(self, args: tuple = ()):
        """Evento do clique

        :param args: argumentos da função alvo caso não sejam constantes
        :type args: tuple
        """
        self.__preenchimento = (0, 0, 0)
        self.__peso = 4

        # chamar alvo
        if self.__args:
            return self.__alvo(self.__args)
        elif args:
            return self.__alvo(*args)
        else:
            return self.__alvo()

    def desenhar(self):
        """Renderiza o botão"""
        if self.__marked:
            rgb = (20,20,0)
        else:
            rgb = (128,128,128)
        self._desenhar(rgb)
    
    def _desenhar(self, rgb: tuple):
        """Renderiza o botão"""
        # Desenha o quadro principal
        pygame.draw.rect(
            self.tela,
            rgb,
            (self.__pos, self.tamanho),
            self.__peso,
        )

        # Constrói o texto do label do botão
        self._type(
            self.__label_botao,
            rgb,
            (
                self.__pos[0] + self.tamanho[0] // 4 + self.__s[0],
                self.__pos[1] + self.tamanho[1] // 8 + self.__s[1],
            ),
            self.__tamanhoFonte,
        )

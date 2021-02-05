"""
# Classe Threads para implementação de pararelismo
#
# Autores:
# Data: 16/01/2021
"""
from threading import Thread, ThreadError

class Threads:

    """Construtor"""
    def __init__(self):
        self.__threads = []

    """Inicia uma nova Thread

    :param function: função a ser paralelizada
    :type func: function
    :param _args_: argumentos da função (default => [])
    :type _args_: list (opcional)
    :returns: True se a Thread foi iniciada. False, caso contrário.
    :rtype: bool
    """
    def start(self, func, _args_: list = []) -> bool:
        try:
            processo = Thread(target=func, args=_args_, daemon=True)
            processo.start()
            # Adiciona nova thread à lista de threads
            self.__threads.append(processo)
            return True
        except (ThreadError, RuntimeError) as threadStartEX:
            try:
                # interrompe
                processo.join()
            except RuntimeError:
                pass
            print(f"Erro: {threadStartEX}")
            return False

    """Interrompe todas as Threads da lista
    :returns: True se todas as threads foram interrompidas. False, caso contrário.
    :rtype: bool
    """
    def parar(self) -> bool:
        try:
            for thread in self.__threads:
                thread.join(1)
            self.__threads.clear()
            return True
        except (ThreadError, RuntimeError) as threadStopEX:
            print(f"Erro: {threadStopEX}")
            return False

    """Interrompe todas as Threads da lista e espera a finalização
    :returns: True se todas as threads foram interrompidas. False, caso contrário.
    :rtype: bool
    """
    def esperar(self) -> bool:
        try:
            for thread in self.__threads:
                thread.join()
            self.__threads.clear()
            return True
        except (ThreadError, RuntimeError) as threadStopEX:
            print(f"Erro: {threadStopEX}")
            return False

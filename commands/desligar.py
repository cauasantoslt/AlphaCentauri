# commands/desligar.py
import sys
from utils import falar

# Palavras-chave que ativam este comando
KEYWORDS = ("desligar", "encerrar", "fechar programa", "tchau")

def execute(comando=None):
    """
    Encerra a execução do Alpha Centauri.
    """
    falar("Desligando. Até a próxima.")
    
    # sys.exit() termina o programa principal de forma limpa.
    sys.exit()
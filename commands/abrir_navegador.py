# commands/abrir_navegador.py
import webbrowser

# Palavras-chave que ativam este comando
KEYWORDS = ("navegador", "google", "chrome")

def execute(comando=None):
    """
    Abre o navegador padrão na página do Google.
    """
    print("   [AÇÃO] Abrindo o navegador...")
    webbrowser.open("https://www.google.com")
    
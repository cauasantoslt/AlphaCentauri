# commands/abrir_bloco_de_notas.py
import subprocess
import time
import pyautogui
import pygetwindow as gw

# Palavras-chave que ativam este comando
KEYWORDS = ("bloco de notas",)

def execute(comando=None):
    """
    Abre o Bloco de Notas e digita uma mensagem.
    """
    print("   [AÇÃO] Abrindo o Bloco de Notas...")
    try:
        subprocess.Popen(['notepad.exe'])
        time.sleep(1)
        
        window_title_pt = "Sem título - Bloco de Notas"
        window_title_en = "Untitled - Notepad"
        
        notepad_window = gw.getWindowsWithTitle(window_title_pt) or gw.getWindowsWithTitle(window_title_en)
        
        if notepad_window:
            notepad_window[0].activate()
            pyautogui.write("Alpha Centauri 2.0 no controle!", interval=0.05)
        else:
            print("   (Aviso) Não foi possível encontrar a janela do Bloco de Notas para digitar.")
            
    except FileNotFoundError:
        print("   -> ERRO: 'notepad.exe' não encontrado.")
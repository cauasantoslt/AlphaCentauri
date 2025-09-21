# main.py (Versão Final 4.0 - Arquitetura Corrigida)
import os
import importlib
import json
import sys
from dotenv import load_dotenv
from utils import falar, ouvir_comando

# --- CONFIGURAÇÃO ---
load_dotenv()
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
if GOOGLE_CREDENTIALS_PATH and os.path.exists(GOOGLE_CREDENTIALS_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH
else:
    print("AVISO: Credenciais do Google Speech-to-Text não encontradas.")

command_registry = {}

def load_commands():
    print("A mapear comandos...")
    command_files = os.listdir('commands')
    for file in command_files:
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            try:
                module = importlib.import_module(f'commands.{module_name}')
                if hasattr(module, 'KEYWORDS') and hasattr(module, 'execute'):
                    for keyword in module.KEYWORDS:
                        command_registry[keyword] = module.execute
            except Exception as e:
                print(f"  -> ERRO ao carregar o comando '{module_name}': {e}")
    try:
        with open('learned_commands.json', 'r', encoding='utf-8') as f:
            learned_commands = json.load(f)
            for command_data in learned_commands.values():
                keywords, code_str = command_data['keywords'], command_data['code']
                def create_executable_function(code_to_execute):
                    def executable(comando=None): exec(code_to_execute)
                    return executable
                for keyword in keywords:
                    command_registry[keyword] = create_executable_function(code_str)
    except FileNotFoundError: pass

def main():
    load_commands()
    falar("Alpha Centauri online. Todos os sistemas operacionais.")
    
    while True:
        comando = ouvir_comando()

        if comando:
            # --- LÓGICA DE ENCERRAMENTO CORRETA ---
            # Verificamos primeiro se o comando é para desligar.
            palavras_de_saida = ["desligar", "encerrar", "fechar programa", "tchau"]
            if any(palavra in comando for palavra in palavras_de_saida):
                falar("A desligar. Até a próxima.")
                break # Quebra o loop 'while' e encerra o programa de forma limpa.

            # Se não for para desligar, procura por outros comandos.
            comando_executado = False
            for keyword, action_function in command_registry.items():
                if keyword in comando:
                    action_function(comando)
                    comando_executado = True
                    break
            
            if not comando_executado:
                # O fallback para conversa pode ser adicionado aqui se quisermos
                falar("Desculpe, não reconheci este comando.")

if __name__ == "__main__":
    main()
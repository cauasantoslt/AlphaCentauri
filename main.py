# main.py (Com Inteligência Social de Fallback - v2.9)
import os
import importlib
import json
import sys
from dotenv import load_dotenv
from utils import falar, ouvir_comando
import google.generativeai as genai # Importamos o Gemini aqui também

# --- CONFIGURAÇÃO (continua a mesma) ---
load_dotenv()
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
if GOOGLE_CREDENTIALS_PATH and os.path.exists(GOOGLE_CREDENTIALS_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH
else:
    print("AVISO: Credenciais do Google Speech-to-Text não encontradas.")

# Configuração do Gemini (necessária para o fallback)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

command_registry = {}

def load_commands():
    # ... (esta função não muda)
    print("Carregando comandos nativos...")
    command_files = os.listdir('commands')
    for file in command_files:
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            try:
                module = importlib.import_module(f'commands.{module_name}')
                if hasattr(module, 'KEYWORDS') and hasattr(module, 'execute'):
                    for keyword in module.KEYWORDS:
                        command_registry[keyword] = module.execute
            except Exception: pass
    print("Carregando comandos aprendidos...")
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

# --- NOVA FUNÇÃO DE FALLBACK ---
def handle_fallback(comando):
    """
    Se nenhum comando for encontrado, esta função é chamada para
    tentar gerar uma resposta conversacional.
    """
    print("[Fallback] Nenhum comando encontrado. Verificando se é uma conversa...")
    if not GEMINI_API_KEY:
        return "Desculpe, não reconheci este comando."
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        Você é o Alpha Centauri, um assistente de IA. O usuário disse algo que não corresponde a um comando programado.
        Analise a frase do usuário: '{comando}'.
        Se for um agradecimento, um cumprimento, uma despedida ou uma pergunta simples, forneça uma resposta curta, amigável e apropriada.
        Se parecer um comando que você simplesmente não entende ou uma frase sem sentido, responda com a palavra exata 'UNKNOWN'.
        """
        response = model.generate_content(prompt)
        
        if "UNKNOWN" in response.text:
            return "Desculpe, não reconheci este comando."
        else:
            return response.text # Retorna a resposta amigável do Gemini
            
    except Exception as e:
        print(f"   [ERRO Fallback] {e}")
        return "Desculpe, não reconheci este comando."

def main():
    load_commands()
    mensagem_inicial = "Alpha Centauri finalizado e com inteligência social. Como posso ajudar?"
    falar(mensagem_inicial)
    
    while True:
        comando = ouvir_comando()
        if comando:
            comando_executado = False
            for keyword, action_function in command_registry.items():
                if keyword in comando:
                    action_function(comando)
                    comando_executado = True
                    break
            
            # --- LÓGICA DE FALLBACK ATUALIZADA ---
            if not comando_executado:
                resposta_fallback = handle_fallback(comando)
                falar(resposta_fallback)

if __name__ == "__main__":
    main()
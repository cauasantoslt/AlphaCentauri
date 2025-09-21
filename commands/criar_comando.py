# commands/criar_comando.py (Com execução automática)
import subprocess
import os
import sys
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURAÇÃO SEGURA DA API ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERRO CRÍTICO: 'GEMINI_API_KEY' não encontrada no .env")
else:
    genai.configure(api_key=GEMINI_API_KEY)

KEYWORDS = ("crie um comando", "escreva um script", "gere um código", "faça um script")

def gerar_codigo_com_ia_real(pedido_do_usuario):
    # (Esta função permanece a mesma da versão anterior)
    if not GEMINI_API_KEY:
        return "ERRO: A chave da API do Gemini não está configurada."
    print(f"   [IA Gemini] Enviando pedido para a API do Google: '{pedido_do_usuario}'")
    prompt_completo = f"""
    Você é um assistente de automação especialista em Python para Windows.
    Sua tarefa é converter o seguinte pedido do usuário em um único e autônomo script Python.
    Gere apenas o código Python puro. Não adicione explicações, comentários desnecessários, 
    nem ```python no início ou ``` no final.
    Use bibliotecas que já vêm com o Python ou que são comumente usadas para automação no Windows, 
    como 'os', 'subprocess', 'webbrowser', 'pyautogui', 'pygetwindow', 'pycaw', 'shutil'.
    O código deve ser funcional e direto ao ponto.

    Pedido do usuário: "{pedido_do_usuario}"
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt_completo, safety_settings={'HATE': 'BLOCK_NONE','HARASSMENT': 'BLOCK_NONE','SEXUAL': 'BLOCK_NONE','DANGEROUS': 'BLOCK_NONE'})
        codigo_gerado = response.text.strip()
        if codigo_gerado.startswith("```python"): codigo_gerado = codigo_gerado[9:]
        if codigo_gerado.endswith("```"): codigo_gerado = codigo_gerado[:-3]
        return codigo_gerado.strip()
    except Exception as e:
        print(f"   [ERRO DE API] Não foi possível conectar com o Google Gemini: {e}")
        return None

# --- A FUNÇÃO EXECUTE FOI ATUALIZADA ---
def execute(comando_completo):
    pedido = ""
    for kw in KEYWORDS:
        if kw in comando_completo:
            pedido = comando_completo.split(kw, 1)[1].strip()
            break
    if not pedido:
        print("   [ERRO] Não entendi o que você quer que eu crie.")
        return
    
    codigo_gerado = gerar_codigo_com_ia_real(pedido)
    if codigo_gerado is None or "ERRO:" in codigo_gerado:
        print(f"   [IA] Desculpe, não foi possível gerar um código para isso. ({codigo_gerado})")
        return

    print("-" * 50)
    print("   [IA] O seguinte script foi gerado e será executado:")
    print(codigo_gerado)
    print("-" * 50)

    try:
        # --- MUDANÇA PRINCIPAL: A EXECUÇÃO AGORA É AUTOMÁTICA ---
        temp_script_path = "temp_generated_command.py"
        with open(temp_script_path, "w", encoding="utf-8") as f:
            f.write(codigo_gerado)
        print("   [EXECUÇÃO] Executando o script gerado...")
        subprocess.run([sys.executable, temp_script_path], check=True)
        os.remove(temp_script_path)
        
        # O mecanismo de aprendizado continua perguntando, pois é uma ação de salvamento.
        print("-" * 50)
        salvar = input("   Você gostaria de salvar este script como um novo comando permanente? (s/n): ").lower()
        if salvar == 's' or salvar == 'sim':
            keywords_str = input("   Ótimo! Quais palavras-chave devem ativar este comando? (separe por vírgula): ")
            keywords_list = [kw.strip() for kw in keywords_str.split(',')]
            command_name = input("   Qual nome único devemos dar a este comando? (ex: diminuir_volume): ")
            try:
                with open('learned_commands.json', 'r', encoding='utf-8') as f:
                    learned_commands = json.load(f)
            except FileNotFoundError:
                learned_commands = {}
            learned_commands[command_name] = {"keywords": keywords_list, "code": codigo_gerado.strip()}
            with open('learned_commands.json', 'w', encoding='utf-8') as f:
                json.dump(learned_commands, f, indent=4, ensure_ascii=False)
            print(f"   [APRENDIZADO] Comando '{command_name}' salvo com sucesso na memória!")
            print("   Para usá-lo, reinicie o Alpha Centauri.")
    except Exception as e:
        print(f"   [ERRO] Ocorreu um erro durante a execução ou salvamento: {e}")
# commands/conversar.py (Versão 2.1 - Com Saída Robusta)

from utils import falar, ouvir_comando
import google.generativeai as genai
import os

KEYWORDS = ("vamos conversar", "converse comigo", "modo chat", "bater papo")

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def obter_resposta_conversacional(conversa):
    if not GEMINI_API_KEY:
        return "Desculpe, a minha chave de API do Gemini não está configurada."
    
    prompt_do_sistema = """
    Você é o Alpha Centauri, um assistente de IA amigável, prestável e com sentido de humor. 
    O seu trabalho é conversar com o utilizador. Responda de forma concisa e natural.
    """
    
    mensagens_para_api = [{"role": "user", "parts": [prompt_do_sistema]}]
    mensagens_para_api.append({"role": "model", "parts": ["Entendido! Sou o Alpha Centauri. Como posso ajudar?"]})
    mensagens_para_api.append({"role": "user", "parts": [conversa]})

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(mensagens_para_api)
        return response.text
    except Exception as e:
        print(f"[ERRO API Conversa] {e}")
        return "Desculpe, estou com um problema para me ligar à minha inteligência agora."

def execute(comando=None):
    """
    Inicia e gere o modo de conversação.
    """
    falar("Modo de conversação ativado. Para sair, diga 'fim da conversa'.")
    
    # --- VERIFICAÇÃO DE SAÍDA CORRIGIDA E MAIS ROBUSTA ---
    # Criamos uma lista de possíveis frases para sair.
    frases_de_saida = [
        "fim da conversa",
        "fin da conversa",
        "encerrar conversa",
        "chega de papo",
        "sair do modo de conversa",
        "tchau"
    ]
    # --------------------------------------------------------

    while True:
        entrada_usuario = ouvir_comando()

        if entrada_usuario:
            # Agora, verificamos se QUALQUER uma das frases de saída está na fala do utilizador.
            if any(frase in entrada_usuario for frase in frases_de_saida):
                falar("Ok, a encerrar o modo de conversação.")
                break
            
            resposta_ia = obter_resposta_conversacional(entrada_usuario)
            falar(resposta_ia)
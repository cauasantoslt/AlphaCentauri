# commands/conversar.py (Com saída robusta)

from utils import falar, ouvir_comando
import google.generativeai as genai
import os

# O início do arquivo (KEYWORDS, configuração, obter_resposta_conversacional) continua o mesmo...
KEYWORDS = ("vamos conversar", "converse comigo", "modo chat", "bater papo")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def obter_resposta_conversacional(conversa):
    if not GEMINI_API_KEY:
        return "Desculpe, minha chave de API do Gemini não está configurada."
    prompt_do_sistema = "Você é o Alpha Centauri, um assistente de IA amigável e prestativo. Responda de forma concisa e natural."
    mensagens_para_api = [{"role": "user", "parts": [prompt_do_sistema]}, {"role": "model", "parts": ["Entendido! Sou o Alpha Centauri. Como posso ajudar?"]}]
    mensagens_para_api.append({"role": "user", "parts": [conversa]})
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(mensagens_para_api)
        return response.text
    except Exception as e:
        print(f"[ERRO API Conversa] {e}")
        return "Desculpe, estou com um problema para me conectar com minha inteligência agora."

def execute(comando=None):
    falar("Modo de conversação ativado. Para sair, diga 'fim da conversa'.")
    
    while True:
        entrada_usuario = ouvir_comando()

        if entrada_usuario:
            # --- VERIFICAÇÃO DE SAÍDA CORRIGIDA E MAIS ROBUSTA ---
            # Agora, qualquer frase que contenha "fim" E "conversa" irá funcionar,
            # independentemente de pequenas falhas de transcrição.
            if "fim" in entrada_usuario and "conversa" in entrada_usuario:
                falar("Ok, encerrando o modo de conversação.")
                break # SAI DO LOOP DE CONVERSA
            # --------------------------------------------------------
            
            resposta_ia = obter_resposta_conversacional(entrada_usuario)
            falar(resposta_ia)
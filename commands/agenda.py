# commands/agenda.py (Versão 2.1 - Correção de import e lógica)
import datetime
import os.path
import sys
import json # <-- PASSO 1: ADICIONAMOS O IMPORT QUE FALTAVA
from utils import falar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.readonly"]
KEYWORDS = ("agenda", "compromisso", "reunião", "evento", "marque", "crie") 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- FUNÇÕES DE AUTENTICAÇÃO E LÓGICA ---
def authenticate_google_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_next_event(service):
    # (Esta função não muda)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary", timeMin=now, maxResults=1,
        singleEvents=True, orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    if not events:
        return "Você não tem nenhum compromisso futuro na sua agenda."
    event = events[0]
    start = event["start"].get("dateTime", event["start"].get("date"))
    return f"Seu próximo compromisso é {event['summary']} em {start}."

def create_event(service, comando):
    # (Esta função não muda)
    falar("Entendido. Deixe-me pensar nos detalhes para criar o evento.")
    if not GEMINI_API_KEY:
        return "Não consigo processar os detalhes do evento sem minha chave de API do Gemini."

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Analise o seguinte pedido do usuário e extraia o título, a data e a hora para um evento de calendário.
    A data e hora atuais são: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
    Responda apenas com um JSON contendo 'titulo', 'data' (no formato YYYY-MM-DD) e 'hora' (no formato HH:MM:SS).
    Se alguma informação estiver faltando, use um valor nulo.

    Pedido do usuário: "{comando}"
    """
    response = model.generate_content(prompt)
    
    try:
        ia_response_text = response.text.strip().replace("```json", "").replace("```", "")
        event_details = json.loads(ia_response_text)
        
        titulo = event_details.get('titulo')
        data = event_details.get('data')
        hora = event_details.get('hora')

        if not all([titulo, data, hora]):
            return "Não consegui extrair todos os detalhes necessários. Por favor, tente ser mais específico sobre o título, data e hora."

        start_time = f"{data}T{hora}"
        end_time_dt = datetime.datetime.fromisoformat(start_time) + datetime.timedelta(hours=1)
        end_time = end_time_dt.isoformat()
        
        event_body = {
            'summary': titulo,
            'start': {'dateTime': start_time, 'timeZone': 'America/Sao_Paulo'},
            'end': {'dateTime': end_time, 'timeZone': 'America/Sao_Paulo'},
        }

        falar(f"Ok, estou criando o evento: {titulo} para o dia {data} às {hora}.")
        
        created_event = service.events().insert(calendarId='primary', body=event_body).execute()
        return f"Pronto! O evento foi criado com sucesso. Você pode vê-lo na sua agenda."

    except Exception as e:
        return f"Ocorreu um erro ao processar os detalhes ou criar o evento: {e}"

def execute(comando=None):
    """
    Função principal que decide se lê ou cria um evento.
    """
    try:
        creds = authenticate_google_calendar()
        service = build("calendar", "v3", credentials=creds)
        
        # --- PASSO 2: LÓGICA DE DECISÃO MELHORADA ---
        palavras_de_criacao = ["crie", "marque", "agende", "adicione"]
        if any(palavra in comando.split() for palavra in palavras_de_criacao):
            resposta = create_event(service, comando)
        else:
            resposta = get_next_event(service)
            
        falar(resposta)

    except Exception as e:
        falar(f"Ocorreu um erro geral no módulo da agenda: {e}")
# commands/gmail.py

import os.path
import base64
from utils import falar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURAÇÃO ---
# Adicionamos o escopo do Gmail aqui também para garantir consistência.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.readonly"]
KEYWORDS = ("gmail", "e-mail", "email", "caixa de entrada")

# A função de autenticação é a mesma da Agenda, garantindo que o token funcione para ambos.
def authenticate_google():
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

def read_emails(service):
    """
    Busca os 3 e-mails mais recentes não lidos e lê o remetente e o assunto.
    """
    try:
        # Pede a lista de mensagens não lidas
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=3).execute()
        messages = results.get('items', [])

        if not messages:
            return "Você não tem novos e-mails na sua caixa de entrada."

        falar(f"Você tem {len(messages)} novos e-mails. Lendo os mais recentes.")

        summary = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            
            # Procura pelo Assunto e Remetente nos cabeçalhos
            subject = [i['value'] for i in headers if i['name'] == 'Subject'][0]
            sender = [i['value'] for i in headers if i['name'] == 'From'][0]

            # Limpa o nome do remetente para uma leitura mais agradável
            if '<' in sender:
                sender = sender.split('<')[0].strip()

            falar(f"E-mail de {sender}. Assunto: {subject}")
        
        return "Fim da leitura dos e-mails."

    except HttpError as error:
        return f"Ocorreu um erro ao acessar a API do Gmail: {error}"
    except Exception as e:
        return f"Ocorreu um erro inesperado no módulo de e-mail: {e}"

def execute(comando=None):
    """
    Função principal que é chamada pelo main.py.
    """
    try:
        creds = authenticate_google()
        service = build("gmail", "v1", credentials=creds)
        
        # Por enquanto, a única função é ler os e-mails
        resposta = read_emails(service)
        falar(resposta)

    except Exception as e:
        falar(f"Ocorreu um erro geral no módulo do Gmail: {e}")
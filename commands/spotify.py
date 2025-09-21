# commands/spotify.py (Versão 3.2 - IA de Pesquisa Avançada e Comando Padrão)
import os
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from utils import falar
import google.generativeai as genai

KEYWORDS = ("spotify", "música", "som", "toque", "tocar", "pausar", "pular", "próxima", "continuar", "põe")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

sp = None

def authenticate_spotify():
    # (Esta função continua a mesma)
    global sp
    if sp: return True
    try:
        falar("A ligar ao Spotify. Por favor, autorize no seu navegador se ele abrir.")
        scope = "user-modify-playback-state user-read-playback-state playlist-read-private"
        auth_manager = SpotifyOAuth(scope=scope)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        user_name = sp.current_user()['display_name']
        print(f"Ligado ao Spotify com sucesso como {user_name}.")
        return True
    except Exception as e:
        print(f"ERRO: Não foi possível ligar ao Spotify. Detalhes: {e}")
        sp = None
        return False

# --- FUNÇÃO DE IA MELHORADA ---
def extract_song_details_with_gemini(comando):
    """
    Usa a IA do Gemini para extrair o título e o artista de um comando de voz.
    Retorna um dicionário.
    """
    if not GEMINI_API_KEY:
        return None

    print(f"   [IA Gemini] A extrair detalhes da música de: '{comando}'")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    A partir do seguinte pedido de um utilizador, extraia o título da música e o nome do artista.
    Responda APENAS com um objeto JSON com as chaves "titulo" e "artista". O valor de "artista" pode ser nulo se não for mencionado.
    Exemplo 1: Se o pedido for "põe para tocar a música hotel california dos eagles", a sua resposta deve ser {{"titulo": "Hotel California", "artista": "Eagles"}}.
    Exemplo 2: Se o pedido for "toque a música quer voar", a sua resposta deve ser {{"titulo": "Quer Voar", "artista": null}}.

    Pedido do utilizador: "{comando}"
    """
    try:
        response = model.generate_content(prompt)
        # Limpa e converte a resposta para um dicionário Python
        ia_response_text = response.text.strip().replace("```json", "").replace("```", "")
        details = json.loads(ia_response_text)
        print(f"   [IA Gemini] Detalhes extraídos: {details}")
        return details
    except Exception as e:
        print(f"   [ERRO Gemini] Não foi possível analisar a resposta da IA: {e}")
        return None

def execute(comando=None):
    if not authenticate_spotify():
        falar("Falha na autenticação com o Spotify. Não posso continuar.")
        return

    try:
        # Verifica se é um pedido para tocar uma música específica
        if any(palavra in comando for palavra in ["toque", "tocar", "põe"]):
            
            details = extract_song_details_with_gemini(comando)
            
            if not details or not details.get("titulo"):
                falar("Não consegui entender qual música você quer ouvir.")
                return

            # Constrói uma pesquisa precisa
            titulo = details.get("titulo")
            artista = details.get("artista")
            
            query = f"track:{titulo}"
            if artista:
                query += f" artist:{artista}"
            
            falar(f"Ok, a procurar por {titulo} no Spotify.")
            print(f"   [Spotify Search] A pesquisar com a query: '{query}'")
            results = sp.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[track_uri])
                song_name = results['tracks']['items'][0]['name']
                artist_name = results['tracks']['items'][0]['artists'][0]['name']
                falar(f"A tocar {song_name} de {artist_name}.")
            else:
                falar(f"Não encontrei resultados para {titulo} no Spotify.")
        
        elif "pausar" in comando or "parar" in comando:
            sp.pause_playback()
            falar("Música pausada.")
            
        elif "continuar" in comando:
            sp.start_playback()
            falar("A continuar a música.")
            
        elif "pular" in comando or "próxima" in comando:
            sp.next_track()
            falar("A pular para a próxima faixa.")
            
        else:
            # --- COMANDO PADRÃO INTELIGENTE ---
            # Se o comando não for específico, ele continua a música.
            falar("Entendido. A continuar a música no Spotify.")
            sp.start_playback()

    except Exception as e:
        falar("Ocorreu um erro ao comunicar com o Spotify. Verifique se tem o Spotify aberto e ativo num dos seus aparelhos.")
        print(f"ERRO SPOTIFY: {e}")
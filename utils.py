# utils.py (Com tempo de fala estendido)

import speech_recognition as sr
import os
from google.cloud import texttospeech
import pygame
import time

def falar(texto):
    # (Esta função não muda)
    print(f"[Alpha] -> {texto}")
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=texto)
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name="pt-BR-Wavenet-B"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        arquivo_de_audio = "temp_response.mp3"
        with open(arquivo_de_audio, "wb") as out:
            out.write(response.audio_content)
        pygame.mixer.init()
        pygame.mixer.music.load(arquivo_de_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload() 
        pygame.mixer.quit()
        for _ in range(5):
            try:
                os.remove(arquivo_de_audio)
                break
            except PermissionError:
                time.sleep(0.2)
    except Exception as e:
        print(f"   [ERRO TTS] Não foi possível falar: {e}")

def ouvir_comando():
    """
    Captura o áudio do microfone e o transcreve usando a API do Google.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Você] -> Ouvindo...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # --- AQUI ESTÁ A MUDANÇA ---
            # Aumentamos o tempo limite da frase de 10 para 15 segundos.
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            
            print("[Alpha] -> Processando...")
            texto_comando = r.recognize_google_cloud(audio, language_code='pt-BR')
            print(f"[Você] -> Comando reconhecido: '{texto_comando}'")
            return texto_comando.lower()
        except Exception as e:
            print(f"   (Erro no reconhecimento de voz: {e})")
            return None
        
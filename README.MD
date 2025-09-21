# 🚀 Alpha Centauri - Assistente Pessoal com IA Generativa

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Bem-vindo ao Alpha Centauri! Este é um assistente de voz avançado para desktop, construído em Python. Ele vai além de simples comandos, utilizando um cérebro de IA generativa (Google Gemini) para aprender novas habilidades em tempo real, integrar-se com serviços essenciais do seu dia a dia e manter conversas naturais.

Este projeto foi construído de forma colaborativa e documenta a jornada desde um simples script até uma plataforma de assistente robusta e modular.

## ✨ Funcionalidades Principais

O Alpha Centauri foi projetado para ser poderoso e extensível. As suas capacidades atuais incluem:

#### **Núcleo do Assistente:**
* **Reconhecimento de Voz Contínuo:** Utiliza a API `Speech-to-Text` do Google para uma transcrição precisa e contínua dos comandos.
* **Síntese de Voz Natural:** Responde com uma voz WaveNet de alta qualidade da API `Text-to-Speech` do Google, processada de forma robusta com `Pygame`.
* **Arquitetura Modular:** Comandos são organizados em módulos individuais, permitindo que novas funcionalidades sejam adicionadas de forma limpa e rápida.
* **Gerenciamento Seguro de Segredos:** Todas as chaves de API e credenciais são geridas de forma segura através de um ficheiro `.env`, mantendo o código fonte limpo e partilhável.

#### **Inteligência Artificial & Aprendizado:**
* **IA Generativa (Google Gemini):** O cérebro por trás das operações complexas. É usado para interpretar a linguagem natural, extrair informações (como detalhes de um evento ou nomes de músicas) e até mesmo gerar código Python.
* **Capacidade de Aprendizagem:** O assistente pode criar e salvar permanentemente novos comandos. Basta pedir-lhe para "criar um comando para...", e ele usará a IA para escrever o script, que pode ser salvo na sua memória.
* **Memória Persistente:** Os comandos aprendidos são guardados num ficheiro `learned_commands.json`, tornando o assistente cada vez mais personalizado com o uso.
* **Modo de Conversa Aberta:** Pode entrar num modo de "bate-papo" para conversar sobre qualquer assunto, alimentado diretamente pelo Gemini.
* **Inteligência Social (Fallback):** Se um comando não for reconhecido, o assistente usa a IA para determinar se foi um cumprimento ou agradecimento e responde de forma apropriada.

#### **Integrações Atuais:**
* **Google Agenda:** Lê os seus próximos compromissos e cria novos eventos na sua agenda com base em comandos de voz naturais.
* **Gmail:** Lê um resumo dos seus e-mails mais recentes não lidos.
* **Spotify:** Controla a reprodução de músicas e playlists (tocar, pausar, pular) de forma inteligente, usando a IA para identificar a música e o artista que você pediu.
* **Controlo do Windows:** Executa ações básicas no sistema operativo, como abrir programas.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Voz & IA:** Google Cloud (Speech-to-Text, Text-to-Speech), Google Gemini (`gemini-1.5-flash-latest`)
* **Integrações:** Google Calendar API, Gmail API, Spotify Web API (`Spotipy`)
* **Automação e GUI:** `pyautogui`, `pygetwindow`, `pycaw`, `pygame`
* **Segurança:** `python-dotenv`

## ⚙️ Configuração do Projeto
Siga os passos abaixo para executar o Alpha Centauri na sua máquina.

### 1. Clonar o Repositório
```bash
git clone https://github.com/cauasantoslt/AlphaCentauri
cd AlphaCentauri
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Git Bash / WSL
python -m venv venv
source venv/Scripts/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale todos os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 4. Configurando as Chaves de API (Passo Crucial)

Este projeto precisa de acesso a algumas APIs do Google para funcionar. Você precisará obter suas próprias chaves.

**A) Crie os Arquivos de Segredos:**
1.  Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
    ```bash
    # Windows
    copy .env.example .env

    # Git Bash / WSL
    cp .env.example .env
    ```
2.  Siga os tutoriais do Google para criar e baixar seus arquivos de credenciais:
    * **Gemini API Key:** Crie no [Google AI Studio](https://aistudio.google.com/) e cole a chave dentro do arquivo `.env`.
    * **Google Cloud Credentials (`.json`):**
        * Ative as APIs "Speech-to-Text", "Text-to-Speech" e "Google Calendar".
        * Crie um "ID do cliente OAuth" para "App para computador".
        * Baixe o arquivo JSON, renomeie-o para `google_credentials.json` e coloque-o na pasta principal do projeto.
        * Na "Tela de consentimento OAuth", adicione seu e-mail como "Usuário de teste".

### 5. Executar
Com tudo configurado, inicie o assistente:
```bash
python main.py
```
Na primeira vez que usar um comando da agenda, uma janela do navegador se abrirá para que você autorize o acesso à sua conta Google.

## 🎤 Comandos Disponíveis

* **Nativos:** "abrir bloco de notas", "abrir navegador", "vamos conversar", "desligar".
* **Agenda:** "qual meu próximo compromisso?", "marque um evento...".
* **Generativos:** "crie um comando para...", "escreva um script para...".

---
Desenvolvido por cauasantoslt / Alisonjs0 - 2025
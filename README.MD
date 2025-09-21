# 🚀 Alpha Centauri - Assistente de Voz com IA Generativa

Bem-vindo ao Alpha Centauri! Este é um protótipo de assistente de voz para desktop, construído em Python, capaz de executar comandos, aprender novas habilidades em tempo real e manter conversas, tudo com uma voz natural e de alta qualidade.

## ✨ Funcionalidades

* **Reconhecimento de Voz Contínuo:** Utiliza a API Speech-to-Text do Google para transcrição precisa.
* **Voz Natural:** Responde com uma voz de alta qualidade da API Google Cloud Text-to-Speech.
* **Arquitetura Modular:** Comandos são organizados em módulos, facilitando a expansão.
* **IA Generativa (Google Gemini):** Pode gerar e executar código Python para novas tarefas sob demanda.
* **Mecanismo de Aprendizado:** Salva os comandos gerados pela IA em um arquivo `learned_commands.json` para uso futuro.
* **Modo Conversa:** Mantém um diálogo aberto sobre qualquer assunto.
* **Integração com Google Agenda:** Capaz de ler e criar eventos na agenda do usuário.
* **Gerenciamento Seguro de Segredos:** Utiliza arquivos `.env` para proteger as chaves de API.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Reconhecimento de Voz:** `speech_recognition` + Google Cloud Speech-to-Text
* **Síntese de Voz:** `pygame` + Google Cloud Text-to-Speech
* **IA Generativa:** `google-generativeai` (Gemini)
* **Autenticação Google:** `google-auth-oauthlib`
* **Automação Windows:** `pyautogui`, `pygetwindow`, `pycaw`

## ⚙️ Configuração do Projeto

Siga os passos abaixo para executar o Alpha Centauri na sua máquina.

### 1. Clonar o Repositório
```bash
git clone [URL_DO_SEU_REPOSITORIO]
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
Desenvolvido por [cauasantoslt / alison.js] - 2025
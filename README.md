Geração Automática de Questões (generate): Conecta-se à API do Gemini para criar perguntas inéditas sobre tópicos específicos de Java, formatando-as no padrão rigoroso exigido pelo backend e salvando-as diretamente via API.

    Correção e Análise (submit): Submete um lote de respostas ao backend, recupera o gabarito oficial e utiliza IA para gerar um feedback educacional customizado com base nos erros e acertos do usuário.

📋 Pré-requisitos

    Python 3.8+

    Acesso à API do Google Gemini

    Backend do QuizByte rodando localmente ou em produção

🔧 Instalação

    Clone o repositório:

Bash

git clone https://github.com/seu-usuario/quizbyte-ai-agent.git
cd quizbyte-ai-agent

    Crie e ative um ambiente virtual:

Bash

python3 -m venv venv
source venv/bin/activate

    Instale as dependências necessárias:

Bash

pip install requests google-generativeai

⚙️ Configuração (Variáveis de Ambiente)

O agente funciona 100% baseado em variáveis de ambiente. Antes de executá-lo, exporte as variáveis abaixo no seu terminal:
Bash

# Credenciais do Gemini
export GEMINI_API_KEY="sua_chave_aqui"

# Credenciais e URL do QuizByte
export QUIZBYTE_BASE_URL="http://localhost:8080" # ou a URL de produção
export QUIZBYTE_USER="seu_usuario"
export QUIZBYTE_PASSWORD="sua_senha"

💻 Como usar

O script possui dois modos de operação, controlados pela variável de ambiente AGENT_ACTION.
1. Gerar uma nova questão

Para criar e inserir uma nova questão no banco do QuizByte:
Bash

export AGENT_ACTION="generate"
export QUIZ_ID="1"
export QUIZ_TOPIC="fundamentos"
export QUIZ_ORDER_INDEX="1"

python agent.py

2. Submeter respostas e gerar análise

Para simular a resolução de um quiz e receber o feedback da IA:
Bash

export AGENT_ACTION="submit"
export QUIZ_SLUG="fundamentos"
export QUIZ_ANSWERS='[{"questionId": 1, "choice": "B"}, {"questionId": 2, "choice": "A"}]'

python agent.py
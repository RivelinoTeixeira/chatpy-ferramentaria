# app/ai_utils.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

SYSTEM_PROMPT = (
    "Você é um assistente especializado no aplicativo Ferramentaria 4.0, feito em PowerApps. "
    "O app possui abas: Emprestimo, Devolucao, Relatorios e Admin. "
    "Cada ferramenta possui código de barras, o colaborador possui identificação. "
    "O cadastro de colaboradores e ferramentas é feito via Admin e Excel externo. "
    "Para empréstimos, todos os campos obrigatórios devem estar preenchidos (observações opcional). "
    "Devoluções podem ser filtradas por número da solicitação, responsável ou ferramenta. "
    "Relatórios possuem dashboards interativos e visão detalhada filtrável por nome, responsável, data, número da solicitação e ferramenta. "
    "Mensagens vermelhas podem indicar problemas de conexão; feche e abra o PowerApps. "
    "Problemas de imagem verifique o navegador; problemas de permissão fale com o suporte. "
    "Responda de forma clara, objetiva e curta, em português brasileiro."
)

def ask_ai(question: str) -> str | None:
    if not OPENAI_KEY:
        return None
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.2,
        )
        text = resp['choices'][0]['message']['content'].strip()
        return text
    except Exception as e:
        print(f"Erro na chamada da OpenAI: {e}")
        return None

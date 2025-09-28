# app/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.responses import get_response
from app.email_utils import send_email
from app.ai_utils import ask_ai

router = APIRouter()

class Question(BaseModel):
    message: str

@router.post("/chat")
async def chat(question: Question):
    text = question.message or ""
    resposta = get_response(text)
    if resposta:
        return {"reply": resposta}

    ai_reply = ask_ai(text)
    if ai_reply:
        return {"reply": ai_reply}

    send_email(
        assunto="Dúvida não resolvida - Ferramentaria 4.0",
        corpo=f"Mensagem do usuário: {text}"
    )
    return {"reply": "Não encontrei a resposta. Encaminhei sua dúvida para o suporte para rivelino.teixeira@cajuinasaogeraldo.com.br."}

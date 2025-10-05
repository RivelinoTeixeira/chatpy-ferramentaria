# app/router.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.responses import get_response

# Configurar router e templates
router = APIRouter()
templates = Jinja2Templates(directory="/Templates")


# Model para mensagens
class ChatMessage(BaseModel):
    message: str


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página principal - Serve o HTML do chat
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat")
async def chat(msg: ChatMessage):
    """
    Endpoint do chat - Processa mensagens
    
    Recebe: {"message": "texto da mensagem"}
    Retorna: {"reply": "resposta do bot"}
    """
    # Log da mensagem recebida
    print(f"\n{'='*70}")
    print(f"📨 MENSAGEM RECEBIDA: '{msg.message}'")
    print(f"{'='*70}")
    
    # Processa com get_response
    resposta = get_response(msg.message)
    
    # Log da resposta
    print(f"✅ RESPOSTA GERADA: {resposta[:100]}...")
    print(f"{'='*70}\n")
    
    # Retorna JSON
    return {"reply": resposta}


@router.get("/health")
async def health():
    """
    Health check - Verifica se a API está funcionando
    """
    return {
        "status": "healthy",
        "service": "Chatbot Ferramentaria 4.0",
        "version": "1.0.0"
    }

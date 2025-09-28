Chatbot Ferramentaria 4.0 (com IA)
==================================

Instruções rápidas:

1. Copie `.env.sample` para `.env` e coloque suas credenciais (OPENAI_API_KEY).
2. Instale dependências:
   pip install -r requirements.txt
3. Rode o servidor:
   uvicorn main:app --reload
4. Abra no navegador:
   http://127.0.0.1:8000/

Segurança:
- NÃO compartilhe sua OPENAI_API_KEY em chats públicos.
- Se você acidentalmente expôs uma chave, revogue/rotacione a chave nas configurações da OpenAI.

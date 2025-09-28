# app/responses.py
import unicodedata
import re

SUPPORT_EMAIL = "rivelino.teixeira@cajuinasaogeraldo.com.br"

MENU_TEXT = (
    "Olá! Eu sou o Chatbot da Ferramentaria 4.0 (PowerApps).\n\n"
    "Escolha uma opção digitando o número ou clicando no botão:\n"
    "1 - Suporte ao sistema\n"
    "2 - Falar com o suporte\n"
    "3 - Consultar ferramentas\n"
    "4 - Registrar empréstimo\n"
    "5 - Registrar devolução\n\n"
    "Digite 'menu' a qualquer momento para ver estas opções novamente."
)

SUBMENU_SUPPORT = (
    "Você escolheu Suporte. Escolha o tópico digitando o número ou escrevendo o assunto:\n"
    "1 - Problemas ao registrar empréstimos\n"
    "2 - Problemas ao registrar devoluções\n"
    "3 - Erros / problemas de conexão\n"
    "4 - Problemas de permissão\n"
    "5 - Voltar ao menu principal"
)

SUPPORT_TOPIC_RESPONSES = {
    "1": (
        "Problemas ao registrar empréstimos:\n"
        "- Abra a aba 'Registrar Empréstimo'.\n"
        "- Use o leitor de código de barras para identificar a ferramenta.\n"
        "- Preencha todos os campos obrigatórios (Observações é opcional).\n"
        "- Cada empréstimo gera um número de solicitação único.\n"
        f"Se continuar com erro, envie um e-mail para: {SUPPORT_EMAIL}"
    ),
    "2": (
        "Problemas ao registrar devoluções:\n"
        "- Abra a aba 'Devoluções' e verifique a lista de itens emprestados.\n"
        "- Use filtro por número da solicitação, responsável ou código da ferramenta.\n"
        f"Se não resolver, envie um e-mail para: {SUPPORT_EMAIL}"
    ),
    "3": (
        "Erros / problemas de conexão:\n"
        "- Mensagens vermelhas costumam indicar instabilidade de rede ou falha de sincronização.\n"
        "- Feche e abra o PowerApps; teste outro navegador se for erro de imagem.\n"
        f"Persistindo, contate: {SUPPORT_EMAIL}"
    ),
    "4": (
        "Problemas de permissão:\n"
        "- A gestão de acessos é feita pelo Admin (cadastro externo no Excel).\n"
        "- Para alterar permissões, fale com o suporte: {email}"
    ).replace("{email}", SUPPORT_EMAIL),
    "5": "Voltando ao menu principal..."
}

TOP_LEVEL_RESPONSES = {
    "2": f"Para falar com o suporte, envie um e-mail para: {SUPPORT_EMAIL}",
    "3": (
        "Consultar ferramentas:\n"
        "- Use a busca no PowerApps por nome, código ou leia o código de barras.\n"
        "- Nos relatórios você pode filtrar por nome, responsável, data, número da solicitação e ferramenta."
    ),
    "4": (
        "Registrar empréstimo:\n"
        "- Abra 'Registrar Empréstimo' no PowerApps.\n"
        "- Leia a ferramenta com o leitor de código de barras e selecione o colaborador.\n"
        "- Preencha todos os campos obrigatórios (Observações é opcional) e confirme."
    ),
    "5": (
        "Registrar devolução:\n"
        "- Abra 'Devoluções'.\n"
        "- Localize a solicitação (filtre por número, responsável ou ferramenta) e confirme a devolução."
    )
}


def normalize_text(text: str) -> str:
    """Normaliza texto: tira acentos, coloca em minúsculas e remove espaços extras."""
    if text is None:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    # substitui múltiplos espaços por um só
    text = re.sub(r"\s+", " ", text)
    return text


def parse_numeric_pair(s: str):
    """
    Detecta padrões como:
      '1' -> ('1', None)
      '1.2' / '1-2' / '1 2' / '1,2' -> ('1','2')
    Retorna tuple (primary, secondary) com strings ou (None, None)
    """
    s = s.strip()
    m = re.match(r"^(\d+)(?:[.,\- ]+(\d+))?$", s)
    if m:
        return m.group(1), m.group(2)
    return None, None


def get_response(message: str) -> str:
    """
    Resposta principal. Aceita números, subseleções (1.2) e palavras-chave.
    Retorna texto simples em pt-BR.
    """
    message_norm = normalize_text(message)

    # vazio -> mostrar menu
    if not message_norm:
        return MENU_TEXT

    # se pedir menu explicitamente
    if message_norm in {"menu", "inicio", "início"}:
        return MENU_TEXT

    # detectar padrões numéricos: '1', '2', '1.2', '1 2', etc.
    primary, secondary = parse_numeric_pair(message_norm)
    if primary:
        # caso '1 2' -> primary=1 secondary=2
        if primary == "1" and (secondary is None):
            # 1 sozinho => mostrar submenu suporte
            return SUBMENU_SUPPORT
        if primary == "1" and secondary:
            # 1.x -> sub-topico do suporte
            sec = secondary
            if sec in SUPPORT_TOPIC_RESPONSES:
                resp = SUPPORT_TOPIC_RESPONSES[sec]
                # se for voltar (5) retornamos menu
                if sec == "5":
                    return MENU_TEXT
                return resp
            # se nao conhecido
            return (
                "Opção do Suporte inválida. Digite um número entre 1 e 5 ou escreva o assunto.\n"
                + SUBMENU_SUPPORT
            )
        # primary sem secondary (top-level)
        if primary in TOP_LEVEL_RESPONSES:
            return TOP_LEVEL_RESPONSES[primary]
        # se número fora do range
        return "Opção inválida. Digite 'menu' para ver as opções."

    # agora tratar por palavras-chave (normalizadas, sem acento)
    # SUporte
    if "suporte" in message_norm:
        return SUBMENU_SUPPORT

    # palavras relacionadas ao contato
    if any(k in message_norm for k in ("contato", "falar", "suportar", "entrar em contato", "email")):
        return TOP_LEVEL_RESPONSES["2"]

    # consultar ferramentas / relatórios
    if any(k in message_norm for k in ("consultar", "consulta", "ferramentas", "relatorio", "relatórios", "dashboard")):
        return TOP_LEVEL_RESPONSES["3"]

    # registrar empréstimo
    if any(k in message_norm for k in ("emprestimo", "emprestar", "registrar emprestimo", "registrar emprestimo")):
        return TOP_LEVEL_RESPONSES["4"]

    # registrar devolução
    if any(k in message_norm for k in ("devolucao", "devolver", "devolucao")):
        return TOP_LEVEL_RESPONSES["5"]

    # erros / conexão
    if any(k in message_norm for k in ("erro", "falha", "conexao", "conexão", "instabilidade", "sincroniz")):
        return SUPPORT_TOPIC_RESPONSES["3"]

    # permissão
    if any(k in message_norm for k in ("permissao", "permissão", "acesso", "autorizacao", "autorização")):
        return SUPPORT_TOPIC_RESPONSES["4"]

    # voltar
    if "voltar" in message_norm:
        return MENU_TEXT

    # palavras curtas que podem indicar submenu como "empréstimo" sem acento
    if "emprestimo" in message_norm:
        return SUPPORT_TOPIC_RESPONSES["1"]
    if "devolucao" in message_norm:
        return SUPPORT_TOPIC_RESPONSES["2"]

    # se nada bateu, resposta padrão
    return (
        "Desculpe, não consegui entender sua mensagem.\n"
        f"Se quiser, digite 'menu' para ver as opções ou envie sua dúvida por e-mail: {SUPPORT_EMAIL}"
    )

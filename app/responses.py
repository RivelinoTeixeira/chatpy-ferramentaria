# app/responses.py
"""
Sistema de respostas do chatbot Ferramentaria 4.0
Processa mensagens e retorna respostas apropriadas
"""

import unicodedata
import re

# Configurações
SUPPORT_EMAIL = "rivelino.teixeira@cajuinasaogeraldo.com.br"

# ============================================
# MENSAGENS DO SISTEMA
# ============================================

MENU_TEXT = """Olá! Eu sou o Chatbot da Ferramentaria 4.0 (PowerApps).

Escolha uma opção digitando o número:
1 - Suporte ao sistema
2 - Falar com o suporte
3 - Consultar ferramentas
4 - Registrar empréstimo
5 - Registrar devolução
6 - Administração (Admin)

Digite 'menu' a qualquer momento para voltar."""

SUBMENU_SUPPORT = """📋 MENU DE SUPORTE

Escolha o tópico:
1 - Problemas ao registrar empréstimos
2 - Problemas ao registrar devoluções
3 - Erros / problemas de conexão
4 - Problemas de permissão
5 - Problemas com cadastro
6 - Voltar ao menu principal"""

# ============================================
# RESPOSTAS DO SUBMENU SUPORTE
# ============================================

SUPPORT_RESPONSES = {
    "1": f"""🔧 PROBLEMAS AO REGISTRAR EMPRÉSTIMOS

Passos para registrar:
1. Abra a aba 'Registrar Empréstimo'
2. Use o leitor de código de barras
3. Preencha todos os campos obrigatórios

Problemas comuns:
• Ferramenta não aparece? Verifique se está cadastrada
• Código de barras não lê? Digite manualmente
• Campos faltando? Preencha todos exceto Observações
• Colaborador não encontrado? Verifique cadastro no Admin

📧 Persistindo? {SUPPORT_EMAIL}""",
    
    "2": f"""📦 PROBLEMAS AO REGISTRAR DEVOLUÇÕES

Como devolver:
1. Abra a aba 'Devoluções'
2. Use filtros: número da solicitação, responsável ou código
3. Selecione o item e confirme a devolução

Problemas comuns:
• Item não aparece na lista? Verifique se empréstimo foi registrado
• Filtros não funcionam? Limpe os filtros e tente novamente
• Erro ao confirmar? Verifique sua conexão

📧 Precisa de ajuda? {SUPPORT_EMAIL}""",
    
    "3": f"""⚠️ ERROS / PROBLEMAS DE CONEXÃO

Soluções rápidas:
• Mensagens vermelhas = rede instável ou falha de sincronização
• Feche e abra o PowerApps novamente
• Teste outro navegador (recomendado: Chrome ou Edge)
• Verifique sua conexão com a internet
• Limpe o cache do navegador

Erros comuns:
• 'Erro de sincronização': aguarde alguns segundos e tente novamente
• 'Falha ao carregar dados': verifique sua conexão
• Tela branca ou congelada: recarregue a página (F5)

📧 Ainda com problema? {SUPPORT_EMAIL}""",
    
    "4": f"""🔒 PROBLEMAS DE PERMISSÃO

A gestão de acessos é feita pelo Administrador através de cadastro externo (Excel/base de dados).

Tipos de permissão:
• Usuário comum: consultar, registrar empréstimos e devoluções
• Admin: acesso total + cadastros de ferramentas e colaboradores

Sem acesso a alguma funcionalidade?
• Verifique se seu usuário está cadastrado
• Confirme se tem a permissão necessária
• Solicite alteração de permissões ao suporte

📧 Para alterar permissões: {SUPPORT_EMAIL}""",
    
    "5": f"""📝 PROBLEMAS COM CADASTRO

Formatos corretos:
• Ferramentas: FERXXX (exemplo: FER001, FER002, FER150)
• Chaves: CHAVXX (exemplo: CHAV01, CHAV02, CHAV25)
• Colaboradores: sequência numérica

Problemas comuns:
• Código duplicado? Verifique se já existe no sistema
• Formato incorreto? Siga o padrão indicado acima
• Campos obrigatórios vazios? Preencha todos os campos necessários

Todos os cadastros são sincronizados com site externo (Excel/banco de dados).
Acesse a aba Admin para realizar cadastros.

📧 Dúvidas sobre cadastros? {SUPPORT_EMAIL}""",
    
    "6": "⬅️ Voltando ao menu principal..."
}

# ============================================
# RESPOSTAS DO MENU PRINCIPAL
# ============================================

TOP_RESPONSES = {
    "2": f"""📧 FALAR COM O SUPORTE:

Para entrar em contato com o Suporte, envie um e-mail para:
{SUPPORT_EMAIL}

O Suporte responderá em breve!""",
    
    "3": """🔍 CONSULTAR FERRAMENTAS

Como consultar:
• Use a busca no PowerApps por nome, código ou código de barras
• Nos relatórios você pode filtrar por:
  - Nome da ferramenta
  - Responsável
  - Data
  - Número da solicitação
  - Código da ferramenta

Dicas úteis:
• Use o dashboard para visualizar estatísticas gerais
• Combine filtros para buscas mais específicas
• Exporte relatórios quando necessário""",
    
    "4": """📋 REGISTRAR EMPRÉSTIMO

Passo a passo completo:

1. Abra a aba 'Registrar Empréstimo' no PowerApps
2. Leia o código de barras da ferramenta (ou digite manualmente)
3. Selecione o colaborador responsável
4. Preencha todos os campos obrigatórios:
   • Data/hora do empréstimo
   • Responsável
   • Ferramenta
   • Observações (este é opcional)
5. Confirme o registro

✅ Um número de solicitação único será gerado automaticamente!
Guarde este número para facilitar a devolução.""",
    
    "5": """📦 REGISTRAR DEVOLUÇÃO

Passo a passo completo:

1. Abra a aba 'Devoluções' no PowerApps
2. Localize a solicitação usando um dos filtros:
   • Número da solicitação
   • Nome do responsável
   • Código da ferramenta
3. Verifique se as informações estão corretas
4. Confirme a devolução

✅ A ferramenta ficará disponível novamente para novos empréstimos!
O histórico completo será mantido no sistema.""",
    
    "6": f"""⚙️ ADMINISTRAÇÃO (ADMIN)

A aba Admin permite cadastrar:

1️⃣ Ferramentas (código FERXXX):
   • Use o padrão FERXXX onde XXX é um número sequencial
   • Exemplo: FER001, FER002, FER150
   • Preencha nome, descrição e outras informações

2️⃣ Chaves (código CHAVXX):
   • Use o padrão CHAVXX onde XX é um número sequencial
   • Exemplo: CHAV01, CHAV02, CHAV25

3️⃣ Colaboradores (sequência numérica):
   • Cadastre nome, matrícula e setor
   • Use numeração sequencial para identificação

⚠️ Importante:
• Todos os cadastros são sincronizados com um site externo (Excel/banco de dados)
• Apenas usuários com permissão Admin podem acessar esta funcionalidade

📧 Dúvidas sobre cadastros? {SUPPORT_EMAIL}"""
}


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def normalize_text(text: str) -> str:
    """
    Normaliza texto: remove acentos, converte para minúsculas,
    remove espaços extras.
    
    Args:
        text: Texto a ser normalizado
        
    Returns:
        Texto normalizado
    """
    if not text:
        return ""
    
    # Remove espaços e converte para minúsculas
    text = text.strip().lower()
    
    # Remove acentos
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    
    # Remove múltiplos espaços
    text = re.sub(r"\s+", " ", text)
    
    return text


def parse_number(text: str):
    """
    Detecta padrões numéricos como '1', '1.2', '1-2', '1 2'.
    
    Args:
        text: Texto a ser analisado
        
    Returns:
        Tupla (primary, secondary) com os números ou (None, None)
    """
    text = text.strip()
    match = re.match(r"^(\d+)(?:[.,\-\s]+(\d+))?$", text)
    if match:
        return match.group(1), match.group(2)
    return None, None


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def get_response(message: str) -> str:
    """
    Função principal de processamento de mensagens.
    Analisa a mensagem e retorna a resposta apropriada.
    
    Args:
        message: Mensagem do usuário
        
    Returns:
        Resposta do chatbot (sempre retorna uma string válida)
    """
    # Mensagem vazia -> menu
    if not message:
        return MENU_TEXT
    
    # Normaliza a mensagem
    norm = normalize_text(message)
    print(f"🔍 Mensagem normalizada: '{norm}'")
    
    # ========================================
    # 1. COMANDOS EXPLÍCITOS
    # ========================================
    if norm in ["menu", "inicio", "início", "voltar", "principal"]:
        return MENU_TEXT
    
    # ========================================
    # 2. NÚMEROS (1, 2, 1.2, etc)
    # ========================================
    primary, secondary = parse_number(norm)
    
    if primary:
        # Opção 1 (Suporte)
        if primary == "1":
            if not secondary:
                # "1" sozinho -> submenu
                return SUBMENU_SUPPORT
            # "1.X" -> sub-opção
            if secondary in SUPPORT_RESPONSES:
                # "1.6" volta ao menu
                if secondary == "6":
                    return MENU_TEXT
                return SUPPORT_RESPONSES[secondary]
            # Sub-opção inválida
            return "Opção inválida.\n\n" + SUBMENU_SUPPORT
        
        # Opções 2-6 do menu principal
        if primary in TOP_RESPONSES:
            return TOP_RESPONSES[primary]
        
        # Número fora do range
        return "Opção inválida. Digite 'menu' para ver as opções ou um número de 1 a 6."
    
    # ========================================
    # 3. PALAVRAS-CHAVE
    # ========================================
    
    # Saudações
    if any(k in norm for k in ["oi", "ola", "olá", "hey", "opa", "bom dia", "boa tarde", "boa noite", "alo", "alô"]):
        return MENU_TEXT
    
    # Agradecimentos
    if any(k in norm for k in ["obrigad", "valeu", "vlw", "thanks", "brigadao"]):
        return "Por nada! Se precisar de mais alguma coisa, é só chamar. Digite 'menu' para ver as opções. 😊"
    
    # Ajuda
    if any(k in norm for k in ["ajuda", "help", "socorro", "como usar", "como funciona", "nao sei"]):
        return MENU_TEXT
    
    # Suporte
    if "suporte" in norm:
        return SUBMENU_SUPPORT
    
    # Contato / Falar com suporte
    if any(k in norm for k in ["contato", "falar", "conversar", "email", "e-mail", "mail", "ligar"]):
        return TOP_RESPONSES["2"]
    
    # Admin / Cadastro
    if any(k in norm for k in ["admin", "administracao", "administração", "cadastr", "ferxxx", "chavxx", "criar", "adicionar", "novo"]):
        return TOP_RESPONSES["6"]
    
    # Consultar / Buscar
    if any(k in norm for k in ["consultar", "consulta", "buscar", "busca", "procurar", "encontrar", "pesquisar", "ferramenta", "ferramentas", "relatorio", "relatórios", "dashboard", "lista", "ver"]):
        return TOP_RESPONSES["3"]
    
    # Empréstimo
    if any(k in norm for k in ["emprestimo", "empréstimo", "emprestar", "pegar", "retirar", "solicitar", "pedir"]):
        # Verifica se é problema
        if any(p in norm for p in ["problema", "erro", "nao consigo", "não consigo", "nao funciona", "dificuldade"]):
            return SUPPORT_RESPONSES["1"]
        return TOP_RESPONSES["4"]
    
    # Devolução
    if any(k in norm for k in ["devolucao", "devolução", "devolver", "retornar", "retorno", "entregar", "entrega"]):
        # Verifica se é problema
        if any(p in norm for p in ["problema", "erro", "nao consigo", "não consigo", "nao funciona"]):
            return SUPPORT_RESPONSES["2"]
        return TOP_RESPONSES["5"]
    
    # Erros / Problemas técnicos
    if any(k in norm for k in ["erro", "falha", "bug", "problema", "quebrou", "travou", "trava", "nao funciona", "não funciona", "nao abre", "nao carrega"]):
        return SUPPORT_RESPONSES["3"]
    
    # Conexão / Rede
    if any(k in norm for k in ["conexao", "conexão", "internet", "rede", "offline", "desconectado", "sincroniz"]):
        return SUPPORT_RESPONSES["3"]
    
    # Permissão / Acesso
    if any(k in norm for k in ["permissao", "permissão", "acesso", "bloqueado", "nao tenho acesso", "não tenho acesso", "autorizar", "autorizacao", "senha"]):
        return SUPPORT_RESPONSES["4"]
    
    # Código de barras
    if any(k in norm for k in ["codigo de barras", "código de barras", "barras", "leitor", "scanner", "escanear", "ler codigo"]):
        return f"""📱 CÓDIGO DE BARRAS

Para usar o leitor de código de barras:
1. Ative o leitor no PowerApps
2. Aponte para o código na ferramenta
3. Aguarde a leitura automática

Se não funcionar:
• Digite o código manualmente
• Verifique se o código está legível
• Teste em boa iluminação
• Limpe a câmera do dispositivo

📧 Problemas persistentes? {SUPPORT_EMAIL}"""
    
    # Colaborador / Usuário
    if any(k in norm for k in ["colaborador", "usuario", "usuário", "pessoa", "funcionario", "funcionário"]):
        return f"""👥 COLABORADORES

Para cadastrar ou consultar colaboradores:
• Acesse a aba Admin (apenas para administradores)
• Use sequência numérica para identificação
• Preencha nome, matrícula e setor

Se você não consegue acessar, solicite permissão ao administrador.

📧 Contato: {SUPPORT_EMAIL}"""
    
    # Número de solicitação
    if any(k in norm for k in ["numero", "número", "solicitacao", "solicitação", "codigo", "código", "id"]):
        return """🔢 NÚMERO DE SOLICITAÇÃO

Cada empréstimo gera um número único de solicitação.

Como usar:
• Anote o número ao fazer o empréstimo
• Use para localizar na aba Devoluções
• Facilita consultas e relatórios

Se perdeu o número:
• Busque por nome do responsável
• Busque por código da ferramenta
• Consulte os relatórios no dashboard"""
    
    # PowerApp / Sistema
    if any(k in norm for k in ["powerapp", "powerapps", "sistema", "aplicativo", "app", "programa"]):
        return f"""💻 SISTEMA POWERAPPS - FERRAMENTARIA 4.0

Funcionalidades principais:
1. Registrar empréstimos de ferramentas
2. Registrar devoluções
3. Consultar ferramentas disponíveis
4. Visualizar relatórios e histórico
5. Administrar cadastros (Admin)

Digite 'menu' para ver todas as opções disponíveis.

📧 Suporte técnico: {SUPPORT_EMAIL}"""
    
    # ========================================
    # 4. RESPOSTA PADRÃO
    # ========================================
    return f"""Desculpe, não entendi sua mensagem. 😕

Você pode:
• Digite 'menu' para ver todas as opções
• Digite um número de 1 a 6
• Use palavras-chave como: empréstimo, devolução, consultar, admin, erro, suporte

📧 E-mail do suporte: {SUPPORT_EMAIL}

Estou aqui para ajudar!"""
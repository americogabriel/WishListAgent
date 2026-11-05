# 🛒 WishList HTML Creator Agent

Um agente inteligente desenvolvido com o **Google ADK** (Agent Development Kit) e o ecossistema **Antigravity**. O agente recebe a lista de desejos do usuário, pesquisa as melhores ofertas disponíveis na web em Reais (BRL) e gera uma página web `wishlist.html` estilizada, interativa e responsiva pronta para visualização em qualquer navegador.

---

## 🎯 Funcionalidades

- **Mensagem Inicial Guiada**: Responde de imediato com instruções claras caso o usuário inicie apenas com uma saudação.
- **Curadoria de Menor Preço**: Identifica a menor cotação em moeda local (BRL) para cada item informado.
- **Validação de Schema (Pydantic)**: Valida `titulo`, `preco`, `loja`, `url_produto` e `url_imagem` com regras de fallback robustas.
- **Geração Web Autônoma**: Compila o arquivo `wishlist.html` com design responsivo (Grid CSS), cartões modernos e links seguros (`target="_blank" rel="noopener noreferrer"`).
- **Execução Nativa com Google ADK**: Suporta interação via Terminal CLI (`adk run`) e Web UI oficial do ADK (`adk web`).

---

## 🏗️ Estrutura do Projeto

```text
WishListAgent/
├── wishlist_agent/              # Pacote do Agente Google ADK
│   ├── __init__.py              # Exporta root_agent
│   ├── agent.py                 # Definição do LlmAgent (ADK) e prompts
│   ├── models.py                # Contrato de dados Pydantic (schema.md)
│   └── tools.py                 # Ferramentas: pesquisa de ofertas e gerador HTML
├── agent-skills/                # Especificações e referências
│   ├── SKILLS.md                # Diretrizes operacionais da skill
│   └── references/              # Schema JSON e templates HTML/CSS
├── tests/                       # Testes automatizados unitários
│   └── test_wishlist.py
├── AGENTS.md                    # Diretrizes globais de negócio
├── main.py                      # Launcher CLI interativo
├── wishlist.html                # Arquivo HTML gerado pelo agente
├── requirements.txt             # Dependências Python
└── .env.example                 # Modelo de configuração de chaves de API
```

---

## 🚀 Como Executar

### 1. Configurar Chave de API

Copie o arquivo de exemplo e insira sua chave da API Gemini:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
GEMINI_API_KEY=sua_chave_gemini_aqui
```

*(Ou configure a variável de ambiente: `export GEMINI_API_KEY="sua_chave"`)*

---

### 2. Modos de Execução com Google ADK

#### A. Chat Interativo via Terminal (Recomendado)

Utilizando o CLI nativo do **Google ADK**:

```bash
adk run wishlist_agent
```
ou 
```bash
uv run adk web --allow_origins="*"
```

Ou através do script inicializador:

```bash
python main.py
```

#### B. Consulta Rápida (Turno Único)

Envie a lista de produtos diretamente como argumento:

```bash
adk run wishlist_agent "Console PS5 Slim, Headset HyperX Cloud Stinger, Monitor 144Hz"
```

#### C. Interface Web Gráfica do Google ADK

Inicie o servidor Web UI integrado do ADK:

```bash
adk web .
```

Acesse o navegador no endereço indicado (geralmente `http://localhost:8000`) para interagir visualmente com o agente.

---

## 🧪 Executando os Testes

Execute a suíte de testes unitários para validar modelos, ferramentas e geração do HTML:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 Licença

Projeto desenvolvido sob as diretrizes do Google ADK e Antigravity.

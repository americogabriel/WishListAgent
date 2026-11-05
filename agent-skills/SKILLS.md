# SKILLS.md — Habilidades Técnicas e Operacionais do Agente

Especificação detalhada das ferramentas e algoritmos determinísticos executados pelo agente no **Google ADK**.

---

## 1. Mapeamento das Ferramentas (ADK Tools)

1. `pesquisar_ofertas_produto(termo_busca: str) -> dict`: Varredura comparativa real, extração de float BRL (`Min(Preços)`), bloqueio de links de busca/esgotados e busca visual estrita (Top 10 Google Imagens).
2. `gerar_wishlist_html(produtos: list[dict]) -> str`: Validação rigorosa contra `references/schema.md` e compilação de `wishlist.html` na raiz.

---

## 2. Pipeline Determinístico de Curadoria (`pesquisar_ofertas_produto`)

Para cada produto informado pelo usuário, execute sequencialmente as 5 etapas obrigatórias:

### Etapa 1: Filtragem Semântica e Descarte de Acessórios
- **Regra de Isolamento**: Quando o item solicitado for o produto principal (ex: *"Console PlayStation 5"*, *"iPhone 15"*, *"Suporte de Guitarra"*):
  * **DESCARTE SUMÁRIO**: Rejeitar ofertas de acessórios (capas, cabos, películas, peças de reposição, suportes incompatíveis, caixas vazias) e produtos usados/recondicionados/seminovos.
  * Considerar estritamente o item completo, original e novo.

### Etapa 2: Varredura Comparativa Real em >= 3 Lojas (Anti-Mock)
- **PROIBIÇÃO EXPRESSA DE PREÇO SIMULADO**: É estritamente proibido inventar valores padrão (ex: R$ 199,90, 0.00 ou números fictícios repetidos).
- **Varredura Obrigatória**: Consultar simultaneamente no mínimo **3 e-commerces distintos** (ex: Mercado Livre, Magalu, Shopee, Kabum, Pichau, Amazon).
- **Critério de Preço**: Preço à vista/tabela em Reais (BRL), excluindo frete variável por CEP.
- **Diversidade de Lojas**: O campo `loja` deve registrar o e-commerce que ofertou o menor valor real apurado. PROIBIDO atribuir "Amazon" por conveniência para todos os itens.
- **Cálculo Numérico Estrito**:
  $$\text{Ofertas} = [P_1, P_2, P_3] \implies \text{Selecionar } \min(P_i) \text{ onde } P_i \text{ é float ativo em BRL com estoque}$$

### Etapa 3: Bloqueio Absoluto de Anúncios Inativos e Esgotados
- **Inspeção de Status**: Rejeitar anúncios com *"Fora de estoque"*, *"Esgotado"*, *"Indisponível"*, *"Anúncio Pausado"*, links 404 ou redirecionamentos de afiliados expirados.
- **Regra de Avanço e Omissão**: Se o menor preço estiver esgotado, avançar para a próxima cotação ativa com estoque. Se todas as fontes estiverem esgotadas/inválidas, **omitir o item do HTML** e alertá-lo expressamente no chat sob a seção de itens indisponíveis.

### Etapa 4: Validação e Higienização Canônica do Link (`url_produto`)
- **BLOQUEIO TOTAL DE PÁGINAS DE BUSCA**: É estritamente PROIBIDO preencher `url_produto` com páginas de busca/listagem (ex: `amazon.com.br/s?k=...`, `google.com/search?q=...`, `mercadolivre.com.br/busca`).
- **Validação e Higienização**: O link DEVE ser a URL canônica e direta da página de detalhes/checkout do produto na loja vencedora, higienizada sem parâmetros agressivos de rastreamento (`utm_*`, `gclid`, `fbclid`, `session_id`). Se a URL for de busca, REJEITAR a oferta e cotar a próxima válida.

### Etapa 5: Algoritmo de Busca Visual Estrita no Google Imagens (`url_imagem`)
- **PROIBIÇÃO**: NÃO extrair a foto da página do anúncio selecionado na loja.
- **Protocolo dos 4 Passos**:
  1. **Título Exato**: Capturar o título limpo e exato do produto solicitado.
  2. **Consulta Focada**: Disparar busca no Google Imagens com o título exato.
  3. **Seleção Top 10 Obrigatória**: Selecionar obrigatoriamente uma Raw URL direta (.jpg, .png, .webp, CDN público ou thumbnail oficial `encrypted-tbn0.gstatic.com`) que esteja **ENTRE AS 10 PRIMEIRAS FOTOS** retornadas na busca, prevenindo erros de hotlinking (403).
  4. **Validação Semântica do Objeto**: Validar se o objeto visual da imagem corresponde 100% ao produto solicitado. Descartar sumariamente categorias incorretas (ex: rejeitar imagem de microfone para "suporte de guitarra").
  5. **Injeção Limpa**: Injetar a URL pura diretamente em `url_imagem` sem formatação Markdown (`[...]`) ou caracteres de escape indesejados.

---

## 3. Renderização HTML (`gerar_wishlist_html`)

1. **Validação**: Validar cada item contra o contrato estrito em `references/schema.md`.
2. **Injeção do Card**: Inserir a Raw URL validada no atributo `src="{url_imagem}"` da tag `<img>`.
3. **Template**: Injetar os cards compilados no marcador `<!-- INSERT_CARDS_HERE -->` de `references/template.md`.
4. **Persistência**: Gravar o arquivo final `wishlist.html` na raiz do projeto.

---

## 4. Entrega e Acesso no Chat (Obrigatório)

Após invocar `gerar_wishlist_html`, a resposta final no chat DEVE conter:

1. **Confirmação Visual**: Ex: "✅ Sua Wishlist foi gerada com sucesso!"
2. **Tabela Resumo das Cotações**:
   | Produto | Menor Preço (BRL) | Loja Oficial |
   | :--- | :--- | :--- |
   | Nome do Produto | R$ X.XXX,XX | Loja Real Encontrada |
3. **Alerta de Indisponibilidade**: Indicar claramente se algum item solicitado não possui estoque ativo no mercado.
4. **Instrução e Link Markdown**:
   > *"Sua Wishlist foi gerada com sucesso! Abra o arquivo [wishlist.html](wishlist.html) na raiz do seu ambiente para visualizar as ofertas e acessar as lojas."*

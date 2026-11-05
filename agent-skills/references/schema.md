# Schema de Dados dos Produtos (JSON)

Contrato obrigatório de dados consumido por `gerar_wishlist_html` e produzido por `pesquisar_ofertas_produto`.

---

## 1. Exemplo do Payload JSON (Valores Reais e Raw URLs)

```json
[
  {
    "titulo": "Console PlayStation 5 Slim Edição Digital",
    "preco": 3499.00,
    "loja": "Mercado Livre",
    "url_produto": "https://www.mercadolivre.com.br/playstation-5-slim/p/MLB12345678",
    "url_imagem": "https://m.media-amazon.com/images/I/61S9JmsxPPL._AC_SL1500_.jpg"
  },
  {
    "titulo": "Headset Gamer HyperX Cloud Stinger 2",
    "preco": 249.90,
    "loja": "Kabum",
    "url_produto": "https://www.kabum.com.br/produto/384650",
    "url_imagem": "https://images.unsplash.com/photo-1546435770-a3e426bf472b"
  }
]
```

---

## 2. Dicionário de Campos e Regras Determinísticas

| Campo | Tipo | Obrigatório | Descrição & Regras de Validação | Proibições Expressas (Tolerância Zero) |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | `string` | **Sim** | Nome exato, limpo e canônico do produto completo solicitado. | PROIBIDO termos promocionais genéricos ("Super Oferta", "Preço Baixo") ou peças/acessórios incompatíveis. |
| `preco` | `number` | **Sim** | Menor valor numérico float em Reais (BRL) apurado em >= 3 lojas ativas com estoque (`Min(Preços)`). | **PROIBIDO usar preço estático/simulado (ex: R$ 199,90, 0.00)**. PROIBIDO strings monetárias (`"R$ 299,90"`). |
| `loja` | `string` | **Sim** | Nome da loja nacional que realmente apresentou o menor preço ativo. | **PROIBIDO atribuir loja padrão/fixa ("Amazon" para tudo)**. Diversificar conforme o menor preço real apurado (Mercado Livre, Magalu, Shopee, Kabum, Pichau, etc.). |
| `url_produto` | `string (URI)` | **Sim** | URL direta e canônica da página do produto/checkout na loja vendedora, higienizada sem tracking agressivo (`utm_*`, `gclid`). | **BLOQUEIO ABSOLUTO de URLs de busca** (`google.com/search`, `amazon.com.br/s?k=`, `mercadolivre.com.br/busca`). PROIBIDO links 404, pausados ou sintaxe Markdown (`[url](url)`). |
| `url_imagem` | `string (URI)` | **Sim** | Raw URL direta da foto obtida **ENTRE AS 10 PRIMEIRAS FOTOS** do Google Imagens com validação semântica do objeto. Aceita thumbnails oficiais (`gstatic.com`) contra 403. | **PROIBIDO extrair da página do anúncio**. PROIBIDO objetos desalinhados (ex: microfone para suporte de guitarra). PROIBIDO sintaxe Markdown. Formatos aceitos: `.jpg`, `.png`, `.webp`, CDN público ou thumbnail oficial. |

---

## 3. Validações Negativas Críticas (Anti-Alucinação)

- ❌ **PREÇO MOCK REJEITADO**: `"preco": 199.90` (valor estático/fictício sem cotação em 3 fontes)
- ✅ **PREÇO REAL OBTIDO**: `"preco": 3499.00` (menor cotação real apurada: `Min(3499.00, 3699.00, 3750.00)`)

- ❌ **LOJA FIXA REJEITADA**: Atribuir "Amazon" cegamente a todos os itens
- ✅ **LOJA DIVERSIFICADA**: Registrar a loja vencedora real (`"Mercado Livre"`, `"Kabum"`, `"Magalu"`, `"Pichau"`, `"Shopee"`, `"Amazon"`)

- ❌ **LINK DE BUSCA REJEITADO**: `"url_produto": "https://www.amazon.com.br/s?k=suporte+guitarra"` ou `"https://www.google.com/search?q=..."`
- ✅ **LINK DIRETO DA LOJA**: `"url_produto": "https://www.kabum.com.br/produto/384650"`

- ❌ **IMAGEM INCORRETA/DESALINHADA**: Foto de microfone para "suporte de guitarra" ou extraída do anúncio
- ✅ **IMAGEM DO TOP 10 GOOGLE IMAGENS**: Foto focada no objeto exato capturada entre as 10 primeiras posições do Google Imagens

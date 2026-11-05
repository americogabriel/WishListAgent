# Template Visual e Estrutura do Arquivo `wishlist.html`

Modelo de código HTML5 e CSS3 responsivo utilizado para renderizar a página da Wishlist.

---

## 1. Estrutura Visual e Comportamento

- **Grid Responsivo (`.grid`)**: Grid auto-ajustável (`repeat(auto-fill, minmax(260px, 1fr))`) para telas de mobile, tablet e desktop.
- **Tratamento da Imagem (`.card img`)**: A propriedade `object-fit: contain` garante que a imagem capturada entre as 10 primeiras do Google Imagens seja exibida sem distorções em área de 180px.
- **Hierarquia de Preço & Ação (`.meta`)**: Menor preço real em BRL em verde destacado (`#16a34a`, 1.35rem) e botão "Ver na Loja" direcionando para a URL canônica direta com `target="_blank" rel="noopener noreferrer"`.
- **Ponto de Injeção (`<!-- INSERT_CARDS_HERE -->`)**: Marcador substituído pelo bloco consolidado de cards.

---

## 2. Estrutura dos Cards Gerados Dinamicamente

Para cada item validado contra o schema, gerar o seguinte fragmento HTML:

```html
<div class="card">
  <img src="{url_imagem}" alt="{titulo}" loading="lazy">
  <div class="title">{titulo}</div>
  <div class="meta">
    <div class="price">R$ {preco}</div>
    <div class="store">Melhor oferta em: <strong>{loja}</strong></div>
    <a href="{url_produto}" target="_blank" rel="noopener noreferrer" class="btn">Ver na Loja</a>
  </div>
</div>
```

> **Atenção Técnica para Injeção**:
> - `{url_imagem}`: Raw URL direta obtida **entre as 10 primeiras fotos do Google Imagens** com validação semântica estrita do objeto (sem Markdown, sem imagem de anúncio).
> - `{url_produto}`: Link de destino canônico direto do produto na loja (BLOQUEIO TOTAL de links de busca como `google.com/search` ou `amazon.com.br/s?k=`).
> - `{preco}`: Menor preço float real em BRL formatado no padrão brasileiro (`R$ X.XXX,XX`). PROIBIDO valores fictícios/padrão (ex: R$ 199,90).

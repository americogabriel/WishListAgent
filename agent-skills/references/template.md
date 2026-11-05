# Template Visual e Estrutura do Arquivo `wishlist.html`

Este documento contém o modelo de código HTML5 e CSS3 responsivo utilizado para gerar a página da Wishlist. 

---

## 1. Explicação da Estrutura Visual

A página foi construída com foco em legibilidade, desempenho e design moderno (clean/dashboard):

- **Grid Responsivo (`.grid`)**: Utiliza `display: grid` com `repeat(auto-fill, minmax(260px, 1fr))`. Os cartões dos produtos se reorganizam automaticamente conforme a largura da tela (celular, tablet ou desktop).
- **Cards dos Produtos (`.card`)**: Possuem bordas suaves, sombra discreta e um efeito de elevação (*hover*) quando o usuário passa o mouse por cima (`transform: translateY(-4px)`).
- **Tratamento de Imagem (`.card img`)**: A propriedade `object-fit: contain` garante que as fotos dos produtos sejam redimensionadas proporcionalmente dentro de uma área de 180px, sem cortar nem distorcer a imagem original.
- **Hierarquia de Preço & Ação (`.meta`)**: O preço final é exibido em verde (`#16a34a`) com fonte em destaque (1.35rem, negrito). O botão de ação abre o link da loja em uma nova aba com os atributos de segurança `target="_blank" rel="noopener noreferrer"`.
- **Ponto de Injeção (`<!-- INSERT_CARDS_HERE -->`)**: Marcador utilizado pelo código Python / ADK para identificar o local exato onde a lista de cartões formatados deve ser colada.

---

## 2. Estrutura dos Cards Gerados Dinamicamente

Para cada produto contido no payload de dados, o agente deve gerar o seguinte fragmento HTML:

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
# Schema de Dados dos Produtos (JSON)

Este documento especifica o formato de dados obrigatório que a skill deve construir após a pesquisa de preços e antes de gerar o arquivo HTML final.

---

## Estrutura JSON (Payload)

O agente deve consolidar os produtos encontrados em um array de objetos JSON seguindo rigorosamente as chaves e tipos abaixo:

```json
[
  {
    "titulo": "Nome completo e formatado do produto",
    "preco": 299.90,
    "loja": "Nome da Loja Vendedora",
    "url_produto": "[https://link-direto-de-compra.com/produto](https://link-direto-de-compra.com/produto)",
    "url_imagem": "[https://link-da-imagem.com/foto.jpg](https://link-da-imagem.com/foto.jpg)"
  }
]
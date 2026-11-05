# SKILLS.md — Habilidades do Agente Wishlist HTML

Este arquivo instrui o harness/executor do agente sobre como orquestrar a recepção da lista de produtos, realizar as pesquisas de ofertas e compilar o arquivo final `.html`.

---

## Estrutura de Referências Disponíveis

O harness deve carregar e utilizar os seguintes recursos auxiliares localizados no diretório `references/`:

- **`references/schema.md`**: Especifica o contrato de dados JSON e os valores padrões (fallbacks) para os produtos pesquisados.
- **`references/template.md`**: Contém a estrutura do card HTML e o código base completo do arquivo `wishlist.html` com o CSS embutido.

---

## Habilidade Principal: `gerar_wishlist_html`

### 1. Triagem e Mensagem Inicial
Antes de iniciar qualquer busca, avalie o conteúdo da mensagem recebida:

- **Se a mensagem for vazia, saudação ou sem produtos explícitos**:
  - Interrompa a execução da skill e responda com a mensagem de boas-vindas:
    > "Olá! Sou seu assistente de Wishlist. Por favor, envie a lista de todos os itens que você deseja adquirir (ex: *Console PS5 Slim, Headset Gamer HyperX, Monitor 144Hz*). Vou pesquisar os melhores preços e criar uma página web (.html) exclusiva com a sua lista!"

- **Se a mensagem contiver uma lista de produtos**:
  - Extraia individualmente cada item mencionado e prossiga para a **Etapa 2**.

---

### 2. Pesquisa e Validação do Contrato de Dados (Schema)
Para cada produto extraído:

1. Execute a pesquisa de cotação para identificar o menor preço disponível no mercado.
2. Formate e valide o resultado de acordo com as especificações contidas em `references/schema.md`:
   - `titulo`: Nome formatado do produto.
   - `preco`: Valor numérico (float em BRL).
   - `loja`: Nome da loja vendedora.
   - `url_produto`: Link direto da oferta.
   - `url_imagem`: Link direto para a imagem do produto.
3. **Aplicação de Fallbacks**: Caso algum dado (como imagem ou loja) não seja encontrado na busca, aplique estritamente as regras e URLs padrões descritas na tabela de fallback do `references/schema.md`.

---

### 3. Renderização do HTML (Template)
Com o array de objetos JSON validado, consulte o arquivo `references/template.md` e siga os passos de renderização:

1. **Montagem dos Cards**: Para cada objeto do array JSON, gere o bloco `<div class="card">` utilizando a estrutura HTML informada na **Seção 2** do `references/template.md`.
2. **Interpolação de Variáveis**:
   - Substitua `{url_imagem}`, `{titulo}`, `{preco}`, `{loja}` e `{url_produto}` pelos respectivos valores processados.
3. **Compilação da Página**:
   - Carregue o código HTML base contido na **Seção 3** do `references/template.md`.
   - Substitua a tag de marcação `<!-- INSERT_CARDS_HERE -->` pela concatenação de todos os cards gerados.

---

### 4. Entrega e Finalização
1. Invoque a ferramenta de escrita de arquivos (`gerar_arquivo_html` ou equivalente do harness) e salve o código resultante no arquivo `wishlist.html`.
2. Responda ao usuário confirmando a conclusão:
   - Exiba um resumo textual simples dos produtos e preços encontrados.
   - Confirme que o arquivo `wishlist.html` foi gerado e está pronto para ser aberto em qualquer navegador.
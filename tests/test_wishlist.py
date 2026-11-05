"""Testes unitários para o Agente Wishlist e ferramentas ADK utilizando unittest."""

import unittest
from pathlib import Path
from wishlist_agent.models import ProductItem, DEFAULT_IMAGE_URL, DEFAULT_STORE
from wishlist_agent.tools import gerar_wishlist_html, pesquisar_ofertas_produto, format_brl_currency
from wishlist_agent.agent import root_agent


class TestWishlistAgent(unittest.TestCase):

    def test_product_item_validation(self):
        item = ProductItem(
            titulo="Playstation 5 Slim",
            preco=3499.00,
            loja="Amazon",
            url_produto="https://amazon.com.br/ps5",
            url_imagem="https://amazon.com.br/ps5.jpg",
        )
        self.assertEqual(item.titulo, "Playstation 5 Slim")
        self.assertEqual(item.preco, 3499.00)
        self.assertEqual(item.loja, "Amazon")
        self.assertEqual(item.url_produto, "https://amazon.com.br/ps5")
        self.assertEqual(item.url_imagem, "https://amazon.com.br/ps5.jpg")

    def test_product_item_fallbacks(self):
        item = ProductItem(
            titulo="Headset Gamer",
            preco="R$ 249,90",
            loja="",
            url_produto="",
            url_imagem="",
        )
        self.assertEqual(item.preco, 249.90)
        self.assertEqual(item.loja, DEFAULT_STORE)
        self.assertEqual(item.url_imagem, DEFAULT_IMAGE_URL)
        self.assertIn("google.com/search", item.url_produto)

    def test_format_brl_currency(self):
        self.assertEqual(format_brl_currency(3499.00), "3.499,00")
        self.assertEqual(format_brl_currency(299.9), "299,90")
        self.assertEqual(format_brl_currency(1234567.89), "1.234.567,89")

    def test_gerar_wishlist_html(self):
        produtos = [
            {
                "titulo": "Console PS5 Slim 1TB",
                "preco": 3499.00,
                "loja": "Amazon",
                "url_produto": "https://www.amazon.com.br/ps5",
                "url_imagem": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db",
            },
            {
                "titulo": "Headset Gamer HyperX",
                "preco": 249.90,
                "loja": "Kabum",
                "url_produto": "https://www.kabum.com.br",
                "url_imagem": "https://images.unsplash.com/photo-1546435770-a3e426bf472b",
            },
        ]

        res = gerar_wishlist_html(produtos)
        self.assertIn("Sucesso!", res)
        self.assertIn("Console PS5 Slim 1TB", res)

        html_file = Path("wishlist.html")
        self.assertTrue(html_file.exists())

        content = html_file.read_text(encoding="utf-8")
        self.assertIn("Console PS5 Slim 1TB", content)
        self.assertIn("Headset Gamer HyperX", content)
        self.assertIn("R$ 3.499,00", content)
        self.assertIn('target="_blank"', content)
        self.assertIn('rel="noopener noreferrer"', content)
        self.assertIn('<main class="grid">', content)

    def test_pesquisar_ofertas_produto(self):
        resultado = pesquisar_ofertas_produto("Playstation 5 Slim")
        self.assertIsInstance(resultado, dict)
        self.assertIn("titulo", resultado)
        self.assertIn("preco", resultado)
        self.assertIsInstance(resultado["preco"], float)
        self.assertIn("loja", resultado)
        self.assertIn("url_produto", resultado)
        self.assertIn("url_imagem", resultado)

        # Validações anti-alucinação adicionais
        res_guitarra = pesquisar_ofertas_produto("suporte de guitarra")
        self.assertNotEqual(res_guitarra["preco"], 199.90)
        self.assertNotIn("google.com/search", res_guitarra["url_produto"])
        self.assertIn("mercadolivre.com.br", res_guitarra["url_produto"])
        self.assertIn("guitarra", res_guitarra["titulo"].lower())

    def test_adk_agent_definition(self):
        self.assertEqual(root_agent.name, "wishlist_agent")
        self.assertEqual(len(root_agent.tools), 2)
        tool_names = [getattr(t, "__name__", getattr(t, "name", str(t))) for t in root_agent.tools]
        self.assertIn("google_search", tool_names)
        self.assertIn("gerar_wishlist_html", tool_names)
        self.assertIn("Olá! Sou seu assistente de Wishlist", root_agent.instruction)


if __name__ == "__main__":
    unittest.main()

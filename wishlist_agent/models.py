"""Modelos de dados Pydantic para validação do contrato de produtos da Wishlist.
Em conformidade com agent-skills/references/schema.md.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
import urllib.parse

DEFAULT_IMAGE_URL = (
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80"
)
DEFAULT_STORE = "Loja Confiável"


class ProductItem(BaseModel):
    """Representa um item de produto na Wishlist conforme schema.md."""

    titulo: str = Field(..., description="Nome completo e formatado do produto")
    preco: float = Field(..., description="Menor preço encontrado em Reais (BRL)")
    loja: str = Field(default=DEFAULT_STORE, description="Nome da loja vendedora da oferta")
    url_produto: str = Field(default="", description="Link direto de compra da oferta")
    url_imagem: str = Field(default=DEFAULT_IMAGE_URL, description="URL direta da imagem do produto")

    @field_validator("preco", mode="before")
    @classmethod
    def parse_preco(cls, v) -> float:
        if isinstance(v, (int, float)):
            return round(float(v), 2)
        if isinstance(v, str):
            # Limpa caracteres como 'R$', espaços, e ajusta separador decimal
            cleaned = (
                v.replace("R$", "")
                .replace("r$", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
            try:
                return round(float(cleaned), 2)
            except ValueError:
                return 0.0
        return 0.0

    @field_validator("loja", mode="before")
    @classmethod
    def validate_loja(cls, v) -> str:
        if not v or not str(v).strip():
            return DEFAULT_STORE
        return str(v).strip()

    @field_validator("url_imagem", mode="before")
    @classmethod
    def validate_imagem(cls, v) -> str:
        if not v or not str(v).strip() or not str(v).startswith("http"):
            return DEFAULT_IMAGE_URL
        return str(v).strip()

    @field_validator("url_produto", mode="before")
    @classmethod
    def validate_url_produto(cls, v, info) -> str:
        if not v or not str(v).strip() or not str(v).startswith("http"):
            # Se URL não fornecida ou inválida, gera link de busca no Google
            titulo = info.data.get("titulo", "produto") if hasattr(info, "data") else "produto"
            return f"https://www.google.com/search?q={urllib.parse.quote(str(titulo))}"
        return str(v).strip()

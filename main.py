#!/usr/bin/env python3
"""Ponto de entrada para execução do WishList Agent utilizando o Google ADK.

Uso:
  python main.py                     -> Inicia o chat interativo com o agente via Google ADK
  python main.py "itens desejados"   -> Executa o agente para uma consulta pontual
  adk run wishlist_agent             -> Execução nativa direta pelo CLI do Google ADK
  adk web .                          -> Inicia a interface Web oficial do Google ADK
"""

import sys
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente de .env se existir
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
AGENT_DIR = PROJECT_ROOT / "wishlist_agent"


def print_banner():
    print("=" * 68)
    print("🛒  WishList HTML Creator Agent (Google ADK)")
    print("=" * 68)
    print("💡 Digite seus produtos desejados para pesquisar os menores preços")
    print("   e gerar a página web 'wishlist.html' estilizada.")
    print("=" * 68)
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  AVISO: Chave GEMINI_API_KEY não encontrada no ambiente ou .env.")
        print("   Para habilitar o modelo Gemini e a busca web ao vivo, configure:")
        print("   export GEMINI_API_KEY='sua_chave_aqui'")
        print("=" * 68)
    print()


def main():
    print_banner()

    # Monta comando do Google ADK CLI
    cmd = ["adk", "run", str(AGENT_DIR)]

    # Se o usuário passou argumentos adicionais na linha de comando
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        cmd.append(query)

    try:
        # Executa o processo do Google ADK conectando stdout/stdin interativamente
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\nSessão encerrada pelo usuário. Até logo!")
    except FileNotFoundError:
        print("Erro: Comando 'adk' não encontrado no PATH do sistema.")
        print("Certifique-se de que o pacote google-adk está instalado (`pip install google-adk`).")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()

"""
=========================================================
Tarifador Asterisk

config.py

Configurações gerais do projeto

=========================================================
"""

from pathlib import Path

VERSAO = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent

PASTA_ARQUIVOS = BASE_DIR / "arquivos"
PASTA_LOGS = BASE_DIR / "logs"
PASTA_TEMP = BASE_DIR / "temp"

NOME_PROJETO = "Tarifador Asterisk"
"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    constants.py

Descrição:
    Constantes utilizadas em todo o projeto.

Versão:
    2.0.0

=========================================================
"""

# ==========================================================
# Telefonia
# ==========================================================

# Quantidade de dígitos

TAMANHO_RAMAL = 4

TAMANHO_LOCAL = 8

TAMANHO_DDD_FIXO = 10

TAMANHO_DDD_CELULAR = 11


# ==========================================================
# Prefixos
# ==========================================================

PREFIXO_INTERNACIONAL = "00"

PREFIXO_0300 = "0300"

PREFIXO_0800 = "0800"

PREFIXO_300 = "300"

PREFIXO_400 = "400"


# ==========================================================
# Prefixos de Operadoras
# ==========================================================

PREFIXOS_OPERADORA = (
    "012",
    "015",
    "021",
    "023",
    "025",
    "031",
    "041",
    "043",
)


# ==========================================================
# Contextos do Asterisk
# ==========================================================

CONTEXTO_RAMAIS = "ramais"

CONTEXTO_EXTERNO = "externo"


# ==========================================================
# Arquivos
# ==========================================================

ARQUIVO_RAMAIS = "pjsip.ramais"

ARQUIVO_CDR = "Master.csv"

ARQUIVO_VIVO = "VIVO.csv"


# ==========================================================
# CSV
# ==========================================================

SEPARADOR_CSV = ";"

ENCODING_CSV = "utf-8-sig"
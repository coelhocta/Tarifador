"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    telefone.py

Descrição:
    Funções relacionadas à manipulação de números telefônicos.

Versão:
    2.0.1

=========================================================
"""

from core.constants import (
    PREFIXO_INTERNACIONAL,
    PREFIXO_0300,
    PREFIXO_0800,
    PREFIXO_300,
    PREFIXO_400,
    PREFIXOS_OPERADORA,
    TAMANHO_RAMAL,
    TAMANHO_LOCAL,
    TAMANHO_DDD_FIXO,
    TAMANHO_DDD_CELULAR,
)

from core.models import TipoDestino
from core.utils import somente_digitos


# ==========================================================
# Normalização
# ==========================================================

def remover_prefixo_internacional(numero: str) -> str:
    """Remove o prefixo internacional (00)."""

    while numero.startswith(PREFIXO_INTERNACIONAL):
        numero = numero[2:]

    return numero


def remover_prefixo_operadora(numero: str) -> str:
    """Remove o código da operadora."""

    for prefixo in PREFIXOS_OPERADORA:
        if numero.startswith(prefixo):
            return numero[len(prefixo):]

    return numero


def remover_zero_inicial(numero: str) -> str:
    """Remove um único zero inicial."""

    if numero.startswith("0"):
        return numero[1:]

    return numero


def normalizar_numero(numero: str | None) -> str:
    """
    Normaliza um número telefônico.
    """

    numero = somente_digitos(numero)

    if not numero:
        return ""

    numero = remover_prefixo_internacional(numero)

    numero = remover_prefixo_operadora(numero)

    # IMPORTANTE:
    # O zero faz parte dos números 0800 e 0300.
    if not (
        numero.startswith(PREFIXO_0800)
        or numero.startswith(PREFIXO_0300)
    ):
        numero = remover_zero_inicial(numero)

    return numero


# ==========================================================
# Classificação
# ==========================================================

def identificar_tipo_destino(numero: str | None) -> TipoDestino:
    """
    Identifica o tipo do número telefônico.
    """

    numero = normalizar_numero(numero)

    if not numero:
        return TipoDestino.DESCONHECIDO

    # Serviços vêm primeiro
    if numero.startswith(PREFIXO_0800):
        return TipoDestino.SERVICO_0800

    if numero.startswith(PREFIXO_0300):
        return TipoDestino.SERVICO_0300

    if numero.startswith(PREFIXO_300):
        return TipoDestino.SERVICO_300X

    if numero.startswith(PREFIXO_400):
        return TipoDestino.SERVICO_400X

    # Ramal
    if len(numero) == TAMANHO_RAMAL:
        return TipoDestino.RAMAL

    # Telefones
    if len(numero) == TAMANHO_LOCAL:
        return TipoDestino.LOCAL

    if len(numero) == TAMANHO_DDD_FIXO:
        return TipoDestino.DDD_FIXO

    if len(numero) == TAMANHO_DDD_CELULAR:
        return TipoDestino.DDD_CELULAR

    return TipoDestino.DESCONHECIDO


# ==========================================================
# Extração
# ==========================================================

def extrair_ddd(numero: str | None) -> str:
    """Retorna o DDD."""

    numero = normalizar_numero(numero)

    tipo = identificar_tipo_destino(numero)

    if tipo in (TipoDestino.DDD_FIXO, TipoDestino.DDD_CELULAR):
        return numero[:2]

    return ""


def extrair_numero_local(numero: str | None) -> str:
    """Retorna apenas o número local."""

    numero = normalizar_numero(numero)

    tipo = identificar_tipo_destino(numero)

    if tipo == TipoDestino.LOCAL:
        return numero

    if tipo in (TipoDestino.DDD_FIXO, TipoDestino.DDD_CELULAR):
        return numero[2:]

    return numero


# ==========================================================
# Comparação
# ==========================================================

def telefone_comparacao(numero: str | None) -> str:
    """
    Retorna a chave utilizada na conciliação.
    """

    numero = normalizar_numero(numero)

    tipo = identificar_tipo_destino(numero)

    if tipo == TipoDestino.RAMAL:
        return numero

    if tipo == TipoDestino.LOCAL:
        return numero

    if tipo in (TipoDestino.DDD_FIXO, TipoDestino.DDD_CELULAR):
        return numero[2:]

    if tipo in (
        TipoDestino.SERVICO_0800,
        TipoDestino.SERVICO_0300,
        TipoDestino.SERVICO_300X,
        TipoDestino.SERVICO_400X,
    ):
        return numero

    return numero
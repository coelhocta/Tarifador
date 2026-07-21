"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    utils.py

Descrição:
    Funções utilitárias utilizadas em todo o projeto.

Versão:
    2.0.0

=========================================================
"""

from datetime import datetime
import re


# ==========================================================
# Texto
# ==========================================================

def somente_digitos(texto: str | None) -> str:
    """
    Retorna apenas os dígitos de uma string.

    Exemplos:

        "(16) 3203-4091"
        -> "1632034091"

        "001632034091"
        -> "001632034091"
    """

    if texto is None:
        return ""

    return re.sub(r"\D", "", str(texto))


# ==========================================================
# Data e Hora
# ==========================================================

def texto_para_data_hora(texto: str) -> datetime:
    """
    Converte texto para datetime.

    Formato esperado:

        YYYY-MM-DD HH:MM:SS
    """

    return datetime.strptime(texto, "%Y-%m-%d %H:%M:%S")


def data_hora_para_texto(data: datetime) -> str:
    """
    Converte datetime para texto.

    Retorno:

        YYYY-MM-DD HH:MM:SS
    """

    return data.strftime("%Y-%m-%d %H:%M:%S")


def data_para_texto_br(data: datetime) -> str:
    """
    Retorna apenas a data no formato brasileiro.

        DD/MM/YYYY
    """

    return data.strftime("%d/%m/%Y")


def hora_para_texto(data: datetime) -> str:
    """
    Retorna apenas a hora.

        HH:MM:SS
    """

    return data.strftime("%H:%M:%S")


# ==========================================================
# Tempo
# ==========================================================

def segundos_para_hhmmss(segundos: int) -> str:
    """
    Converte segundos para HH:MM:SS.

    Exemplos:

        65
        -> 00:01:05

        3725
        -> 01:02:05
    """

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f"{horas:02}:{minutos:02}:{segundos:02}"


# ==========================================================
# Validação
# ==========================================================

def esta_vazio(valor) -> bool:
    """
    Retorna True se o valor estiver vazio.
    """

    if valor is None:
        return True

    if isinstance(valor, str):
        return valor.strip() == ""

    return False
"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    inferencia.py

Descrição:
    Inferência de ramais utilizando histórico
    de chamadas conciliadas.

=========================================================
"""

from core.models import ResultadoConciliacao


def inferir_resultados(
    resultados: list[ResultadoConciliacao],
) -> None:
    """
    Aplica inferência aos resultados da conciliação.
    """

    pass
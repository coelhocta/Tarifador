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

from core.padroes import construir_historico


def aplicar_inferencia(
    resultados: list[ResultadoConciliacao],
) -> None:
    """
    Aplica inferência aos resultados da conciliação.
    """

    historico = construir_historico(resultados)

    # Ainda não faz nada.
    _ = historico
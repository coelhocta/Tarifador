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

from core.models import (
    ResultadoConciliacao,
    StatusConciliacao,
)

from core.padroes import (
    construir_historico,
    construir_indice_ramais,
    obter_ramal_preferencial,
)


def aplicar_inferencia(
    resultados: list[ResultadoConciliacao],
) -> None:
    """
    Aplica inferência aos resultados da conciliação.
    """

    historico = construir_historico(resultados)
    indice_ramais = construir_indice_ramais(resultados)

    for resultado in resultados:

        if (
            resultado.status
            != StatusConciliacao.NAO_ENCONTRADA
        ):
            continue

        destino = (
            resultado.chamada_vivo
            .chave_comparacao
            .split("|")[1]
        )

        ramal = obter_ramal_preferencial(
            historico,
            destino,
        )

        if ramal is None:
            continue

        resultado.status = (
            StatusConciliacao.INFERIDA
        )

        resultado.ramal_inferido = ramal

        resultado.nome_ramal_inferido = (
            indice_ramais[ramal]
        )
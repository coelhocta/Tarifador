"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    inferencia_asterisk.py

Descrição:
    Inferência utilizando todo o histórico de chamadas
    do Asterisk.
    
    Somente resultados com status
    NAO_ENCONTRADA são processados.

=========================================================
"""

from core.models import (
    ChamadaAsterisk,
    ResultadoConciliacao,
    StatusConciliacao,
)

from core.padroes import (
    construir_historico_asterisk,
    obter_estatistica_preferencial,
)


def aplicar_inferencia_asterisk(
    resultados: list[ResultadoConciliacao],
    chamadas: list[ChamadaAsterisk],
) -> None:
    """
    Aplica inferência utilizando todo o histórico
    do Asterisk.
    """

    historico = construir_historico_asterisk(
        chamadas
    )

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

        preferencial = (
            obter_estatistica_preferencial(
                historico,
                destino,
            )
        )

        if preferencial is None:
            continue

        ramal, estatistica = preferencial

        resultado.ramal_inferido = ramal
        resultado.nome_ramal_inferido = (
            estatistica.nome
        )

        resultado.status = (
            StatusConciliacao.INFERIDA
        )
"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    padroes.py

Descrição:
    Construção do histórico de padrões de ligação.

Versão:
    1.0.0

=========================================================
"""

from collections import Counter

from core.models import (
    ResultadoConciliacao,
    StatusConciliacao,
)

MIN_OCORRENCIAS_PADRAO = 2


def construir_historico(
    resultados: list[ResultadoConciliacao],
) -> dict[str, Counter]:
    """
    Constrói um histórico de ocorrências por destino.

    Apenas chamadas conciliadas com sucesso são utilizadas.
    """

    historico: dict[str, Counter] = {}

    for resultado in resultados:

        if (
            resultado.status
            != StatusConciliacao.ENCONTRADA
        ):
            continue

        destino = (
            resultado.chamada_vivo
            .chave_comparacao
            .split("|")[1]
        )

        ramal = resultado.chamada_asterisk.ramal

        if destino not in historico:
            historico[destino] = Counter()

        historico[destino][ramal] += 1

    return historico


def obter_ramal_preferencial(
    historico: dict[str, Counter],
    destino: str,
) -> str | None:
    """
    Retorna o ramal mais frequente para um destino.

    Apenas considera destinos que possuam pelo menos
    MIN_OCORRENCIAS_PADRAO ocorrências.
    """

    contador = historico.get(destino)

    if contador is None:
        return None

    ramal, ocorrencias = contador.most_common(1)[0]

    if ocorrencias < MIN_OCORRENCIAS_PADRAO:
        return None

    return ramal


def construir_indice_ramais(
    resultados: list[ResultadoConciliacao],
) -> dict[str, str]:
    """
    Constrói um índice contendo o nome de cada ramal.

    Retorna:

    {
        "7476": "Andre",
        "7480": "Carlos",
    }
    """

    indice: dict[str, str] = {}

    for resultado in resultados:

        if (
            resultado.status
            != StatusConciliacao.ENCONTRADA
        ):
            continue

        chamada = resultado.chamada_asterisk

        if chamada is None:
            continue

        indice[chamada.ramal] = chamada.nome_ramal

    return indice

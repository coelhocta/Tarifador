"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    conciliador.py

Descrição:
    Conciliação das chamadas do Asterisk com a fatura
    da operadora.

Versão:
    2.0.0

=========================================================
"""

from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    ResultadoConciliacao,
    StatusConciliacao,
)


def conciliar(
    chamadas_asterisk: list[ChamadaAsterisk],
    chamadas_vivo: list[ChamadaVivo],
) -> list[ResultadoConciliacao]:
    """
    Concilia as cobranças da Vivo com as chamadas do Asterisk.
    """

    resultados: list[ResultadoConciliacao] = []

    uniqueids_utilizados: set[str] = set()

    for chamada_vivo in chamadas_vivo:

        candidatos_exatos: list[ChamadaAsterisk] = []
        candidatos_proximo_minuto: list[ChamadaAsterisk] = []

        for chamada_asterisk in chamadas_asterisk:

            if chamada_asterisk.uniqueid in uniqueids_utilizados:
                continue

            if (
                chamada_asterisk.chave_comparacao
                == chamada_vivo.chave_comparacao
            ):
                candidatos_exatos.append(
                    chamada_asterisk
                )

            elif (
                chamada_asterisk.chave_comparacao_proximo_minuto
                == chamada_vivo.chave_comparacao
            ):
                candidatos_proximo_minuto.append(
                    chamada_asterisk
                )

        if candidatos_exatos:

            candidatos = candidatos_exatos

        else:

            candidatos = candidatos_proximo_minuto

        if candidatos:

            chamada_encontrada = min(
                candidatos,
                key=lambda chamada: abs(
                    chamada.duracao_segundos
                    - chamada_vivo.duracao_segundos
                ),
            )

            uniqueids_utilizados.add(
                chamada_encontrada.uniqueid
            )

            resultado = ResultadoConciliacao(
                chamada_vivo=chamada_vivo,
                chamada_asterisk=chamada_encontrada,
                status=StatusConciliacao.ENCONTRADA,
            )

        else:

            resultado = ResultadoConciliacao(
                chamada_vivo=chamada_vivo,
                chamada_asterisk=None,
                status=StatusConciliacao.NAO_ENCONTRADA,
            )

        resultados.append(resultado)

    return resultados
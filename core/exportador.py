"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    exportador.py

Descrição:
    Exportação dos registros de cobrança do SATA.

=========================================================
"""

from csv import writer
from pathlib import Path

from core.cobranca import RegistroCobranca

from core.models import (
    ResultadoConciliacao,
    StatusConciliacao,
)


def exportar_cobrancas(
    registros: list[RegistroCobranca],
    arquivo: Path,
) -> None:
    """
    Exporta os registros de cobrança identificados
    para um arquivo CSV.
    """

    with arquivo.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as csvfile:

        escritor = writer(
            csvfile,
            delimiter=";",
        )

        escritor.writerow([
            "Ramal",
            "Nome/Setor",
            "Data",
            "Hora",
            "Destino",
            "Tipo",
            "Duracao",
            "Valor",
        ])

        for registro in registros:

            escritor.writerow([
                registro.ramal,
                registro.nome_ramal,
                registro.data_hora.strftime(
                    "%d/%m/%Y"
                ),
                registro.data_hora.strftime(
                    "%H:%M:%S"
                ),
                registro.destino,
                registro.tipo_vivo,
                _formatar_duracao(
                    registro.duracao_segundos
                ),
                _formatar_valor(
                    registro.valor
                ),
            ])


def _formatar_duracao(
    segundos: int,
) -> str:
    """
    Converte segundos para HH:MM:SS.
    """

    horas = segundos // 3600

    minutos = (
        segundos % 3600
    ) // 60

    segundos_restantes = segundos % 60

    return (
        f"{horas:02d}:"
        f"{minutos:02d}:"
        f"{segundos_restantes:02d}"
    )


def _formatar_valor(
    valor,
) -> str:
    """
    Formata valor monetário utilizando vírgula decimal.
    """

    return f"{valor:.2f}".replace(".", ",")


def exportar_cobrancas_nao_identificadas(
    resultados: list[ResultadoConciliacao],
    arquivo: Path,
) -> None:
    """
    Exporta cobranças da Vivo que não foram
    identificadas no Asterisk.
    """

    with arquivo.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as csvfile:

        escritor = writer(
            csvfile,
            delimiter=";",
        )

        escritor.writerow([
            "Data",
            "Hora",
            "Destino",
            "Tipo",
            "Duracao",
            "Valor",
        ])

        for resultado in resultados:

            if (
                resultado.status
                != StatusConciliacao.NAO_ENCONTRADA
            ):
                continue

            chamada = resultado.chamada_vivo

            escritor.writerow([
                chamada.data_hora.strftime(
                    "%d/%m/%Y"
                ),
                chamada.data_hora.strftime(
                    "%H:%M:%S"
                ),
                chamada.destino,
                chamada.tipo_vivo,
                _formatar_duracao(
                    chamada.duracao_segundos
                ),
                _formatar_valor(
                    chamada.valor
                ),
            ])
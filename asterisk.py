"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    asterisk.py

Descrição:
    Importação das chamadas exportadas pelo Asterisk.

Versão:
    1.0.0

=========================================================
"""

from csv import DictReader
from datetime import datetime
from pathlib import Path

from core.models import ChamadaAsterisk, OrigemDados
from core.telefone import identificar_tipo_destino
from core.utils import (
    gerar_chave_comparacao,
    gerar_chave_comparacao_proximo_minuto,
)


def carregar_chamadas(
    arquivo: Path,
) -> list[ChamadaAsterisk]:
    """
    Carrega um arquivo CSV exportado pelo Asterisk.

    Retorna:

        list[ChamadaAsterisk]
    """

    if not arquivo.exists():
        raise FileNotFoundError(arquivo)

    with arquivo.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csvfile:

        leitor = DictReader(
            csvfile,
            delimiter=";",
            skipinitialspace=True,
        )

        _validar_cabecalho(leitor.fieldnames)

        chamadas = []

        for linha in leitor:

            chamadas.append(
                _criar_chamada(linha)
            )

    return chamadas


def _validar_cabecalho(
    cabecalho: list[str] | None,
) -> None:
    """
    Valida o cabeçalho do CSV.
    """

    esperado = [
        "Ramal",
        "Nome",
        "Data",
        "Hora",
        "Duracao",
        "Destino",
        "UniqueID",
    ]

    if cabecalho != esperado:
        raise ValueError(
            "Cabeçalho do arquivo inválido."
        )


def _criar_chamada(
    linha: dict[str, str],
) -> ChamadaAsterisk:
    """
    Converte uma linha do CSV em um objeto ChamadaAsterisk.
    """

    data_hora = datetime.strptime(
        f'{linha["Data"]} {linha["Hora"]}',
        "%d/%m/%Y %H:%M:%S",
    )

    ramal = linha["Ramal"].strip()

    nome_ramal = linha["Nome"].strip()

    destino = linha["Destino"].strip()

    uniqueid = linha["UniqueID"].strip()

    return ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,

        chave_id=uniqueid,

        chave_comparacao=gerar_chave_comparacao(
            data_hora,
            destino,
        ),

        chave_comparacao_proximo_minuto=
        gerar_chave_comparacao_proximo_minuto(
            data_hora,
            destino,
        ),

        data_hora=data_hora,

        destino=destino,

        tipo_destino=identificar_tipo_destino(
            destino,
        ),

        duracao_segundos=int(
            linha["Duracao"]
        ),

        ramal=ramal,

        nome_ramal=nome_ramal,

        uniqueid=uniqueid,
        
    )
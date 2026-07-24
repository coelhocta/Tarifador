"""
=========================================================
SATA

Sistema de Auditoria Telefonica para Asterisk

Arquivo:
    teste_integracao.py

Descricao:
    Testes de integracao do pipeline do SATA.

=========================================================
"""

from datetime import datetime
from decimal import Decimal

from core.conciliador import conciliar
from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    OrigemDados,
    StatusConciliacao,
)

from pathlib import Path

from core.importador_asterisk import (
    carregar_chamadas as carregar_chamadas_asterisk,
)

from core.importador_vivo import (
    carregar_chamadas as carregar_chamadas_vivo,
)


def teste_pipeline_conciliacao():

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 25),
        destino="3510-1711",
        duracao_segundos=58,
        ramal="7001",
        nome_ramal="SETOR A",
        uniqueid="123456",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 30),
        destino="3510-1711",
        duracao_segundos=60,
        valor=Decimal("0.61"),
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert (
        resultado.status
        == StatusConciliacao.ENCONTRADA
    )

    assert resultado.chamada_asterisk is chamada_asterisk
    assert resultado.chamada_vivo is chamada_vivo

    # Dados de identificação vindos do Asterisk
    assert resultado.chamada_asterisk.ramal == "7001"
    assert resultado.chamada_asterisk.nome_ramal == "SETOR A"

    # Dados da cobrança vindos da Vivo
    assert resultado.chamada_vivo.data_hora == datetime(
        2026, 6, 25, 10, 2, 30
    )

    assert resultado.chamada_vivo.destino == "3510-1711"
    assert resultado.chamada_vivo.duracao_segundos == 60
    assert resultado.chamada_vivo.valor == Decimal("0.61")
    
    
def teste_pipeline_com_csv_vivo():

    chamadas_vivo = carregar_chamadas_vivo(
        Path("dados_teste") / "vivo_uma_ligacao.csv"
    )

    assert len(chamadas_vivo) == 1

    chamada_vivo = chamadas_vivo[0]

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 25),
        destino="3510-1711",
        duracao_segundos=58,
        ramal="7001",
        nome_ramal="SETOR A",
        uniqueid="123456",
    )

    resultados = conciliar(
        [chamada_asterisk],
        chamadas_vivo,
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert (
        resultado.status
        == StatusConciliacao.ENCONTRADA
    )

    assert resultado.chamada_asterisk is chamada_asterisk

    assert resultado.chamada_asterisk.ramal == "7001"
    assert resultado.chamada_asterisk.nome_ramal == "SETOR A"

    assert resultado.chamada_vivo.data_hora == datetime(
        2026, 6, 25, 10, 2, 30
    )

    assert resultado.chamada_vivo.destino == "3510-1711"
    assert resultado.chamada_vivo.duracao_segundos == 60
    assert resultado.chamada_vivo.valor == Decimal("0.61")
    
    
def teste_pipeline_completo_com_csvs():

    chamadas_asterisk = carregar_chamadas_asterisk(
        Path("dados_teste") / "asterisk_integracao.csv"
    )

    chamadas_vivo = carregar_chamadas_vivo(
        Path("dados_teste") / "vivo_uma_ligacao.csv"
    )

    assert len(chamadas_asterisk) == 1
    assert len(chamadas_vivo) == 1

    resultados = conciliar(
        chamadas_asterisk,
        chamadas_vivo,
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert (
        resultado.status
        == StatusConciliacao.ENCONTRADA
    )

    assert resultado.chamada_asterisk is not None

    # Identificação: Asterisk
    assert resultado.chamada_asterisk.ramal == "7001"
    assert (
        resultado.chamada_asterisk.nome_ramal
        == "SETOR A"
    )

    # Cobrança: Vivo
    assert resultado.chamada_vivo.data_hora == datetime(
        2026, 6, 25, 10, 2, 30
    )

    assert (
        resultado.chamada_vivo.destino
        == "3510-1711"
    )

    assert (
        resultado.chamada_vivo.duracao_segundos
        == 60
    )

    assert (
        resultado.chamada_vivo.valor
        == Decimal("0.61")
    )
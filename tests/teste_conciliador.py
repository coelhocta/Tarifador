"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_conciliador.py

Descrição:
    Testes do módulo conciliador.py.

Versão:
    2.0.0

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


def teste_encontra_chamada_por_chave_exata():

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 30),
        destino="3510-1711",
        duracao_segundos=60,
        ramal="7001",
        nome_ramal="TESTE",
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

    assert (
        resultado.chamada_vivo
        is chamada_vivo
    )

    assert (
        resultado.chamada_asterisk
        is chamada_asterisk
    )
    
    
def teste_encontra_chamada_no_proximo_minuto():

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 59),
        destino="3510-1711",
        duracao_segundos=60,
        ramal="7001",
        nome_ramal="TESTE",
        uniqueid="123456",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:03|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:04|35101711",
        data_hora=datetime(2026, 6, 25, 10, 3, 0),
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

    assert (
        resultado.chamada_vivo
        is chamada_vivo
    )

    assert (
        resultado.chamada_asterisk
        is chamada_asterisk
    )
    
   
def teste_chamada_vivo_nao_encontrada():

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
        [],
        [chamada_vivo],
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert (
        resultado.status
        == StatusConciliacao.NAO_ENCONTRADA
    )

    assert (
        resultado.chamada_vivo
        is chamada_vivo
    )

    assert resultado.chamada_asterisk is None
    

def teste_escolhe_candidato_pela_duracao():

    chamada_curta = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:00|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:01|35101711",
        data_hora=datetime(2026, 6, 25, 10, 0, 0),
        destino="3510-1711",
        duracao_segundos=5,
        ramal="7001",
        nome_ramal="SETOR A",
        uniqueid="123456",
    )

    chamada_correta = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-2",
        chave_comparacao="2026-06-25 10:00|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:01|35101711",
        data_hora=datetime(2026, 6, 25, 10, 0, 45),
        destino="3510-1711",
        duracao_segundos=600,
        ramal="7002",
        nome_ramal="SETOR B",
        uniqueid="123457",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:00|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:01|35101711",
        data_hora=datetime(2026, 6, 25, 10, 0, 50),
        destino="3510-1711",
        duracao_segundos=600,
        valor=Decimal("6.15"),
    )

    resultados = conciliar(
        [
            chamada_curta,
            chamada_correta,
        ],
        [chamada_vivo],
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert (
        resultado.status
        == StatusConciliacao.ENCONTRADA
    )

    assert (
        resultado.chamada_asterisk
        is chamada_correta
    )
    

def teste_prioriza_minuto_exato():

    chamada_minuto_anterior = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:01|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:02|35101711",
        data_hora=datetime(2026, 6, 25, 10, 1, 59),
        destino="3510-1711",
        duracao_segundos=600,
        ramal="7001",
        nome_ramal="SETOR A",
        uniqueid="123456",
    )

    chamada_minuto_exato = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-2",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 10),
        destino="3510-1711",
        duracao_segundos=590,
        ramal="7002",
        nome_ramal="SETOR B",
        uniqueid="123457",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 20),
        destino="3510-1711",
        duracao_segundos=600,
        valor=Decimal("6.15"),
    )

    resultados = conciliar(
        [
            chamada_minuto_anterior,
            chamada_minuto_exato,
        ],
        [chamada_vivo],
    )

    resultado = resultados[0]

    assert (
        resultado.chamada_asterisk
        is chamada_minuto_exato
    )
    
    
def teste_chamada_asterisk_nao_pode_ser_reutilizada():

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="asterisk-1",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 10),
        destino="3510-1711",
        duracao_segundos=60,
        ramal="7001",
        nome_ramal="SETOR A",
        uniqueid="123456",
    )

    chamada_vivo_1 = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 20),
        destino="3510-1711",
        duracao_segundos=60,
        valor=Decimal("0.61"),
    )

    chamada_vivo_2 = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 40),
        destino="3510-1711",
        duracao_segundos=60,
        valor=Decimal("0.61"),
    )

    resultados = conciliar(
        [chamada_asterisk],
        [
            chamada_vivo_1,
            chamada_vivo_2,
        ],
    )

    assert len(resultados) == 2

    assert (
        resultados[0].status
        == StatusConciliacao.ENCONTRADA
    )

    assert (
        resultados[0].chamada_asterisk
        is chamada_asterisk
    )

    assert (
        resultados[1].status
        == StatusConciliacao.NAO_ENCONTRADA
    )

    assert (
        resultados[1].chamada_asterisk
        is None
    )
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
    
    
def teste_concilia_ddd_com_ddd_somente_no_asterisk():

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779730567.1827",
        chave_comparacao="2026-05-25 14:36|1432278099",
        chave_comparacao_proximo_minuto="2026-05-25 14:37|1432278099",
        data_hora=datetime(2026, 5, 25, 14, 36, 7),
        destino="1432278099",
        duracao_segundos=59,
        ramal="7476",
        nome_ramal="",
        uniqueid="1779730567.1827",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-25 14:36|32278099",
        chave_comparacao_proximo_minuto="2026-05-25 14:37|32278099",
        data_hora=datetime(2026, 5, 25, 14, 36, 6),
        destino="3227-8099",
        duracao_segundos=66,
        valor=Decimal("0.68"),
        tipo_destino="DDD",
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
        resultado.chamada_asterisk
        is chamada_asterisk
    )

    assert resultado.chamada_asterisk.ramal == "7476"
    
    
def teste_ddd_escolhe_candidato_mais_proximo_no_tempo():

    chamada_antiga = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779730413.1774",
        chave_comparacao="2026-05-25 14:33|1432278099",
        chave_comparacao_proximo_minuto="2026-05-25 14:34|1432278099",
        data_hora=datetime(2026, 5, 25, 14, 33, 33),
        destino="1432278099",
        duracao_segundos=18,
        ramal="7478",
        nome_ramal="",
        uniqueid="1779730413.1774",
    )

    chamada_correta = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779730567.1827",
        chave_comparacao="2026-05-25 14:36|1432278099",
        chave_comparacao_proximo_minuto="2026-05-25 14:37|1432278099",
        data_hora=datetime(2026, 5, 25, 14, 36, 7),
        destino="1432278099",
        duracao_segundos=59,
        ramal="7476",
        nome_ramal="",
        uniqueid="1779730567.1827",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-25 14:36|32278099",
        chave_comparacao_proximo_minuto="2026-05-25 14:37|32278099",
        data_hora=datetime(2026, 5, 25, 14, 36, 6),
        destino="3227-8099",
        duracao_segundos=66,
        valor=Decimal("0.68"),
        tipo_destino="DDD",
    )

    resultados = conciliar(
        [
            chamada_antiga,
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

    assert resultado.chamada_asterisk.ramal == "7476"
    
    
def teste_ddd_aceita_diferenca_de_42_segundos():
    """
    Caso real observado na fatura Vivo.

    Vivo:
        26/05/2026 14:34:06
        3227-8099
        DDD
        60 segundos

    Asterisk:
        26/05/2026 14:34:48
        14 3227-8099
        17 segundos
        Ramal 7476

    A diferenca entre os horarios e de 42 segundos.
    """

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779816888.5204",
        chave_comparacao="2026-05-26 14:34|1432278099",
        chave_comparacao_proximo_minuto="2026-05-26 14:35|1432278099",
        data_hora=datetime(2026, 5, 26, 14, 34, 48),
        destino="1432278099",
        duracao_segundos=17,
        ramal="7476",
        nome_ramal="",
        uniqueid="1779816888.5204",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-26 14:34|32278099",
        chave_comparacao_proximo_minuto="2026-05-26 14:35|32278099",
        data_hora=datetime(2026, 5, 26, 14, 34, 6),
        destino="3227-8099",
        duracao_segundos=60,
        valor=Decimal("0.61"),
        tipo_destino="DDD",
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert resultado.status == StatusConciliacao.ENCONTRADA
    assert resultado.chamada_asterisk is chamada_asterisk
    assert resultado.chamada_asterisk.ramal == "7476"


def teste_numero_compativel_nao_aceita_diferenca_acima_de_60_segundos():
    """
    A conciliacao alternativa por numero deve respeitar
    o limite maximo de 60 segundos.
    """

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="teste-61",
        chave_comparacao="2026-05-26 14:35|1432278099",
        chave_comparacao_proximo_minuto="2026-05-26 14:36|1432278099",
        data_hora=datetime(2026, 5, 26, 14, 35, 7),
        destino="1432278099",
        duracao_segundos=60,
        ramal="7476",
        nome_ramal="",
        uniqueid="teste-61",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-26 14:34|32278099",
        chave_comparacao_proximo_minuto="2026-05-26 14:35|32278099",
        data_hora=datetime(2026, 5, 26, 14, 34, 6),
        destino="3227-8099",
        duracao_segundos=60,
        valor=Decimal("0.61"),
        tipo_destino="DDD",
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1

    resultado = resultados[0]

    assert resultado.status == StatusConciliacao.NAO_ENCONTRADA
    assert resultado.chamada_asterisk is None
    
    
def teste_concilia_vc1_com_numero_sem_ddd_no_asterisk():
    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779804842.2401",
        chave_comparacao="2026-05-26 11:14|998005377",
        chave_comparacao_proximo_minuto="2026-05-26 11:15|998005377",
        data_hora=datetime(2026, 5, 26, 11, 14, 2),
        destino="998005377",
        duracao_segundos=5,
        ramal="7149",
        nome_ramal="SAC RECE FISI",
        uniqueid="1779804842.2401",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-26 11:14|998005377",
        chave_comparacao_proximo_minuto="2026-05-26 11:15|998005377",
        data_hora=datetime(2026, 5, 26, 11, 14, 0),
        destino="99800-5377",
        duracao_segundos=30,
        valor=Decimal("0.30"),
        tipo_destino="VC1",
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1
    assert resultados[0].status == StatusConciliacao.ENCONTRADA
    assert resultados[0].chamada_asterisk is chamada_asterisk
    assert resultados[0].chamada_asterisk.ramal == "7149"


def teste_concilia_vc3_com_ddd_diferente_no_asterisk():
    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779806153.2786",
        chave_comparacao="2026-05-26 11:35|61984401626",
        chave_comparacao_proximo_minuto="2026-05-26 11:36|61984401626",
        data_hora=datetime(2026, 5, 26, 11, 35, 53),
        destino="61984401626",
        duracao_segundos=7,
        ramal="7149",
        nome_ramal="SAC RECE FISI",
        uniqueid="1779806153.2786",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-26 11:35|984401626",
        chave_comparacao_proximo_minuto="2026-05-26 11:36|984401626",
        data_hora=datetime(2026, 5, 26, 11, 35, 54),
        destino="98440-1626",
        duracao_segundos=30,
        valor=Decimal("0.44"),
        tipo_destino="VC3",
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1
    assert resultados[0].status == StatusConciliacao.ENCONTRADA
    assert resultados[0].chamada_asterisk is chamada_asterisk
    assert resultados[0].chamada_asterisk.ramal == "7149"


def teste_concilia_vc2_com_ddd_diferente_no_asterisk():
    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1779819010.5948",
        chave_comparacao="2026-05-26 15:10|11941754723",
        chave_comparacao_proximo_minuto="2026-05-26 15:11|11941754723",
        data_hora=datetime(2026, 5, 26, 15, 10, 10),
        destino="11941754723",
        duracao_segundos=50,
        ramal="7478",
        nome_ramal="",
        uniqueid="1779819010.5948",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-05-26 15:10|941754723",
        chave_comparacao_proximo_minuto="2026-05-26 15:11|941754723",
        data_hora=datetime(2026, 5, 26, 15, 10, 12),
        destino="94175-4723",
        duracao_segundos=54,
        valor=Decimal("0.74"),
        tipo_destino="VC2",
    )

    resultados = conciliar(
        [chamada_asterisk],
        [chamada_vivo],
    )

    assert len(resultados) == 1
    assert resultados[0].status == StatusConciliacao.ENCONTRADA
    assert resultados[0].chamada_asterisk is chamada_asterisk
    assert resultados[0].chamada_asterisk.ramal == "7478"
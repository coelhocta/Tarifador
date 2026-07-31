from datetime import datetime
from decimal import Decimal

from core.cobranca import gerar_registros_cobranca
from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    OrigemDados,
    ResultadoConciliacao,
    StatusConciliacao,
)


def teste_gera_registro_cobranca():

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
        tipo_vivo="DDD",
        valor=Decimal("0.61"),
    )

    resultado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        chamada_asterisk=chamada_asterisk,
        status=StatusConciliacao.ENCONTRADA,
    )

    registros = gerar_registros_cobranca(
        [resultado]
    )

    assert len(registros) == 1

    registro = registros[0]

    # Identificação vinda do Asterisk
    assert registro.ramal == "7001"
    assert registro.nome_ramal == "SETOR A"

    # Dados da cobrança vindos da Vivo
    assert registro.data_hora == datetime(
        2026, 6, 25, 10, 2, 30
    )
    assert registro.destino == "3510-1711"
    assert registro.tipo_vivo == "DDD"
    assert registro.duracao_segundos == 60
    assert registro.valor == Decimal("0.61")
    
    
def teste_nao_gera_cobranca_sem_identificacao_asterisk():

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 30),
        destino="3510-1711",
        duracao_segundos=60,
        tipo_vivo="DDD",
        valor=Decimal("0.61"),
    )

    resultado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        chamada_asterisk=None,
        status=StatusConciliacao.NAO_ENCONTRADA,
    )

    registros = gerar_registros_cobranca(
        [resultado]
    )

    assert registros == []
    
    
def teste_gera_somente_cobrancas_identificadas():

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

    chamada_vivo_identificada = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 30),
        destino="3510-1711",
        duracao_segundos=60,
        tipo_vivo="DDD",
        valor=Decimal("0.61"),
    )

    chamada_vivo_nao_identificada = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 11:00|998005377",
        chave_comparacao_proximo_minuto="2026-06-25 11:01|998005377",
        data_hora=datetime(2026, 6, 25, 11, 0, 10),
        destino="99800-5377",
        duracao_segundos=120,
        tipo_vivo="VC2",
        valor=Decimal("2.50"),
    )

    resultados = [
        ResultadoConciliacao(
            chamada_vivo=chamada_vivo_identificada,
            chamada_asterisk=chamada_asterisk,
            status=StatusConciliacao.ENCONTRADA,
        ),
        ResultadoConciliacao(
            chamada_vivo=chamada_vivo_nao_identificada,
            chamada_asterisk=None,
            status=StatusConciliacao.NAO_ENCONTRADA,
        ),
    ]

    registros = gerar_registros_cobranca(
        resultados
    )

    assert len(registros) == 1

    registro = registros[0]

    assert registro.ramal == "7001"
    assert registro.nome_ramal == "SETOR A"
    assert registro.tipo_vivo == "DDD"
    assert registro.valor == Decimal("0.61")
    
    
def teste_gera_cobranca_com_ramal_inferido():

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-25 10:02|35101711",
        chave_comparacao_proximo_minuto="2026-06-25 10:03|35101711",
        data_hora=datetime(2026, 6, 25, 10, 2, 30),
        destino="3510-1711",
        duracao_segundos=60,
        tipo_vivo="DDD",
        valor=Decimal("0.61"),
    )

    resultado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        chamada_asterisk=None,
        status=StatusConciliacao.INFERIDA,
        ramal_inferido="7001",
        nome_ramal_inferido="SETOR A",
    )

    registros = gerar_registros_cobranca(
        [resultado]
    )

    assert len(registros) == 1

    registro = registros[0]

    assert registro.ramal == "7001"
    assert registro.nome_ramal == "SETOR A"

    assert registro.data_hora == datetime(
        2026, 6, 25, 10, 2, 30
    )
    assert registro.destino == "3510-1711"
    assert registro.tipo_vivo == "DDD"
    assert registro.duracao_segundos == 60
    assert registro.valor == Decimal("0.61")
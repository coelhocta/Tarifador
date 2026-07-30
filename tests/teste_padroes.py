"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_padroes.py

Descrição:
    Testes do módulo padroes.py

Versão:
    1.0.0

=========================================================
"""

from datetime import datetime
from decimal import Decimal

from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    OrigemDados,
    ResultadoConciliacao,
    StatusConciliacao,
)

from core.padroes import (
    construir_historico,
    obter_ramal_preferencial,
)

def criar_resultado(
    destino: str,
    ramal: str,
    status: StatusConciliacao,
):

    chamada_asterisk = ChamadaAsterisk(
        origem_dados=OrigemDados.ASTERISK,
        chave_id="1",
        chave_comparacao="",
        chave_comparacao_proximo_minuto="",
        data_hora=datetime.now(),
        destino=destino,
        duracao_segundos=60,
        ramal=ramal,
        nome_ramal="TESTE",
        uniqueid="1",
    )

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="1",
        chave_comparacao=f"2026-06-25 10:00|{destino}",
        chave_comparacao_proximo_minuto="",
        data_hora=datetime.now(),
        destino=destino,
        duracao_segundos=60,
        valor=Decimal("0.50"),
    )

    return ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        chamada_asterisk=chamada_asterisk,
        status=status,
    )


def teste_constroi_historico():

    resultados = [

        criar_resultado(
            "33389039",
            "7476",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "33389039",
            "7476",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "33389039",
            "7478",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "32278099",
            "7478",
            StatusConciliacao.ENCONTRADA,
        ),

    ]

    historico = construir_historico(resultados)

    assert historico["33389039"]["7476"] == 2

    assert historico["33389039"]["7478"] == 1

    assert historico["32278099"]["7478"] == 1


def teste_ignora_resultados_nao_conciliados():

    resultados = [

        criar_resultado(
            "33389039",
            "7476",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "33389039",
            "7478",
            StatusConciliacao.NAO_ENCONTRADA,
        ),

    ]

    historico = construir_historico(resultados)

    assert historico["33389039"]["7476"] == 1

    assert "7478" not in historico["33389039"]
    
    
def teste_retorna_ramal_preferencial():

    resultados = []

    resultados = []

    # Ramal preferencial
    for _ in range(2):
        resultados.append(
            criar_resultado(
                "33389039",
                "7476",
                StatusConciliacao.ENCONTRADA,
            )
        )

    # Outro ramal
    resultados.append(
        criar_resultado(
            "33389039",
            "7478",
            StatusConciliacao.ENCONTRADA,
        )
    )

    historico = construir_historico(resultados)

    assert (
        obter_ramal_preferencial(
            historico,
            "33389039",
        )
        == "7476"
    )
    
    
def teste_nao_retorna_ramal_com_poucas_ocorrencias():

    resultados = []

    for _ in range(1):

        resultados.append(
            criar_resultado(
                "33389039",
                "7476",
                StatusConciliacao.ENCONTRADA,
            )
        )

    historico = construir_historico(resultados)

    assert (
        obter_ramal_preferencial(
            historico,
            "33389039",
        )
        is None
    )
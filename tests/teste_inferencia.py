"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_inferencia.py

Descrição:
    Testes do módulo inferencia.py

=========================================================
"""

from core.inferencia import aplicar_inferencia

from datetime import datetime
from decimal import Decimal

from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    OrigemDados,
    StatusConciliacao,
    ResultadoConciliacao,
)


def teste_aplicar_inferencia_sem_resultados():

    resultados = []

    aplicar_inferencia(resultados)

    assert resultados == []
    
    
def criar_resultado(
    destino: str,
    ramal: str,
    nome_ramal: str,
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
        nome_ramal=nome_ramal,
        uniqueid=f"{ramal}-{destino}",
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
        chamada_asterisk=(
            chamada_asterisk
            if status == StatusConciliacao.ENCONTRADA
            else None
        ),
        status=status,
    )
    
    
def teste_aplica_inferencia():

    resultados = [

        criar_resultado(
            "33389039",
            "7476",
            "Andre",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "33389039",
            "7476",
            "Andre",
            StatusConciliacao.ENCONTRADA,
        ),

        criar_resultado(
            "33389039",
            "",
            "",
            StatusConciliacao.NAO_ENCONTRADA,
        ),
    ]

    aplicar_inferencia(resultados)

    resultado = resultados[2]

    assert resultado.status == StatusConciliacao.INFERIDA

    assert resultado.ramal_inferido == "7476"

    assert resultado.nome_ramal_inferido == "Andre"
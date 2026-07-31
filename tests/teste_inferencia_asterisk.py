from datetime import datetime
from decimal import Decimal

from core.inferencia_asterisk import (
    aplicar_inferencia_asterisk,
)

from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    OrigemDados,
    ResultadoConciliacao,
    StatusConciliacao,
)


def teste_inferencia_asterisk_encontra_ramal_mais_frequente():

    chamadas = [

        ChamadaAsterisk(
            origem_dados=OrigemDados.ASTERISK,
            chave_id="1",
            chave_comparacao="2026-06-25 10:00|1699626098",
            chave_comparacao_proximo_minuto="2026-06-25 10:01|1699626098",
            data_hora=datetime(2026, 6, 25, 10, 0, 0),
            destino="1699626098",
            duracao_segundos=20,
            ramal="7479",
            nome_ramal="Financeiro",
            uniqueid="1",
        ),

        ChamadaAsterisk(
            origem_dados=OrigemDados.ASTERISK,
            chave_id="2",
            chave_comparacao="2026-06-25 10:01|1699626098",
            chave_comparacao_proximo_minuto="2026-06-25 10:02|1699626098",
            data_hora=datetime(2026, 6, 25, 10, 1, 0),
            destino="1699626098",
            duracao_segundos=20,
            ramal="7479",
            nome_ramal="Financeiro",
            uniqueid="2",
        ),

        ChamadaAsterisk(
            origem_dados=OrigemDados.ASTERISK,
            chave_id="3",
            chave_comparacao="2026-06-25 10:02|1699626098",
            chave_comparacao_proximo_minuto="2026-06-25 10:03|1699626098",
            data_hora=datetime(2026, 6, 25, 10, 2, 0),
            destino="1699626098",
            duracao_segundos=20,
            ramal="7480",
            nome_ramal="Almoxarifado",
            uniqueid="3",
        ),
    ]

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao="2026-06-26 08:30|1699626098",
        chave_comparacao_proximo_minuto="2026-06-26 08:31|1699626098",
        data_hora=datetime(2026, 6, 26, 8, 30, 0),
        destino="1699626098",
        duracao_segundos=25,
        valor=Decimal("0.25"),
    )

    resultado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        status=StatusConciliacao.NAO_ENCONTRADA,
    )

    aplicar_inferencia_asterisk(
        [resultado],
        chamadas,
    )

    assert resultado.status == StatusConciliacao.INFERIDA
    assert resultado.ramal_inferido == "7479"
    assert resultado.nome_ramal_inferido == "Financeiro"
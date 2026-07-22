from pathlib import Path

import pytest

from extrai_vivo import extrair_pdf
from extrai_vivo import _extrair_linhas
from extrai_vivo import _eh_ligacao
from extrai_vivo import LigacaoVivoBruta
from extrai_vivo import _converter_linha
from extrai_vivo import _extrair_chamadas


ARQUIVO_VALIDO = (
    Path("dados_teste")
    / "vivo_fatura_valida.pdf"
)

ARQUIVO_INEXISTENTE = (
    Path("dados_teste")
    / "arquivo_inexistente.pdf"
)


def teste_pdf_inexistente():

    with pytest.raises(FileNotFoundError):
        extrair_pdf(
            ARQUIVO_INEXISTENTE,
            Path("saida.csv"),
        )


def teste_pdf_valido(tmp_path):

    arquivo_saida = tmp_path / "saida.csv"

    extrair_pdf(
        ARQUIVO_VALIDO,
        arquivo_saida,
    )
    
    
def teste_extrair_linhas():

    linhas = _extrair_linhas(ARQUIVO_VALIDO)

    assert len(linhas) > 0

    assert any(linha.strip() for linha in linhas)
    
    
def teste_eh_ligacao():

    assert _eh_ligacao(
        "18/06/2026 13:34:24 00:04:42 99838-1378 AREA-035 VC3 R$ 4,18"
    )


def teste_cabecalho_nao_e_ligacao():

    assert not _eh_ligacao(
        "Data Hora Duração Número de Destino Destino Tipo Valor da Ligação"
    )


def teste_subtotal_nao_e_ligacao():

    assert not _eh_ligacao(
        "SUBTOTAL R$ 1.399,34"
    )


def teste_rodape_nao_e_ligacao():

    assert not _eh_ligacao(
        "Telefônica Brasil S/A"
    )


def teste_pagina_nao_e_ligacao():

    assert not _eh_ligacao(
        "PÁGINA: 34/41"
    )
    
    
def teste_converter_linha_vc3():

    ligacao = _converter_linha(
        "18/06/2026 13:34:24 00:04:42 99838-1378 AREA-035 VC3 R$ 4,18"
    )

    assert ligacao == LigacaoVivoBruta(
        data="18/06/2026",
        hora="13:34:24",
        duracao="00:04:42",
        numero="99838-1378",
        destino="AREA-035",
        tipo="VC3",
        valor="4,18",
    )
    

def teste_converter_linha_ddd_destino_uma_palavra():

    ligacao = _converter_linha(
        "18/06/2026 13:37:24 00:01:00 3227-8099 BAURU DDD R$ 0,61"
    )

    assert ligacao == LigacaoVivoBruta(
        data="18/06/2026",
        hora="13:37:24",
        duracao="00:01:00",
        numero="3227-8099",
        destino="BAURU",
        tipo="DDD",
        valor="0,61",
    )
    

def teste_converter_linha_ddd_destino_duas_palavras():

    ligacao = _converter_linha(
        "09/06/2026 14:48:42 00:20:24 2224-7050 SAO PAULO DDD R$ 12,64"
    )

    assert ligacao.destino == "SAO PAULO"
    assert ligacao.tipo == "DDD"


def teste_converter_linha_ddd_destino_quatro_palavras():

    ligacao = _converter_linha(
        "09/06/2026 12:50:06 00:01:00 3203-4091 SAO JOSE DO RIO DDD R$ 0,61"
    )

    assert ligacao.destino == "SAO JOSE DO RIO"
    assert ligacao.tipo == "DDD"


def teste_converter_linha_vc2():

    ligacao = _converter_linha(
        "09/06/2026 13:43:24 00:00:36 99760-7445 AREA-016 VC2 R$ 0,49"
    )

    assert ligacao.destino == "AREA-016"
    assert ligacao.tipo == "VC2"
    

def teste_extrair_chamadas():

    linhas = [
        "Telefônica Brasil S/A",
        "PÁGINA: 34/41",
        "Data Hora Duração Número de Destino Destino Tipo Valor da Ligação",
        "18/06/2026 13:34:24 00:04:42 99838-1378 AREA-035 VC3 R$ 4,18",
        "18/06/2026 13:37:24 00:01:00 3227-8099 BAURU DDD R$ 0,61",
        "SUBTOTAL R$ 4,79",
    ]

    ligacoes = _extrair_chamadas(linhas)

    assert len(ligacoes) == 2

    assert ligacoes[0].numero == "99838-1378"
    assert ligacoes[1].numero == "3227-8099"
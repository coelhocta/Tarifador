from pathlib import Path

import pytest

from extrai_vivo import extrair_pdf, _extrair_linhas, _eh_ligacao 


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
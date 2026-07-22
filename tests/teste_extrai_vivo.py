from pathlib import Path

import pytest

from extrai_vivo import extrair_pdf


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
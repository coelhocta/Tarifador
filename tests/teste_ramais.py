from pathlib import Path

import pytest

from ramais import carregar_ramais


ARQUIVO = Path("dados_teste") / "pjsip.ramais"


@pytest.fixture(scope="module")
def ramais():

    return carregar_ramais(ARQUIVO)


def teste_arquivo_carregado(ramais):

    assert len(ramais) > 0


def teste_ramal_5000_existe(ramais):

    assert "5000" in ramais


def teste_ramal_6001_existe(ramais):

    assert "6001" in ramais


def teste_nome_ramal_5000(ramais):

    assert ramais["5000"].nome == "TESTE123"


def teste_nome_ramal_6001(ramais):

    assert ramais["6001"].nome == "CCAE CMD VÍDEO CONF"


def teste_contexto_ramal_6001(ramais):

    assert ramais["6001"].contexto == "ramais"
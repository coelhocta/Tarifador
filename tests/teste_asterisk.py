"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_asterisk.py

Descrição:
    Testes do módulo asterisk.py

=========================================================
"""

from pathlib import Path

import pytest

from asterisk import carregar_chamadas


ARQUIVO_VALIDO = (
    Path("dados_teste") / "Jun.26.ASTERISK.csv"
)

ARQUIVO_INEXISTENTE = (
    Path("dados_teste") / "arquivo_inexistente.csv"
)


# ==========================================================
# Arquivo inexistente
# ==========================================================

def teste_arquivo_inexistente():

    with pytest.raises(FileNotFoundError):
        carregar_chamadas(ARQUIVO_INEXISTENTE)


# ==========================================================
# Arquivo válido
# ==========================================================

def teste_carregar_chamadas():

    chamadas = carregar_chamadas(ARQUIVO_VALIDO)

    assert chamadas is not None

    assert isinstance(chamadas, list)

    assert len(chamadas) > 0


# ==========================================================
# Primeira chamada
# ==========================================================

def teste_primeira_chamada():

    chamadas = carregar_chamadas(ARQUIVO_VALIDO)

    chamada = chamadas[0]

    assert chamada.ramal != ""

    assert chamada.nome_ramal != ""

    assert chamada.destino != ""

    assert chamada.duracao_segundos >= 0

    assert chamada.uniqueid != ""
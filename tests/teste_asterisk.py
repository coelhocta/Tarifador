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

from core.importador_asterisk import carregar_chamadas

ARQUIVO_VALIDO = (
    Path("dados_teste") / "asterisk_valido.csv"
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

    assert isinstance(chamadas, list)

    assert len(chamadas) == 3


# ==========================================================
# Primeira chamada
# ==========================================================

def teste_primeira_chamada():

    chamadas = carregar_chamadas(ARQUIVO_VALIDO)

    chamada = chamadas[0]

    assert chamada.ramal == "7476"

    assert chamada.nome_ramal == ""

    assert chamada.destino == "1732034091"

    assert chamada.duracao_segundos == 59

    assert chamada.uniqueid == "1777597396.48962"

# ==========================================================
# Segunda chamada
# ==========================================================

def teste_segunda_chamada():

    chamadas = carregar_chamadas(ARQUIVO_VALIDO)

    chamada = chamadas[1]

    assert chamada.ramal == "7117"

    assert chamada.nome_ramal == "CH ADM PAYS"

    assert chamada.destino == "6120232155"

    assert chamada.duracao_segundos == 172

    assert chamada.uniqueid == "1777897897.4896"
    
# ==========================================================
# Terceira chamada
# ==========================================================

def teste_terceira_chamada():

    chamadas = carregar_chamadas(ARQUIVO_VALIDO)

    chamada = chamadas[2]

    assert chamada.ramal == "7826"

    assert chamada.nome_ramal == "SSTAE AUX 1"

    assert chamada.destino == "6121095123"

    assert chamada.duracao_segundos == 4

    assert chamada.uniqueid == "1777899629.5637"
    

# ==========================================================
# Cabecalho inválido
# ==========================================================
    
ARQUIVO_CABECALHO_INVALIDO = (
    Path("dados_teste") / "asterisk_cabecalho_invalido.csv"
)


def teste_cabecalho_invalido():

    with pytest.raises(ValueError):
        carregar_chamadas(ARQUIVO_CABECALHO_INVALIDO)
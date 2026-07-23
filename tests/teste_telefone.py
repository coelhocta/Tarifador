"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_telefone.py

Descrição:
    Testes do módulo telefone.py

Versão:
    2.0.1

=========================================================
"""

from core.models import TipoDestino

from core.telefone import (
    remover_prefixo_internacional,
    remover_prefixo_operadora,
    remover_zero_inicial,
    normalizar_numero,
    identificar_tipo_destino,
    extrair_ddd,
    extrair_numero_local,
    telefone_comparacao,
)


# ==========================================================
# Prefixos
# ==========================================================

def teste_remover_prefixo_internacional():

    assert (
        remover_prefixo_internacional("001632034091")
        == "1632034091"
    )


def teste_remover_prefixo_operadora():

    assert (
        remover_prefixo_operadora("0151632034091")
        == "1632034091"
    )


def teste_remover_zero_inicial():

    assert (
        remover_zero_inicial("01632034091")
        == "1632034091"
    )


# ==========================================================
# Normalização
# ==========================================================

def teste_normalizacao_com_parenteses():

    assert (
        normalizar_numero("(16)3203-4091")
        == "1632034091"
    )


def teste_normalizacao_com_espacos():

    assert (
        normalizar_numero("16 3203 4091")
        == "1632034091"
    )


def teste_normalizacao_ramal():

    assert (
        normalizar_numero("7001")
        == "7001"
    )


# ==========================================================
# Tipo
# ==========================================================

def teste_tipo_ramal():

    assert (
        identificar_tipo_destino("7001")
        == TipoDestino.RAMAL
    )


def teste_tipo_local():

    assert (
        identificar_tipo_destino("32034091")
        == TipoDestino.LOCAL
    )


def teste_tipo_ddd_fixo():

    assert (
        identificar_tipo_destino("1632034091")
        == TipoDestino.DDD_FIXO
    )


def teste_tipo_celular():

    assert (
        identificar_tipo_destino("16998005377")
        == TipoDestino.DDD_CELULAR
    )


def teste_tipo_0800():

    assert (
        identificar_tipo_destino("08001234567")
        == TipoDestino.SERVICO_0800
    )


def teste_tipo_0300():

    assert (
        identificar_tipo_destino("03001234567")
        == TipoDestino.SERVICO_0300
    )


def teste_tipo_300x():

    assert (
        identificar_tipo_destino("30031234")
        == TipoDestino.SERVICO_300X
    )


def teste_tipo_400x():

    assert (
        identificar_tipo_destino("40041234")
        == TipoDestino.SERVICO_400X
    )


# ==========================================================
# DDD
# ==========================================================

def teste_extrair_ddd_fixo():

    assert (
        extrair_ddd("1632034091")
        == "16"
    )


def teste_extrair_ddd_celular():

    assert (
        extrair_ddd("16998005377")
        == "16"
    )


def teste_extrair_ddd_local():

    assert (
        extrair_ddd("32034091")
        == ""
    )


# ==========================================================
# Número Local
# ==========================================================

def teste_numero_local_fixo():

    assert (
        extrair_numero_local("1632034091")
        == "32034091"
    )


def teste_numero_local_celular():

    assert (
        extrair_numero_local("16998005377")
        == "998005377"
    )


def teste_numero_local():

    assert (
        extrair_numero_local("32034091")
        == "32034091"
    )


# ==========================================================
# Comparação
# ==========================================================

def teste_comparacao_ramal():

    assert (
        telefone_comparacao("7001")
        == "7001"
    )


def teste_comparacao_fixo():

    assert (
        telefone_comparacao("1632034091")
        == "32034091"
    )


def teste_comparacao_celular():

    assert (
        telefone_comparacao("16998005377")
        == "998005377"
    )


def teste_comparacao_local():

    assert (
        telefone_comparacao("32034091")
        == "32034091"
    )


def teste_comparacao_0800():

    assert (
        telefone_comparacao("08001234567")
        == "08001234567"
    )
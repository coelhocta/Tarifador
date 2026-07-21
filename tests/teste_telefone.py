"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_telefone.py

Descrição:
    Testes do módulo telefone.py

Versão:
    2.0.0

=========================================================
"""

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

from core.models import TipoDestino


def testar(descricao, obtido, esperado):

    if obtido == esperado:
        print(f"✓ {descricao}")
    else:
        print(f"✗ {descricao}")
        print(f"    Obtido..: {obtido}")
        print(f"    Esperado: {esperado}")


print()
print("=" * 70)
print("TESTES - TELEFONE")
print("=" * 70)
print()

# ==========================================================
# Prefixos
# ==========================================================

testar(
    "Prefixo Internacional",
    remover_prefixo_internacional("001632034091"),
    "1632034091",
)

testar(
    "Prefixo Operadora",
    remover_prefixo_operadora("0151632034091"),
    "1632034091",
)

testar(
    "Zero Inicial",
    remover_zero_inicial("01632034091"),
    "1632034091",
)

# ==========================================================
# Normalização
# ==========================================================

testar(
    "Normalização 1",
    normalizar_numero("(16)3203-4091"),
    "1632034091",
)

testar(
    "Normalização 2",
    normalizar_numero("16 3203 4091"),
    "1632034091",
)

testar(
    "Normalização 3",
    normalizar_numero("7001"),
    "7001",
)

# ==========================================================
# Tipo
# ==========================================================

testar(
    "Tipo Ramal",
    identificar_tipo_destino("7001"),
    TipoDestino.RAMAL,
)

testar(
    "Tipo Local",
    identificar_tipo_destino("32034091"),
    TipoDestino.LOCAL,
)

testar(
    "Tipo DDD Fixo",
    identificar_tipo_destino("1632034091"),
    TipoDestino.DDD_FIXO,
)

testar(
    "Tipo Celular",
    identificar_tipo_destino("16998005377"),
    TipoDestino.DDD_CELULAR,
)

testar(
    "Tipo 0800",
    identificar_tipo_destino("08001234567"),
    TipoDestino.SERVICO_0800,
)

testar(
    "Tipo 0300",
    identificar_tipo_destino("03001234567"),
    TipoDestino.SERVICO_0300,
)

testar(
    "Tipo 300X",
    identificar_tipo_destino("30031234"),
    TipoDestino.SERVICO_300X,
)

testar(
    "Tipo 400X",
    identificar_tipo_destino("40041234"),
    TipoDestino.SERVICO_400X,
)

# ==========================================================
# DDD
# ==========================================================

testar(
    "DDD Fixo",
    extrair_ddd("1632034091"),
    "16",
)

testar(
    "DDD Celular",
    extrair_ddd("16998005377"),
    "16",
)

testar(
    "DDD Local",
    extrair_ddd("32034091"),
    "",
)

# ==========================================================
# Número Local
# ==========================================================

testar(
    "Número Local Fixo",
    extrair_numero_local("1632034091"),
    "32034091",
)

testar(
    "Número Local Celular",
    extrair_numero_local("16998005377"),
    "998005377",
)

testar(
    "Número Local",
    extrair_numero_local("32034091"),
    "32034091",
)

# ==========================================================
# Comparação
# ==========================================================

testar(
    "Comparação Ramal",
    telefone_comparacao("7001"),
    "7001",
)

testar(
    "Comparação Fixo",
    telefone_comparacao("1632034091"),
    "32034091",
)

testar(
    "Comparação Celular",
    telefone_comparacao("16998005377"),
    "998005377",
)

testar(
    "Comparação Local",
    telefone_comparacao("32034091"),
    "32034091",
)

testar(
    "Comparação 0800",
    telefone_comparacao("08001234567"),
    "08001234567",
)

print()
print("=" * 70)
print("FIM DOS TESTES")
print("=" * 70)
print()
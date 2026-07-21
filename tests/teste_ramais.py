"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_ramais.py

Descrição:
    Testes do módulo ramais.py.

Versão:
    2.0.0

=========================================================
"""

from pathlib import Path

from ramais import carregar_ramais


ARQUIVO = Path("dados_teste") / "pjsip.ramais"


def testar(descricao: str, obtido, esperado):
    """
    Exibe o resultado de um teste.
    """

    if obtido == esperado:
        print(f"✓ {descricao}")
    else:
        print(f"✗ {descricao}")
        print(f"    Obtido..: {obtido}")
        print(f"    Esperado: {esperado}")


print()
print("=" * 70)
print("TESTES - RAMAIS")
print("=" * 70)
print()

print(f"Arquivo........: {ARQUIVO.resolve()}")
print(f"Existe.........: {ARQUIVO.exists()}")

print()

ramais = carregar_ramais(ARQUIVO)

testar(
    "Arquivo carregado",
    len(ramais) > 0,
    True,
)

print(f"Total Ramais...: {len(ramais)}")

print()

# ----------------------------------------------------------
# Testes conhecidos do arquivo de exemplo
# ----------------------------------------------------------

testar(
    "Ramal 5000 existe",
    "5000" in ramais,
    True,
)

testar(
    "Ramal 6001 existe",
    "6001" in ramais,
    True,
)

testar(
    "Nome do ramal 5000",
    ramais["5000"].nome,
    "TESTE123",
)

testar(
    "Nome do ramal 6001",
    ramais["6001"].nome,
    "CCAE CMD VÍDEO CONF",
)

testar(
    "Contexto do ramal 6001",
    ramais["6001"].contexto,
    "ramais",
)

print()
print("-" * 70)
print("Primeiros 10 ramais")
print("-" * 70)

for ramal in list(ramais.values())[:10]:

    print(f"Ramal........: {ramal.numero}")
    print(f"Nome.........: {ramal.nome}")
    print(f"Contexto.....: {ramal.contexto}")
    print(f"Call Group...: {ramal.call_group}")
    print(f"Pickup Group.: {ramal.pickup_group}")
    print()

print("=" * 70)
print("FIM DOS TESTES")
print("=" * 70)
print()
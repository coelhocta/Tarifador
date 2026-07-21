from core.utils import (
    somente_digitos,
    normalizar_numero,
    telefone_comparacao,
)

print("=" * 60)
print("TESTE DO UTILS")
print("=" * 60)

casos = [
    "32034091",
    "1632034091",
    "16998005377",
    "0151632034091",
    "0016332034091",
    "(16)3203-4091",
    "16 3203 4091",
    "16-3203-4091",
    "",
    None,
]

for numero in casos:

    print(f"\nEntrada........: {numero}")

    print(f"Somente dígitos: {somente_digitos(numero)}")

    print(f"Normalizado....: {normalizar_numero(numero)}")

    print(f"Comparação.....: {telefone_comparacao(numero)}")
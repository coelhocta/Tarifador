#!/usr/bin/env python3

import csv
import re
from datetime import datetime

ARQUIVO_CDR = "/var/log/asterisk/cdr-csv/Master.csv"
ARQUIVO_RAMAIS = "/etc/asterisk/pjsip.ramais"

# ==========================================================
# Descobre o mês anterior
# ==========================================================

hoje = datetime.today()

if hoje.month == 1:
    ano = hoje.year - 1
    mes = 12
else:
    ano = hoje.year
    mes = hoje.month - 1

meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]

arquivo_saida = f"{meses[mes - 1]}.{str(ano)[2:]}.ASTERISK.csv"

# ==========================================================
# Carrega os nomes dos ramais
# ==========================================================

ramais = {}

with open(ARQUIVO_RAMAIS, encoding="utf-8") as f:

    ramal = None

    for linha in f:

        linha = linha.strip()

        m = re.match(r"\[(\d+)\]\(endpoint\)", linha)

        if m:
            ramal = m.group(1)
            ramais[ramal] = ""
            continue

        if ramal is None:
            continue

        if linha.startswith("callerid="):

            m = re.search(r'"(.*?)"', linha)

            if m:
                ramais[ramal] = m.group(1)

# ==========================================================
# Normaliza número telefônico
# ==========================================================

def normaliza_numero(numero):

    numero = "".join(c for c in numero if c.isdigit())

    # Remove prefixo internacional (00)
    while numero.startswith("00"):
        numero = numero[2:]

    # Remove CSP (015,021,031...)
    if numero.startswith("0") and len(numero) >= 12:
        numero = numero[3:]

    # Remove zero restante
    if numero.startswith("0"):
        numero = numero[1:]

    return numero

# ==========================================================
# Lê o CDR
# ==========================================================

linhas_saida = []

with open(ARQUIVO_CDR, newline="", encoding="utf-8") as entrada:

    leitor = csv.reader(entrada)

    for linha in leitor:

        if len(linha) < 15:
            continue

        contexto = linha[3].strip('"')

        if contexto != "externo":
            continue

        status = linha[14].strip('"')

        if status != "ANSWERED":
            continue

        origem = linha[1].strip('"')
        destino = linha[2].strip('"')

        if not destino:
            continue

        # Origem deve ser um ramal
        if not (origem.isdigit() and len(origem) == 4):
            continue

        # Ignora ramal -> ramal
        if destino.isdigit() and len(destino) == 4:
            continue

        inicio = linha[9].strip('"')

        if not inicio:
            continue

        dt = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")

        # Apenas mês anterior
        if dt.year != ano or dt.month != mes:
            continue

        destino = normaliza_numero(destino)

        # Descarta números inválidos
        if len(destino) < 8:
            continue

        linhas_saida.append([
            origem,
            ramais.get(origem, ""),
            dt.strftime("%d/%m/%Y"),
            dt.strftime("%H:%M:%S"),
            int(linha[13]),
            destino
        ])

# ==========================================================
# Ordena por data/hora
# ==========================================================

linhas_saida.sort(
    key=lambda x: datetime.strptime(
        x[2] + " " + x[3],
        "%d/%m/%Y %H:%M:%S"
    )
)

# ==========================================================
# Grava CSV
# ==========================================================

with open(arquivo_saida, "w", newline="", encoding="utf-8-sig") as saida:

    escritor = csv.writer(saida, delimiter=";")

    escritor.writerow([
        "Ramal",
        "Nome",
        "Data",
        "Hora",
        "Duracao",
        "Destino"
    ])

    escritor.writerows(linhas_saida)

print()
print("=" * 60)
print("EXPORTAÇÃO DE CHAMADAS - SATA")
print("=" * 60)
print(f"Período........: {meses[mes - 1]}/{ano}")
print(f"Chamadas.......: {len(linhas_saida)}")
print(f"Arquivo........: {arquivo_saida}")
print("=" * 60)
print()
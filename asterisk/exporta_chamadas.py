#!/usr/bin/env python3

import csv
import re
from datetime import date, datetime, timedelta

ARQUIVO_CDR = "/var/log/asterisk/cdr-csv/Master.csv"
ARQUIVO_RAMAIS = "/etc/asterisk/pjsip.ramais"

# ==========================================================
# Índices do Master.csv (cdr_csv)
# ==========================================================

IDX_SRC = 1
IDX_DST = 2
IDX_CONTEXT = 3
IDX_START = 9
IDX_BILLSEC = 13
IDX_DISPOSITION = 14
IDX_UNIQUEID = 16

# ==========================================================
# Descobre o período de exportação
# (Mês retrasado + mês anterior)
# ==========================================================

hoje = date.today()

primeiro_dia_mes_atual = hoje.replace(day=1)
ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
primeiro_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

ultimo_dia_mes_retrasado = primeiro_dia_mes_anterior - timedelta(days=1)
primeiro_dia_mes_retrasado = ultimo_dia_mes_retrasado.replace(day=1)

data_inicio = primeiro_dia_mes_retrasado
data_fim = ultimo_dia_mes_anterior

meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]

arquivo_saida = (
    f"{meses[primeiro_dia_mes_anterior.month - 1]}."
    f"{str(primeiro_dia_mes_anterior.year)[2:]}"
    ".ASTERISK.csv"
)

# ==========================================================
# Carrega os nomes dos ramais
# ==========================================================

def carregar_ramais():

    ramais = {}

    with open(ARQUIVO_RAMAIS, encoding="utf-8") as arquivo:

        ramal = None

        for linha in arquivo:

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

    return ramais

# ==========================================================
# Normaliza número telefônico
# ==========================================================

def normaliza_numero(numero):

    numero = "".join(c for c in numero if c.isdigit())

    while numero.startswith("00"):
        numero = numero[2:]

    if numero.startswith("0") and len(numero) >= 12:
        numero = numero[3:]

    if numero.startswith("0"):
        numero = numero[1:]

    return numero

# ==========================================================
# Exporta chamadas
# ==========================================================

def exportar_chamadas():

    ramais = carregar_ramais()

    linhas_saida = []

    with open(ARQUIVO_CDR, newline="", encoding="utf-8") as entrada:

        leitor = csv.reader(entrada)

        for linha in leitor:

            if len(linha) <= IDX_UNIQUEID:
                continue

            contexto = linha[IDX_CONTEXT].strip('"')

            if contexto != "externo":
                continue

            status = linha[IDX_DISPOSITION].strip('"')

            if status != "ANSWERED":
                continue

            origem = linha[IDX_SRC].strip('"')

            destino = linha[IDX_DST].strip('"')

            if not destino:
                continue

            if not any(c.isdigit() for c in destino):
                continue

            if not (origem.isdigit() and len(origem) == 4):
                continue

            if destino.isdigit() and len(destino) == 4:
                continue

            inicio = linha[IDX_START].strip('"')

            if not inicio:
                continue

            dt = datetime.strptime(
                inicio,
                "%Y-%m-%d %H:%M:%S"
            )

            if not (data_inicio <= dt.date() <= data_fim):
                continue

            destino = normaliza_numero(destino)

            # O SATA fará a validação completa do número.
            # Aqui descartamos apenas destinos claramente inválidos.
            if len(destino) < 8:
                continue

            linhas_saida.append([
                origem,
                ramais.get(origem, ""),
                dt.strftime("%d/%m/%Y"),
                dt.strftime("%H:%M:%S"),
                int(linha[IDX_BILLSEC]),
                destino,
                linha[IDX_UNIQUEID].strip('"')
            ])

    linhas_saida.sort(
        key=lambda x: datetime.strptime(
            x[3] + " " + x[4],
            "%d/%m/%Y %H:%M:%S"
        )
    )

    with open(
        arquivo_saida,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as saida:

        escritor = csv.writer(saida, delimiter=";")

        escritor.writerow([
            "Ramal",
            "Nome",
            "Data",
            "Hora",
            "Duracao",
            "Destino",
            "UniqueID"
        ])

        escritor.writerows(linhas_saida)

    print()
    print("=" * 60)
    print("EXPORTAÇÃO DE CHAMADAS - SATA")
    print("=" * 60)
    print(
        "Período........: "
        f"{data_inicio.strftime('%d/%m/%Y')} até "
        f"{data_fim.strftime('%d/%m/%Y')}"
    )
    print(f"Chamadas.......: {len(linhas_saida)}")
    print(f"Arquivo........: {arquivo_saida}")
    print("=" * 60)
    print()

# ==========================================================
# Programa principal
# ==========================================================

if __name__ == "__main__":
    exportar_chamadas()
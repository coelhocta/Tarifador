"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    extrai_vivo.py

Descrição:
    Extrai as ligações da fatura PDF da Vivo para
    um CSV padronizado.

Versão:
    1.0.0

=========================================================
"""

from pathlib import Path
import csv

import pdfplumber
import re
from dataclasses import dataclass

CABECALHO_CSV = [
    "Data",
    "Hora",
    "Duracao",
    "Numero",
    "Destino",
    "Tipo",
    "Valor",
]

@dataclass(slots=True)
class LigacaoVivoBruta:
    data: str
    hora: str
    duracao: str
    numero: str
    destino: str
    tipo: str
    valor: str

    def para_lista(self) -> list[str]:
        return [
            self.data,
            self.hora,
            self.duracao,
            self.numero,
            self.destino,
            self.tipo,
            self.valor,
        ]

REGEX_DATA = re.compile(
    r"^\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}"
)

REGEX_LIGACAO = re.compile(
    r"""
    ^
    (\d{2}/\d{2}/\d{4})      # Data
    \s+
    (\d{2}:\d{2}:\d{2})      # Hora
    \s+
    (\d{2}:\d{2}:\d{2})      # Duração
    \s+
    (\S+)                    # Número
    \s+
    (.+?)                    # Destino (1 ou mais palavras)
    \s+
    (\S+)                    # Tipo (DDD, VC2, VC3, DDI, VOZ, etc.)
    \s+
    R\$
    \s+
    ([\d,]+)                 # Valor
    $
    """,
    re.VERBOSE,
)

def extrair_pdf(
    arquivo_pdf: Path,
    arquivo_csv: Path,
) -> None:
    """
    Extrai as ligações da fatura Vivo para um CSV.
    """

    if not arquivo_pdf.exists():
        raise FileNotFoundError(arquivo_pdf)

    linhas = _extrair_linhas(arquivo_pdf)

    ligacoes = _extrair_chamadas(linhas)

    _gravar_csv(
        ligacoes,
        arquivo_csv,
    )


def _extrair_linhas(
    arquivo_pdf: Path,
) -> list[str]:
    """
    Extrai todas as linhas do PDF.

    O retorno preserva apenas a ordem das linhas,
    independentemente da página onde estavam.
    """

    linhas = []

    with pdfplumber.open(arquivo_pdf) as pdf:

        for pagina in pdf.pages:

            texto = pagina.extract_text()

            if not texto:
                continue

            linhas.extend(texto.splitlines())

    return linhas


def _eh_ligacao(
    linha: str,
) -> bool:
    """
    Retorna True quando a linha representa uma ligação.
    """

    return bool(REGEX_DATA.match(linha))


def _converter_linha(
    linha: str,
) -> LigacaoVivoBruta:

    correspondencia = REGEX_LIGACAO.match(linha)

    if correspondencia is None:
        raise ValueError(f"Linha inválida: {linha}")

    return LigacaoVivoBruta(
        data=correspondencia.group(1),
        hora=correspondencia.group(2),
        duracao=correspondencia.group(3),
        numero=correspondencia.group(4),
        destino=correspondencia.group(5),
        tipo=correspondencia.group(6),
        valor=correspondencia.group(7),
    )
    
    
def _extrair_chamadas(
    linhas: list[str],
) -> list[LigacaoVivoBruta]:

    ligacoes = []

    for linha in linhas:

        if not _eh_ligacao(linha):
            continue

        print(repr(linha))

        ligacoes.append(
            _converter_linha(linha)
    )

    return ligacoes


def _gravar_csv(
    ligacoes: list[LigacaoVivoBruta],
    arquivo_csv: Path,
) -> None:

    with arquivo_csv.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as arquivo:

        writer = csv.writer(
            arquivo,
            delimiter=";",
        )

        writer.writerow(CABECALHO_CSV)

        for ligacao in ligacoes:
            writer.writerow(
                ligacao.para_lista()
            )
            
            
if __name__ == "__main__":

    arquivo_pdf = Path("dados_teste") / "vivo_fatura_valida.pdf"

    arquivo_csv = Path("dados_teste") / "Jun.26.VIVO.csv"

    extrair_pdf(
        arquivo_pdf,
        arquivo_csv,
    )

    print(f"CSV gerado: {arquivo_csv}")
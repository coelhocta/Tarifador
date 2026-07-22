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

import pdfplumber
import re
from dataclasses import dataclass

@dataclass(slots=True)
class LinhaVivo:
    data: str
    hora: str
    duracao: str
    numero: str
    destino: str
    tipo: str
    valor: str

REGEX_DATA = re.compile(
    r"^\d{2}/\d{2}/\d{4}"
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
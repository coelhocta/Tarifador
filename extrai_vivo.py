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


def extrair_pdf(
    arquivo_pdf: Path,
    arquivo_csv: Path,
) -> None:
    """
    Extrai as ligações da fatura Vivo para um CSV.
    """

    if not arquivo_pdf.exists():
        raise FileNotFoundError(arquivo_pdf)

    with pdfplumber.open(arquivo_pdf):
        pass
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
class LigacaoVivoBruta:
    """Representa uma linha de ligação extraída da fatura da Vivo."""

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
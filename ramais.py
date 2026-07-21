"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    ramais.py

Descrição:
    Leitura do arquivo pjsip.ramais.

Versão:
    2.0.0

=========================================================
"""

import re
from pathlib import Path

from core.models import Ramal


# ==========================================================
# Ramais
# ==========================================================

def carregar_ramais(arquivo: str | Path) -> dict[str, Ramal]:
    """
    Carrega os ramais do arquivo pjsip.ramais.

    Retorna um dicionário indexado pelo número do ramal.

    Exemplo:

        ramais["6001"].nome
    """

    arquivo = Path(arquivo)

    if not arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    ramais: dict[str, Ramal] = {}

    ramal_atual: Ramal | None = None

    with arquivo.open(
        encoding="utf-8"
    ) as arquivo_ramais:

        for linha in arquivo_ramais:

            linha = linha.strip()

            if not linha:
                continue

            # ----------------------------------------------
            # Novo endpoint
            # ----------------------------------------------

            match = re.match(
                r"\[(\d+)\]\(endpoint\)",
                linha,
            )

            if match:

                numero = match.group(1)

                ramal_atual = Ramal(
                    numero=numero,
                    nome="",
                )

                ramais[numero] = ramal_atual

                continue

            if ramal_atual is None:
                continue

            # ----------------------------------------------
            # CallerID
            # ----------------------------------------------

            if linha.startswith("callerid="):

                match = re.search(
                    r'"(.*?)"',
                    linha,
                )

                if match:
                    ramal_atual.nome = match.group(1)

                continue

            # ----------------------------------------------
            # Contexto
            # ----------------------------------------------

            if linha.startswith("context="):

                ramal_atual.contexto = (
                    linha
                    .split("=", 1)[1]
                    .strip()
                )

                continue

            # ----------------------------------------------
            # Call Group
            # ----------------------------------------------

            if linha.startswith("call_group="):

                ramal_atual.call_group = (
                    linha
                    .split("=", 1)[1]
                    .strip()
                )

                continue

            # ----------------------------------------------
            # Pickup Group
            # ----------------------------------------------

            if linha.startswith("pickup_group="):

                ramal_atual.pickup_group = (
                    linha
                    .split("=", 1)[1]
                    .strip()
                )

                continue

    return dict(sorted(ramais.items()))
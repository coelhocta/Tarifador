"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    pipeline.py

Descrição:
    Orquestra o processamento principal do SATA.

=========================================================
"""

from pathlib import Path

from core.cobranca import gerar_registros_cobranca
from core.conciliador import conciliar
from core.exportador import (
    exportar_cobrancas,
    exportar_cobrancas_nao_identificadas,
)
from core.importador_asterisk import (
    carregar_chamadas as carregar_chamadas_asterisk,
)
from core.importador_vivo import (
    carregar_chamadas as carregar_chamadas_vivo,
)


def executar_pipeline(
    arquivo_asterisk: Path,
    arquivo_vivo: Path,
    arquivo_cobrancas: Path,
    arquivo_nao_identificadas: Path,
) -> None:
    """
    Executa o pipeline completo do SATA.
    """

    chamadas_asterisk = carregar_chamadas_asterisk(
        arquivo_asterisk
    )

    chamadas_vivo = carregar_chamadas_vivo(
        arquivo_vivo
    )

    resultados = conciliar(
        chamadas_asterisk,
        chamadas_vivo,
    )

    registros = gerar_registros_cobranca(
        resultados
    )

    exportar_cobrancas(
        registros,
        arquivo_cobrancas,
    )

    exportar_cobrancas_nao_identificadas(
        resultados,
        arquivo_nao_identificadas,
    )
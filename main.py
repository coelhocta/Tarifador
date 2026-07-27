"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    main.py

Descrição:
    Ponto de entrada do sistema SATA.

Versão:
    1.0.0

=========================================================
"""

from pathlib import Path

from core.pipeline import executar_pipeline


PASTA_ASTERISK = (
    Path("arquivos")
    / "entrada"
    / "asterisk"
)

PASTA_VIVO = (
    Path("arquivos")
    / "entrada"
    / "vivo"
)

PASTA_SAIDA = (
    Path("arquivos")
    / "saida"
)


def localizar_csv(
    pasta: Path,
) -> Path:
    """
    Localiza o único arquivo CSV existente na pasta.
    """

    arquivos = list(
        pasta.glob("*.csv")
    )

    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em: {pasta}"
        )

    if len(arquivos) > 1:
        raise ValueError(
            f"Mais de um arquivo CSV encontrado em: {pasta}"
        )

    return arquivos[0]


def main() -> None:
    """
    Executa o SATA.
    """

    print()
    print("=" * 60)
    print("SATA")
    print("Sistema de Auditoria Telefônica para Asterisk")
    print("=" * 60)
    print()

    print("Localizando arquivos de entrada...")

    arquivo_asterisk = localizar_csv(
        PASTA_ASTERISK
    )

    arquivo_vivo = localizar_csv(
        PASTA_VIVO
    )

    print(
        f"Asterisk: {arquivo_asterisk.name}"
    )

    print(
        f"Vivo....: {arquivo_vivo.name}"
    )

    print()

    PASTA_SAIDA.mkdir(
        parents=True,
        exist_ok=True,
    )

    arquivo_cobrancas = (
        PASTA_SAIDA
        / "cobrancas_identificadas.csv"
    )

    arquivo_nao_identificadas = (
        PASTA_SAIDA
        / "cobrancas_nao_identificadas.csv"
    )

    print("Processando chamadas...")

    executar_pipeline(
        arquivo_asterisk=arquivo_asterisk,
        arquivo_vivo=arquivo_vivo,
        arquivo_cobrancas=arquivo_cobrancas,
        arquivo_nao_identificadas=(
            arquivo_nao_identificadas
        ),
    )

    print()
    print("Processamento concluído.")
    print()

    print("Arquivos gerados:")

    print(
        f"  {arquivo_cobrancas}"
    )

    print(
        f"  {arquivo_nao_identificadas}"
    )

    print()


if __name__ == "__main__":
    main()
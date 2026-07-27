from pathlib import Path

from core.pipeline import executar_pipeline


def teste_executar_pipeline(tmp_path):

    arquivo_asterisk = (
        Path("dados_teste")
        / "asterisk_integracao.csv"
    )

    arquivo_vivo = (
        Path("dados_teste")
        / "vivo_uma_ligacao.csv"
    )

    arquivo_cobrancas = (
        tmp_path
        / "cobrancas_identificadas.csv"
    )

    arquivo_nao_identificadas = (
        tmp_path
        / "cobrancas_nao_identificadas.csv"
    )

    executar_pipeline(
        arquivo_asterisk=arquivo_asterisk,
        arquivo_vivo=arquivo_vivo,
        arquivo_cobrancas=arquivo_cobrancas,
        arquivo_nao_identificadas=(
            arquivo_nao_identificadas
        ),
    )

    assert arquivo_cobrancas.exists()

    assert arquivo_nao_identificadas.exists()

    conteudo = arquivo_cobrancas.read_text(
        encoding="utf-8-sig"
    )

    assert "7001" in conteudo
    assert "SETOR A" in conteudo
    assert "3510-1711" in conteudo
    assert "DDD" in conteudo
    assert "0,61" in conteudo
from datetime import datetime
from decimal import Decimal

from core.cobranca import RegistroCobranca

from core.conciliador import ResultadoConciliacao
from core.exportador import (
    exportar_cobrancas,
    exportar_cobrancas_nao_identificadas,
)
from core.models import (
    ChamadaVivo,
    OrigemDados,
    StatusConciliacao,
)

def teste_exportar_cobrancas(tmp_path):

    registro = RegistroCobranca(
        ramal="7001",
        nome_ramal="SETOR A",
        data_hora=datetime(
            2026, 6, 25, 10, 2, 30
        ),
        destino="3510-1711",
        tipo_vivo="DDD",
        duracao_segundos=60,
        valor=Decimal("0.61"),
    )

    arquivo = (
        tmp_path
        / "cobrancas_identificadas.csv"
    )

    exportar_cobrancas(
        [registro],
        arquivo,
    )

    assert arquivo.exists()

    conteudo = arquivo.read_text(
        encoding="utf-8-sig"
    )

    assert (
        "Ramal;Nome/Setor;Data;Hora;"
        "Destino;Tipo;Duracao;Valor"
        in conteudo
    )

    assert (
        "7001;SETOR A;25/06/2026;"
        "10:02:30;3510-1711;DDD;"
        "00:01:00;0,61"
        in conteudo
    )
    
    
def teste_exportar_cobrancas_nao_identificadas(
    tmp_path,
):

    chamada_vivo = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao=(
            "2026-06-25 11:00|998005377"
        ),
        chave_comparacao_proximo_minuto=(
            "2026-06-25 11:01|998005377"
        ),
        data_hora=datetime(
            2026, 6, 25, 11, 0, 10
        ),
        destino="99800-5377",
        duracao_segundos=120,
        tipo_vivo="VC2",
        valor=Decimal("2.50"),
    )

    resultado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo,
        chamada_asterisk=None,
        status=StatusConciliacao.NAO_ENCONTRADA,
    )

    arquivo = (
        tmp_path
        / "cobrancas_nao_identificadas.csv"
    )

    exportar_cobrancas_nao_identificadas(
        [resultado],
        arquivo,
    )

    assert arquivo.exists()

    conteudo = arquivo.read_text(
        encoding="utf-8-sig"
    )

    assert (
        "Data;Hora;Destino;Tipo;Duracao;Valor"
        in conteudo
    )

    assert (
        "25/06/2026;11:00:10;"
        "99800-5377;VC2;"
        "00:02:00;2,50"
        in conteudo
    )
    
    
def teste_exportador_nao_identificadas_ignora_encontradas(
    tmp_path,
):

    chamada_vivo_encontrada = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao=(
            "2026-06-25 10:00|35101711"
        ),
        chave_comparacao_proximo_minuto=(
            "2026-06-25 10:01|35101711"
        ),
        data_hora=datetime(
            2026, 6, 25, 10, 0, 10
        ),
        destino="3510-1711",
        duracao_segundos=60,
        tipo_vivo="DDD",
        valor=Decimal("0.61"),
    )

    chamada_vivo_nao_identificada = ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao=(
            "2026-06-25 11:00|998005377"
        ),
        chave_comparacao_proximo_minuto=(
            "2026-06-25 11:01|998005377"
        ),
        data_hora=datetime(
            2026, 6, 25, 11, 0, 10
        ),
        destino="99800-5377",
        duracao_segundos=120,
        tipo_vivo="VC2",
        valor=Decimal("2.50"),
    )

    resultado_encontrado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo_encontrada,
        chamada_asterisk=None,
        status=StatusConciliacao.ENCONTRADA,
    )

    resultado_nao_encontrado = ResultadoConciliacao(
        chamada_vivo=chamada_vivo_nao_identificada,
        chamada_asterisk=None,
        status=StatusConciliacao.NAO_ENCONTRADA,
    )

    arquivo = (
        tmp_path
        / "cobrancas_nao_identificadas.csv"
    )

    exportar_cobrancas_nao_identificadas(
        [
            resultado_encontrado,
            resultado_nao_encontrado,
        ],
        arquivo,
    )

    conteudo = arquivo.read_text(
        encoding="utf-8-sig"
    )

    # Não identificada deve aparecer
    assert "99800-5377" in conteudo
    assert "VC2" in conteudo
    assert "2,50" in conteudo

    # Encontrada não pode aparecer
    assert "3510-1711" not in conteudo
    assert "0,61" not in conteudo
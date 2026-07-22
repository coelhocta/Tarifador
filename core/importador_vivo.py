import csv

from pathlib import Path

from core.models import (
    ChamadaVivo,
    OrigemDados,
    TipoDestino,
)

from core.utils import (
    texto_para_data_hora,
    gerar_chave_comparacao,
    gerar_chave_comparacao_proximo_minuto,
)

from decimal import Decimal


def carregar_chamadas(
    arquivo_csv: Path,
) -> list[ChamadaVivo]:

    if not arquivo_csv.exists():
        raise FileNotFoundError(arquivo_csv)

    with arquivo_csv.open(
        encoding="utf-8",
        newline="",
    ) as arquivo:

        leitor = csv.reader(
            arquivo,
            delimiter=";",
        )

        next(leitor, None)

        chamadas: list[ChamadaVivo] = []

        for linha in leitor:
            chamadas.append(
                _converter_linha(linha)
            )

        return chamadas


def _converter_linha(
    campos: list[str],
) -> ChamadaVivo:

    data_hora = texto_para_data_hora(
        f"{campos[0]} {campos[1]}"
    )

    destino = campos[3]

    chave_comparacao = gerar_chave_comparacao(
        data_hora,
        destino,
    )   

    chave_comparacao_proximo = (
        gerar_chave_comparacao_proximo_minuto(
            data_hora,
            destino,
        )
    )

    return ChamadaVivo(
        origem_dados=OrigemDados.VIVO,
        chave_id="",
        chave_comparacao=chave_comparacao,
        chave_comparacao_proximo_minuto=chave_comparacao_proximo,
        data_hora=data_hora,
        destino=destino,
        tipo_destino=TipoDestino.DESCONHECIDO,
        duracao_segundos=_duracao_para_segundos(campos[2]),
        valor=Decimal(
            campos[6].replace(",", ".")
        ),
    )


def _duracao_para_segundos(
    duracao: str,
) -> int:

    horas, minutos, segundos = map(
        int,
        duracao.split(":"),
    )

    return (
        horas * 3600
        + minutos * 60
        + segundos
    )
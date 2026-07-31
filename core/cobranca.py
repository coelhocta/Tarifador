from core.models import (
    RegistroCobranca,
    ResultadoConciliacao,
    StatusConciliacao,
)


def gerar_registros_cobranca(
    resultados: list[ResultadoConciliacao],
) -> list[RegistroCobranca]:
    """
    Gera os registros que serão apresentados para cobrança.

    Somente chamadas conciliadas são incluídas.
    """

    registros: list[RegistroCobranca] = []

    for resultado in resultados:

        if resultado.status not in (
            StatusConciliacao.ENCONTRADA,
            StatusConciliacao.INFERIDA,
        ):
            continue

        chamada_vivo = resultado.chamada_vivo

        if resultado.status == StatusConciliacao.ENCONTRADA:

            chamada_asterisk = resultado.chamada_asterisk

            if chamada_asterisk is None:
                continue

            ramal = chamada_asterisk.ramal
            nome_ramal = chamada_asterisk.nome_ramal

        else:

            ramal = resultado.ramal_inferido
            nome_ramal = resultado.nome_ramal_inferido

        registros.append(
            RegistroCobranca(
                ramal=ramal,
                nome_ramal=nome_ramal,
                data_hora=chamada_vivo.data_hora,
                destino=chamada_vivo.destino,
                tipo_vivo=chamada_vivo.tipo_vivo,
                duracao_segundos=chamada_vivo.duracao_segundos,
                valor=chamada_vivo.valor,
            )
        )

    return registros
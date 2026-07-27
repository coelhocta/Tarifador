"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    conciliador.py

Descrição:
    Conciliação das chamadas do Asterisk com a fatura
    da operadora.

Versão:
    2.0.0

=========================================================
"""

from core.models import (
    ChamadaAsterisk,
    ChamadaVivo,
    ResultadoConciliacao,
    StatusConciliacao,
)


def _numeros_compativeis(
    chamada_asterisk: ChamadaAsterisk,
    chamada_vivo: ChamadaVivo,
) -> bool:
    """
    Verifica se os números podem representar o mesmo destino.

    A Vivo pode omitir o DDD no número exibido na fatura,
    enquanto o Asterisk mantém o DDD no destino.
    """

    numero_asterisk = "".join(
        caractere
        for caractere in chamada_asterisk.destino
        if caractere.isdigit()
    )

    numero_vivo = "".join(
        caractere
        for caractere in chamada_vivo.destino
        if caractere.isdigit()
    )

    if not numero_asterisk or not numero_vivo:
        return False

    return numero_asterisk.endswith(numero_vivo)


def _diferenca_tempo_segundos(
    chamada_asterisk: ChamadaAsterisk,
    chamada_vivo: ChamadaVivo,
) -> float:
    """
    Retorna a diferença absoluta entre os horários
    das chamadas, em segundos.
    """

    return abs(
        (
            chamada_asterisk.data_hora
            - chamada_vivo.data_hora
        ).total_seconds()
    )


def conciliar(
    chamadas_asterisk: list[ChamadaAsterisk],
    chamadas_vivo: list[ChamadaVivo],
) -> list[ResultadoConciliacao]:
    """
    Concilia as cobranças da Vivo com as chamadas do Asterisk.
    """

    resultados: list[ResultadoConciliacao] = []

    uniqueids_utilizados: set[str] = set()

    for chamada_vivo in chamadas_vivo:

        candidatos_exatos: list[ChamadaAsterisk] = []
        candidatos_proximo_minuto: list[ChamadaAsterisk] = []
        candidatos_numero: list[ChamadaAsterisk] = []

        # ==================================================
        # Procura candidatos no Asterisk
        # ==================================================

        for chamada_asterisk in chamadas_asterisk:

            # Uma chamada do Asterisk não pode ser
            # utilizada em duas cobranças da Vivo.
            if chamada_asterisk.uniqueid in uniqueids_utilizados:
                continue

            # ----------------------------------------------
            # Compatibilidade pelo número e horário
            # ----------------------------------------------
            #
            # Exemplo:
            #
            # Vivo:
            #   3227-8099
            #
            # Asterisk:
            #   1432278099
            #
            # O Asterisk possui o DDD e a Vivo pode
            # apresentar somente o número local.
            #
            # A diferença máxima permitida é 60 segundos.
            # ----------------------------------------------

            if (
                _numeros_compativeis(
                    chamada_asterisk,
                    chamada_vivo,
                )
                and _diferenca_tempo_segundos(
                    chamada_asterisk,
                    chamada_vivo,
                ) <= 60
            ):
                candidatos_numero.append(
                    chamada_asterisk
                )

            # ----------------------------------------------
            # Chave de comparação exata
            # ----------------------------------------------

            if (
                chamada_asterisk.chave_comparacao
                == chamada_vivo.chave_comparacao
            ):
                candidatos_exatos.append(
                    chamada_asterisk
                )

            # ----------------------------------------------
            # Chamada iniciada no minuto anterior
            # ----------------------------------------------

            elif (
                chamada_asterisk.chave_comparacao_proximo_minuto
                == chamada_vivo.chave_comparacao
            ):
                candidatos_proximo_minuto.append(
                    chamada_asterisk
                )

        # ==================================================
        # Define a prioridade dos candidatos
        # ==================================================

        if candidatos_exatos:

            candidatos = candidatos_exatos

        elif candidatos_proximo_minuto:

            candidatos = candidatos_proximo_minuto

        else:

            candidatos = candidatos_numero

        # ==================================================
        # Escolhe a chamada encontrada
        # ==================================================

        if candidatos:

            # Para a nova comparação por número,
            # o horário é o principal critério.
            #
            # A duração é usada como desempate.

            if candidatos is candidatos_numero:

                chamada_encontrada = min(
                    candidatos,
                    key=lambda chamada: (
                        _diferenca_tempo_segundos(
                            chamada,
                            chamada_vivo,
                        ),
                        abs(
                            chamada.duracao_segundos
                            - chamada_vivo.duracao_segundos
                        ),
                    ),
                )

            # Para as regras antigas, preservamos
            # o comportamento já validado pelos testes.

            else:

                chamada_encontrada = min(
                    candidatos,
                    key=lambda chamada: abs(
                        chamada.duracao_segundos
                        - chamada_vivo.duracao_segundos
                    ),
                )

            # Impede reutilização da mesma chamada.

            uniqueids_utilizados.add(
                chamada_encontrada.uniqueid
            )

            resultado = ResultadoConciliacao(
                chamada_vivo=chamada_vivo,
                chamada_asterisk=chamada_encontrada,
                status=StatusConciliacao.ENCONTRADA,
            )

        # ==================================================
        # Nenhuma chamada correspondente
        # ==================================================

        else:

            resultado = ResultadoConciliacao(
                chamada_vivo=chamada_vivo,
                chamada_asterisk=None,
                status=StatusConciliacao.NAO_ENCONTRADA,
            )

        resultados.append(resultado)

    return resultados
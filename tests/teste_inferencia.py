"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    teste_inferencia.py

Descrição:
    Testes do módulo inferencia.py

=========================================================
"""

from core.inferencia import aplicar_inferencia

from core.models import StatusConciliacao


def teste_aplicar_inferencia_sem_resultados():

    resultados = []

    aplicar_inferencia(resultados)

    assert resultados == []
    
    
def teste_aplicar_inferencia_sem_historico():

    resultados = []

    aplicar_inferencia(resultados)

    assert resultados == []
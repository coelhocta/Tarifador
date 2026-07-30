from core.inferencia import inferir_resultados


def teste_inferencia_sem_resultados():

    resultados = []

    inferir_resultados(resultados)

    assert resultados == []
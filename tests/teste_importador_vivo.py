import pytest

from pathlib import Path

from core.importador_vivo import carregar_chamadas
from core.models import OrigemDados


def teste_csv_inexistente():

    arquivo = Path("arquivo_inexistente.csv")

    try:
        carregar_chamadas(arquivo)
        assert False, "Era esperado FileNotFoundError"
    except FileNotFoundError:
        pass
    
    
from pathlib import Path

from core.importador_vivo import carregar_chamadas


def teste_csv_vazio():

    arquivo = Path("dados_teste/vivo_vazio.csv")

    chamadas = carregar_chamadas(arquivo)

    assert chamadas == []
    
    
def teste_importa_uma_ligacao():

    chamadas = carregar_chamadas(
        Path("dados_teste/vivo_uma_ligacao.csv")
    )

    assert len(chamadas) == 1

    chamada = chamadas[0]

    assert chamada.origem_dados == OrigemDados.VIVO
    assert chamada.destino == "3510-1711"
    assert chamada.duracao_segundos == 60
    
    
def teste_linha_invalida():

    with pytest.raises(ValueError):
        carregar_chamadas(
            Path("dados_teste/vivo_linha_invalida.csv")
        )
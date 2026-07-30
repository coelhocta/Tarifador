"""
=========================================================
SATA

Sistema de Auditoria Telefônica para Asterisk

Arquivo:
    models.py

Descrição:
    Modelos de dados utilizados pelo sistema.

Versão:
    1.4.2

=========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto


# ==========================================================
# Enumerações
# ==========================================================

class TipoDestino(Enum):
    """Classificação do número telefônico."""

    RAMAL = auto()

    LOCAL = auto()

    DDD_FIXO = auto()

    DDD_CELULAR = auto()

    INTERNACIONAL = auto()

    SERVICO_0300 = auto()

    SERVICO_0800 = auto()

    SERVICO_300X = auto()

    SERVICO_400X = auto()

    DESCONHECIDO = auto()


class OrigemDados(Enum):
    """Origem das informações."""

    ASTERISK = auto()

    VIVO = auto()

    MANUAL = auto()


class StatusConciliacao(Enum):
    """Situação da conciliação."""

    PENDENTE = auto()

    ENCONTRADA = auto()

    INFERIDA = auto()

    DIFERENCA_DURACAO = auto()

    DUPLICADA = auto()

    NAO_ENCONTRADA = auto()

    IGNORADA = auto()


# ==========================================================
# Ramal
# ==========================================================

@dataclass(slots=True, kw_only=True)
class Ramal:
    """Cadastro de um ramal."""

    numero: str

    nome: str

    contexto: str = ""

    call_group: str = ""

    pickup_group: str = ""

    ativo: bool = True


# ==========================================================
# Chamada (Classe Base)
# ==========================================================

@dataclass(slots=True, kw_only=True)
class Chamada:
    """Representa uma chamada telefônica."""

    origem_dados: OrigemDados

    chave_id: str

    chave_comparacao: str

    chave_comparacao_proximo_minuto: str

    data_hora: datetime

    destino: str

    tipo_destino: TipoDestino | None = None

    duracao_segundos: int

    status_conciliacao: StatusConciliacao = (
        StatusConciliacao.PENDENTE
    )

    observacao: str = ""


# ==========================================================
# Chamada Asterisk
# ==========================================================

@dataclass(slots=True, kw_only=True)
class ChamadaAsterisk(Chamada):
    """Registro proveniente do Asterisk."""

    ramal: str

    nome_ramal: str
    
    uniqueid: str


# ==========================================================
# Chamada Vivo
# ==========================================================

@dataclass(slots=True, kw_only=True)
class ChamadaVivo(Chamada):
    """Registro proveniente da fatura Vivo."""

    tipo_vivo: str = ""

    valor: Decimal = Decimal("0")


# ==========================================================
# Resultado da Conciliação
# ==========================================================

@dataclass(slots=True, kw_only=True)
class ResultadoConciliacao:
    """Resultado da conciliação de uma cobrança da Vivo."""

    chamada_vivo: ChamadaVivo

    chamada_asterisk: ChamadaAsterisk | None = None

    status: StatusConciliacao = StatusConciliacao.PENDENTE

    ramal_inferido: str | None = None

    nome_ramal_inferido: str = ""
    
    
@dataclass(slots=True, kw_only=True)
class RegistroCobranca:
    """Registro de uma chamada que será apresentada para cobrança."""

    ramal: str

    nome_ramal: str

    data_hora: datetime

    destino: str

    tipo_vivo: str

    duracao_segundos: int

    valor: Decimal
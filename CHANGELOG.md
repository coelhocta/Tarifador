# Changelog

## Versão 1.3.1

### Documentação

- Início da documentação da arquitetura.
- Início da documentação das regras de negócio.

### Utils

- Implementada função somente_digitos()
- Implementada função normalizar_numero()
- Implementada função telefone_comparacao()
- Criados testes automatizados do módulo utils

## Versão 1.3.0

### Models

- Refatoração definitiva do models.py
- Inclusão do enum OrigemDados
- Inclusão dos tipos RAMAL e SERVICO_300X
- Padronização das enumerações com auto()
- Estrutura da classe Chamada estabilizada



## Versão 1.2.0 (Em desenvolvimento)

### Refatoração

- Refatoração completa do models.py
- Criação da classe base Chamada
- Criação das classes ChamadaAsterisk e ChamadaVivo
- Criação do enum TipoDestino
- Criação do enum StatusConciliacao
- Criação do módulo core
- Criação do arquivo constants.py

### Organização

- Criação do pacote core
- Criação do arquivo __init__.py
- Reorganização dos módulos compartilhados


---

## Versão 1.1.0

### Ramais

- Implementada leitura do arquivo pjsip.ramais
- Criação automática dos objetos Ramal
- Teste do módulo concluído
- Aproximadamente 2000 ramais carregados com sucesso

---

## Versão 1.0.0

### Infraestrutura

- Estrutura inicial do projeto
- Criação dos módulos principais
- Ambiente virtual
- Configuração inicial
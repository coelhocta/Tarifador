# Decisões de Arquitetura

## 14/07/2026

### Telefone

Decisão

A lógica de telefones ficará em telefone.py.

Motivo

Evitar misturar regras de negócio com funções utilitárias.

---

### Core

Decisão

O pacote core conterá apenas infraestrutura.

Motivo

Separação entre infraestrutura e domínio.

---

### Testes

Decisão

Os testes serão executados inicialmente por scripts simples.

Motivo

Projeto ainda em desenvolvimento.

Migração para pytest prevista para V6.
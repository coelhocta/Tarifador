# Padrões do Projeto SATA (Sistema de Auditoria Telefônica Asterisk)

## Código

- Uma função = uma responsabilidade.
- Um módulo = uma responsabilidade.
- Todo módulo deve possuir documentação.
- Toda função deve possuir docstring.

## Testes

Nenhuma função entra no projeto sem teste.

## Versionamento

Toda alteração deve atualizar:

- CHANGELOG.md
- TODO.md

## Organização

Nunca usar números mágicos.

Sempre utilizar constants.py.

Nunca acessar linha[13].

Sempre utilizar cdr_fields.BILLSEC.
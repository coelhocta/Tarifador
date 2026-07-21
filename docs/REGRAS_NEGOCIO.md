# SATA

# Sistema de Auditoria Telefônica para Asterisk

---

# Regras de Negócio

Este documento contém todas as regras oficiais utilizadas pelo SATA.

Sempre que houver dúvida sobre qualquer comportamento do sistema, este documento prevalece sobre o código-fonte.

---

# 1. Ramais

É considerado ramal qualquer número com exatamente 4 dígitos.

Exemplos

7001

7434

6585

6000

Nunca sofrerão normalização.

---

# 2. Telefones Locais

Telefone local é todo número com exatamente 8 dígitos.

Exemplos

32034091

35618684

Será utilizado exatamente como informado.

---

# 3. Telefones DDD Fixo

Número com 10 dígitos.

Formato

DD + Telefone

Exemplo

1632034091

11 32244556

Será armazenado exatamente neste formato.

---

# 4. Telefones DDD Celular

Número com 11 dígitos.

Formato

DD + 9 + Número

Exemplos

16998005377

11993017173

Será armazenado exatamente neste formato.

---

# 5. Telefones Internacionais

Todo número com mais de 11 dígitos.

Exemplo

00331472580000

00114085551234

Não sofrerão qualquer alteração além da remoção dos prefixos.

---

# 6. Prefixos removidos

## Prefixo internacional

Será removido

00

Exemplo

0016332034091

↓

1632034091

---

## Prefixos de operadora

Serão removidos

014

015

021

023

025

031

041

043

Exemplo

0151632034091

↓

1632034091

---

# 7. Caracteres removidos

Durante a normalização serão removidos automaticamente

Espaços

-

(

)

.

/

+

Qualquer caractere que não seja número.

Exemplo

(16)3203-4091

↓

1632034091

---

# 8. Chave de Comparação

Esta regra será utilizada na conciliação entre

ASTERISK

↓

VIVO

## Ramal

7001

↓

7001

---

## Local

32034091

↓

32034091

---

## DDD Fixo

1632034091

↓

32034091

(remover o DDD)

---

## DDD Celular

16998005377

↓

998005377

(remover apenas o DDD)

---

## Internacional

Será utilizado o número normalizado completo.

---

# 9. Contextos do Asterisk

Os contextos conhecidos atualmente são

ramais

externo

ura

Somente chamadas do contexto

externo

serão tarifadas.

Chamadas

ramais

↓

ramais

não serão conciliadas.

---

# 10. Chamadas consideradas

Na exportação do Asterisk serão consideradas apenas chamadas

ANSWERED

Chamadas

NO ANSWER

BUSY

FAILED

serão descartadas.

---

# 11. Fatura Vivo

Serão extraídos

Data

Hora

Destino

Duração

Valor

Categoria

---

# 12. Conciliação

A conciliação utilizará a seguinte prioridade

1)

Número

+

Hora exata

↓

Encontrou

Fim.

---

2)

Número

+

Próximo minuto

↓

Encontrou

Fim.

---

3)

Número

+

Minuto anterior

↓

Encontrou

Fim.

---

4)

Não encontrou

↓

Registrar divergência.

---

# 13. Divergências

Uma chamada poderá estar

PENDENTE

ENCONTRADA

DIFERENCA_DURACAO

DUPLICADA

NAO_ENCONTRADA

---

# 14. Geração de Arquivos

Entrada

arquivos/entrada

Saída

arquivos/saida

Backup

arquivos/backup

---

# 15. Estrutura do Projeto

core

Infraestrutura compartilhada.

telefone.py

Regras de telefonia.

ramais.py

Cadastro de ramais.

asterisk.py

Importação do Master.csv.

vivo.py

Importação da fatura Vivo.

conciliador.py

Conciliação das chamadas.

excel.py

Geração das planilhas.

estatisticas.py

Relatórios gerenciais.

---

# 16. Objetivo do SATA

Conferir automaticamente a fatura telefônica da operadora através da conciliação com os registros do Asterisk, permitindo identificar divergências, calcular custos por ramal e gerar relatórios gerenciais.
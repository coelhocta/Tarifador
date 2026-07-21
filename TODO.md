# TODO

## V1.2

- [x] Refatorar models.py
- [x] Criar constants.py
- [x] Criar cdr_fields.py
- [ ] Desenvolver utils.py
- [ ] Desenvolver asterisk.py

## Infraestrutura

- [ ] exceptions.py
- [ ] logger.py

## Documentação

- [ ] ARQUITETURA.md
- [ ] REGRAS_NEGOCIO.md
- [ ] MANUAL_USUARIO.md

---

## V1.3

- [x] somente_digitos()
- [x] normalizar_numero()
- [x] telefone_comparacao()
- [ ] identificar_tipo_destino()
- [ ] gerar_chaves()
- [ ] datas
- [ ] horários

---

## V2.0

- [ ] Ler automaticamente o único PDF da pasta
- [ ] Extrair ligações da Vivo
- [ ] Normalizar números
- [ ] Gerar objetos ChamadaVivo

---

# V3.0 - Automação

## Importador

- [ ] Criar importador.py
- [ ] Buscar automaticamente o CSV do Asterisk
- [ ] Buscar automaticamente a fatura da Vivo
- [ ] Copiar arquivos para a pasta dados/
- [ ] Verificar se o mês já foi importado
- [ ] Registrar log da importação
- [ ] Mover arquivos antigos para backup/

---

## V1.4

- [x] Criar estrutura de testes do módulo telefone
- [ ] Implementar normalizar_numero()
- [ ] Implementar telefone_comparacao()
- [ ] Implementar identificar_tipo_destino()
- [ ] Implementar extrair_ddd()
- [ ] Implementar extrair_numero_local()
- [ ] Implementar gerar_chaves()

---

## V5.0

Estatísticas

- [ ] Gasto por ramal
- [ ] Gasto por setor
- [ ] Ligações por dia
- [ ] Ranking
- [ ] Gráficos

---

## Melhorias Futuras

- [ ] pytest
- [ ] Interface gráfica
- [ ] SQLite
- [ ] Dashboard
- [ ] Histórico anual
- [ ] Multioperadora
- [ ] Exportação PDF

## Refatorações futuras

- [ ] Avaliar renomear TipoDestino para TipoTelefone
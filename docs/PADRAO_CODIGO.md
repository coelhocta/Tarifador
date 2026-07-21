# Padrão de Código

## Idioma

Todo o código será escrito em português.

---

## Nomes de funções

Sempre utilizar verbos.

Exemplos:

- carregar_ramais()
- importar_asterisk()
- importar_vivo()
- normalizar_numero()
- identificar_tipo_destino()
- extrair_ddd()
- gerar_chave()

---

## Type Hints

Obrigatórios.

---

## Docstrings

Obrigatórias.

---

## Dataclasses

Sempre utilizar

```python
@dataclass(slots=True, kw_only=True)
```

---

## Imports

Ordem:

1. Biblioteca padrão
2. Bibliotecas externas
3. Projeto

---

## Comentários

Sempre em português.
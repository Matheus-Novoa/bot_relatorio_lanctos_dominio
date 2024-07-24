# bot_relatorio_lanctos_dominio
Automação da geração de relatórios de lançamentos contábeis no sistema Domínio

## Entradas:
- **numero_primeiro_lote** -> número do primeiro lote a ser lançado
- **mes** -> mês correspondente aos lançamentos

## Saída:
- Impressão dos relatórios por lote

## Interrupções:
- O *bot* será interrompido quando o lote conter apenas 1 (um) lançamento. Isso foi feito em conformidade com a regra de negócio.
- Para retomar o funcionamento do *bot*, modifique a variável **numero_primeiro_lote**, inserindo o múmero do lote pelo qual deseja o processo seja retomado.

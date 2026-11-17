# [Nome do relacionamento]

> **Como usar este modelo.** Responda só o que você sabe e consegue comprovar. O que não souber, deixe em branco e anote em "Perguntas em aberto", com quem pode responder. Um campo em branco é melhor do que um palpite.

## Identificação

Os campos marcados com **(obrigatório)** são o mínimo para começar. Os demais você completa quando a versão for aprovada.

| Campo | Preenchimento |
|---|---|
| Identificador do assunto (estável) **(obrigatório)** | |
| Tipo de documento | Relacionamento entre tabelas |
| Estado **(obrigatório)** | Rascunho |
| Responsável (cargo ou área) **(obrigatório)** | |
| Quem aprova (cargo ou área) **(obrigatório)** | |
| Versão atual **(obrigatório)** | 0.1 |
| Data desta versão **(obrigatório)** | |
| Fonte oficial | |
| Identificador desta versão | |
| Substitui qual versão? | |
| Vale a partir de | |
| Último dia de vigência (em branco se não houver fim) | |

Estados possíveis: **Rascunho**, **Pendente de aprovação**, **Aprovado**, **Obsoleto**. Só marque "Aprovado" quando quem aprova tiver confirmado por escrito.

## Pergunta de negócio
- Por que precisamos associar estes datasets?
- Quando a relação não deve ser utilizada?

## Tabelas e granularidade
- Tabela A e o que uma linha representa:
- Tabela B e o que uma linha representa:
- Chave A e significado:
- Chave B e significado:

## Cardinalidade e cobertura
- Cardinalidade esperada: 1:1, 1:N ou N:N?
- Chaves órfãs ou nulas são esperadas?
- Uma junção pode multiplicar linhas?
- Quando usar INNER, LEFT ou outro tipo de junção (se isso foi validado)?

## Tempo e histórico
- Relação depende de data ou versão?
- É snapshot ou entidade historizada?
- O relacionamento é válido ao longo de todo o período?

## Limites e testes
- Exemplos de registros associados corretamente:
- Contraexemplos e junções proibidas:
- Efeito na contagem e nos indicadores:
- Validação realizada pelo time de dados:
- Quem aprova e perguntas em aberto:

## Histórico de versões

Acrescente uma linha a cada mudança, a mais recente primeiro. Registre o que mudou na regra, não só que o texto foi editado. **Guarde o documento completo de cada versão aprovada:** o resumo abaixo não permite reconstruir a definição anterior.

| Versão | Data | O que mudou e por quê | Aprovado por (cargo ou área) |
|---|---|---|---|
| 0.1 | | Primeiro rascunho | |

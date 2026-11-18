# Nota de design: deriva entre documentos e sistemas

- **Estado:** nota de design, sem código. Implementar fica para depois da v1.0.
- **Data:** 2026-11-17
- **Fase:** F7 mantém a nota ([ADR 0029](../adr/0029-agentes-e-prova.md)); a decisão de adiar vale até a v1.0 ser publicada
- **Origem:** [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-30; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F7 e regra de desacoplamento

## Por que uma nota

Um documento aprovado pode dizer que uma coluna existe, ou que um evento é publicado num contêiner, e esse fato mudar nos sistemas sem que o documento mude. A nota registra o que uma comparação automática faria, para que a implementação, quando vier, comece de um ponto escrito. Nada é lido, comparado nem publicado nesta fase.

## O que compararia

- **Colunas citadas que não existem:** colunas que um documento de evento, indicador ou conjunto de dados cita, e que não existem no warehouse do time.
- **Eventos sem contrapartida:** eventos citados num documento que não aparecem no contêiner de tags, e eventos publicados no contêiner que não têm documento.
- **Revisão vencida:** documentos cuja data de revisão, calculada pelo `review_interval`, já passou.

A comparação não decide nada. Ela aponta o que merece a atenção de quem aprova.

## Por que depois

A comparação depende de conexão e de permissão de leitura nos sistemas de cada time. As pilhas variam: um time usa um warehouse, outro usa outro, e o contêiner de tags pode ser de um fornecedor diferente. Uma ferramenta única exigiria um adaptador por time antes de a v1.0 sair, e a v1.0 não depende disso.

## Entrada offline

Uma opção sem credencial: o time exporta a lista de colunas das tabelas e o JSON do contêiner de tags, e entrega esses arquivos à comparação. Os dois arquivos não carregam segredo. A comparação roda sobre eles, sem conexão.

## Saída

Um relatório para revisão humana, no mesmo formato do relatório de erros de `scripts/erros_para_perguntas.py`. O relatório lista os achados, com o documento e a versão de origem. Ele não altera documento, e quem decide é quem aprova.

## Regras de desacoplamento

- O núcleo (documentos, schema e identificadores) não ganha nenhum campo de deriva ([ADR 0025](../adr/0025-instrucao-minima-ao-agente.md)).
- A comparação seria um adaptador descartável. Se a pilha de um time mudar, troca-se o adaptador, e os documentos continuam iguais.

## Perguntas em aberto

- Quais exportações cada time consegue entregar sem conceder acesso de escrita?
- Um evento que existe no contêiner e não tem documento é lacuna do documento ou evento que não deveria estar publicado? Quem responde?
- Com que frequência o relatório deve ser gerado: antes de cada revisão, ou a cada mudança no contêiner?

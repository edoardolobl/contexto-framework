# 0026. Schema 1.0 e fonte única

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto na F3; aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F3; [11-decisoes.md](../../auditoria/11-decisoes.md), decisões 5, 8 e 14; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-11 a I-17 (I-17 adiado, veja Fica em aberto)

## Contexto

Cada modelo existe em dois arquivos escritos à mão, .md e .yaml, que já divergem (MOD-04, TEC-18). Os campos mudam de um tipo para outro, o cabeçalho comum varia entre os tipos, e a pergunta em aberto aparece em formatos diferentes, sem campo de resolução (MOD-07). Versões históricas citam versões posteriores (MOD-12, AUR-04), e a versão do produto não segue a regra que o próprio projeto ensina (EDI-19, MET-13). A decisão 5 da auditoria adota uma fonte única em Markdown com frontmatter; este ADR registra as escolhas menores que a acompanham.

## Decisão

1. **Pastas de fontes:** os modelos ficam em `src/modelos/<slug>.md` e os exemplos em `src/exemplos/<nome>.md`, ambos em Markdown com frontmatter.
2. **Gerados:** o `.yaml` de cada fonte é igual ao frontmatter. O `.md` de download tem os campos no topo e as seções "Identificação" e "Histórico de versões" geradas. `scripts/gerar_downloads.py` produz os dois. Os gerados ficam versionados no repositório, e o CI confere se estão em sincronia com as fontes.
3. **Tipo igual ao slug:** o campo `type` tem o mesmo valor do slug do modelo.
4. **Núcleo de oito campos** para sair do rascunho: `id`, `title`, `version`, `status`, `owner`, `approver`, `version_date` e `intent.question`. Os blocos técnicos continuam opcionais, conforme a decisão 5.
5. **Schema por tipo:** um JSON Schema por tipo de documento, mais `common.schema.json` para o cabeçalho comum e o `intent`. O identificador (`$id`) é um URN; a publicação por URL fica para a F6.
6. **Convenção de chaves:** inglês e `snake_case`, exceto onde há equivalente no ODCS 3.2.0 (`context` com `instructions`, `verifiedStatements` e `constraints`; `synonyms`; `authoritativeDefinitions`). Nesses casos vale a grafia do ODCS (ADR 0015).
7. **Conceito em SKOS:** o bloco `vocabulary` usa `prefLabel`, `altLabel`, `broader`, `related` e `not_synonyms`.
8. **Estado Substituído:** o rótulo em português de `superseded` é "Substituído". A fronteira com `deprecated` (Obsoleto) está na seção Estados do contrato, versão 0.8: substituído tem outra versão do mesmo `id` no lugar; obsoleto deixou de valer.
9. **`recorded_at` só em `superseded`:** a data do registro aparece só na cópia histórica substituída (I-15).
10. **`review_interval` em ISO 8601:** duração como `P6M`, obrigatória quando houver `context.instructions`.
11. **Versão do documento X.Y:** segue MAJOR.MINOR. PATCH é aceito pelo formato, sem uso nos exemplos (ADR 0009).
12. **Indicador com versão maior:** exige `history_recalculation`, com `recalculate` ou `method_break` (I-14).
13. **Modelos 0.x:** a pasta `historico/0.x` preserva só os modelos da versão 0.x, não os exemplos.
14. **Downloads antigos sem redirecionamento:** os arquivos 0.x não ganham redirecionamento para os novos.

## Fica em aberto

- **Fusões de tipos (ADR 0013):** Dataset com Relacionamento e Decisão em "Regra e decisão". Esta fase não faz a fusão. Ela continua em aberto e precisa de decisão do mantenedor antes de mudar a chave `type` e os campos afetados.
- **Seções autocontidas para RAG e NotebookLM (I-17):** adiadas para a F6. A incorporação pede id, escopo e vigência repetidos no subtítulo de cada seção, para que um trecho cortado por uma ferramenta de busca continue dizendo de que documento e de que período ele é. Nesta fase não há onde aplicar isso: os modelos são formulários em branco, com `id` e `valid_from` nulos, e os exemplos são baixados só em `.yaml`. A regra entra na F6, quando os exemplos ganham `.md` para download e o portal ganha a página "Preparar para NotebookLM ou RAG" ([10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F6). Até lá, os títulos de seção seguem o ADR 0016, que já ajuda nesses cortes.
- **Formato dos itens de `context`:** `verifiedStatements` e `constraints` seguem o formato do ODCS 3.2.0 (itens com `question` e `answer` opcional, e com `constraint`), conferido no JSON Schema oficial. As demais chaves que o ODCS aceita nesses itens (`id`, `tags`, `authoritativeDefinitions`, `customProperties`) ficam para a F6, junto do crosswalk.
- **Renomeação das demais chaves com equivalente ODCS** (por exemplo `physical_name`): fica para a F6, junto do crosswalk com o ODCS 3.2.0.

## Alternativas consideradas

- **Manter o par .md e .yaml escritos à mão, com teste de paridade:** recomendação do juiz da auditoria (ADR 0006), descartada pela decisão 5 por causa da divergência que já ocorreu.
- **Um schema único para todos os tipos:** menos arquivos, mas a validação deixa de dizer o que falta em cada tipo.
- **Gerar os downloads só no build:** o arquivo baixado deixaria de aparecer no repositório, e o CI não conferiria o que o leitor recebe.
- **Publicar o `$id` por URL já nesta fase:** depende de domínio próprio, adiado pelo ADR 0011; fica para a F6.
- **Preservar também os exemplos 0.x:** aumenta o peso do repositório sem ajudar quem migra, porque a tabela de migração de campos cobre o que mudou.

## Consequências

- **Positivas:** uma fonte por documento; o schema é conferido a cada mudança; o arquivo baixado é o mesmo que a página mostra.
- **Negativas:** a F3 reescreve 10 modelos, 20 exemplos e 2 arquivos de histórico. O núcleo de oito campos ainda é um formato longo para o público não técnico, e a convenção de chaves exige um dicionário de campos.
- **Fases afetadas:** F3 (esta fase); F4 e F5 nascem no formato final; F6 (renomeação das chaves com equivalente ODCS, crosswalk e publicação do `$id` por URL).
- **Breaking:** sim, no schema 1.0 (ADR 0009). Quebram: as chaves renomeadas para seguir o ODCS, as cópias históricas reclassificadas (de `approved` para `superseded` ou `deprecated`), os campos novos obrigatórios e a mudança de `type` se a fusão de tipos for aprovada. A migração de campos fica publicada na página de referência de migração do portal.

# 0028. Saídas para máquinas

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto na F6; aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F6 e regra de desacoplamento; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-26 a I-28; [08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), AG-01, AG-05, AG-06, AG-07 e AG-11

## Contexto

Um agente que recebe o portal ou um modelo baixado não tem como saber qual versão aprovada vale numa data, nem onde ler o schema que valida o documento (AG-05, AG-06). O llms.txt sozinho não mostra que o agente acerta, e por isso a F6 precisa de um kit mínimo que um agente consiga usar (I-26, I-27). A nota de MCP (AG-07) é escrita na F6; a decisão de implementar fica para a F7. Os endereços publicados precisam ser decididos agora, porque mudar um endereço publicado custa caro.

## Decisão

1. **Caminhos publicados.** Documentos, schemas, o kit e o llms.txt saem de caminhos públicos gerados por `scripts/gerar_saidas.py`: `public/documentos/`, `public/schemas/`, `public/downloads/kit/` e `public/llms.txt`. Nenhum deles se edita à mão.
2. **URN no `$id` dos schemas, URL no publicado; `source_url` é a exceção.** O `$id` de cada schema na fonte é um URN, um nome sem endereço web: `urn:contexto:schemas:<versão>:<slug>`, como `urn:contexto:schemas:1.1.0:kpi`. A cópia publicada em `public/schemas/<versão>/<slug>.schema.json` troca o URN pela URL completa no GitHub Pages. Os documentos saem em `documentos/<id>@<versão>.md` e `.yaml`. O campo `source_url` dos exemplos é a exceção assumida: ele guarda a URL completa do documento publicado, com o domínio, porque um arquivo copiado para fora do portal precisa dizer de onde veio. A URL do site fica num só lugar, `URL_DO_SITE` em `scripts/enderecos.py`, e `check_schemas.py` confere que cada `source_url` bate com ela.
3. **Schema 1.0.0 congelado; 1.1.0 aditivo.** O schema 1.0.0 fica publicado e congelado em `schemas/historico/1.0.0/`. A 1.1.0 só acrescenta os campos opcionais `license` e `source_url`. Um documento pode declarar `schema_version` 1.0.0 ou 1.1.0, e a validação aceita as duas. A cópia histórica guarda o texto como foi aprovado (contrato editorial): se foi aprovada na 1.0.0, continua na 1.0.0, sem `license` nem `source_url`, e `check_schemas.py` aceita isso só quando ela está `superseded` e tem `recorded_at`.
4. **`license` e `source_url`.** `license` usa o identificador SPDX, como CC-BY-4.0. `source_url` traz o endereço publicado do documento. Nos modelos em branco os dois ficam `null`, porque cada time escolhe a sua licença. Nos exemplos vigentes, `license` é CC-BY-4.0 e `source_url` é o endereço publicado.
5. **Composição do kit.** O kit para download tem o AGENTS.md curto do kit (`src/kit/AGENTS.md`), o glossário, os contratos e o histórico de contratos, os gabaritos, os dados e a Skill `auditar-coleta`. A fonte é `src/kit/kit.yaml`.
6. **Glossário do kit.** O glossário é de conceitos, não um catálogo de documentos. Cada termo tem o termo preferido, os sinônimos, o que não confundir com ele, um resumo em linguagem direta e o id@versão do documento de origem (I-12, I-16). Os termos saem dos documentos aprovados de Conceito, Indicador e Evento de coleta, e dos termos listados em `src/kit/kit.yaml`, cada um apontando o documento aprovado que o define. Gabaritos, rubricas e processos não viram termo.
7. **Formato do Markdown publicado.** O título de cada documento traz o id, a versão e a vigência. Assim, um trecho recortado para RAG ainda diz de qual documento e de qual período ele é (I-17).
8. **llms.txt por script, sem plugin.** O `public/llms.txt` sai do mesmo script, sem o plugin starlight-llms-txt. A compatibilidade desse plugin com a versão do Starlight ainda não foi confirmada, e o script dispensa essa dependência.
9. **MCP só como nota.** O desenho de resources e tools fica em `docs/design/mcp.md`. Nada é implementado nesta fase (I-28).
10. **Critério da F6.** A F6 fecha quando um agente com o kit mínimo responde às perguntas marcadas como onboarding, pelo protocolo de `docs/experimentos/onboarding.md` (I-26).

## Alternativas consideradas

- **Alternativa A, plugin starlight-llms-txt:** não foi escolhida. Depende de uma compatibilidade ainda não confirmada e cria uma dependência de terceiros para um arquivo que um script gera.
- **Alternativa B, URL no `$id` dos schemas da fonte:** não foi escolhida. O domínio entraria em cada schema e em cada `$ref` entre eles, e trocar de endereço mudaria os schemas, não só a cópia publicada. O `source_url` dos exemplos aceita esse custo de propósito (decisão 2).
- **Alternativa C, página HTML por id@versão:** não foi escolhida. Cria uma página por versão para quem lê no navegador, enquanto o agente lê melhor o Markdown com o mesmo conteúdo.
- **Alternativa D, renomear as chaves para fugir do ODCS:** não foi escolhida. Quebra a correspondência com o ODCS 3.2.0 que o [ADR 0015](./0015-chaves-em-ingles-rotulos-em-portugues.md) mantém.

## Consequências

- **Positivas:** o agente recebe o documento com endereço, versão e vigência; o schema publicado valida o que ele recebe; o núcleo continua sem campo de protocolo.
- **Negativas:** os endereços ficam presos ao github.io até haver domínio próprio ([ADR 0011](./0011-adiar-dominio-proprio.md)). Mudar de domínio exige um `$id` novo nos schemas publicados, redirecionamentos para os endereços já citados e regenerar o `source_url` de todos os exemplos, que contêm o domínio na fonte. O kit e o llms.txt precisam ser regenerados a cada mudança de documento, e o CI confere isso.
- **Fases afetadas:** F6 (este ADR, o kit, os schemas e o llms.txt, a nota de MCP e o protocolo de onboarding); F7 (a nota de MCP vira projeto só se a reconferência mudar a decisão).
- **Breaking:** nenhum. Os modelos e exemplos 1.0.0 continuam válidos, e o schema 1.1.0 só acrescenta campos opcionais.

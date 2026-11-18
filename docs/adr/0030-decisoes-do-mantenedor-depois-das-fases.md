# 0030. Decisões do mantenedor depois das fases

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor
- **Origem:** respostas do mantenedor em 17/11/2026 às perguntas que as fases F1 a F7 deixaram em aberto; [protocolo de onboarding](../experimentos/onboarding.md), primeira execução; [ROADMAP.md](../ROADMAP.md), pendências com o mantenedor

## Contexto

As fases F1 a F7 deixaram decisões com o mantenedor: doze ADRs propostos (0018 a 0029), oito versões propostas do contrato editorial (0.5 a 0.12), perguntas em aberto nos ADRs 0009 e 0013 e três falhas da primeira execução do protocolo de onboarding (Q06 e Q03 da QA-AURORA-002 e Q03 da QA-AURORA-001). Sem essas respostas, a versão do produto não podia sair do 0.4 e os gabaritos continuavam a pontuar contra um kit que não tinha a regra certa. Este ADR registra as respostas num lugar só.

## Decisão

**Correções depois do onboarding (F6):**

1. **Q06 da QA-AURORA-002 (receita de purchase): criar uma definição aprovada.** O Lab 2 ganha o indicador KPI-AURORA-002@1.0, aprovado, com a consulta `aurora-lab2-receita-purchase.sql`, sem junção. A receita certa da BR em 02/11/2026 é R$ 500; somar depois da junção com os itens dá R$ 1.100. O `check_lab2_mensuracao.py` refaz as duas contas. A Q06 passa a citar o indicador em `required_sources`, e o gabarito sobe para QA-AURORA-002@1.1.
2. **Q03 da QA-AURORA-001 (conversão sem qualificação): regra no AGENTS.md.** O AGENTS.md do kit e a Skill `contexto-consultar` ganham a regra do termo ambíguo: o agente compara a palavra da pergunta com o nome e com os sinônimos registrados de cada indicador aprovado. Se não houver correspondência, ou se houver mais de uma, ele mostra as opções e confirma qual antes de calcular.
3. **Q03 da QA-AURORA-002 (generate_lead sem operação): aceitar as duas formas.** O comportamento esperado continua sendo pedir esclarecimento. O gabarito aceita também responder, com uma condição: a resposta precisa dizer que no México o evento não está ativo. O campo `also_accepted` entra como opcional no schema das perguntas de negócio, com rótulos em `src/data/campos.yaml`.
4. **Repetir o experimento agora.** O protocolo de onboarding é refeito com o kit regenerado. A seção da primeira execução fica como está.
5. **Vigência retroativa declarada.** Um documento aprovado só pode ter `valid_from` anterior a `version_date` se for a primeira versão do assunto e se declarar a retroatividade no campo `retroactive_validity`, com o motivo (`reason`) e quem confirmou (`confirmed_by`). Uma versão que substitui outra nunca reescreve a vigência da anterior. A regra entra no contrato editorial 0.13 e no `check_revisions.py`.

**ADRs, contrato e nomes:**

6. **ADRs 0018 a 0029: aprovados todos.** Passam a **Aceito**, decididos pelo mantenedor, com data 2026-11-17.
7. **Contrato editorial: aprovada a versão 0.12 inteira.** As versões 0.5 a 0.12 passam a ter o mantenedor como quem aprovou. As regras desta decisão entram na 0.13.
8. **Título principal da home: mantido o proposto.**
9. **Nomes de produção nos exemplos da Aurora: confirmados.** O Lab 1 usa `sessoes_web` e `pedidos` no SQLite, que espelham `aurora-analytics.web.sessoes_web` e `aurora-analytics.vendas.pedidos`. A cópia histórica do KPI-AURORA-001@1.0 recebe os nomes novos e uma `archival_note` que explica a correção.
10. **Tipos do ADR 0013: mantidos separados.** Dataset, Relacionamento e Decisão continuam como modelos próprios. Isso fecha a pergunta em aberto do ADR 0013.
11. **Versão dos documentos: mantido MAJOR.MINOR.** A versão de cada documento segue 1.0, 1.1, 2.0. Isso fecha a pergunta em aberto do ADR 0009.
12. **Versão do produto: 1.0.0-rc.1.** É uma candidata a lançamento. A 1.0 final depende do piloto do ADR 0029.
13. **Chaves com equivalente direto no ODCS 3.2.0: renomeadas agora.** No schema 1.1.0, `physical_name` vira `physicalName`, `business_name` vira `businessName` e `technical_type` vira `physicalType`, como marca a página de correspondência com o ODCS. Nenhuma versão 1.x tinha sido publicada, por isso a troca não tem período de transição.

**Limpeza e operação:**

14. **Arquivos antigos de casos-teste: removidos.** Saem `public/downloads/historico/0.x/` e a página `referencias/migracao-schema-1-0`. O site publicado (0.4) nunca teve nenhum dos dois, e ninguém usa o schema 1.x; então nenhum endereço publicado passa a dar 404. Ficam os históricos de exemplo (KPI 1.0, Conceito 1.0) e os redirecionamentos de páginas.
15. **Checagem visual no CI: mantida, com cache.** O fluxo guarda o navegador do Playwright em cache, com a versão do `playwright-core` na chave, e instala só as bibliotecas do sistema quando o cache acerta.
16. **CLAUDE.md na raiz: criado,** com a linha `@AGENTS.md`, para o Claude Code ler as mesmas instruções do AGENTS.md.

## Alternativas consideradas

- **Afrouxar os gabaritos para o onboarding passar:** não foi escolhida. Cada falha virou uma mudança de regra ou de documento, e o experimento é repetido.
- **Q06 como abster-se, sem indicador:** não foi escolhida. A receita de purchase é uma pergunta legítima, e a regra de não somar depois da junção merece um documento aprovado.
- **Aprovar o contrato versão por versão:** não foi escolhida. As versões 0.5 a 0.12 foram escritas em sequência e dependem umas das outras.
- **Fundir Dataset com Relacionamento e Decisão com regra:** não foi escolhida. A fusão mudaria os modelos sem ganho medido.
- **Versão de documento em MAJOR.MINOR.PATCH:** não foi escolhida. O terceiro número não ajuda quem aprova a regra.
- **Publicar direto a 1.0.0:** não foi escolhida. O ADR 0029 condiciona a 1.0 ao piloto.
- **Manter as chaves em snake_case até um schema 2.0:** não foi escolhida. Como o 1.x não foi publicado, renomear agora não quebra ninguém.
- **Manter `historico/0.x` para evitar 404:** não foi escolhida. Os arquivos não são usados, e o site publicado nunca teve esses endereços.
- **Tirar a checagem visual do CI:** não foi escolhida. Ela pega regressões que os outros validadores não pegam.

## Consequências

- **Positivas:** as decisões pendentes ficam registradas e citáveis. O kit tem a regra do termo ambíguo, o Lab 2 tem o indicador de receita, e os gabaritos pontuam as duas formas aceitas da Q03 da QA-AURORA-002. A versão do produto sai do 0.4. O repositório fica sem arquivos que ninguém usa.
- **Negativas:** o experimento de onboarding precisa ser refeito, e o resultado da primeira execução não vale para o kit novo. Quem já escreveu um dataset em 1.0.0 precisa trocar três chaves. A versão 1.0 final ainda espera o piloto.
- **Fases afetadas:** F3 (schema 1.1.0 com as chaves do ODCS e os campos `also_accepted` e `retroactive_validity`), F4 (KPI-AURORA-002 e checagem da receita), F5 (exemplos com nomes de produção), F6 (kit, gabaritos e protocolo de onboarding) e F7 (piloto como portão da 1.0).
- **Breaking:** a renomeação das três chaves do dataset quebra um arquivo escrito no schema 1.0.0. Como nenhuma versão 1.x foi publicada, a migração é trocar as três chaves, sem período de transição.

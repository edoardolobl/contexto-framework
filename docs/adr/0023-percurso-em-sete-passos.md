# 0023. Percurso em sete passos

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria (F2)
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), seção 1.5, item 2; [05-navegacao-e-ux.md](../../auditoria/05-navegacao-e-ux.md), NAV-03 a NAV-07, NAV-13 e NAV-14; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-06

## Contexto

O menu não parte da pergunta do leitor: as perguntas de negócio, que deveriam abrir o percurso, ficam no fim de um grupo recolhido e com três nomes (NAV-03), e as pastas não batem com os grupos (NAV-04). A paginação automática sugere próximos passos ilógicos, e há becos sem saída e páginas órfãs (NAV-05, NAV-06). Falta o passo de delimitar o acervo (NAV-13), e a home não oferece entrada por sintoma para quem chega com um problema de dados (NAV-07, I-06). O seletor de modelos duplica a tabela e não oferece essa entrada (NAV-14).

## Decisão

- **Grupos do menu:** Comece aqui (tutorial de negócio e visão do método), Percurso, Modelos, Laboratórios, Entender, Consultar e Usar com IA.
- **Sete passos**, com fonte em `src/data/percurso.yaml`: 1 Escreva a pergunta de negócio; 2 Delimite o acervo; 3 Descubra o que falta; 4 Escreva com o modelo; 5 Revise e aprove; 6 Teste com as perguntas; 7 Leve à sua ferramenta de IA. O passo 4 é a página de modelos.
- **Próximo passo e prev/next:** toda página do percurso termina com o bloco Próximo passo, e o prev/next segue a ordem do menu.
- **Entradas por sintoma:** a home tem cinco entradas por sintoma (I-06). Cada uma tem um destino provisório registrado, que o tree test da F2 confirma ou troca.
- **Endereços movidos:** toda página movida ou renomeada ganha redirecionamento em `astro.config.mjs`. Os endereços dos modelos continuam em `/templates/...`.
- **Validador:** `scripts/check_navegacao.py` recusa página órfã, beco sem saída e link para endereço antigo.
- **Em aberto:** a ordem das páginas dentro de cada grupo, a ser confirmada no tree test; e o tutorial de dados em Comece aqui, previsto na direção (seção 1.5, item 2), que ainda não existe. Até lá, o percurso de dados é o Laboratório Aurora, no grupo Laboratórios.

## Alternativas consideradas

- **Cinco movimentos:** manter o método de cinco movimentos como estrutura do menu. Não foi escolhida, porque o menu deve seguir a pergunta do leitor (NAV-04) e o método ganhou o passo de delimitar (NAV-13).
- **Mover todas as pastas:** trocar todas as pastas de uma vez para espelhar os grupos. Não foi escolhida, porque muda muitos endereços de uma vez; mover só o que o percurso exige, com redirecionamento, é menos arriscado.
- **Menu gerado a partir de dados:** montar o menu inteiro a partir de um YAML. Não foi escolhida nesta fase: o percurso já tem fonte única em `percurso.yaml`, e gerar o menu inteiro antes do teste com pessoas adiciona uma camada sem prova de uso.

## Consequências

- **Positivas:** o leitor encontra a pergunta de negócio no início; o validador impede páginas órfãs e becos sem saída.
- **Negativas:** os redirecionamentos precisam ser mantidos; mudar a ordem de um passo muda o prev/next.
- **Fases afetadas:** F2 (menu em grupos, sete passos, bloco Próximo passo, entradas por sintoma e validador). O tree test previsto na F2 confere a estrutura (ver [PLANO_VALIDACAO.md](../PLANO_VALIDACAO.md), seção F2).
- **Breaking:** nenhum no formato dos modelos. Endereços movidos continuam válidos por redirecionamento.

# 0017. Tamanho de página de modelo

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria
- **Origem:** [13-ui-ux-tasteskill.md](../../auditoria/13-ui-ux-tasteskill.md), seção "O que entra no plano antes e durante a F0", segunda linha (UX-03); [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-24

## Contexto

A página Indicador junta numa rolagem só orientação, problema, perguntas, dois exemplos com abas, histórico de versões, exercícios, downloads, nota técnica e fundamentação. Ela tem 7,4 telas no desktop, 13 no celular e 1.951 elementos na página (UX-03). No celular, a pessoa não técnica perde o fio entre "o que é" e "baixe o modelo". A sequência didática de seis degraus prevista para a F5 (I-24) acrescenta blocos e deixaria a página ainda maior.

## Decisão

- Cada página de modelo tem **no máximo 4 telas** numa janela de 1440 x 900 px (altura da página dividida por 900).
- A **sequência didática** do I-24 (par contrastante, exemplo comentado, erro para encontrar, campo para completar, caso em branco, "Teste você") é dividida em passos ou em páginas. Passos recolhíveis podem usar os componentes Steps e Tabs do Starlight.
- A **referência de campos** (o que cada campo significa e aceita) fica numa página própria, separada da página que ensina.
- O limite entra no contrato editorial junto com o I-24, antes de reescrever as páginas.
- Um limite para o celular e a escolha entre passos e páginas para cada tipo ficam em aberto.

## Alternativas consideradas

- **Sem limite, só recolher seções** (levantada na redação do ADR): o conteúdo continua na mesma página, com o mesmo peso, e nada impede que ela volte a crescer.
- **Limite por número de elementos da página, não por telas** (levantada na redação do ADR): mede o custo técnico, mas não o que a pessoa sente ao rolar.
- **Seguir a regra da tasteskill de uma seção por tela:** é regra de landing page e não serve para documentação ([13-ui-ux-tasteskill.md](../../auditoria/13-ui-ux-tasteskill.md), seção "Descartados").

## Consequências

- **Positivas:** cada página tem um propósito; a pessoa chega mais rápido ao download; a referência de campos fica fácil de linkar.
- **Negativas:** mais páginas por tipo, mais links para manter e mais itens no menu.
- **Fases afetadas:** F2 (o tree test precisa incluir as páginas novas); F5 (sequência didática e checklist visual por PR medindo as 4 telas).
- **Breaking:** nenhum para os modelos. Âncoras e endereços de páginas atuais podem mudar, com redirecionamento.

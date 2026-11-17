import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const base = process.env.BASE_PATH || '/contexto-framework';

export default defineConfig({
  site: process.env.SITE_URL || 'https://edoardolobl.github.io',
  base,
  integrations: [
    starlight({
      title: 'Contexto',
      description: 'Método para documentar conhecimento organizacional de modo explícito, contextualizado e verificável.',
      logo: { src: './src/assets/brand.svg', alt: 'Contexto' },
      favicon: '/favicon.svg', // Starlight já acrescenta o base
      // SVG não aparece em todos os navegadores (Safari, por exemplo): PNG e ICO como alternativa.
      head: [
        { tag: 'link', attrs: { rel: 'icon', type: 'image/png', sizes: '32x32', href: base.replace(/\/$/, '') + '/favicon-32.png' } },
        { tag: 'link', attrs: { rel: 'alternate icon', href: base.replace(/\/$/, '') + '/favicon.ico' } },
        { tag: 'link', attrs: { rel: 'apple-touch-icon', sizes: '180x180', href: base.replace(/\/$/, '') + '/apple-touch-icon.png' } },
      ],
      locales: { root: { label: 'Português', lang: 'pt-BR' } },
      customCss: ['./src/styles/custom.css'],
      components: { Footer: './src/components/SiteFooter.astro' },
      social: [
        { icon: 'github', label: 'Repositório no GitHub', href: 'https://github.com/edoardolobl/contexto-framework' },
        { icon: 'linkedin', label: 'Edoardo Lobl no LinkedIn', href: 'https://www.linkedin.com/in/edoardolobl/' }
      ],
      sidebar: [
        { label: 'Comece por uma tarefa', items: [
          { slug: 'fundamentos/comece-em-5-minutos', label: 'Comece em 5 minutos' },
          { slug: 'validacao/checklist', label: 'Revisar um documento' },
          { slug: 'fundamentos/escolher-documento', label: 'Encontrar um modelo' }
        ] },
        { label: 'Guias para fazer', items: [
          { slug: 'metodo/elicitar', label: 'Descobrir o que falta' },
          { slug: 'metodo/revisao-e-entrega', label: 'Preparar para revisão' },
          { slug: 'fundamentos/como-ler-os-campos', label: 'Entender os campos' },
          { slug: 'metodo/identificacao-versoes', label: 'Versões e vigência' }
        ] },
        { label: 'Modelos para reutilizar', collapsed: true, items: [
          { slug: 'templates', label: 'Todos os modelos' },
          { slug: 'templates/conceito', label: 'Conceito e glossário' },
          { slug: 'templates/processo', label: 'Processo e procedimento' },
          { slug: 'templates/decisao', label: 'Regras e decisões' },
          { slug: 'templates/politica', label: 'Política e referência' },
          { slug: 'templates/kpi', label: 'Indicador (KPI)' },
          { slug: 'templates/rubrica', label: 'Rubrica de avaliação' }
        ] },
        { label: 'Exemplos comentados', collapsed: true, items: [
          { slug: 'exemplos/conceito-onboarding', label: 'Um conceito em RH' },
          { slug: 'exemplos/processo-campanha', label: 'Processo de campanha' },
          { slug: 'exemplos/decisao-campanha', label: 'Decisão e precedência' },
          { slug: 'exemplos/politica-despesas', label: 'Versões conflitantes' },
          { slug: 'exemplos/kpi', label: 'KPI de conversão' },
          { slug: 'exemplos/rubrica-case', label: 'Rubrica de uma análise' }
        ] },
        { label: 'Dados e Analytics', collapsed: true, items: [
          { slug: 'dados/visao-geral', label: 'Por onde começar' },
          { slug: 'dados/semantica', label: 'Além do schema' },
          { slug: 'dados/contrato-de-conhecimento', label: 'Contrato de conhecimento' },
          { slug: 'templates/dataset', label: 'Dataset e dicionário' },
          { slug: 'templates/relacionamento', label: 'Relacionamento entre tabelas' },
          { slug: 'templates/dashboard', label: 'Dashboard e interpretação' },
          { slug: 'templates/casos-teste', label: 'Perguntas de referência' },
          { slug: 'exemplos/analytics-integrado', label: 'Laboratório Aurora' },
          { slug: 'exemplos/testes-analytics', label: 'Perguntas do laboratório' }
        ] },
        { label: 'Entenda o método', collapsed: true, items: [
          { slug: 'fundamentos/promessa', label: 'Promessa e limites' },
          { slug: 'fundamentos/conhecimento-tacito', label: 'Conhecimento tácito' },
          { slug: 'metodo/visao-geral', label: 'Visão geral' },
          { slug: 'metodo/oito-dimensoes', label: 'As oito dimensões' },
          { slug: 'metodo/limites', label: 'Quando o método não basta' }
        ] },
        { label: 'Sobre e referências', collapsed: true, items: [
          { slug: 'governanca/papeis', label: 'Responsabilidades' },
          { slug: 'referencias', label: 'Fontes e bibliografia' },
          { slug: 'sobre/creditos', label: 'Autoria e licenças' }
        ] }
      ]
    })
  ]
});

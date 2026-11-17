import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const base = process.env.BASE_PATH || '/contexto-framework';
const site = process.env.SITE_URL || 'https://edoardolobl.github.io';
// Imagem de compartilhamento (UX-10): URL absoluta, gerada de src/assets/og-contexto.svg.
const ogImage = site.replace(/\/$/, '') + base.replace(/\/$/, '') + '/og-contexto.png';

export default defineConfig({
  site,
  base,
  // Páginas fundidas em outras (rodada 3): o endereço antigo leva ao novo.
  redirects: {
    '/exemplos/conceito-onboarding/': `${base}/templates/conceito/`,
    '/exemplos/processo-campanha/': `${base}/templates/processo/`,
    '/exemplos/decisao-campanha/': `${base}/templates/decisao/`,
    '/exemplos/politica-despesas/': `${base}/templates/politica/`,
    '/exemplos/kpi/': `${base}/templates/kpi/`,
    '/exemplos/rubrica-case/': `${base}/templates/rubrica/`,
    '/dados/semantica/': `${base}/dados/visao-geral/`,
    '/dados/contrato-de-conhecimento/': `${base}/dados/visao-geral/`,
    '/fundamentos/promessa/': `${base}/metodo/visao-geral/`,
    '/fundamentos/escolher-documento/': `${base}/templates/`,
    // Percurso em sete passos (F2): cada endereço antigo leva direto ao destino final, sem cadeia.
    '/templates/casos-teste/': `${base}/templates/perguntas-de-negocio/`,
    '/exemplos/testes-analytics/': `${base}/templates/perguntas-de-negocio/`,
    '/metodo/elicitar/': `${base}/percurso/descubra-o-que-falta/`,
    '/validacao/checklist/': `${base}/percurso/revise-e-aprove/`,
    '/metodo/revisao-e-entrega/': `${base}/percurso/revise-e-aprove/`
  },
  integrations: [
    starlight({
      title: 'Contexto',
      description: 'Transforme perguntas de negócio em documentos aprovados e versionados que uma IA consegue consultar sem inventar definições, seja a ferramenta que você usa direto, seja o sistema que a engenharia monta.',
      logo: { src: './src/assets/brand.svg', alt: 'Contexto' },
      favicon: '/favicon.svg', // Starlight já acrescenta o base
      // SVG não aparece em todos os navegadores (Safari, por exemplo): PNG e ICO como alternativa.
      head: [
        { tag: 'link', attrs: { rel: 'icon', type: 'image/png', sizes: '32x32', href: base.replace(/\/$/, '') + '/favicon-32.png' } },
        { tag: 'link', attrs: { rel: 'alternate icon', href: base.replace(/\/$/, '') + '/favicon.ico' } },
        { tag: 'link', attrs: { rel: 'apple-touch-icon', sizes: '180x180', href: base.replace(/\/$/, '') + '/apple-touch-icon.png' } },
        { tag: 'meta', attrs: { property: 'og:image', content: ogImage } },
        { tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
        { tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
        { tag: 'meta', attrs: { property: 'og:image:alt', content: 'Contexto: uma IA não deveria adivinhar como sua organização funciona.' } },
        // Cor da barra do navegador no celular, igual ao fundo de cada tema (--context-bg).
        { tag: 'meta', attrs: { name: 'theme-color', media: '(prefers-color-scheme: light)', content: '#faf9f6' } },
        { tag: 'meta', attrs: { name: 'theme-color', media: '(prefers-color-scheme: dark)', content: '#17181c' } },
      ],
      locales: { root: { label: 'Português', lang: 'pt-BR' } },
      customCss: ['./src/styles/custom.css'],
      components: { Footer: './src/components/SiteFooter.astro', Hero: './src/components/LandingHero.astro' },
      social: [
        { icon: 'github', label: 'Repositório no GitHub', href: 'https://github.com/edoardolobl/contexto-framework' },
        { icon: 'linkedin', label: 'Edoardo Lobl no LinkedIn', href: 'https://www.linkedin.com/in/edoardolobl/' }
      ],
      // Sem rótulos próprios nas páginas: o menu mostra o título da página, então os dois nunca divergem.
      // O grupo Percurso segue src/data/percurso.yaml, na mesma ordem (scripts/check_navegacao.py confere).
      // Em Modelos, os cinco tipos do núcleo (ADR 0013) vêm antes dos demais.
      sidebar: [
        { label: 'Início', link: '/' },
        { label: 'Comece aqui', items: ['fundamentos/comece-em-5-minutos', 'metodo/visao-geral'] },
        { label: 'Percurso', items: [
          'percurso/escreva-a-pergunta', 'percurso/delimite-o-acervo', 'percurso/descubra-o-que-falta', 'templates',
          'percurso/revise-e-aprove', 'percurso/teste-com-as-perguntas', 'percurso/leve-a-sua-ferramenta-de-ia'
        ] },
        { label: 'Modelos', items: [
          { label: 'Comece por estes', items: [
            'templates/kpi', 'templates/dataset', 'templates/relacionamento', 'templates/decisao', 'templates/perguntas-de-negocio'
          ] },
          { label: 'Mais modelos', collapsed: true, items: [
            'templates/conceito', 'templates/politica', 'templates/processo', 'templates/dashboard'
          ] },
          { label: 'Trilha complementar', collapsed: true, items: ['templates/rubrica'] }
        ] },
        { label: 'Laboratórios', items: ['exemplos/analytics-integrado'] },
        { label: 'Entender', collapsed: true, items: [
          'dados/visao-geral', 'fundamentos/conhecimento-tacito', 'metodo/limites'
        ] },
        { label: 'Consultar', collapsed: true, items: [
          'metodo/oito-dimensoes', 'fundamentos/como-ler-os-campos', 'metodo/identificacao-versoes',
          'governanca/papeis', 'referencias', 'sobre/creditos'
        ] },
        { label: 'Usar com IA', items: ['usar-com-ia/agents-md'] }
      ]
    })
  ]
});

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
    '/exemplos/testes-analytics/': `${base}/templates/casos-teste/`,
    '/dados/semantica/': `${base}/dados/visao-geral/`,
    '/dados/contrato-de-conhecimento/': `${base}/dados/visao-geral/`,
    '/fundamentos/promessa/': `${base}/metodo/visao-geral/`,
    '/metodo/revisao-e-entrega/': `${base}/validacao/checklist/`,
    '/fundamentos/escolher-documento/': `${base}/templates/`
  },
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
      // Sem rótulos próprios: o menu mostra o título da página, então os dois nunca divergem.
      sidebar: [
        { label: 'Início', link: '/' },
        { label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },
        { label: 'Guias', items: ['metodo/elicitar', 'metodo/identificacao-versoes'] },
        { label: 'Documentos do negócio', collapsed: true, items: [
          'templates/conceito', 'templates/processo', 'templates/decisao', 'templates/politica', 'templates/rubrica'
        ] },
        { label: 'Dados e Analytics', collapsed: true, items: [
          'dados/visao-geral', 'exemplos/analytics-integrado', 'templates/kpi', 'templates/dataset',
          'templates/relacionamento', 'templates/dashboard', 'templates/casos-teste'
        ] },
        { label: 'Entenda o método', collapsed: true, items: [
          'metodo/visao-geral', 'metodo/oito-dimensoes', 'fundamentos/conhecimento-tacito', 'metodo/limites'
        ] },
        { label: 'Consulta', collapsed: true, items: [
          'fundamentos/como-ler-os-campos', 'governanca/papeis', 'referencias', 'sobre/creditos'
        ] }
      ]
    })
  ]
});

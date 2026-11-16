import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const base = process.env.BASE_PATH || '/contexto-framework';
const favicon = (base === '/' ? '' : base.replace(/\/$/, '')) + '/favicon.svg';

export default defineConfig({
  site: process.env.SITE_URL || 'https://edoardolobl.github.io',
  base,
  integrations: [
    starlight({
      title: 'Contexto',
      description: 'Método para documentar conhecimento organizacional de modo explícito, contextualizado e verificável.',
      logo: { src: './src/assets/brand.svg', alt: 'Contexto' },
      favicon,
      locales: { root: { label: 'Português', lang: 'pt-BR' } },
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        { label: 'Comece aqui', items: [
          { slug: 'fundamentos/promessa' },
          { slug: 'fundamentos/conhecimento-tacito' },
          { slug: 'fundamentos/escolher-documento' }
        ] },
        { label: 'O método', items: [
          { slug: 'metodo/visao-geral' },
          { slug: 'metodo/oito-dimensoes' },
          { slug: 'metodo/elicitar' },
          { slug: 'metodo/revisao-e-entrega' }
        ] },
        { label: 'Biblioteca transversal', items: [
          { slug: 'templates' },
          { slug: 'templates/conceito' },
          { slug: 'templates/processo' },
          { slug: 'templates/decisao' },
          { slug: 'templates/politica' },
          { slug: 'templates/kpi' }
        ] },
        { label: 'Exemplos transversais', items: [
          { slug: 'exemplos/conceito-onboarding' },
          { slug: 'exemplos/processo-campanha' },
          { slug: 'exemplos/decisao-campanha' },
          { slug: 'exemplos/politica-despesas' },
          { slug: 'exemplos/kpi' }
        ] },
        { label: 'Dados e Analytics', items: [
          { slug: 'dados/visao-geral' },
          { slug: 'dados/semantica' },
          { slug: 'dados/contrato-de-conhecimento' },
          { slug: 'templates/dataset' },
          { slug: 'templates/relacionamento' },
          { slug: 'templates/dashboard' },
          { slug: 'templates/rubrica' },
          { slug: 'templates/casos-teste' },
          { slug: 'exemplos/analytics-integrado' },
          { slug: 'exemplos/rubrica-case' },
          { slug: 'exemplos/testes-analytics' }
        ] },
        { label: 'Validação', items: [{ slug: 'validacao/checklist' }] },
        { label: 'Governança', items: [{ slug: 'governanca/papeis' }] },
        { label: 'Referências', items: [{ slug: 'referencias' }] }
      ]
    })
  ]
});

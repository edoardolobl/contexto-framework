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
        { label: 'Comece aqui', items: [{ slug: 'fundamentos/promessa' }, { slug: 'fundamentos/conhecimento-tacito' }] },
        { label: 'O método', items: [{ slug: 'metodo/visao-geral' }, { slug: 'metodo/oito-dimensoes' }, { slug: 'metodo/elicitar' }] },
        { label: 'Templates', items: [{ slug: 'templates' }, { slug: 'templates/kpi' }] },
        { label: 'Exemplos', items: [{ slug: 'exemplos/kpi' }] },
        { label: 'Dados e Analytics', items: [{ slug: 'dados/semantica' }] },
        { label: 'Validação', items: [{ slug: 'validacao/checklist' }] },
        { label: 'Governança', items: [{ slug: 'governanca/papeis' }] },
        { label: 'Referências', items: [{ slug: 'referencias' }] }
      ]
    })
  ]
});

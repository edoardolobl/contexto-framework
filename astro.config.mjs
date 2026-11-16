import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: process.env.SITE_URL || 'https://edoardolobl.github.io',
  base: process.env.BASE_PATH || '/contexto-framework',
  integrations: [
    starlight({
      title: 'Contexto',
      description: 'Método para documentar conhecimento organizacional de modo explícito, contextualizado e verificável.',
      locales: { root: { label: 'Português', lang: 'pt-BR' } },
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        { label: 'Comece aqui', items: [{ slug: 'fundamentos/promessa' }] },
        { label: 'O método', items: [{ slug: 'metodo/oito-dimensoes' }] },
        { label: 'Templates', items: [{ slug: 'templates/kpi' }] },
        { label: 'Exemplos', items: [{ slug: 'exemplos/kpi' }] },
        { label: 'Dados e Analytics', items: [{ slug: 'dados/semantica' }] },
        { label: 'Referências', items: [{ slug: 'referencias' }] }
      ]
    })
  ]
});

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
      components: { Footer: './src/components/SiteFooter.astro' },
      social: [
        { icon: 'github', label: 'Repositório no GitHub', href: 'https://github.com/edoardolobl/contexto-framework' },
        { icon: 'linkedin', label: 'Edoardo Lobl no LinkedIn', href: 'https://www.linkedin.com/in/edoardolobl/' }
      ],
      sidebar: [
        { label: 'Comece aqui', items: [
          { slug: 'fundamentos/comece-em-5-minutos' },
          { slug: 'fundamentos/promessa' },
          { slug: 'fundamentos/conhecimento-tacito' },
          { slug: 'fundamentos/escolher-documento' },
          { slug: 'fundamentos/como-ler-os-campos' }
        ] },
        { label: 'O método', items: [
          { slug: 'metodo/visao-geral' },
          { slug: 'metodo/oito-dimensoes' },
          { slug: 'metodo/elicitar' },
          { slug: 'metodo/revisao-e-entrega' },
          { slug: 'metodo/limites' }
        ] },
        { label: 'Modelos', items: [
          { slug: 'templates', label: 'Biblioteca de modelos' },
          { slug: 'templates/conceito', label: 'Conceito e glossário' },
          { slug: 'templates/processo', label: 'Processo e procedimento' },
          { slug: 'templates/decisao', label: 'Regras e decisões' },
          { slug: 'templates/politica', label: 'Política e referência' },
          { slug: 'templates/kpi', label: 'KPI e métricas' },
          { slug: 'templates/rubrica', label: 'Rubrica de avaliação' }
        ] },
        { label: 'Exemplos', items: [
          { slug: 'exemplos/conceito-onboarding', label: 'Um conceito em RH' },
          { slug: 'exemplos/processo-campanha', label: 'Processo de campanha' },
          { slug: 'exemplos/decisao-campanha', label: 'Decisão e precedência' },
          { slug: 'exemplos/politica-despesas', label: 'Versões conflitantes' },
          { slug: 'exemplos/kpi', label: 'KPI de conversão' },
          { slug: 'exemplos/rubrica-case', label: 'Rubrica de uma análise' }
        ] },
        { label: 'Dados e Analytics', items: [
          { slug: 'dados/visao-geral' },
          { slug: 'dados/semantica' },
          { slug: 'dados/contrato-de-conhecimento' },
          { slug: 'templates/dataset', label: 'Modelo: dataset' },
          { slug: 'templates/relacionamento', label: 'Modelo: relacionamentos' },
          { slug: 'templates/dashboard', label: 'Modelo: dashboard' },
          { slug: 'templates/casos-teste', label: 'Modelo: perguntas de referência' },
          { slug: 'exemplos/analytics-integrado', label: 'Laboratório Aurora' },
          { slug: 'exemplos/testes-analytics', label: 'Perguntas do laboratório' }
        ] },
        { label: 'Validação', items: [{ slug: 'validacao/checklist' }] },
        { label: 'Governança', items: [{ slug: 'governanca/papeis' }] },
        { label: 'Referências', items: [{ slug: 'referencias' }] },
        { label: 'Sobre', items: [{ slug: 'sobre/creditos' }] }
      ]
    })
  ]
});

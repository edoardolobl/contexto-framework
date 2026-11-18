// Testes das regras puras do checklist visual (node --test). Sem navegador, sem rede.
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';

import {
  arquivoDaRota,
  avaliarAltura,
  avaliarEstouro,
  escalaUniforme,
  faceCarregada,
  formatarFalha,
  paginasDeModelo,
  paginasDoDist,
  requisicaoExterna,
  tipoDeConteudo,
} from '../visual/regras.mjs';

const MODELOS = `# pagina: endereço da página em src/content/docs/templates/<pagina>.mdx.
tipos:
  - slug: kpi
    pagina: kpi
    nome: Indicador (KPI)
  - slug: evento-coleta
    pagina: "evento-coleta"
    nome: Evento
  - slug: dataset
    pagina: dataset # comentário
`;

test('paginasDeModelo devolve as rotas na ordem do YAML e ignora comentários', () => {
  assert.deepEqual(paginasDeModelo(MODELOS), ['templates/kpi/', 'templates/evento-coleta/', 'templates/dataset/']);
});

test('paginasDeModelo devolve lista vazia para texto sem páginas', () => {
  assert.deepEqual(paginasDeModelo(''), []);
  assert.deepEqual(paginasDeModelo('tipos: []\n'), []);
});

test('paginasDoDist devolve só index.html com <main> e ignora redirecionamentos', () => {
  const dist = mkdtempSync(join(tmpdir(), 'dist-'));
  mkdirSync(join(dist, 'templates', 'kpi'), { recursive: true });
  mkdirSync(join(dist, 'antigo'), { recursive: true });
  writeFileSync(join(dist, 'index.html'), '<html><body><main>home</main></body></html>');
  writeFileSync(join(dist, 'templates', 'kpi', 'index.html'), '<body><main id="x">kpi</main>');
  writeFileSync(join(dist, 'antigo', 'index.html'), '<meta http-equiv="refresh" content="0; url=/novo/">');
  writeFileSync(join(dist, '404.html'), '<main>nada</main>');
  assert.deepEqual(paginasDoDist(dist), ['index.html', 'templates/kpi/index.html']);
});

test('paginasDoDist numa pasta inexistente devolve lista vazia', () => {
  assert.deepEqual(paginasDoDist(join(tmpdir(), 'nao-existe-visual-test')), []);
});

test('avaliarAltura aceita até 4 telas e reprova acima', () => {
  assert.deepEqual(avaliarAltura(3600), { ok: true, telas: 4, limite: 4 });
  assert.equal(avaliarAltura(3601).ok, false);
  assert.equal(avaliarAltura(900).ok, true);
  assert.equal(avaliarAltura(0).ok, true);
});

test('avaliarAltura respeita viewport e limite informados', () => {
  assert.equal(avaliarAltura(1800, 600, 3).ok, true);
  assert.equal(avaliarAltura(2000, 600, 3).ok, false);
  assert.equal(avaliarAltura(4500).telas, 5);
});

test('avaliarEstouro tolera 1px e acusa mais que isso', () => {
  assert.deepEqual(avaliarEstouro(390, 390), { ok: true, excesso: 0 });
  assert.equal(avaliarEstouro(391, 390).ok, true);
  assert.deepEqual(avaliarEstouro(392, 390), { ok: false, excesso: 2 });
  assert.equal(avaliarEstouro(380, 390).ok, true);
  assert.equal(avaliarEstouro(393, 390, 3).ok, true);
  assert.equal(avaliarEstouro(394, 390, 3).ok, false);
});

test('escalaUniforme devolve só os níveis com mais de um tamanho', () => {
  const medidas = [
    { nivel: 'h2', tamanho: '28px' },
    { nivel: 'h2', tamanho: '28px' },
    { nivel: 'h3', tamanho: '22px' },
    { nivel: 'h3', tamanho: '24px' },
    { nivel: 'h4', tamanho: '18px' },
  ];
  assert.deepEqual(escalaUniforme(medidas), [{ nivel: 'h3', tamanhos: ['22px', '24px'] }]);
});

test('escalaUniforme com escala limpa ou vazia devolve lista vazia', () => {
  assert.deepEqual(escalaUniforme([]), []);
  assert.deepEqual(escalaUniforme([{ nivel: 'h2', tamanho: '28px' }, { nivel: 'h2', tamanho: '28px' }]), []);
});

test('requisicaoExterna distingue origem local, outra origem e esquemas sem rede', () => {
  const local = 'http://127.0.0.1:4500';
  assert.equal(requisicaoExterna('http://127.0.0.1:4500/contexto-framework/a.css', local), false);
  assert.equal(requisicaoExterna('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans', local), true);
  assert.equal(requisicaoExterna('http://127.0.0.1:4501/x', local), true);
  assert.equal(requisicaoExterna('data:font/woff2;base64,AAAA', local), false);
  assert.equal(requisicaoExterna('blob:http://127.0.0.1:4500/uuid', local), false);
  assert.equal(requisicaoExterna('about:blank', local), false);
  assert.equal(requisicaoExterna('isto nao e url', local), true);
});

test('tipoDeConteudo cobre as extensões do portal e cai em octet-stream', () => {
  assert.equal(tipoDeConteudo('.html'), 'text/html; charset=utf-8');
  assert.equal(tipoDeConteudo('css'), 'text/css; charset=utf-8');
  assert.equal(tipoDeConteudo('.JS'), 'text/javascript; charset=utf-8');
  assert.equal(tipoDeConteudo('.woff2'), 'font/woff2');
  assert.equal(tipoDeConteudo('.svg'), 'image/svg+xml');
  assert.equal(tipoDeConteudo('.yaml'), 'text/plain; charset=utf-8');
  assert.equal(tipoDeConteudo('.xyz'), 'application/octet-stream');
  assert.equal(tipoDeConteudo(''), 'application/octet-stream');
});

test('formatarFalha traz regra, página, tema, largura e valor medido em uma linha', () => {
  const linha = formatarFalha({ regra: 'R1', pagina: 'templates/kpi/', tema: 'dark', largura: 1440, medido: '4,7 telas (limite 4)' });
  assert.equal(linha, 'FALHA R1 templates/kpi/ tema=dark largura=1440px: 4,7 telas (limite 4)');
  assert.ok(!linha.includes('\n'));
});

test('formatarFalha aceita campos ausentes sem lançar erro', () => {
  assert.equal(formatarFalha({ regra: 'R3', pagina: '/', medido: 'sem fonte' }), 'FALHA R3 / tema=- largura=-: sem fonte');
});

test('arquivoDaRota tira a base e acrescenta index.html nas rotas de pasta', () => {
  assert.equal(arquivoDaRota('/contexto-framework/', '/contexto-framework'), 'index.html');
  assert.equal(arquivoDaRota('/contexto-framework/templates/kpi/', '/contexto-framework'), 'templates/kpi/index.html');
  assert.equal(arquivoDaRota('/contexto-framework/templates/kpi', '/contexto-framework'), 'templates/kpi/index.html');
  assert.equal(arquivoDaRota('/contexto-framework/_astro/a.css?v=1', '/contexto-framework'), '_astro/a.css');
  assert.equal(arquivoDaRota('/contexto-framework/downloads/x.yaml#a', '/contexto-framework'), 'downloads/x.yaml');
  assert.equal(arquivoDaRota('/templates/kpi/', ''), 'templates/kpi/index.html');
});

test('arquivoDaRota recusa fora da base e tentativa de sair de dist', () => {
  assert.equal(arquivoDaRota('/outra/coisa', '/contexto-framework'), null);
  assert.equal(arquivoDaRota('/contexto-framework/../segredo', '/contexto-framework'), null);
  assert.equal(arquivoDaRota('/contexto-framework/%2e%2e/segredo', '/contexto-framework'), null);
  assert.equal(arquivoDaRota('/contexto-framework/a%00b', '/contexto-framework'), null);
  assert.equal(arquivoDaRota('/contexto-framework/a%ZZ', '/contexto-framework'), null);
  assert.equal(arquivoDaRota('/contexto-frameworkx/a', '/contexto-framework'), null);
});

test('faceCarregada exige uma face da família com status loaded', () => {
  const faces = [
    { family: '"IBM Plex Mono"', status: 'loaded' },
    { family: '"IBM Plex Sans"', status: 'unloaded' },
    { family: "'IBM Plex Sans'", status: 'loaded' },
  ];
  assert.equal(faceCarregada(faces, 'IBM Plex Sans'), true);
});

test('faceCarregada reprova quando nenhuma face da família foi declarada ou carregada', () => {
  assert.equal(faceCarregada([], 'IBM Plex Sans'), false);
  assert.equal(faceCarregada([{ family: 'IBM Plex Sans', status: 'unloaded' }], 'IBM Plex Sans'), false);
  assert.equal(faceCarregada([{ family: 'IBM Plex Sans', status: 'error' }], 'IBM Plex Sans'), false);
  assert.equal(faceCarregada([{ family: 'IBM Plex Sans Condensed', status: 'loaded' }], 'IBM Plex Sans'), false);
  assert.equal(faceCarregada(undefined, 'IBM Plex Sans'), false);
});

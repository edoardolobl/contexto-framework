#!/usr/bin/env node
// Checklist visual do portal construído (UX-03, UX-07, ADR 0016, ADR 0017).
// Serve dist/ sob BASE_PATH, abre as páginas no Chrome e mede quatro regras, nos temas claro e escuro:
//   R1 página de modelo a 1440x900 com no máximo 4 telas de altura (passos fechados, como vêm por padrão);
//   R2 toda página a 390x844 sem estouro horizontal;
//   R3 nas páginas de modelo e na home, uma face IBM Plex Sans carregada (document.fonts), aplicada ao body e sem
//      requisição externa;
//   R4 em .sl-markdown-content, um único font-size calculado por nível de h2 a h5 (modelos, home e Revise e aprove).
// Navegador, nesta ordem: CONTEXTO_CHROME; chromium do playwright-core, se o executável existir; canal 'chrome'.
import { existsSync, readFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

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
  VIEWPORT_ALTURA,
} from './visual/regras.mjs';

const RAIZ = resolve(fileURLToPath(new URL('.', import.meta.url)), '..');
const DIST = join(RAIZ, 'dist');
const TEMAS = ['light', 'dark'];
const DESKTOP = { width: 1440, height: VIEWPORT_ALTURA };
const CELULAR = { width: 390, height: 844 };
const ABAS_EM_PARALELO = 4;
const TEMPO_DE_CARGA_MS = 30000;
const FONTE = 'IBM Plex Sans';
// Quantas vezes uma página é visitada de novo quando html[data-theme] não bate com o tema pedido.
const REPETICOES_DE_TEMA = 2;

class ErroDeUso extends Error {}

function baseDoSite() {
  const base = `/${(process.env.BASE_PATH ?? '/contexto-framework').replace(/^\/+|\/+$/g, '')}`;
  return base === '/' ? '' : base;
}

function iniciarServidor(dist, base) {
  const servidor = createServer(async (pedido, resposta) => {
    const relativo = arquivoDaRota(pedido.url ?? '/', base);
    const alvo = relativo ? resolve(dist, relativo) : null;
    if (!alvo || !alvo.startsWith(dist) || !existsSync(alvo)) {
      resposta.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }).end('nao encontrado');
      return;
    }
    try {
      const corpo = await readFile(alvo);
      resposta.writeHead(200, { 'Content-Type': tipoDeConteudo(extname(alvo)) }).end(corpo);
    } catch {
      resposta.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' }).end('erro ao ler');
    }
  });
  return new Promise((ok, falha) => {
    servidor.once('error', falha);
    servidor.listen(0, '127.0.0.1', () => ok({ servidor, origem: `http://127.0.0.1:${servidor.address().port}` }));
  });
}

async function carregarPlaywright() {
  try {
    return (await import('playwright-core')).chromium;
  } catch {
    throw new ErroDeUso('playwright-core não está instalado; rode npm ci (a dependência é playwright-core 1.65.1).');
  }
}

async function abrirNavegador(chromium) {
  const tentativas = [];
  const doAmbiente = process.env.CONTEXTO_CHROME;
  if (doAmbiente) {
    if (!existsSync(doAmbiente)) throw new ErroDeUso(`CONTEXTO_CHROME aponta para um arquivo que não existe: ${doAmbiente}`);
    tentativas.push({ rotulo: 'CONTEXTO_CHROME', opcoes: { executablePath: doAmbiente } });
  }
  const instalado = chromium.executablePath();
  if (instalado && existsSync(instalado)) tentativas.push({ rotulo: 'chromium do playwright-core', opcoes: { executablePath: instalado } });
  tentativas.push({ rotulo: "canal 'chrome' do sistema", opcoes: { channel: 'chrome' } });
  const motivos = [];
  for (const { rotulo, opcoes } of tentativas) {
    try {
      const navegador = await chromium.launch({ headless: true, ...opcoes });
      console.log(`Navegador: ${rotulo}`);
      return navegador;
    } catch (erro) {
      motivos.push(`${rotulo}: ${String(erro.message).split('\n')[0]}`);
    }
  }
  throw new ErroDeUso(
    'Nenhum Chrome encontrado. Defina CONTEXTO_CHROME com o caminho do executável, ou rode ' +
      '"npx playwright-core install --with-deps chromium", ou instale o Google Chrome.\n  ' + motivos.join('\n  '),
  );
}

/** Roda no navegador: devolve todas as medidas de uma vez; as regras decidem fora. */
function medirNaPagina() {
  return document.fonts.ready.then(() => {
    const raiz = document.documentElement;
    const niveis = ['h2', 'h3', 'h4', 'h5'];
    const escala = [...document.querySelectorAll('.sl-markdown-content :is(h2, h3, h4, h5)')]
      .filter((h) => niveis.includes(h.tagName.toLowerCase()))
      .map((h) => ({ nivel: h.tagName.toLowerCase(), tamanho: getComputedStyle(h).fontSize }));
    return {
      tema: raiz.dataset.theme ?? null,
      altura: raiz.scrollHeight,
      largura: raiz.scrollWidth,
      faces: [...document.fonts].map((face) => ({ family: face.family, status: face.status })),
      familiaDoBody: getComputedStyle(document.body).fontFamily,
      escala,
    };
  });
}

function rotaPublicada(arquivo) {
  return arquivo === 'index.html' ? '' : arquivo.replace(/index\.html$/, '');
}

// Páginas fora dos modelos e da home em que só a escala de títulos (R4) é medida, como pede a frente visual.
const PAGINAS_SO_ESCALA = ['percurso/revise-e-aprove/'];

function regrasDesktop(modelos) {
  return (rota) => {
    if (modelos.includes(rota)) return ['R1', 'R3', 'R4'];
    if (PAGINAS_SO_ESCALA.includes(rota)) return ['R4'];
    return ['R3', 'R4'];
  };
}

function tarefasDe({ modelos, todas }) {
  return [
    { viewport: DESKTOP, regrasPorPagina: regrasDesktop(modelos), paginas: ['', ...modelos, ...PAGINAS_SO_ESCALA] },
    { viewport: CELULAR, regrasPorPagina: () => ['R2'], paginas: todas },
  ];
}

async function visitarUmaVez(contexto, url, origem, tema) {
  const pagina = await contexto.newPage();
  const externas = [];
  pagina.on('request', (pedido) => {
    if (requisicaoExterna(pedido.url(), origem)) externas.push(pedido.url());
  });
  try {
    await pagina.emulateMedia({ colorScheme: tema === 'dark' ? 'dark' : 'light' });
    await pagina.goto(url, { waitUntil: 'networkidle', timeout: TEMPO_DE_CARGA_MS });
    // O Starlight define html[data-theme] por script; sob carga a medida pode chegar antes dele.
    await pagina
      .waitForFunction((esperado) => document.documentElement.dataset.theme === esperado, tema, { timeout: TEMPO_DE_CARGA_MS })
      .catch(() => { /* a regra TEMA registra o valor encontrado */ });
    const medidas = await pagina.evaluate(medirNaPagina);
    return { medidas, externas };
  } finally {
    await pagina.close();
  }
}

async function visitar(contexto, url, origem, tema) {
  let visita = await visitarUmaVez(contexto, url, origem, tema);
  for (let i = 0; i < REPETICOES_DE_TEMA && visita.medidas.tema !== tema; i += 1) {
    visita = await visitarUmaVez(contexto, url, origem, tema);
  }
  return visita;
}

function julgar({ regras, rota, tema, viewport, medidas, externas }) {
  const resultados = [];
  const ponto = (regra, ok, medido) => resultados.push({ regra, ok, medido });
  if (medidas.tema !== tema) ponto('TEMA', false, `html[data-theme] é ${medidas.tema}, esperado ${tema}`);
  if (regras.includes('R1')) {
    const { ok, telas, limite } = avaliarAltura(medidas.altura);
    ponto('R1', ok, `${telas.toFixed(2)} telas de ${VIEWPORT_ALTURA}px (limite ${limite}), altura ${medidas.altura}px`);
  }
  if (regras.includes('R2')) {
    const { ok, excesso } = avaliarEstouro(medidas.largura, viewport.width);
    ponto('R2', ok, `scrollWidth ${medidas.largura}px em ${viewport.width}px (excesso ${excesso}px)`);
  }
  if (regras.includes('R3')) {
    const familia = medidas.familiaDoBody.replace(/["']/g, '').trim();
    const comecaPorPlex = familia.startsWith(FONTE);
    const carregada = faceCarregada(medidas.faces, FONTE);
    const detalhes = [`face carregada ${carregada}`, `body ${familia.split(',')[0]}`, `requisições externas ${externas.length}`];
    ponto('R3', carregada && comecaPorPlex && externas.length === 0,
      detalhes.join('; ') + (externas.length ? ` (${externas.slice(0, 3).join(' ')})` : ''));
  }
  if (regras.includes('R4')) {
    const quebrados = escalaUniforme(medidas.escala);
    ponto('R4', quebrados.length === 0,
      quebrados.length ? quebrados.map((q) => `${q.nivel}: ${q.tamanhos.join(' e ')}`).join('; ') : `${medidas.escala.length} títulos, um tamanho por nível`);
  }
  return resultados.map((r) => ({ ...r, pagina: rota || '/', tema, largura: viewport.width }));
}

async function executarTarefa(navegador, tarefa, tema, ctx) {
  const contexto = await navegador.newContext({ viewport: tarefa.viewport, colorScheme: tema });
  await contexto.addInitScript((valor) => {
    try { localStorage.setItem('starlight-theme', valor); } catch { /* sem armazenamento */ }
  }, tema);
  const fila = [...tarefa.paginas];
  const ordem = new Map(tarefa.paginas.map((rota, i) => [rota || '/', i]));
  const resultados = [];
  const trabalhador = async () => {
    for (let rota = fila.shift(); rota !== undefined; rota = fila.shift()) {
      const regras = tarefa.regrasPorPagina(rota);
      const url = `${ctx.origem}${ctx.base}/${rota}`;
      try {
        const { medidas, externas } = await visitar(contexto, url, ctx.origem, tema);
        resultados.push(...julgar({ regras, rota, tema, viewport: tarefa.viewport, medidas, externas }));
      } catch (erro) {
        resultados.push({ regra: 'CARGA', ok: false, pagina: rota || '/', tema, largura: tarefa.viewport.width,
          medido: String(erro.message).split('\n')[0] });
      }
    }
  };
  try {
    await Promise.all(Array.from({ length: Math.min(ABAS_EM_PARALELO, fila.length) }, trabalhador));
  } finally {
    await contexto.close();
  }
  return resultados.sort((a, b) => ordem.get(a.pagina) - ordem.get(b.pagina));
}

async function principal() {
  if (!existsSync(join(DIST, 'index.html'))) throw new ErroDeUso('dist/ não existe ou está vazio; rode npm run build antes do checklist visual.');
  const base = baseDoSite();
  const modelos = paginasDeModelo(readFileSync(join(RAIZ, 'src', 'data', 'modelos.yaml'), 'utf8'));
  if (modelos.length === 0) throw new ErroDeUso('nenhuma página de modelo em src/data/modelos.yaml.');
  const todas = paginasDoDist(DIST).map(rotaPublicada);
  const faltando = modelos.filter((m) => !todas.includes(m));
  if (faltando.length) throw new ErroDeUso(`páginas de modelo ausentes em dist/: ${faltando.join(', ')}`);
  const chromium = await carregarPlaywright();
  const navegador = await abrirNavegador(chromium);
  const { servidor, origem } = await iniciarServidor(DIST, base);
  const falhas = [];
  let total = 0;
  try {
    for (const tarefa of tarefasDe({ modelos, todas })) {
      for (const tema of TEMAS) {
        const resultados = await executarTarefa(navegador, tarefa, tema, { origem, base });
        for (const r of resultados) {
          total += 1;
          const linha = formatarFalha({ ...r, medido: r.medido });
          console.log(r.ok ? linha.replace('FALHA', 'OK   ') : linha);
          if (!r.ok) falhas.push(linha);
        }
      }
    }
  } finally {
    await navegador.close();
    servidor.close();
  }
  console.log(falhas.length ? `\n${falhas.length} falha(s) em ${total} medições.` : `\nOK: ${total} medições, nenhuma falha.`);
  process.exitCode = falhas.length ? 1 : 0;
}

principal().catch((erro) => {
  console.error(`ERRO: ${erro instanceof ErroDeUso ? erro.message : `falha inesperada: ${erro.message}`}`);
  process.exitCode = 1;
});

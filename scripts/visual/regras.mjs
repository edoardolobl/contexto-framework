// Regras puras do checklist visual (UX-03, UX-07, ADR 0016, ADR 0017). Sem navegador e sem rede:
// o que precisa de Chrome fica em scripts/check_visual.mjs; aqui ficam as contas e os formatos.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

export const VIEWPORT_ALTURA = 900;
export const LIMITE_DE_TELAS = 4;
export const TOLERANCIA_DE_ESTOURO = 1;

const TIPOS = {
  html: 'text/html; charset=utf-8',
  css: 'text/css; charset=utf-8',
  js: 'text/javascript; charset=utf-8',
  mjs: 'text/javascript; charset=utf-8',
  json: 'application/json; charset=utf-8',
  svg: 'image/svg+xml',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  webp: 'image/webp',
  ico: 'image/x-icon',
  woff2: 'font/woff2',
  woff: 'font/woff',
  txt: 'text/plain; charset=utf-8',
  yaml: 'text/plain; charset=utf-8',
  yml: 'text/plain; charset=utf-8',
  md: 'text/plain; charset=utf-8',
  sql: 'text/plain; charset=utf-8',
  xml: 'application/xml; charset=utf-8',
  pdf: 'application/pdf',
  wasm: 'application/wasm',
};

/** Rotas `templates/<pagina>/` na ordem de src/data/modelos.yaml (lê só as linhas `pagina:`). */
export function paginasDeModelo(textoModelosYaml) {
  const rotas = [];
  for (const linha of String(textoModelosYaml).split('\n')) {
    const achado = /^\s*(?:-\s+)?pagina:\s*["']?([A-Za-z0-9_-]+)["']?\s*(?:#.*)?$/.exec(linha);
    if (achado) rotas.push(`templates/${achado[1]}/`);
  }
  return rotas;
}

function indices(dir, relativo = '') {
  const achados = [];
  for (const entrada of readdirSync(join(dir, relativo), { withFileTypes: true })) {
    const caminho = relativo ? `${relativo}/${entrada.name}` : entrada.name;
    if (entrada.isDirectory()) achados.push(...indices(dir, caminho));
    else if (entrada.name === 'index.html') achados.push(caminho);
  }
  return achados;
}

/** Caminhos (relativos a `dir`, com `/`) dos index.html que têm <main>; redirecionamentos ficam de fora. */
export function paginasDoDist(dir) {
  if (!existsSync(dir)) return [];
  return indices(dir)
    .filter((caminho) => /<main[\s>]/.test(readFileSync(join(dir, ...caminho.split('/')), 'utf8')))
    .sort();
}

export function avaliarAltura(alturaPx, viewport = VIEWPORT_ALTURA, limite = LIMITE_DE_TELAS) {
  const telas = alturaPx / viewport;
  return { ok: telas <= limite, telas, limite };
}

export function avaliarEstouro(scrollWidth, larguraViewport, tolerancia = TOLERANCIA_DE_ESTOURO) {
  const excesso = Math.max(0, scrollWidth - larguraViewport);
  return { ok: excesso <= tolerancia, excesso };
}

/** Níveis (h2 a h5) que aparecem com mais de um font-size calculado, com os tamanhos achados. */
export function escalaUniforme(medidas) {
  const porNivel = new Map();
  for (const { nivel, tamanho } of medidas) {
    if (!porNivel.has(nivel)) porNivel.set(nivel, new Set());
    porNivel.get(nivel).add(tamanho);
  }
  return [...porNivel.entries()]
    .filter(([, tamanhos]) => tamanhos.size > 1)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([nivel, tamanhos]) => ({ nivel, tamanhos: [...tamanhos].sort() }));
}

/**
 * Verdadeiro quando alguma face de `familia` (vinda de document.fonts) terminou de carregar.
 * document.fonts.check() não serve: devolve true quando nenhuma face foi declarada.
 */
export function faceCarregada(faces, familia) {
  return (faces ?? []).some((face) => String(face.family).replace(/["']/g, '').trim() === familia && face.status === 'loaded');
}

/** Verdadeiro quando a requisição sai para outra origem. data:, blob: e about: não usam a rede. */
export function requisicaoExterna(url, origemLocal) {
  let endereco;
  try {
    endereco = new URL(url);
  } catch {
    return true;
  }
  if (['data:', 'blob:', 'about:'].includes(endereco.protocol)) return false;
  return endereco.origin !== origemLocal;
}

export function tipoDeConteudo(extensao) {
  const chave = String(extensao).replace(/^\./, '').toLowerCase();
  return TIPOS[chave] ?? 'application/octet-stream';
}

export function formatarFalha({ regra, pagina, tema, largura, medido }) {
  return `FALHA ${regra} ${pagina} tema=${tema ?? '-'} largura=${largura == null ? '-' : `${largura}px`}: ${medido}`;
}

/** Arquivo de dist/ (relativo, com `/`) para o caminho pedido sob `base`; null se fora da base ou suspeito. */
export function arquivoDaRota(caminhoDaUrl, base) {
  const semConsulta = caminhoDaUrl.split('#')[0].split('?')[0];
  const raiz = base.replace(/\/+$/, '');
  if (raiz && semConsulta !== raiz && !semConsulta.startsWith(`${raiz}/`)) return null;
  let resto;
  try {
    resto = decodeURIComponent(semConsulta.slice(raiz.length));
  } catch {
    return null;
  }
  if (resto.includes('\0') || resto.includes('\\') || resto.split('/').includes('..')) return null;
  const limpo = resto.replace(/^\/+/, '');
  if (limpo === '' || limpo.endsWith('/')) return `${limpo}index.html`;
  const ultimo = limpo.split('/').pop();
  return ultimo.includes('.') ? limpo : `${limpo}/index.html`;
}


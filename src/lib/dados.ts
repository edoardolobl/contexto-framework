/**
 * Leitura dos arquivos de dados de src/data, a fonte única de modelos, percurso, entradas e dimensões.
 * Mesmo padrão de ExampleDoc: fs no build e o parse do pacote yaml.
 * Arquivo ausente ou campo faltando interrompe o build com uma mensagem que cita o arquivo.
 */
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';

export type Nivel = 'nucleo' | 'segundo' | 'complementar';

export interface Modelo {
  slug: string;
  pagina: string;
  nome: string;
  nivel: Nivel;
  tarefa: string;
  resumo: string;
  quando: string;
  resultado: string;
  preparar: string;
  rotulo_download: string;
}

export interface Passo {
  numero: number;
  pagina: string;
  titulo: string;
}

export interface Destino {
  pagina: string;
  titulo: string;
}

export interface Percurso {
  passos: Passo[];
  depois_do_ultimo: Destino;
}

export interface Entrada {
  sintoma: string;
  texto: string;
  pagina: string;
  provisorio: boolean;
  nota?: string;
}

export interface Dimensao {
  nome: string;
  pergunta: string;
  revisao: string;
  resposta_fraca: string;
  resposta_util: string;
  onde_procurar: string;
  metadado_comum?: string;
}

const PASTA_DE_DADOS = path.join(process.cwd(), 'src', 'data');
const NIVEIS: readonly Nivel[] = ['nucleo', 'segundo', 'complementar'];
const CAMPOS_DO_MODELO = ['slug', 'pagina', 'nome', 'nivel', 'tarefa', 'resumo', 'quando', 'resultado', 'preparar', 'rotulo_download'] as const;
const CAMPOS_DA_DIMENSAO = ['nome', 'pergunta', 'revisao', 'resposta_fraca', 'resposta_util', 'onde_procurar'] as const;

type Registro = Record<string, unknown>;

function lerArquivo(nome: string): Registro {
  const caminho = path.join(PASTA_DE_DADOS, nome);
  if (!fs.existsSync(caminho)) {
    throw new Error(`src/data/${nome} não encontrado.`);
  }
  const dados: unknown = parse(fs.readFileSync(caminho, 'utf8'));
  if (!dados || typeof dados !== 'object' || Array.isArray(dados)) {
    throw new Error(`src/data/${nome} precisa ser um objeto YAML.`);
  }
  return dados as Registro;
}

function lista(dados: Registro, chave: string, arquivo: string): Registro[] {
  const valor = dados[chave];
  if (!Array.isArray(valor) || valor.length === 0) {
    throw new Error(`src/data/${arquivo}: a lista '${chave}' está ausente ou vazia.`);
  }
  return valor.map((item, indice) => {
    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      throw new Error(`src/data/${arquivo}: o item ${indice + 1} de '${chave}' não é um objeto.`);
    }
    return item as Registro;
  });
}

function texto(item: Registro, campo: string, onde: string): string {
  const valor = item[campo];
  if (typeof valor !== 'string' || valor.trim() === '') {
    throw new Error(`${onde}: o campo '${campo}' está ausente ou vazio.`);
  }
  return valor;
}

function textoOpcional(item: Registro, campo: string, onde: string): string | undefined {
  return item[campo] === undefined || item[campo] === null ? undefined : texto(item, campo, onde);
}

/** Base do site sempre com barra no fim, para montar `${baseUrl()}templates/kpi/`. */
export function baseUrl(): string {
  const bruta = import.meta.env.BASE_URL;
  return bruta.endsWith('/') ? bruta : `${bruta}/`;
}

/** Endereço de uma página a partir do slug de src/data ('templates/kpi' vira '/base/templates/kpi/'). */
export function urlDaPagina(pagina: string): string {
  const limpa = pagina.replace(/^\/+|\/+$/g, '');
  return limpa === '' ? baseUrl() : `${baseUrl()}${limpa}/`;
}

export function lerModelos(): Modelo[] {
  return lista(lerArquivo('modelos.yaml'), 'tipos', 'modelos.yaml').map((item, indice) => {
    const onde = `src/data/modelos.yaml, tipo ${indice + 1}`;
    const campos = Object.fromEntries(CAMPOS_DO_MODELO.map((campo) => [campo, texto(item, campo, onde)]));
    if (!NIVEIS.includes(campos.nivel as Nivel)) {
      throw new Error(`${onde}: nível '${campos.nivel}' inválido; use ${NIVEIS.join(', ')}.`);
    }
    return campos as unknown as Modelo;
  });
}

export function modeloPorSlug(slug: string): Modelo {
  const modelo = lerModelos().find((item) => item.slug === slug);
  if (!modelo) {
    throw new Error(`Modelo '${slug}' não está em src/data/modelos.yaml.`);
  }
  return modelo;
}

export function lerPercurso(): Percurso {
  const dados = lerArquivo('percurso.yaml');
  const passos = lista(dados, 'passos', 'percurso.yaml').map((item, indice) => {
    const onde = `src/data/percurso.yaml, passo ${indice + 1}`;
    if (typeof item.numero !== 'number' || item.numero !== indice + 1) {
      throw new Error(`${onde}: 'numero' precisa ser ${indice + 1}.`);
    }
    return { numero: item.numero, pagina: texto(item, 'pagina', onde), titulo: texto(item, 'titulo', onde) };
  });
  const depois = dados.depois_do_ultimo;
  if (!depois || typeof depois !== 'object' || Array.isArray(depois)) {
    throw new Error("src/data/percurso.yaml: 'depois_do_ultimo' está ausente.");
  }
  const onde = 'src/data/percurso.yaml, depois_do_ultimo';
  const destino = depois as Registro;
  return { passos, depois_do_ultimo: { pagina: texto(destino, 'pagina', onde), titulo: texto(destino, 'titulo', onde) } };
}

export function lerEntradas(): Entrada[] {
  return lista(lerArquivo('entradas.yaml'), 'entradas', 'entradas.yaml').map((item, indice) => {
    const onde = `src/data/entradas.yaml, entrada ${indice + 1}`;
    if (typeof item.provisorio !== 'boolean') {
      throw new Error(`${onde}: o campo 'provisorio' precisa ser true ou false.`);
    }
    const nota = textoOpcional(item, 'nota', onde);
    if (item.provisorio && !nota) {
      throw new Error(`${onde}: entrada provisória precisa de 'nota'.`);
    }
    return {
      sintoma: texto(item, 'sintoma', onde),
      texto: texto(item, 'texto', onde),
      pagina: texto(item, 'pagina', onde),
      provisorio: item.provisorio,
      nota,
    };
  });
}

export function lerDimensoes(): Dimensao[] {
  return lista(lerArquivo('dimensoes.yaml'), 'dimensoes', 'dimensoes.yaml').map((item, indice) => {
    const onde = `src/data/dimensoes.yaml, dimensão ${indice + 1}`;
    const campos = Object.fromEntries(CAMPOS_DA_DIMENSAO.map((campo) => [campo, texto(item, campo, onde)]));
    return { ...campos, metadado_comum: textoOpcional(item, 'metadado_comum', onde) } as Dimensao;
  });
}

/** Rota da página atual como em percurso.yaml: sem barras e sem o sufixo index. */
export function rotaDaPagina(id: string): string {
  return id.replace(/(^|\/)index$/, '').replace(/^\/+|\/+$/g, '');
}

---
name: mapear-projeto
description: "Analisa um projeto/codebase existente e gera (ou atualiza) o MAPA-PROJETO.md — o doc de 'como o projeto funciona por dentro' (arquitetura, arquivos-chave, fluxos de dados, tabelas, gotchas) pra você parar de re-explorar toda sessão. Use SEMPRE que disser: mapear projeto, gerar mapa do projeto, documentar como funciona, criar MAPA-PROJETO, onboard do codebase, entender o projeto e salvar, atualizar o mapa, /mapear-projeto — ou ao começar a trabalhar num projeto que ainda não tem MAPA-PROJETO.md."
model: sonnet
effort: high
---

# /mapear-projeto — Gera o MAPA-PROJETO.md de um codebase

## O que é

Analisa um projeto existente e destila **como ele funciona** num `MAPA-PROJETO.md` persistente na raiz do projeto. Isso para o re-trabalho de re-explorar o codebase toda sessão.

Faz parte do **padrão de contexto persistente** (trio de docs):
- `CLAUDE.md` — regras/convenções ("faça assim")
- **`MAPA-PROJETO.md`** — como funciona por dentro (ESTA skill gera)
- `HISTORICO-SESSOES.md` — o que mudou por sessão (via `zx-worklog.py`)

## Quando usar
- Projeto sem `MAPA-PROJETO.md` ainda (primeiro mapeamento).
- Atualizar mapa depois de mudança estrutural relevante.
- Backfill: destilar conhecimento acumulado (código + notas) pro mapa.

## Processo

### 1. Localizar o projeto
Diretório passado pelo usuário, ou o cwd. Confirmar que existe.

### 2. Coletar contexto de MÚLTIPLAS fontes (em paralelo)
Disparar Agent(Explore) em paralelo (1 por frente) — investigação aberta é o caso de fan-out:
- **Estrutura & entrypoints:** linguagem/stack, como roda (dev/build/deploy), rotas/entrypoints, pastas-chave (arquivo → o que faz).
- **Modelo de dados:** tabelas/schema, storage, migrations; que dados cada área lê/escreve.
- **Fluxos principais:** os 2-4 fluxos de dados críticos ponta-a-ponta (ex: venda → tabela X → efeito Y).
- **Gotchas & deploy:** armadilhas conhecidas, comandos de deploy, integrações externas, segredos (SEM copiar valores).

Também ler direto (barato): `CLAUDE.md`/`README` do projeto.

### 3. VERIFICAR antes de afirmar
Notas antigas são ponto-no-tempo; código muda. Toda afirmação do mapa deve bater com o código ATUAL. Se algo não se confirma mais no código, marcar como "a verificar" ou omitir — nunca copiar cego.

> **O golpe:** ao verificar cada afirmação contra o código, a skill não só documenta — ela **audita**. É comum ela achar README desatualizado, config apontando pro lugar errado ou até segredo vazado no histórico. Documentar vira auditoria de brinde.

### 4. Escrever MAPA-PROJETO.md (template)
Prepend do header padrão (com a ressalva de verificação) + seções. Template de referência em `templates/MAPA-PROJETO.template.md` (adaptar ao projeto — nem toda seção existe em todo projeto):

```markdown
# Mapa do Projeto — <nome>

> **Como o projeto funciona por dentro.** Doc vivo: leio ao começar aqui em vez de re-explorar.
> Código muda — ponto de partida rápido. **Verificar contra o código atual antes de afirmar como fato.**
> Complementa: `CLAUDE.md` (regras) · `HISTORICO-SESSOES.md` (o que mudou). Seed: <data>.

## Visão geral
## Stack
## Entrypoints / páginas-chave (rota/arquivo → o que faz)
## Modelo de dados (tabelas/schema → papel)
## Fluxos principais (ponta-a-ponta)
## Integrações externas
## Gotchas / armadilhas conhecidas
## Comandos (dev / build / deploy)
```

Regras de conteúdo:
- Concreto e verificado: file:line quando ajudar, valores literais (nomes de tabela, campos, portas).
- SEM segredos (tokens, senhas) — só apontar ONDE vivem.

### 5. Wire-up
- Se o projeto tem `CLAUDE.md` sem ponteiro, adicionar no topo:
  ```
  > **Como o projeto funciona:** ver `MAPA-PROJETO.md` na raiz (ler ao começar).
  > **Histórico de sessões:** ver `HISTORICO-SESSOES.md` na raiz.
  ```

### 6. Reportar
Resumo: path do MAPA gerado, seções preenchidas, e o que ficou "a verificar" (incluindo qualquer defeito/inconsistência encontrado na etapa 3).

## Manutenção do histórico (sem depender de um comando de encerramento)
Ao terminar uma sessão de trabalho, registre o que mudou com o `zx-worklog.py`:

```bash
zx-worklog.py add --dir . \
  --title "o que você fez" \
  --body $'**Feito:** ...\n**Arquivos:** ...\n**Pendências:** ...' \
  --summary "1 linha pro índice"
```

Isso grava em `HISTORICO-SESSOES.md` (na raiz do projeto) e atualiza o índice central. Rode `/mapear-projeto` de novo quando a estrutura mudar de forma relevante.

## Notas
- Projeto PÚBLICO (repo que outros clonam): o MAPA vai commitado — garantir que não tem segredo.
- É o passo de "onboard do codebase" que falta na maioria dos fluxos: dá ao assistente o mapa mental do projeto de uma vez, em vez de reconstruir do zero toda sessão.

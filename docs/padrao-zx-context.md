# O padrão de contexto persistente

> Engenharia de contexto pra Claude Code: fazer a IA lembrar de tudo entre sessões, por projeto.

## O problema — "context rot"

Toda vez que você abre o Claude Code num projeto, ele começa do zero:

- **Re-explora o codebase** — lê os mesmos arquivos, refaz o mesmo mapa mental, gasta os mesmos tokens.
- **Esquece o que já foi feito** — a decisão de ontem, o bug que você já corrigiu, o "não mexa nisso porque quebra".
- **Empurra tudo pra memória global** — que incha, mistura projetos e vira ruído.

O conhecimento do projeto existe só na sua cabeça e no histórico da conversa — que some quando a sessão fecha. Isso é **context rot**: o contexto apodrece a cada nova sessão.

## O conceito — artefatos persistentes por projeto

Engenharia de contexto = tratar o contexto do projeto como **artefato versionado**, que mora na pasta do projeto, não na conversa. Três documentos, cada um com um papel claro:

| Documento | Pergunta que responde | Analogia |
|---|---|---|
| `CLAUDE.md` | **Como eu devo agir aqui?** (regras, convenções, "faça assim") | as regras da casa |
| `MAPA-PROJETO.md` | **Como o projeto funciona por dentro?** (arquitetura, arquivos, fluxos, tabelas, gotchas) | a planta baixa |
| `HISTORICO-SESSOES.md` | **O que mudou, sessão a sessão?** (decisões, entregas, pendências) | o diário de bordo |

Os três juntos dão ao assistente, logo na primeira mensagem, o que antes ele levava meia sessão pra reconstruir.

### De onde vem a ideia
- **Disciplina de processo** (brainstorm → plano → TDD → debug → review) resolve *como trabalhar*, mas não guarda **mapa do codebase** nem **estado entre sessões**.
- Frameworks de contexto (ex.: o padrão CONTEXT/STATE do GSD) resolvem exatamente essas duas lacunas com artefatos persistentes.
- Este padrão junta as duas ideias: `MAPA-PROJETO.md` ≈ o "CONTEXT" (como funciona) e `HISTORICO-SESSOES.md` ≈ o "STATE" (o que mudou).

## O sistema — como funciona na prática

### `MAPA-PROJETO.md` — via skill `/mapear-projeto`
A skill dispara agentes de exploração em paralelo (estrutura, dados, fluxos, gotchas), **verifica cada afirmação contra o código atual** e escreve o mapa na raiz do projeto. Rode uma vez ao chegar num projeto sem mapa, e de novo quando a estrutura mudar.

> **Auditoria de brinde:** como a skill confere tudo contra o código, ela costuma achar defeito real no caminho — README desatualizado, config apontando pro lugar errado, até segredo vazado no histórico. Documentar vira auditoria.

### `HISTORICO-SESSOES.md` — via `zx-worklog.py`
Ao terminar de trabalhar, você registra o que mudou:

```bash
zx-worklog.py add --dir . \
  --title "o que você fez" \
  --body $'**Feito:** ...\n**Arquivos:** ...\n**Pendências:** ...' \
  --summary "1 linha pro índice"
```

Isso faz duas coisas:
1. **Prepend** no `HISTORICO-SESSOES.md` da raiz do projeto (mais recente no topo).
2. **Upsert** num índice central (`~/.context-worklogs/INDEX.md`) que lista TODO projeto com histórico — resolve o caso de projetos espalhados por várias pastas e sem git.

Funciona **com ou sem git** — o histórico é um arquivo markdown, não depende de commits.

### `CLAUDE.md` — você já escreve
É o arquivo de regras nativo do Claude Code. O padrão só pede um ponteiro no topo dele:

```markdown
> **Como o projeto funciona:** ver `MAPA-PROJETO.md` na raiz (ler ao começar).
> **Histórico de sessões:** ver `HISTORICO-SESSOES.md` na raiz.
```

## Por que muda o jogo

- **Zero re-exploração** — o assistente lê o mapa em vez de reconstruí-lo. Menos tokens, menos tempo, respostas certeiras já na primeira mensagem.
- **Continuidade real** — você (ou outra pessoa, ou outra IA) retoma qualquer projeto sem perder o fio.
- **Escala pra N projetos** — quem toca muitos projetos ao mesmo tempo (clientes, produtos) não perde o contexto de nenhum.
- **Onboarding instantâneo** — um projeto novo pra você fica "conhecido" em minutos.

## Fluxo recomendado

1. Chegou num projeto → **`/mapear-projeto`** gera o `MAPA-PROJETO.md`.
2. Adicione o ponteiro no `CLAUDE.md`.
3. Trabalhou → **`zx-worklog.py add`** registra a sessão no `HISTORICO-SESSOES.md`.
4. Retomou depois → **leia os dois** antes de mexer no código.

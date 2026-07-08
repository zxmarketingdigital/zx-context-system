# zx-context-system

**Engenharia de contexto pro Claude Code: faça a IA lembrar de tudo — por projeto, entre sessões.**

Toda vez que você abre o Claude Code num projeto, ele começa do zero: re-explora o codebase, esquece o que já foi feito, empurra tudo pra memória global que incha. Isso é **context rot**.

Este repo é o antídoto: um padrão simples de **três documentos persistentes** por projeto, mais as ferramentas que os mantêm no automático.

| Documento | Responde | Como nasce |
|---|---|---|
| `CLAUDE.md` | Como eu devo agir aqui? (regras) | você escreve (nativo do Claude Code) |
| `MAPA-PROJETO.md` | Como o projeto funciona por dentro? | skill **`/mapear-projeto`** |
| `HISTORICO-SESSOES.md` | O que mudou, sessão a sessão? | script **`zx-worklog.py`** |

Os três juntos entregam ao assistente, já na primeira mensagem, o que antes ele levava meia sessão pra reconstruir.

---

## Instalação

```bash
gh repo clone zxmarketingdigital/zx-context-system
cd zx-context-system
bash install.sh
```

O `install.sh` copia:
- `skills/mapear-projeto` → `~/.claude/skills/mapear-projeto` (com os templates dentro)
- `bin/zx-worklog.py` → `~/bin/zx-worklog.py` (executável)

É idempotente — pode rodar de novo sem medo. Se `~/bin` não estiver no seu `PATH`, o script avisa como adicionar.

---

## Uso

### 1. Mapear um projeto
Abra o projeto no Claude Code e rode a skill:

```
cd ~/seu-projeto && claude
> /mapear-projeto
```

Ela explora o codebase em paralelo, **verifica cada afirmação contra o código atual** e escreve o `MAPA-PROJETO.md` na raiz. Como confere tudo, costuma achar defeito real no caminho (README desatualizado, config errada, segredo vazado) — **documentar vira auditoria de brinde**.

Depois, adicione um ponteiro no topo do seu `CLAUDE.md`:

```markdown
> **Como o projeto funciona:** ver `MAPA-PROJETO.md` na raiz (ler ao começar).
> **Histórico de sessões:** ver `HISTORICO-SESSOES.md` na raiz.
```

### 2. Registrar uma sessão
Ao terminar de trabalhar:

```bash
zx-worklog.py add --dir . \
  --title "o que você fez" \
  --body $'**Feito:** ...\n**Arquivos:** ...\n**Pendências:** ...' \
  --summary "1 linha pro índice"
```

Isso faz prepend no `HISTORICO-SESSOES.md` do projeto **e** upsert num índice central. Funciona **com ou sem git**.

### 3. Ver o índice central
```bash
zx-worklog.py list           # todos os projetos com histórico
zx-worklog.py show --dir .   # histórico de um projeto
```

O índice mora em `~/.context-worklogs` (configurável via `$ZX_WORKLOG_DIR`).

---

## Por que muda o jogo

- **Zero re-exploração** — o assistente lê o mapa em vez de reconstruí-lo. Menos tokens, menos tempo.
- **Continuidade real** — retome qualquer projeto (você, um colega, ou outra IA) sem perder o fio.
- **Escala pra N projetos** — quem toca muitos projetos ao mesmo tempo não perde o contexto de nenhum.

---

## Estrutura do repo

```
README.md                          → o que é, por que, install, uso
install.sh                         → instalador idempotente
skills/mapear-projeto/SKILL.md     → a skill que gera o MAPA-PROJETO.md
bin/zx-worklog.py                  → histórico de sessão por projeto (git-agnóstico)
templates/                         → modelos de MAPA-PROJETO e HISTORICO-SESSOES
docs/padrao-zx-context.md          → o padrão explicado em detalhe
```

Detalhe conceitual completo: [`docs/padrao-zx-context.md`](docs/padrao-zx-context.md).

---

_Feito pela ZX LAB · material da MasterClass "Engenharia de Contexto no Claude Code"._

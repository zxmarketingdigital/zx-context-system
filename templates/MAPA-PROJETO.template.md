# Mapa do Projeto — <NOME DO PROJETO>

> **Como o projeto funciona por dentro.** Doc vivo: leio ao começar a trabalhar aqui em vez de re-explorar.
> Código muda — este mapa é ponto de partida rápido. **Verificar contra o código atual antes de afirmar como fato.**
> Complementa: `CLAUDE.md` (regras) · `HISTORICO-SESSOES.md` (o que mudou a cada sessão).
> Seed: <AAAA-MM-DD>. Expandir conforme aprendo mais áreas.

## Visão geral
<Uma frase: o que é o projeto, pra quem, onde roda em produção.>

## Stack
- **Frontend:** <framework, build, libs de UI>
- **Backend:** <runtime, banco, funções>
- **Auth:** <como autentica, roles>
- **Deploy:** <como sobe pra produção>

## Entrypoints / páginas-chave (rota/arquivo → o que faz)
| Rota / entrypoint | Arquivo | O que é |
|---|---|---|
| `<rota>` | `src/...` | <o que faz> |

## Modelo de dados (tabelas/schema → papel)
| Tabela / coleção | Papel | Observação |
|---|---|---|
| `<tabela>` | <pra que serve> | <RLS, índice, gotcha> |

## Fluxos principais (ponta-a-ponta)
- **<Fluxo 1>:** <gatilho> → <passo> → <passo> → <efeito final>.
- **<Fluxo 2>:** ...

## Integrações externas
- <serviço> — <pra que> (segredo em `<onde vive>`, NÃO copiar valor).

## Gotchas / armadilhas conhecidas
- <coisa que quebra de forma não-óbvia e como evitar>.

## Comandos (dev / build / deploy)
```bash
<comando de dev>
<comando de build>
<comando de deploy>
```

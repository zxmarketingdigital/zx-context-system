#!/usr/bin/env python3
"""
zx-worklog — histórico de sessão por projeto (funciona com ou sem git).

Grava uma entrada em <projeto>/HISTORICO-SESSOES.md (cria se não existir, mais
recente no topo) e faz upsert num índice central que lista TODO projeto com
histórico — resolvendo o caso de projetos espalhados por várias pastas e sem git.

O índice central fica em $ZX_WORKLOG_DIR (default: ~/.context-worklogs).

Uso:
  zx-worklog.py add --dir <path> --title "..." --body "texto multi-linha" \
                    [--date YYYY-MM-DD] [--summary "1 linha p/ o índice"]
  zx-worklog.py list                      # mostra o índice
  zx-worklog.py show --dir <path>         # mostra o histórico de um projeto

O --body aceita markdown. Convenção sugerida de corpo:
  **Feito:** ...
  **Arquivos:** ...
  **Deploy:** ...
  **Pendências:** ...
"""
import argparse
import datetime
import os
import re
import sys

HOME = os.path.expanduser("~")
STORE = os.environ.get("ZX_WORKLOG_DIR") or os.path.join(HOME, ".context-worklogs")
INDEX = os.path.join(STORE, "INDEX.md")

INDEX_HEADER = (
    "# Índice de Históricos de Sessão\n\n"
    "> Auto-mantido por `zx-worklog.py`. NÃO editar à mão.\n"
    "> Cada projeto trabalhado tem um `HISTORICO-SESSOES.md` na própria raiz; aqui é o mapa central.\n\n"
    "| Projeto | Path | Última sessão | Resumo da última |\n"
    "|---------|------|---------------|------------------|\n"
)


def today():
    return datetime.date.today().isoformat()


def short_path(path):
    ap = os.path.abspath(path)
    if ap.startswith(HOME):
        return "~" + ap[len(HOME):]
    return ap


def project_name(path):
    return os.path.basename(os.path.abspath(path.rstrip("/"))) or "raiz"


def cmd_add(args):
    proj_dir = os.path.abspath(os.path.expanduser(args.dir))
    if not os.path.isdir(proj_dir):
        sys.exit(f"✗ diretório não existe: {proj_dir}")
    date = args.date or today()
    title = args.title.strip()
    body = (args.body or "").strip()
    summary = (args.summary or title).strip().replace("\n", " ")

    # --- 1. HISTORICO-SESSOES.md do projeto (prepend) ---
    hist = os.path.join(proj_dir, "HISTORICO-SESSOES.md")
    entry = f"## {date} — {title}\n\n{body}\n\n"
    file_header = (
        f"# Histórico de Sessões — {project_name(proj_dir)}\n\n"
        "> Registro do que foi feito a cada sessão de trabalho neste projeto (mais recente no topo).\n"
        "> Mantido por `zx-worklog.py`. Ler no início pra recuperar contexto.\n\n"
        "---\n\n"
    )
    if os.path.exists(hist):
        with open(hist, encoding="utf-8") as f:
            existing = f.read()
        # separa header do corpo (primeira ocorrência de '---\n\n')
        marker = "---\n\n"
        idx = existing.find(marker)
        if idx != -1:
            head = existing[: idx + len(marker)]
            rest = existing[idx + len(marker):]
        else:
            head = file_header
            rest = existing
        new_content = head + entry + rest
    else:
        new_content = file_header + entry
    with open(hist, "w", encoding="utf-8") as f:
        f.write(new_content)

    # --- 2. Índice central (upsert por path) ---
    os.makedirs(STORE, exist_ok=True)
    rows = {}
    order = []
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", line)
                if m and m.group(2) not in ("Path", "------"):
                    rows[m.group(2)] = (m.group(1), m.group(2), m.group(3), m.group(4))
                    order.append(m.group(2))
    sp = short_path(proj_dir)
    if sp not in rows:
        order.append(sp)
    rows[sp] = (project_name(proj_dir), sp, date, summary)
    # ordena por última sessão desc
    order_sorted = sorted(set(order), key=lambda p: rows[p][2], reverse=True)
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(INDEX_HEADER)
        for p in order_sorted:
            name, pth, dt, summ = rows[p]
            f.write(f"| {name} | {pth} | {dt} | {summ} |\n")

    print(f"✓ histórico gravado: {short_path(hist)}")
    print(f"✓ índice atualizado: {short_path(INDEX)} ({len(rows)} projeto(s))")


def cmd_list(args):
    if not os.path.exists(INDEX):
        print("(índice vazio — nenhum histórico registrado ainda)")
        return
    with open(INDEX, encoding="utf-8") as f:
        print(f.read())


def cmd_show(args):
    hist = os.path.join(os.path.abspath(os.path.expanduser(args.dir)), "HISTORICO-SESSOES.md")
    if not os.path.exists(hist):
        print(f"(sem histórico em {short_path(hist)})")
        return
    with open(hist, encoding="utf-8") as f:
        print(f.read())


def main():
    ap = argparse.ArgumentParser(description="Histórico de sessão por projeto (git ou não).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="adiciona entrada ao histórico de um projeto")
    a.add_argument("--dir", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--body", default="")
    a.add_argument("--date", default="")
    a.add_argument("--summary", default="")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="mostra o índice central")
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="mostra o histórico de um projeto")
    s.add_argument("--dir", required=True)
    s.set_defaults(func=cmd_show)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

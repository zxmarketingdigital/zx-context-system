#!/usr/bin/env bash
#
# install.sh — instala o sistema de contexto persistente no seu ambiente.
#
# Copia:
#   skills/mapear-projeto  ->  ~/.claude/skills/mapear-projeto  (+ templates dentro)
#   bin/zx-worklog.py      ->  ~/bin/zx-worklog.py              (executável)
#
# Idempotente: pode rodar quantas vezes quiser. Respeita $HOME (dá pra testar
# apontando HOME pra uma pasta limpa).
#
set -euo pipefail

# Diretório onde este script (e o repo) está, mesmo se chamado de outro lugar.
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SKILLS_DIR="$HOME/.claude/skills"
BIN_DIR="$HOME/bin"

echo "▸ Instalando sistema de contexto persistente"
echo "  origem : $SRC"
echo "  destino: $HOME"
echo

# 1. Skill /mapear-projeto (+ templates)
mkdir -p "$SKILLS_DIR/mapear-projeto/templates"
cp "$SRC/skills/mapear-projeto/SKILL.md" "$SKILLS_DIR/mapear-projeto/SKILL.md"
cp "$SRC/templates/"*.template.md "$SKILLS_DIR/mapear-projeto/templates/"
echo "✓ skill  -> $SKILLS_DIR/mapear-projeto/ (SKILL.md + templates/)"

# 2. Script zx-worklog.py
mkdir -p "$BIN_DIR"
cp "$SRC/bin/zx-worklog.py" "$BIN_DIR/zx-worklog.py"
chmod +x "$BIN_DIR/zx-worklog.py"
echo "✓ script -> $BIN_DIR/zx-worklog.py"

echo
echo "✅ Instalado."

# 3. Checagem de PATH (aviso, não erro)
case ":$PATH:" in
  *":$BIN_DIR:"*) : ;;
  *)
    echo
    echo "⚠  $BIN_DIR não está no seu PATH. Adicione ao seu ~/.zshrc ou ~/.bashrc:"
    echo "      export PATH=\"\$HOME/bin:\$PATH\""
    echo "   (ou chame o script pelo caminho completo: $BIN_DIR/zx-worklog.py)"
    ;;
esac

cat <<'EOF'

Próximos passos:
  1. Num projeto qualquer, gere o mapa:
       cd ~/seu-projeto && claude   ->  digite: /mapear-projeto
  2. Ao terminar de trabalhar, registre a sessão:
       zx-worklog.py add --dir . --title "o que fez" --summary "resumo curto"
  3. Veja o índice central de tudo que já tem histórico:
       zx-worklog.py list

O índice central mora em ~/.context-worklogs (configurável via $ZX_WORKLOG_DIR).
EOF

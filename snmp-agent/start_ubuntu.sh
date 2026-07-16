#!/usr/bin/env bash
# Ubuntu 一键启动 NTCIP SNMP Agent
# 用法:
#   ./start_ubuntu.sh                  # 默认 --port 1161 --dev-cap 8
#   ./start_ubuntu.sh --full           # 满填（不加 --dev-cap）
#   ./start_ubuntu.sh --port 161       # 特权端口：自动用 sudo .venv/bin/python
#   ./start_ubuntu.sh --port 1161 --dev-cap 16 --verbose
#   ./start_ubuntu.sh -- --community-ro public-ro

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON="$ROOT/.venv/bin/python"
PORT=1161
DEV_CAP=8
FULL=0
EXTRA=()

usage() {
  cat <<'EOF'
Usage: ./start_ubuntu.sh [options] [-- agent.py args...]

Options:
  --port N       UDP port (default: 1161). Port 161 uses sudo + .venv python.
  --dev-cap N    Table dimension cap (default: 8). Ignored with --full.
  --full         Full OID fill (no --dev-cap).
  -h, --help     Show this help.

Examples:
  ./start_ubuntu.sh
  ./start_ubuntu.sh --port 161
  ./start_ubuntu.sh --full --port 1161
  ./start_ubuntu.sh -- --verbose --community-ro readonly
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --port)
      PORT="${2:?--port requires a value}"
      shift 2
      ;;
    --dev-cap)
      DEV_CAP="${2:?--dev-cap requires a value}"
      shift 2
      ;;
    --full)
      FULL=1
      shift
      ;;
    --)
      shift
      EXTRA+=("$@")
      break
      ;;
    *)
      EXTRA+=("$1")
      shift
      ;;
  esac
done

if [[ ! -x "$PYTHON" ]]; then
  echo "ERROR: venv not found or not executable: $PYTHON" >&2
  echo "Create it first:" >&2
  echo "  python3 -m venv .venv && source .venv/bin/activate" >&2
  echo "  python3 -m pip install -U 'pip>=24' setuptools wheel" >&2
  echo "  python3 -m pip install -r requirements.txt" >&2
  echo "See docs/UBUNTU.md if pip times out (use a mirror)." >&2
  exit 1
fi

ARGS=(agent.py --port "$PORT")
if [[ "$FULL" -eq 0 ]]; then
  ARGS+=(--dev-cap "$DEV_CAP")
fi
ARGS+=("${EXTRA[@]}")

echo "Working directory: $ROOT"
echo "Python: $PYTHON"
echo "Command: ${ARGS[*]}"

# Port < 1024 needs root; never use system python3 under sudo.
if [[ "$PORT" -lt 1024 ]]; then
  echo "Port $PORT is privileged — using: sudo $PYTHON"
  exec sudo "$PYTHON" "${ARGS[@]}"
fi

exec "$PYTHON" "${ARGS[@]}"

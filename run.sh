#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

PYTHON_BIN="/home/vik/miniconda3/envs/webshop/bin/python"

echo "================================================="
echo "   Starting Amazon E-Commerce Flow Clone        "
echo "   URL: http://localhost:4000                   "
echo "================================================="

exec "$PYTHON_BIN" app.py

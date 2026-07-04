#!/bin/bash
set -e

# ========================================
# build-prod.sh - Build NumGame Frontend
# ========================================
# This script installs dependencies and builds dist/.
#
# Usage:
#   bash build-prod.sh          # npm install + npm run build
#   bash build-prod.sh --ci     # npm ci --include=dev + npm run build
#
# Prerequisites:
#   - Node.js 18+
# ========================================

echo "=========================================="
echo "  NumGame Frontend - Production Build"
echo "=========================================="
echo ""

CI_MODE=false
for arg in "$@"; do
  if [ "$arg" = "--ci" ]; then
    CI_MODE=true
  fi
done

# ---- Step 1: Install dependencies ----
echo "[1/2] Installing dependencies..."
if [ "$CI_MODE" = true ]; then
  npm install --include=dev
else
  npm install
fi
echo "  ✓ Dependencies installed"

# ---- Step 2: Build dist/ ----
echo "[2/2] Building frontend (npm run build)..."
npm run build
echo "  ✓ Frontend built → dist/"

echo ""
echo "=========================================="
echo "  Build complete!"
echo "=========================================="
echo ""
echo "Next step:"
echo "  cd /path/to/NumGame && docker compose build numgame-frontend"
echo ""
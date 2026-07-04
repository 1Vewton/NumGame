#!/bin/bash
set -e

# ========================================
# build-prod.sh - Build NumGame Frontend
# ========================================
# This script handles two modes:
#
#   1. Local build (no args):
#      - Installs dependencies
#      - Builds dist/ locally
#      - Builds the production Docker image
#      - Restores .dockerignore
#
#   2. CI/Docker build (with --ci flag):
#      - Installs dependencies (npm ci)
#      - Builds dist/ locally only
#      - No Docker operations
#
# Usage:
#   bash build-prod.sh          # Full local build + Docker image
#   bash build-prod.sh --ci     # CI mode: install + build only
#
# Prerequisites:
#   - Node.js 18+
#   - Docker (for local mode only)

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
echo "[1/3] Installing dependencies..."
if [ "$CI_MODE" = true ]; then
  npm install --include=dev
else
  npm install
fi
echo "  ✓ Dependencies installed"

# ---- Step 2: Build dist/ ----
echo "[2/3] Building frontend (npm run build)..."
npm run build
echo "  ✓ Frontend built → dist/"

# ---- Step 3: Build Docker image (local mode only) ----
if [ "$CI_MODE" = false ]; then
  echo "[3/3] Building Docker image..."

  # Temporarily remove /dist from .dockerignore so COPY dist works
  sed -i '/^\/dist$/d' .dockerignore

  docker build \
    -f Dockerfile.prod \
    -t numgame-frontend:prod \
    .

  echo "  ✓ Docker image built: numgame-frontend:prod"

  # Cleanup: Restore .dockerignore
  mv .dockerignore.bak .dockerignore
  echo "  ✓ .dockerignore restored"
else
  echo "[3/3] Build stage complete — dist/ ready"
fi

echo ""
echo "=========================================="
echo "  Build complete!"
echo "=========================================="
echo ""
if [ "$CI_MODE" = false ]; then
  echo "Next step:"
  echo "  cd /path/to/NumGame && docker compose up -d"
fi
echo ""
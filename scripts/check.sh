#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose version
docker compose config --quiet
docker compose ps
printf 'Configuracion validada. Ejecutar pruebas de docs/ACEPTACION.md.\n'

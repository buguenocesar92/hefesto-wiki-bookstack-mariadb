#!/usr/bin/env python3
"""Verificacion de integridad de un respaldo de hefesto-wiki.

Codigos de salida: 0 integro, 1 uso, 2 integridad o manifiesto invalido,
4 material sensible en claro dentro del respaldo.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import ejecutar, ejecutar_check

SOFTWARE = "hefesto-wiki"
VERSION = "26.09.1"
DATABASE = "mariadb"
# El volumen de configuracion lleva el APP_KEY: nunca puede ir en claro.
PROHIBIDOS = ["config.tar.gz"]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 scripts/check_backup.py /ruta/respaldo")
    ejecutar_check(sys.argv[1], SOFTWARE, VERSION, DATABASE, prohibidos=PROHIBIDOS)
    print("Manifiesto, checksums y ausencia de secretos en claro verificados.")
    print("No demuestra la recuperacion de MariaDB ni del APP_KEY: hace falta la clave age.")
    return 0


if __name__ == "__main__":
    raise SystemExit(ejecutar(main))

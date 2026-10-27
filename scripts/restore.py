#!/usr/bin/env python3
"""Restauracion de hefesto-wiki en un destino nuevo y vacio.

Sin --confirmar CONFIRMAR_RESTAURACION no se escribe nada; con --dry-run se
simula. El volumen de configuracion, cifrado con age, se restaura solo si el
operador entrega su clave privada (AGE_IDENTITY_FILE): es un insumo externo.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import (RespaldoError, auditar, descifrar_con_age, ejecutar,
                               ejecutar_check, escribir_informe, opciones_restore)

SOFTWARE = "hefesto-wiki"
VERSION = "26.09.1"
DATABASE = "mariadb"
RAIZ = Path(__file__).resolve().parents[1]
os.chdir(RAIZ)
os.umask(0o077)
PROHIBIDOS = ["config.tar.gz"]


def dc(*args, **kw):
    return subprocess.run(["docker", "compose", *args], check=True, **kw)


def main():
    modo, origen = opciones_restore(sys.argv[1:])
    origen = Path(origen).resolve()
    ejecutar_check(str(origen), SOFTWARE, VERSION, DATABASE, prohibidos=PROHIBIDOS)
    if modo == "dry-run":
        print("Simulacion: el respaldo es integro y no se escribio nada.")
        print("Para restaurar de verdad: --confirmar CONFIRMAR_RESTAURACION")
        return 0
    if dc("ps", "--status", "running", "-q", "wiki", capture_output=True, text=True).stdout.strip():
        raise RespaldoError("wiki esta activa en el destino; detenerla antes de restaurar", 5)
    if not (RAIZ / ".env").is_file():
        raise RespaldoError("Preparar el .env del destino con scripts/configure.py "
                            "(no viaja en el respaldo)", 5)
    ocupado = dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "find", "wiki", "/config",
                 "-mindepth", "1", "-maxdepth", "1", capture_output=True, text=True).stdout.strip()
    if ocupado:
        raise RespaldoError("El volumen de configuracion del destino no esta vacio; "
                            "usar destino nuevo", 5)
    with (origen / "database.sql").open("rb") as f:
        dc("exec", "-T", "db", "sh", "-c",
           'MYSQL_PWD="$MARIADB_PASSWORD" mariadb -u "$MARIADB_USER" "$MARIADB_DATABASE"',
           stdin=f)
    if (origen / "config.tar.gz.age").is_file():
        with tempfile.TemporaryDirectory(prefix="hefesto-wiki-restore-") as d:
            plano = Path(d) / "config.tar.gz"
            descifrar_con_age(origen / "config.tar.gz.age", plano)
            with plano.open("rb") as f:
                dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar", "wiki",
                   "-xzf", "-", "-C", "/config", stdin=f)
    else:
        print("El respaldo no trae la configuracion cifrada: hay que regenerar el APP_KEY "
              "del destino con scripts/configure.py (ver docs).")
    escribir_informe(origen, software=SOFTWARE, version=VERSION, database=DATABASE,
                     modo="confirmado", resultado="restaurado", destino=str(RAIZ))
    auditar(RAIZ, operacion="restore", kit=SOFTWARE, origen=str(origen), destino=str(RAIZ),
            resultado="restaurado")
    print("Datos restaurados. Probar el wiki por entorno privado antes de publicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(ejecutar(main))

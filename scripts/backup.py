#!/usr/bin/env python3
"""Respaldo de hefesto-wiki (BookStack + MariaDB).

Reglas de material sensible:
- El .env nunca se copia en claro: solo env.vars y, si hay receptor age, el
  .env cifrado (env.age).
- El volumen de configuracion contiene el .env interno de BookStack con el
  APP_KEY y la contrasena de la base: se cifra en linea con age
  (config.tar.gz.age) o no viaja y el manifiesto lo declara.
Ver docs/CONTRATO-RESPALDO.md.
"""
import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import (RespaldoError, cifrar_con_age, escribir_manifiesto,
                               ejecutar, exportar_env, marcar_fallido, receptor_age)

SOFTWARE = "hefesto-wiki"
VERSION = "26.09.1"
DATABASE = "mariadb"
RAIZ = Path(__file__).resolve().parents[1]
os.chdir(RAIZ)
os.umask(0o077)


def dc(*args, **kw):
    return subprocess.run(["docker", "compose", *args], check=True, **kw)


def main():
    if not (RAIZ / ".env").is_file():
        raise SystemExit("Falta .env")
    if not dc("ps", "--status", "running", "-q", "wiki", capture_output=True, text=True).stdout.strip():
        raise SystemExit("wiki no esta activa en este contexto Compose; revisar recurso/proyecto.")
    carpeta = RAIZ / "backups" / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    carpeta.mkdir(parents=True, mode=0o700)
    try:
        dc("stop", "wiki")
        with (carpeta / "database.sql").open("wb") as out:
            dc("exec", "-T", "db", "sh", "-c",
               'MYSQL_PWD="$MARIADB_PASSWORD" mariadb-dump -u "$MARIADB_USER" '
               '--single-transaction --skip-lock-tables --no-tablespaces "$MARIADB_DATABASE"',
               stdout=out)
        meta = exportar_env(RAIZ, carpeta)
        if meta.get("env_cifrado"):
            receptor = receptor_age()
            cifrar_con_age(
                lambda flujo: dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar", "wiki",
                                 "-czf", "-", "-C", "/config", ".", stdout=flujo),
                carpeta / "config.tar.gz.age", receptor)
            meta["config"] = "config.tar.gz.age (cifrado con age)"
        else:
            meta["config"] = ("excluido: el volumen de configuracion contiene el APP_KEY y no "
                              "hay receptor age configurado")
        if (RAIZ / "compose.yaml").is_file():
            shutil.copy2(RAIZ / "compose.yaml", carpeta / "compose.yaml")
        artefactos = [n for n in ("database.sql", "env.vars", "compose.yaml")
                      if (carpeta / n).is_file()]
        for n in ("env.age", "config.tar.gz.age"):
            if (carpeta / n).is_file():
                artefactos.append(n)
        escribir_manifiesto(carpeta, SOFTWARE, VERSION, DATABASE, artefactos, extra=meta)
    except Exception:
        marcar_fallido(carpeta, SOFTWARE, VERSION, DATABASE)
        raise
    finally:
        dc("start", "wiki")
    print("Respaldo completo:", carpeta)
    print("El .env y el volumen de configuracion no viajan en claro: solo cifrados con age "
          "o fuera del respaldo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(ejecutar(main))

# Política de tratamiento de datos personales — Wiki (Hefesto Studio)

Estado: vigente desde 2026-10-20. Responsable del tratamiento: el cliente que
opera el kit. Este documento describe qué datos guarda el kit, por qué, cuánto
tiempo los retiene y cómo se exercise los derechos del titular (Ley 21.719).

## 1. Qué datos guarda este kit

El kit de wiki (BookStack) guarda, por persona usuaria y por pagina:

- **Cuentas**: nombre, correo, hash de contrasena, rol y preferencias.
- **Paginas y revisiones**: contenido, autor, historial de revisiones, fecha de
  creacion y de modificacion.
- **Comentarios**: texto, autor y fecha.
- **Adjuntos**: imagenes y archivos adjuntos a las paginas, con su nombre y
  fecha de subida.
- **Actividad**: registro de accesos y acciones (inicios de sesion, cambios de
  contrasena, eliminaciones) con direccion IP.
- **Claves del servicio**: el `APP_KEY` y la contrasena de la base de datos, que
  viven en el `.env` interno de BookStack dentro del volumen `config`.
- **Copias locales de respaldo**: `backups/<timestamp>/` con el dump de MariaDB
  (`database.sql`) y la configuracion cifrada (`config.tar.gz.age`).

Un wiki interno documenta la operacion de una organizacion: sus paginas
suelen contener datos de clientes, proveedores o empleados.

## 2. Qué datos NO guarda este kit

- El `.env` **no** se copia en claro al respaldo: solo sus nombres de
  variable (`env.vars`) y, si hay un receptor `age` configurado, el `.env`
  cifrado (`env.age`).
- El volumen de configuracion, con el `APP_KEY` y la contrasena de la base,
  **tampoco** viaja en claro: se cifra con `age` (`config.tar.gz.age`) o no se
  incluye y el manifiesto lo declara. Ver `docs/CONTRATO-RESPALDO.md`, regla 5.
- El kit no envia paginas ni cuentas a servicios de terceros.

## 3. Base legal y deberes

- **Minimización**: el kit guarda lo necesario para servir el wiki: cuentas, paginas, revisiones
  y actividad. No agrega metadatos de seguimiento ni perfila a los lectores.
- **Finalidad**: documentar y compartir el conocimiento interno del cliente. Los datos no se usan para otros fines ni se ceden a terceros.
- **Seguridad**: los respaldos se cifran en reposo con `age` hacia el destino del operador, la clave privada no está en este servidor, el `.env` y el `APP_KEY` nunca salen en claro y la base exige TLS local con credenciales de MariaDB.
- **Auditoría**: cada respaldo y cada restauración dejan registro en `logs/restore.log` con origen, sha256 verificado, destino y resultado. Es registro de actividades de tratamiento: no guarda valores de secretos.

## 4. Retención

| Dato | Dónde | Retención por defecto | Quién lo borra |
|---|---|---|---|
| Paginas, revisiones y comentarios | MariaDB (volumen `database`) | mientras el cliente los mantenga | el operador, desde la interfaz |
| Cuentas y actividad (con IP) | MariaDB (volumen `database`) | mientras la cuenta exista | el operador |
| Adjuntos | volumen `config` | mientras el cliente los mantenga | el operador |
| `APP_KEY` y clave de la base | volumen `config`, cifrado en el respaldo | mientras el kit este en uso; rotar si se sospecha uso indebido | el operador |
| Respaldos en disco | `backups/<timestamp>/` | **a definir por el operador**; el kit no borra nada por su cuenta | el operador |
| Registro de auditoría | `logs/restore.log` | append-only; se trunca por política del cliente | el operador |

**El kit no borra respaldos ni datos por su cuenta.** Borrar es una decisión del
operador, porque un respaldo borrado no se recupera.

## 5. Derechos del titular (acceso, rectificación y supresión)

El cliente que opera el kit debe poder atender las solicitudes de sus
titulares:

1. **Acceso**: entregar el contenido de una pagina o el registro de actividad
   de una cuenta al titular que lo solicite.
2. **Rectificación**: corregir el contenido de una pagina desde la interfaz.
3. **Supresión**: eliminar una cuenta, su actividad y los respaldos que las
   contengan, y dejar constancia en el registro de auditoria.
4. **Revocación del consentimiento**: si el tratamiento depende del
   consentimiento, eliminar la cuenta y su registro de actividad.

El kit garantiza que los datos son localizables, corregibles y borrables; el
cliente es quien conoce la identidad de los titulares.

## 6. Verificación

- `bats tests/backup_restore.bats` comprueba, con datos sintéticos, que el
  `.env` ni el volumen de configuracion quedan en claro, que el manifiesto lleva
  las cinco claves, que un artefacto alterado se rechaza y que un destino no
  vacío aborta la restauración.
- `gitleaks` corre en CI sobre el repositorio y su historial.

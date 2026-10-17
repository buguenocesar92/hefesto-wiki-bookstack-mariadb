# Respaldo y recuperación
## Crear
`python3 scripts/backup.py` en el directorio/contexto Compose real. Detiene wiki, mantiene MariaDB para el dump y comprime todo /config. Finalmente intenta reiniciar wiki. Incluye .env, compose.yaml y manifest con checksums. Verificar salida y servicio activo. Hay una pausa de acceso durante el respaldo.

Usar Python3.11+. En Coolify, ejecutar en el recurso correcto y sus variables: un directorio separado con otros nombres puede apuntar a otra instancia. No editar /config ni permitir escrituras externas mientras se respalda.

Los respaldos contienen APP_KEY, credenciales, documentos y datos personales. Cifrarlos, copiarlos fuera del VPS y acordar retención. El script no hace cifrado, subida externa, programación ni rotación automática. Nunca enviar el ZIP de datos por un canal público.

## Restaurar
Usar la misma imagen y versión en un proyecto aislado con volúmenes VACÍOS. El archivo manifest.json debe indicar completed; comparar SHA-256 de cada archivo antes de restaurar. No iniciar wiki antes de cargar base y archivos: su arranque ejecuta migraciones automáticamente.
1. Extraer este paquete. Recuperar .env original con modo0600; conservar APP_KEY y contraseñas. Para pruebas, cambiar nombres de proyecto y ambos volúmenes para no tocar origen.
2. `docker compose up -d db`; esperar estado healthy.
3. Comprobar que la base bookstack destino está vacía. Si ya contiene tablas, detenerse y preparar otra base; no sobrescribir datos.
4. Importar: `docker compose exec -T db sh -c 'MYSQL_PWD="$MARIADB_PASSWORD" mariadb -u "$MARIADB_USER" "$MARIADB_DATABASE"' < /ruta/respaldo/database.sql`
5. Restaurar /config: `docker compose run --rm --no-deps -T --entrypoint tar wiki -xzf - -C /config < /ruta/respaldo/config.tar.gz`
6. Revisar entorno antes de iniciar: puede contener SMTP/webhooks de producción dentro de /config. En pruebas, aislar la salida externa y mantener SMTP sin activar.
7. Iniciar con bootstrap privado, comprobar usuarios, permisos, historial, imágenes y adjuntos. Si cambió la URL, ejecutar bookstack:update-url según docs/COOLIFY.md.
8. Publicar solo tras verificar y retirar datos de prueba. Nunca arrancar dos contenedores sobre el mismo /config o datadir MariaDB.

Los comandos de restauración son para copias propias confiables en destinos nuevos. No incluir extracción de archivos desconocidos ni borrar volúmenes existentes para forzar el proceso.

## Actualizaciones
Leer notas oficiales y respaldar antes de cambiar imagen. Probar nueva versión con copia aislada. LinuxServer ejecuta migraciones al arrancar; volver a una imagen anterior puede requerir restaurar también la base. Conservar un respaldo compatible y documentar la ventana de mantenimiento.

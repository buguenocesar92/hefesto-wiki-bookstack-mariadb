# Publicación y configuración
## Antes de publicar
Crear DNS wiki.cliente.cl, tener HTTPS y realizar bootstrap privado del README. Cambiar la cuenta inicial, probar reingreso y guardar recuperación MFA en un gestor seguro. No agregar documentación real hasta validar permisos.

La APP_KEY generada contiene32bytes aleatorios en base64, compatible con la clave de Laravel. Conservarla durante respaldos y migraciones: no regenerarla al cambiar de VPS.

## Pasar de bootstrap a Coolify
1. Detener con `docker compose -f compose.yaml -f compose.bootstrap.yaml down` SIN `-v`.
2. Subir los archivos versionables a un repositorio privado, excluyendo .env y backups.
3. Crear recurso Docker Compose con compose.yaml. Copiar las variables de .env al editor seguro de Coolify, incluidas APP_KEY, DB_PASSWORD y DB_ROOT_PASSWORD originales.
4. Verificar que DB_VOLUME y CONFIG_VOLUME se mantengan exactamente: contienen el administrador preparado y sus archivos. No usar volúmenes vacíos.
5. Asignar https://wiki.cliente.cl al servicio wiki, puerto80. No exponer db. Desplegar.
6. Si se crearon páginas o imágenes durante bootstrap, actualizar URLs mediante el comando nativo, desde el contexto de ese recurso:
   `docker compose exec wiki php /app/www/artisan bookstack:update-url http://127.0.0.1:6875 https://wiki.cliente.cl`
7. Verificar que la cuenta inicial con su contraseña conocida ya no funciona, que la cuenta propia sí funciona y que el modo público sigue desactivado.

El healthcheck confirma respuesta HTTP del login, no configura cuentas ni verifica permisos. El estado healthy no sustituye el paso privado.

## Proxy y sesiones
APP_URL debe coincidir exactamente con la URL externa. SESSION_SECURE_COOKIE=true en producción. Si hace falta confiar cabeceras del proxy, establecer APP_PROXIES a su IP/CIDR conocido, conforme a la documentación de BookStack. No usar comodín indiscriminado si el contenedor es accesible por redes no confiables. No desactivar TLS para resolver errores de redirección.

## Archivos
/config conserva configuración, imágenes, adjuntos, temas y registros. La base guarda contenido, cuentas y permisos. FILE_UPLOAD_SIZE_LIMIT=20MB en aplicación; comprobar límites efectivos de Nginx, PHP y proxy con un archivo de prueba. No asumir que basta modificar solo uno.

## Correo
Inicialmente SMTP apunta a127.0.0.1:2525 sin servidor: no entrega correos y acciones que requieren envío pueden fallar. Antes de habilitar invitaciones/restablecimiento, configurar variables SMTP_HOST/PORT/USERNAME/PASSWORD/ENCRYPTION y MAIL_FROM, redesplegar y usar la prueba de correo nativa a una dirección autorizada. No se envió ningún correo al preparar este ZIP.

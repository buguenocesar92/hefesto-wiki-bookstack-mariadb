# Hefesto Wiki · BookStack 26.09.1
Base de conocimiento para vender implementación y soporte de manuales internos, procedimientos, documentación de sistemas y entrega de proyectos a clientes.

## Stack
BookStack nativo, imagen comunitaria mantenida por LinuxServer.io (referenciada por la documentación de BookStack), MariaDB11.4 y proxy HTTPS de Coolify. La imagen BookStack está fijada por versión y digest. MariaDB queda en rama11.4: registrar su digest al desplegar.

No requiere Supabase: se usa el motor MySQL/MariaDB esperado por la aplicación. No hay sincronización con Odoo ni autenticación Supabase configurada. Un despliegue aislado por cliente facilita entrega y separación de información.

## Qué contiene
- Compose con base privada, persistencia de /config y bootstrap por túnel SSH.
- Generador de APP_KEY y contraseñas aleatorias, sin sobrescribir .env.
- Respaldo coordinado de base y archivos; guía de recuperación.
- Guías de permisos, configuración, publicación, operación y transferencia.
- Plantillas Markdown de manuales, procedimientos, arquitectura, incorporación e incidentes.

No incluye binarios del producto: Docker descarga la imagen. Las plantillas se incorporan manualmente al editor; no se presentan como datos ya cargados en una instancia.

## Inicio
Requiere Docker Compose v2, Python3.11+ para scripts y un VPS con DNS/HTTPS.
1. `python3 scripts/configure.py cliente-demo wiki.tudominio.cl`
2. En el VPS: `docker compose -f compose.yaml -f compose.bootstrap.yaml up -d`
3. Desde tu computador: `ssh -L 6875:127.0.0.1:6875 usuario@IP_DEL_VPS`
4. Abrir http://127.0.0.1:6875. Entrar con la cuenta inicial nativa admin@admin.com / password. CAMBIAR inmediatamente correo y contraseña; configurar MFA antes de publicar.
5. Revisar que acceso público y registro abierto estén deshabilitados. Seguir docs/COOLIFY.md para transferir al recurso HTTPS conservando volúmenes.
6. Configurar estructura/permisos, cargar plantillas y completar acta de aceptación.

El primer acceso permanece privado porque BookStack instala una cuenta conocida. No asignar dominio público antes de reemplazarla. Nunca ejecutar dos instancias sobre los mismos volúmenes.

## Alcance real
Archivos revisados estáticamente. No se ha ejecutado Docker, desplegado un servidor, creado usuarios ni probado permisos/adjuntos/PDF en este entorno. SMTP está sin configurar y los correos fallarán hasta activarlo. El paquete no añade OCR, firma electrónica, RAG, aprobación documental formal ni cumplimiento normativo automático.

## Recursos y licencia
Inicio orientativo:2vCPU,2GB RAM,20GB SSD local más documentos y respaldos; medir según uso. BookStack mantiene licencia MIT y atribuciones originales. Hefesto comercializa implementación, alojamiento y soporte; este paquete no sustituye las licencias upstream.

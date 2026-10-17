# Transferencia y servicio comercial
## Qué vender
Configuración de wiki, organización de documentación, adaptación de manuales, formación del equipo, alojamiento y mantenimiento. Cobrar por ese trabajo, no atribuirse autoría exclusiva de BookStack.

| Servicio | Entregable a acordar |
|---|---|
| Puesta en marcha | Instancia, roles, estructura y sesión de capacitación |
| Documentación inicial | Manuales/procedimientos revisados con responsables |
| Operación mensual | Actualización, respaldo, recuperación de prueba y soporte |
| Entrega de proyecto | Manual de usuario, guía de operación y documentación técnica |

Definir número de manuales, revisiones, usuarios de formación y horas de soporte antes de cotizar. No incluir automáticamente escritura ilimitada de contenido o atención24/7.

## Entrega técnica
Repo/ZIP, dominio/DNS, acceso VPS/Coolify, imagen/digest, APP_KEY, claves DB, administrador actual, recuperación MFA, configuración SMTP, respaldo restaurado en pruebas, inventario de libros y matriz de permisos. Transferir secretos mediante un gestor seguro separado del repositorio.

Registrar quién mantiene contenido y quién mantiene infraestructura. Rotar accesos del operador saliente según acuerdo; cambiar contraseñas DB exige actualizar usuario de MariaDB y variables, no solo editar .env.

## Migración a otra plataforma
Exportar contenido con las herramientas nativas y probar formato/destino. Una exportación HTML/PDF/Markdown no preserva necesariamente usuarios, permisos, historial, enlaces y adjuntos completos. El respaldo SQL y /config permite restaurar BookStack; no es un importador universal de Odoo/Notion/Moodle.

## Integraciones posibles
BookStack expone API y opciones SSO según configuración nativa. Conectar Keycloak, n8n o RAG requeriría credenciales, mapeos y pruebas adicionales. No se incluyen tokens ni conectores simulados.

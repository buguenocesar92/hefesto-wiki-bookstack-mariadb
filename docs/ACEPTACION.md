# Acta de aceptación pendiente
Registrar cliente, dominio, fecha, responsable, versión y digest.
- [ ] Compose valida; DB healthy; wiki responde sin errores de migración.
- [ ] Bootstrap restringido a túnel; cuenta inicial reemplazada y clave conocida rechazada.
- [ ] MFA configurado, recuperación guardada y reingreso probado.
- [ ] HTTPS, URL canónica y cookies funcionan.
- [ ] Registro abierto y acceso público desactivados según alcance.
- [ ] Crear libro, capítulo, página, imagen y adjunto de prueba.
- [ ] Lector puede leer, editor puede editar, usuario sin permiso no puede acceder.
- [ ] Probar acceso directo a imágenes y adjuntos desde usuario no autorizado y sesión anónima.
- [ ] Buscar y exportar contenido; revisar que exportación no revele información restringida.
- [ ] Reinicio conserva contenido e historial.
- [ ] SMTP probado solo si se configuró; recuperación de cuenta documentada.
- [ ] Respaldo y restauración completos probados en entorno aislado.
- [ ] Recursos, retención, responsables y entrega de secretos acordados.

Verificaciones de empaquetado: YAML, sintaxis de scripts, formato APP_KEY, protección contra sobrescritura de .env y ZIP. Pruebas de Docker, permisos y restauración todavía pendientes en el servidor destino.

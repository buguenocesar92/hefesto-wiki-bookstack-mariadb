# Organización y acceso
## Estructura sugerida
| Estantería | Libro | Capítulos iniciales |
|---|---|---|
| Operaciones | Procedimientos internos | Responsables, atención, continuidad |
| Sistemas | Manual del sistema | Acceso, tareas habituales, errores |
| Proyectos | Entrega de proyecto | Alcance, arquitectura, operación |
| Formación | Incorporación del equipo | Primer día, herramientas, prácticas |

Las estanterías agrupan libros; permisos y herencia deben probarse en cada nivel. Las plantillas Markdown del directorio templates pueden pegarse en páginas usando el editor Markdown nativo. Agregar logo/título/color desde las opciones de personalización. No se ha modificado el código de BookStack.

## Roles propuestos
- Administrador: configuración, usuarios y permisos. Uso excepcional.
- Responsable documental: edición y revisión del contenido de su área.
- Editor: creación/edición del contenido autorizado.
- Lector: lectura y exportación solo si corresponde.

Configurar roles nativos y permisos por contenido con mínimo acceso. Validar con usuarios reales de prueba sin privilegios. No usar administrador para comprobar restricciones. Separar clientes en instancias cuando necesiten administradores independientes; no prometer aislamiento SaaS con una sola cuenta compartida.

## Imágenes y adjuntos
STORAGE_TYPE=local_secure_restricted vincula el acceso a imágenes con permisos del contenido de origen. Los adjuntos se sirven a través de controles de BookStack. Copiar una página a otra con distintos permisos puede dejar imágenes no visibles porque siguen vinculadas al origen; probar y volver a subirlas donde corresponda.

Si ya existen archivos de una instalación con almacenamiento público, cambiar esta variable no los vuelve privados automáticamente: seguir la migración oficial de almacenamiento y eliminar copias públicas después de respaldar y validar. Este paquete está pensado para instalaciones nuevas.

## Gobierno documental
Cada procedimiento debe tener dueño, versión editorial y próxima revisión. Usar historial de páginas como ayuda, sin presentarlo como firma o aprobación formal. Prohibir contraseñas/API keys dentro de manuales; referenciar el gestor de secretos correspondiente. Documentos con datos de clientes requieren criterios de acceso y retención acordados.

El proyecto no implementa clasificación automática, firma electrónica, OCR ni RAG. Se pueden evaluar como integraciones posteriores.

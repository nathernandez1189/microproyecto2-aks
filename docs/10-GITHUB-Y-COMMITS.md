# Entrega en GitHub y organización de commits

Repositorio: **nathernandez1189/microproyecto2-aks**, acceso privado. Rama principal: `main`.

## Qué representa el historial

El trabajo ya existía antes de inicializar este repositorio. La entrega lo registra en commits temáticos creados con la fecha real de publicación. No se simula un calendario de desarrollo ni se atribuyen aportes personales sin evidencia. Los tres integrantes constan en [EQUIPO.md](EQUIPO.md); la cuenta que publica es la de Natalia.

## Orden de los commits

| Bloque | Contenido y razón |
|---|---|
| Base del proyecto | README, integrantes, configuración de ejemplo y exclusiones para conservar datos privados |
| Visión AI | Clasificador, modelo preentrenado, validación de imágenes y observabilidad compartida |
| Campus Planner | CRUD de tareas, SQLite, interfaz y Compose para ejecución local |
| Kubernetes y AKS | Recursos declarativos, publicación AMD64, conexión, despliegue y reactivación |
| Monitoreo de Azure | Configuración de recolección, consultas KQL y exportación de evidencias |
| Extra HPA | Carga CPU local, límites, escalado 1 a 4 y recuperación del Job vencido |
| Pruebas y evidencias | Suite HTTP existente, imagen atribuida y registros revisados del ensayo |
| Documentación y entrega | Guías actualizadas, PDF, resultados, preguntas y exportación segura del ZIP |

Cada mensaje explica los archivos y su propósito. Los commits describen importación y organización del proyecto, no nuevas pruebas en vivo realizadas durante la publicación.

## Consultar y explicar el historial

```bash
git log --oneline --reverse
git log --format=fuller --stat
git show --stat HEAD
git status --short
```

`log` lista cambios; `show` permite revisar uno; `status` identifica archivos modificados. Un commit guarda una versión de código. `push` envía esos commits al repositorio remoto. Ninguno inicia AKS ni publica automáticamente las aplicaciones en Internet.

## Guardar un cambio posterior

Desde una copia del repositorio:

```bash
git status --short
git diff
# Ejemplo: solo si modificaste esta guía.
git add docs/08-REACTIVACION-Y-DEMO.md
git diff --cached
git commit -m "docs: aclarar pasos de la demostración en AKS"
git push origin main
```

Agrupa cambios relacionados y describe el motivo. Evita agregar indiscriminadamente archivos generados o respaldos. Comprueba que las credenciales sigan excluidas con `git check-ignore .env .kube/aks.config`.

## Compartir la entrega

El código y la guía se consultan desde GitHub; los servicios requieren Azure y túneles activos. Un repositorio privado necesita permisos para terceros; compartir solo el enlace no concede acceso. La entrega en la plataforma del curso se confirma por separado.

## Validación de esta publicación

Se revisan sintaxis de Python, scripts de terminal, JavaScript, YAML, enlaces internos, PDF y archivos seleccionados para Git. Las pruebas funcionales de AKS y HPA corresponden al ensayo documentado del 14 de septiembre; la infraestructura permanece detenida durante la publicación.

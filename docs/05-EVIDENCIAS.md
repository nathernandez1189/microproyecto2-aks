# Evidencias y entrega

Una evidencia identifica el entorno, la acción y el resultado. Las ejecuciones de Docker/Minikube y AKS se presentan por separado. El [índice de evidencias](../evidencias/README.md) enlaza la selección publicable; los originales permanecen locales.

| Identificador | Evidencia | Criterio para darla por lista |
|---|---|---|
| A01 | Portal antes y después de crear AKS | Nombre, grupo, región, al menos dos nodos y despliegue correcto |
| A02 | Nodos desde Cloud Shell | Dos o más nodos Ready y origen visible |
| A03 | Nodos desde CLI local | Mismo clúster comprobado desde el computador |
| A04 | Clasificador en AKS | Foto, top cinco, respuesta HTTP y Pod correlacionado |
| A05 | Recursos del clasificador | Dos réplicas disponibles, Service y sondas |
| A06 | Campus Planner en AKS | Crear y cambiar una tarea, con respuesta real de API |
| A07 | Persistencia del tablero | Pod anterior/nuevo, mismo PVC y tarea conservada |
| A08 | Container Insights | CPU/memoria con clúster e intervalo identificables |
| A09 | Logs y KQL | `/predict`, código, duración y request_id |
| A10 | Error controlado | 400 por falta de imagen, Pod aún saludable |
| X01 | HPA local sin carga | Una réplica y métricas disponibles |
| X02 | HPA local con carga | CPU sobre objetivo y aumento de réplicas |
| X03 | HPA local tras detener carga | Regreso a una réplica y eventos del controlador |
| E01 | Entrega | Enlace GitHub y confirmación de entrega en Classroom |

Para cada captura añade una frase de interpretación. Ejemplo de formato, que
debes completar con un valor **observado**: “Durante la inferencia, el Pod ___
registró ___ ms; en ContainerLogV2 se encontró la solicitud ___”.

## GitHub y acceso

Repositorio de esta entrega: [nathernandez1189/microproyecto2-aks](https://github.com/nathernandez1189/microproyecto2-aks).

La publicación se organiza por temas, sin falsificar fechas de trabajo ni atribuciones individuales. El detalle de commits y el flujo de actualización están en [10-GITHUB-Y-COMMITS.md](10-GITHUB-Y-COMMITS.md). Los integrantes están en [EQUIPO.md](EQUIPO.md).

Un repositorio privado requiere acceso autorizado para que el profesor o los compañeros puedan abrirlo. No se añadieron colaboradores solo a partir de los nombres. También puede generarse una copia ZIP del código registrado:

```bash
python3 scripts/package_project.py
```

El archivo queda en `output/Microproyecto2-AKS-Equipo.zip` y contiene un manifiesto SHA-256. `.env`, kubeconfigs, bases y respaldos no se incluyen. No agregues una carpeta completa de evidencias sin revisar su contenido.

## Entrega académica

Adjunta el enlace y/o el ZIP según indique la tarea del curso y comprueba la confirmación de entrega. La publicación en GitHub no envía Classroom ni registra integrantes u horarios en plataformas externas. La evaluación individual incluye explicar conceptos y resolver cambios en vivo; usa la guía 08 y el ensayo 09.

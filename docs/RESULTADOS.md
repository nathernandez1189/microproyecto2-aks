# Resultados comprobados

## Fechas y alcance

Primera ejecución: **9 de septiembre de 2026**. Reactivación, repetición de pruebas y cierre: **14 de septiembre de 2026, Colombia**. Los últimos registros usan UTC y muestran **15 de septiembre**. Esta publicación revisa los resultados guardados; no volvió a encender la infraestructura ni presenta esas pruebas como recién ejecutadas.

## Demostración principal en Azure

| Verificación | Resultado observado | Respaldo |
|---|---|---|
| Creación de AKS por Portal | Clúster creado el 9/09 en Chile Central con dos nodos DS2 v2 | Capturas originales privadas del Portal |
| Verificación desde Cloud Shell | Dos nodos Ready el 9/09 | [Fragmento](../evidencias/publicables/04-cloud-shell-20260909.txt) |
| Verificación desde CLI local | Dos nodos Ready, Kubernetes 1.35.7, repetida el 14/09 | [Salida](../evidencias/publicables/01-nodos-cli-20260914.txt) |
| Despliegues | Dos réplicas de classifier y una de planner disponibles | [Registro de pruebas](../evidencias/publicables/02-pruebas-aks-20260914.txt) |
| HTTP | **12 pruebas aprobadas en 19,804 segundos** | Mismo registro; casos en `tests/test_http.py` |
| Inferencia | Samoyed, puntuación 0,757887 para la fotografía de prueba | Prueba de inferencia real y respuesta original guardada |
| Persistencia | Cambió el UID del Pod; se mantuvieron el PVC y la tarea de evidencia | Mismo registro, pasos antes y después del reinicio |
| Monitoreo | Log Analytics devolvió filas después de generar tráfico y esperar ingesta | [Conteos derivados](../evidencias/publicables/06-resumen-monitoreo.json) y `monitoring/queries.kql` |

Las pruebas HTTP cubren disponibilidad del modelo, inferencia, imagen ausente o inválida, tamaño excesivo y métricas; en Planner, CRUD, validación, estados e identificadores inválidos, caracteres especiales tratados como datos, interfaz/cabeceras y disponibilidad de SQLite.

Cloud Shell tiene evidencia histórica del 9/09. Durante la sesión del 14/09 se abrió, pero no se ejecutó de nuevo la línea preparada desde ese origen; la repetición fue desde CLI local. No se mezclan ambos orígenes como si fueran la misma prueba.

## Extra elegido: HPA local

El profesor permite elegir uno de los dos extras. Se implementó y probó **Horizontal Pod Autoscaler en Minikube**; no se desplegó Kubeflow.

| Fase | Hora UTC, 15/09/2026 | Observación |
|---|---|---|
| Inicio de carga | 01:45:34 | Una réplica inicial |
| Subida comprobada | 01:46:44 | Cuatro réplicas disponibles; se suspende carga |
| Bajada comprobada | 01:49:27 | Una réplica disponible |

Registro completo: [03-hpa-ciclo-20260914.txt](../evidencias/publicables/03-hpa-ciclo-20260914.txt). La CPU llegó a 454% respecto de un request de 100m, frente a un objetivo del 50%. No representa 454% de toda la máquina. El Deployment llegó a una réplica mientras la lectura del HPA aún reflejaba cuatro: la actualización de estado es asíncrona; las condiciones y eventos registraron reducción a una.

Antes del ciclo exitoso se encontró un Job generador vencido (`DeadlineExceeded`). Se reemplazó solo ese Job con `scripts/14-reset-hpa-load.sh`, dejándolo suspendido, y se repitió `09-verify-hpa.sh`. No se utilizó `kubectl scale` para fabricar la subida o bajada. También hubo avisos transitorios de métricas no disponibles durante el arranque; se conservaron en el registro.

## Incidentes y límites observados

- Un Pod antiguo de Planner aparecía en Error por Preempting. Fue archivado y retirado tras verificar el nuevo Pod sano. La evidencia de pruebas conserva su presencia anterior.
- En la reactivación, las tres réplicas disponibles estaban en el mismo nodo. Tener dos nodos no garantiza distribución ni demuestra tolerancia a fallos. La afinidad preferente del clasificador no obliga a separarlos.
- Una consulta inicial de Azure Monitor no devolvió filas; después de generar solicitudes y esperar, aparecieron registros. Los avisos de Kubernetes se consultaron separadamente.
- Las pruebas locales del 9/09 en Docker y Kubernetes prepararon la demostración, pero no sustituyen las pruebas de AKS.
- Una fotografía conocida confirma inferencia; no mide exactitud general del modelo. Las dependencias transitivas y etiquetas de imágenes pueden cambiar al reconstruir.

## Cierre y conservación

Después del ensayo se verificó **AKS Stopped / Succeeded**, VMSS con capacidad cero y Azure Disk conservado en estado Unattached. El perfil Minikube `mp2-hpa`, Docker Desktop y los túneles quedaron detenidos. [Estado guardado de AKS](../evidencias/publicables/07-apagado-aks.json).

Se realizó copia consistente de SQLite con integridad `ok` y dos tareas. La base, exportación de tareas, recursos y verificación permanecen en `privadas/apagado-20260915T020210Z/`, fuera de Git. Persistencia y respaldo son controles diferentes.

Conservar AKS detenido permite reactivar el entorno; no elimina los cargos de discos, registro y otros servicios retenidos. La decisión fue conservar el progreso, no destruir el grupo. Para reanudar, consultar [08-REACTIVACION-Y-DEMO.md](08-REACTIVACION-Y-DEMO.md).

## Entrega y sustentación

El código se organiza en GitHub mediante commits temáticos con fecha real. La publicación no equivale a la confirmación de Classroom ni a la asistencia a la sustentación. Cada integrante debe ejecutar y explicar los pasos, y verificar el horario en el curso.

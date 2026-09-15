# Demostrar supervisión y monitoreo en Azure

Este requisito exige mostrar un servicio de Azure. `kubectl top` y el endpoint
`/metrics` son complementos útiles; por sí solos no demuestran Azure Monitor.

## Preparación

Si el clúster no tiene Container Insights, ejecuta:

```bash
bash scripts/05-monitoring.sh
```

El script crea Log Analytics en el grupo dedicado y habilita la recolección cada
minuto con filtro para `microproyecto2`. Si ya habilitaste monitoreo en el portal,
revisa qué workspace usa y evita crear uno duplicado. Ajusta `.env` para reutilizar
el workspace del mismo grupo o adapta el identificador si está en otro grupo.
Container Insights puede tardar varios minutos en comenzar a mostrar datos.

La configuración no despliega Prometheus administrado ni Grafana. Las aplicaciones
exponen `/metrics` en formato Prometheus, pero **no se recolecta automáticamente**
ese endpoint con esta configuración. La evidencia principal usa registros en
ContainerLogV2 y vistas de Container Insights.
[Habilitar monitoreo](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/kubernetes-monitoring-enable).

## Demostración sugerida de tres minutos

1. En Azure Portal abre AKS > Monitoring > Insights. Selecciona el clúster y el intervalo de la demostración. Muestra utilización de CPU y memoria de nodos o contenedores según las vistas disponibles.
2. Envía cinco fotografías al clasificador y crea una tarea en Campus Planner.
3. Genera un error de cliente controlado: `curl -i -X POST http://localhost:8081/predict`. Debe responder 400 porque falta `img`; esto no indica que el Pod haya fallado.
4. Abre Logs en el workspace. Ejecuta **por separado** las consultas de `monitoring/queries.kql`.
5. Identifica una petición `/predict`, su Pod, código y duración. Filtra por `request_id` si necesitas seguir una solicitud concreta.
6. Explica una observación real, por ejemplo el cambio de CPU bajo inferencia o el registro del error 400. Si el pico no es visible por agregación temporal, explica esa limitación; no lo inventes.

```bash
export KUBECONFIG="$PWD/.kube/aks.config"
kubectl top nodes
kubectl -n microproyecto2 top pods
kubectl -n microproyecto2 logs -l app=classifier --tail=20 --prefix
curl --fail http://localhost:8081/metrics
```

Los logs son JSON en stdout y contienen ruta, estado, duración y request_id. No
incluyen los bytes de las fotografías ni el contenido de las tareas. Gunicorn
puede añadir mensajes propios que las consultas filtran por `http_request`.

## Qué significan las métricas

| Indicador | Lectura correcta |
|---|---|
| CPU en millicores | 1000m equivalen a un núcleo; no es porcentaje de memoria |
| Memoria de trabajo | Uso observado del proceso o contenedor; comparar con su límite |
| p95 de duración | 95 % de las solicitudes observadas tardó ese valor o menos; depende de la muestra |
| 4xx | Solicitud inválida del cliente; no es necesariamente un fallo de infraestructura |
| 5xx | Error del servidor que debe investigarse |
| Reinicios | Veces que un contenedor se reinicia dentro del ciclo observado; un Pod nuevo es otro objeto |

## Si no aparecen datos

- Comprueba workspace, suscripción, clúster, namespace y rango de tiempo.
- Verifica que el add-on de monitoreo está habilitado y que los agentes estén Running.
- Genera nuevas peticiones, espera la ingestión y repite la consulta.
- Comprueba que ContainerLogV2 esté habilitado. Una tabla aún inexistente no prueba ausencia de errores.
- Confirma permisos para consultar Logs y restricciones de red del clúster.
- Los eventos Warning pueden no existir: una consulta vacía en ese caso es válida.

Guarda capturas con rango de tiempo y filtros visibles. Borra o recorta datos de
cuenta innecesarios antes de publicarlas.

# Microproyecto 2: reactivación y demostración

Revisión del 14 de septiembre de 2026 (Colombia). Esta guía reúne los comandos de demostración; las evidencias históricas se distinguen en RESULTADOS.md.

**Cierre posterior solicitado por Natalia:** AKS confirmado `Stopped / Succeeded`, VMSS con capacidad 0 y disco de Planner `Unattached` conservado. Minikube HPA, Docker Desktop y túneles locales detenidos. Se guardó una copia SQLite íntegra con dos tareas en `privadas/apagado-20260915T020210Z/`. Evidencias del cierre en `evidencias/azure/apagado-20260914/`. Las aplicaciones requieren reactivación para abrirse de nuevo.

## Requisitos del profesor

1. Crear AKS desde Azure Portal, con al menos dos nodos; comprobar desde Cloud Shell y desde Azure CLI local.
2. Desplegar y probar un clasificador de imágenes en AKS.
3. Desplegar y probar otra aplicación en AKS.
4. Demostrar supervisión y monitoreo de Azure.
5. Responder la sustentación individual. Extra opcional: Kubeflow o HPA; este proyecto eligió HPA local.

También exige subir los scripts al sitio del curso antes de la sustentación y respetar el horario. Los tres integrantes confirmados para esta entrega figuran en [EQUIPO.md](EQUIPO.md).

## Qué se comprobó en esta reactivación

- AKS `aks-microproyecto2`, grupo `rg-microproyecto2`, Chile Central: Running / Succeeded, Kubernetes 1.35.7 y dos nodos Ready.
- Dos réplicas de classifier y una de planner disponibles.
- Doce pruebas HTTP aprobadas y persistencia comprobada al cambiar el pod de planner, conservando el PVC de 1 GiB.
- Inferencia real: Samoyed, puntuación 0.757887; la puntuación no es una garantía de exactitud.
- Azure Monitor volvió a devolver registros recientes después de la demora inicial de ingesta.
- HPA local comprobado de nuevo: una réplica, cuatro bajo carga y retorno automático a una; registro en `evidencias/local/03-hpa-ciclo.txt`. Se reemplazó el Job vencido sin escalar manualmente la aplicación.
- Se archivó y retiró un pod anterior finalizado por Preempting; la aplicación quedó en un pod nuevo sano.
- Cloud Shell se abrió, pero el control del navegador no permitió enviar Enter. La prueba desde ese origen debe ejecutarse manualmente durante la demostración; hay evidencia histórica separada del 9 de septiembre.

## Entornos y acceso

Las aplicaciones están en AKS, no en VirtualBox. `localhost` es la entrada local de un túnel autenticado a Azure. Docker Desktop y el Minikube `mp2-hpa` se usan para el extra local, separado del clúster de Azure.

- Clasificador: http://localhost:8081/
- Campus Planner: http://localhost:8082/
- Portal: https://portal.azure.com/

Los túneles deben permanecer abiertos. No iniciar Compose en 8081/8082 mientras se utiliza el acceso a AKS.

## Preparar Warp (pestaña A, Mac)

```bash
cd /Users/nataliahernandez/Documents/Proyectos-IA/microproyecto2-aks
mkdir -p build
script -a build/sustentacion-azure.log
```

En la sesión registrada:

```bash
cd /Users/nataliahernandez/Documents/Proyectos-IA/microproyecto2-aks
export AZURE_CONFIG_DIR="$PWD/.azure"
export KUBECONFIG="$PWD/.kube/aks.config"
az account show --query '{suscripcion:name,estado:state}' -o table
az aks show -g rg-microproyecto2 -n aks-microproyecto2 --query '{estado:provisioningState,encendido:powerState.code,region:location}' -o table
```

Solo si está detenido:

```bash
bash scripts/13-start-aks.sh
```

El inicio vuelve a consumir crédito; conserva el clúster existente. Si Azure solicita autenticación, usar `az login` en esta misma sesión con AZURE_CONFIG_DIR configurado.

## Punto 1: dos nodos desde dos orígenes

En Warp:

```bash
bash scripts/01-connect.sh cli-local
kubectl config current-context
kubectl get nodes -o wide
kubectl -n microproyecto2 get deployments,pods,services,pvc -o wide
```

En Azure Portal, abrir Cloud Shell y elegir Bash. Si hay una línea preparada, cancelarla primero con Ctrl+C y ejecutar allí:

```bash
az account set --subscription 'Azure for Students'
az aks get-credentials -g rg-microproyecto2 -n aks-microproyecto2 --overwrite-existing
kubectl cluster-info
kubectl get nodes -o wide
```

Mostrar dos nodos Ready en ambos lugares. En Portal, abrir el recurso AKS y su grupo de nodos. La creación original se hizo en el portal; no crear otro clúster para el ensayo.

Para explicar regiones y permisos, desde A:

```bash
az account list-locations --query '[].name' -o tsv
SUB_ID=$(az account show --query id -o tsv)
az policy assignment show --name sys.regionrestriction --scope "/subscriptions/$SUB_ID" --query 'parameters.listOfAllowedLocations.value' -o tsv
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

La lista global no garantiza autorización, cuota o capacidad. Las regiones permitidas observadas fueron chilecentral, brazilsouth, northcentralus, canadacentral y westus. El PDF de activación es una referencia de 2020 de otra institución: no repetir su correo ni volver a activar una suscripción ya existente.

## Abrir las aplicaciones (pestaña B, Mac)

```bash
cd /Users/nataliahernandez/Documents/Proyectos-IA/microproyecto2-aks
bash scripts/04-open-apps.sh
```

Dejar B abierta. Si los puertos ya están ocupados por los túneles iniciados por Codex, utilizar esos accesos sin iniciar otra copia. El script crea dos port-forward a Services de AKS; cada túnel selecciona un pod y no demuestra balanceo entre réplicas.

## Punto 2: clasificador

En A:

```bash
kubectl -n microproyecto2 get deployment classifier
kubectl -n microproyecto2 get pods -l app=classifier -o wide
curl --fail http://localhost:8081/readyz
curl --fail -F img=@tests/fixtures/dog.jpg http://localhost:8081/predict | python3 -m json.tool
kubectl -n microproyecto2 logs -l app=classifier --tail=20 --prefix
```

En el navegador, seleccionar la fotografía y analizarla. Explicar las cinco categorías, la puntuación, el tiempo y el pod del resultado JSON. Se usa PyTorch con MobileNetV3 Small preentrenado en ImageNet-1K (1000 categorías). Es inferencia, no entrenamiento. El ejemplo MXNet del profesor es una sugerencia, no una biblioteca obligatoria. No se guardan fotografías; los pesos del modelo se incorporan a la imagen al construirla.

## Punto 3: Campus Planner y persistencia

```bash
kubectl -n microproyecto2 get deployment planner
kubectl -n microproyecto2 get pvc planner-data
curl --fail http://localhost:8082/readyz
curl --fail http://localhost:8082/api/tasks | python3 -m json.tool
```

Crear una actividad de demostración, cambiarla a completada y recargar. Campus Planner implementa CRUD con Flask y SQLite. El archivo `/data/planner.db` se guarda en un Azure Disk conectado mediante PVC `planner-data`, clase `managed-csi`. Utiliza una réplica y estrategia Recreate; no es una base de datos distribuida.

Para repetir pruebas y demostrar que cambia el pod pero permanece una tarea:

```bash
bash scripts/11-test-aks.sh
```

El script usa puertos 8083/8084, ejecuta 12 pruebas, crea una tarea de evidencia, reinicia el Deployment de planner y comprueba nuevo UID, mismo volumen y misma tarea. Los datos anteriores se conservan. El túnel del navegador de planner puede terminar al cambiar su pod; si ocurre, cerrar B con Ctrl+C y ejecutar `04-open-apps.sh` otra vez.

## Cómo se publicaron y desplegaron las aplicaciones

```bash
cat apps/classifier/Dockerfile
cat apps/planner/Dockerfile
cat k8s/base/classifier.yaml
cat k8s/base/planner.yaml
cat k8s/overlays/aks/kustomization.yaml
```

Dockerfile construye el paquete; ACR almacena las imágenes; Deployment las ejecuta; Service da acceso interno; PVC solicita almacenamiento. Las imágenes de Azure se construyeron para linux/amd64 aunque el Mac es ARM. Los scripts `02-publish-images.sh` y `03-deploy.sh` publican y despliegan; no es necesario reconstruir ni recrear recursos para cada ensayo.

## Punto 4: monitoreo de Azure

En A, generar solicitudes y consultar:

```bash
curl --fail -F img=@tests/fixtures/dog.jpg http://localhost:8081/predict
curl -i -X POST http://localhost:8081/predict
kubectl top nodes
kubectl -n microproyecto2 top pods
python3 scripts/12-query-monitoring.py
```

La segunda petición omite la imagen y debe producir 400. En Portal, abrir AKS > Supervisión/Monitoring > Insights y mostrar CPU/memoria; en Logs del workspace, ejecutar por separado las consultas de `monitoring/queries.kql`.

```kusto
ContainerLogV2
| where TimeGenerated > ago(1h)
| where PodNamespace == "microproyecto2"
| extend e = parse_json(tostring(LogMessage))
| where tostring(e.event) == "http_request"
| project TimeGenerated, PodName, ruta=tostring(e.path), estado=toint(e.status), duracion_ms=todouble(e.duration_ms)
| order by TimeGenerated desc
```

Azure Monitor observa la operación; Container Insights recoge información del clúster; Log Analytics permite consultar registros mediante KQL. Los logs explican eventos y las métricas muestran cantidades como CPU y memoria. 4xx indica una solicitud inválida, 5xx un error de servidor. p95 resume la duración de una muestra; no garantiza todas las solicitudes futuras. `kubectl top` complementa pero no reemplaza mostrar un servicio de monitoreo de Azure. El endpoint `/metrics` no implica que exista Prometheus administrado: esta configuración no lo despliega.

## Extra: HPA local (pestaña C, Mac)

```bash
cd /Users/nataliahernandez/Documents/Proyectos-IA/microproyecto2-aks
docker desktop start
export MINIKUBE_HOME="$PWD/.tools/minikube-home"
export KUBECONFIG="$PWD/.kube/minikube.config"
.tools/minikube -p mp2-hpa start --driver=docker --cpus=2 --memory=3072mb --kubernetes-version=v1.34.0
kubectl config current-context
kubectl -n mp2-hpa get hpa,deployment,pods
```

Debe indicar contexto mp2-hpa. El cliente kubectl instalado es más reciente que este Kubernetes; para consultas con una versión adecuada se puede usar `.tools/minikube -p mp2-hpa kubectl -- get nodes`.

Preparar un generador nuevo antes de cada ronda. El Job anterior puede haber vencido tras apagar el laboratorio:

```bash
bash scripts/14-reset-hpa-load.sh
bash scripts/09-verify-hpa.sh
```

El primer script reemplaza solo el Job suspendido; no cambia las réplicas de la aplicación. El segundo activa carga, espera cuatro réplicas, suspende carga y espera el retorno a una. El límite del generador es cinco minutos.

Para una demostración manual, en lugar de ejecutar `09`, observar en C:

```bash
kubectl -n mp2-hpa get hpa cpu-demo -w
```

Desde otra pestaña con el mismo KUBECONFIG local, activar y después suspender:

```bash
kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":false}}'
kubectl -n mp2-hpa get pods
kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":true}}'
kubectl -n mp2-hpa describe hpa cpu-demo
```

No pegar los cuatro comandos inmediatamente: esperar el crecimiento antes de suspender. El HPA tiene mínimo 1, máximo 4 y objetivo 50% de la CPU solicitada (100m), equivalente a 50m por pod. No es 50% de todo el computador. HPA cambia pods automáticamente; el escalado manual con `kubectl scale` no demuestra HPA y el autoscaler del clúster cambia nodos, que es otro mecanismo.

## Finalizar cuando termine el ensayo

No se ejecuta el apagado automáticamente con esta guía. Cerrar los túneles con Ctrl+C. Suspender el Job local si sigue activo y detener Minikube:

```bash
KUBECONFIG="$PWD/.kube/minikube.config" kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":true}}'
MINIKUBE_HOME="$PWD/.tools/minikube-home" KUBECONFIG="$PWD/.kube/minikube.config" .tools/minikube -p mp2-hpa stop
```

En la sesión Azure configurada:

```bash
az aks stop -g rg-microproyecto2 -n aks-microproyecto2
az aks show -g rg-microproyecto2 -n aks-microproyecto2 --query '{encendido:powerState.code,estado:provisioningState}' -o table
```

Confirmar Stopped / Succeeded. Detener conserva recursos y el disco; no elimina todo el costo de almacenamiento y servicios conservados. No ejecutar `07-delete-azure.sh`, borrar el grupo ni borrar el PVC durante un ensayo. El profesor recomienda destruir por costos; en este entorno se eligió conservarlo detenido para mantener los datos y reactivarlo. Esa diferencia debe explicarse.

Para terminar el registro de `script`, escribir `exit` en su sesión.

## Explicación breve

En la práctica anterior Kubernetes estaba en una máquina local. Aquí llevé dos aplicaciones a Azure, donde tengo dos nodos administrados por AKS. El clasificador usa un modelo preentrenado para analizar fotografías; Campus Planner administra tareas y conserva sus datos en un disco externo al pod. Publiqué las imágenes en ACR, desplegué los manifiestos y usé Azure Monitor para observar la actividad. En un laboratorio local aparte, el HPA aumenta y reduce automáticamente las réplicas según la carga de CPU. Los túneles permiten acceder desde mi navegador a las aplicaciones de Azure sin publicarlas abiertamente.

# Ruta de trabajo y primera ejecución

El proyecto ya fue desplegado y probado en AKS. El cierre del 14 de septiembre de 2026 conservó el clúster detenido y su disco; consulta [RESULTADOS.md](RESULTADOS.md).

## Elegir el entorno del ensayo

1. **Demostración principal en Azure:** sigue [08-REACTIVACION-Y-DEMO.md](08-REACTIVACION-Y-DEMO.md). Usa `13-start-aks.sh`, verifica dos nodos desde CLI y Cloud Shell y abre los túneles con `04-open-apps.sh`.
2. **Primera instalación en otra suscripción:** sigue [02-AZURE.md](02-AZURE.md), incluyendo la creación por Portal. No recrees el clúster conservado solo para ensayar.
3. **Práctica sin Azure:** usa Docker con los pasos siguientes. Los resultados locales no sustituyen las evidencias de AKS.
4. **Extra HPA:** usa Minikube y [04-HPA.md](04-HPA.md). No comparte el contexto de AKS.
5. **Entrega:** revisa las evidencias, los commits y la confirmación de entrega en la plataforma del curso. La publicación en GitHub no registra el horario ni envía Classroom.

## Abrir las aplicaciones

Abre una terminal dentro de `microproyecto2-aks`. Ejecuta:

```bash
docker compose up -d --build --wait
docker compose ps
```

Abre http://localhost:8081 y carga `tests/fixtures/dog.jpg`. Observa las cinco
predicciones y el tiempo de inferencia. En http://localhost:8082 registra una
actividad con datos de ejemplo y cambia su estado. Los contadores se calculan con
las tareas guardadas; no representan métricas del clúster.

```bash
python3 -m unittest discover -s tests -v
curl --fail -F img=@tests/fixtures/dog.jpg http://localhost:8081/predict
curl --fail http://localhost:8082/api/tasks
```

## Demostrar persistencia en Docker

1. Crea una actividad y anota su identificador con `/api/tasks`.
2. Ejecuta `docker compose up -d --force-recreate planner`.
3. Cuando esté saludable, recarga el tablero y confirma que la actividad sigue ahí.

El contenedor cambia; el volumen `planner-data` conserva SQLite. En AKS esta misma
responsabilidad corresponde al PVC. La persistencia frente a un reinicio **no**
equivale a una copia de seguridad ni protege frente a la eliminación del volumen.

## Detener y recuperar

```bash
docker compose stop
docker compose up -d --wait
```

No uses el reinicio de Docker como evidencia de AKS. Son pruebas en entornos diferentes.
Para liberar puertos antes de los túneles de AKS: `docker compose stop`.

## Repetir el ensayo de aplicaciones en Kubernetes local

La preparación realizada también probó las aplicaciones en el perfil local del
laboratorio. Para repetirla, primero ejecuta `bash scripts/08-hpa-local.sh` y luego:

```bash
export KUBECONFIG="$PWD/.kube/minikube.config"
export MINIKUBE_HOME="$PWD/.tools/minikube-home"
docker compose build
.tools/minikube -p mp2-hpa image load mp2-classifier:v1 mp2-planner:v1
kubectl apply -k k8s/base
kubectl -n microproyecto2 rollout status deployment/classifier --timeout=240s
kubectl -n microproyecto2 rollout status deployment/planner --timeout=240s
bash scripts/10-test-kubernetes-local.sh
```

Si instalaste Minikube en PATH, sustituye `.tools/minikube` por `minikube`.
El ZIP excluye los ejecutables descargados y la caché del clúster. El script de
pruebas usa puertos 8083 y 8084, comprueba ambas APIs y reemplaza el Pod del tablero
para verificar la persistencia. Estos pasos no crean recursos en Azure.

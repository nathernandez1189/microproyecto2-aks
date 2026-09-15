# Punto extra de autoescalado horizontal

Se eligió HPA, una de las dos alternativas de +0,5 del enunciado. No se implementa
Kubeflow. Este laboratorio usa un perfil local de Minikube llamado `mp2-hpa` y
no consume crédito de Azure. Su imagen de carga es distinta de las dos aplicaciones.

## Preparar el entorno

Instala Minikube desde su fuente oficial y mantén Docker Desktop iniciado.
El script admite `minikube` en PATH o `.tools/minikube`.

```bash
bash scripts/08-hpa-local.sh
export KUBECONFIG="$PWD/.kube/minikube.config"
kubectl config current-context
kubectl -n mp2-hpa get hpa,pods
kubectl -n mp2-hpa top pods
```

El contexto debe ser `mp2-hpa`. Nunca ejecutes este ejercicio por accidente en
AKS. El script reserva 2 CPU y aproximadamente 3 GB para el clúster local; las
aplicaciones Docker necesitan memoria adicional.

## Demostrar subida y bajada

Para registrar automáticamente un ciclo completo, una vez listo el laboratorio:
`bash scripts/14-reset-hpa-load.sh` seguido de `bash scripts/09-verify-hpa.sh`. Produce `evidencias/local/03-hpa-ciclo.txt` y falla
si no observa cuatro réplicas disponibles y el regreso a una. No aplica cambios
manuales al número de réplicas durante la observación.

En una terminal observa continuamente:

```bash
export KUBECONFIG="$PWD/.kube/minikube.config"
kubectl -n mp2-hpa get hpa cpu-demo -w
```

En otra terminal inicia la carga:

```bash
export KUBECONFIG="$PWD/.kube/minikube.config"
kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":false}}'
kubectl -n mp2-hpa get pods
```

Observa que el uso supera el objetivo de 50 % y el Deployment crece desde una
réplica, hasta un máximo de cuatro. No uses `kubectl scale` como evidencia de HPA:
ese comando cambia réplicas manualmente.

Después de capturar el crecimiento, suspende la carga:

```bash
kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":true}}'
kubectl -n mp2-hpa describe hpa cpu-demo
```

Espera a que las métricas bajen y termine la ventana de estabilización de 60
segundos. El regreso a una réplica puede tardar más debido al muestreo y a las
decisiones del controlador. El Job también tiene un límite de ejecución de
300 segundos. Si terminó por ese límite, elimínalo y vuelve a aplicar el
manifiesto para otra ronda; reaplicar `demo.yaml` también restablece la réplica
inicial, así que hazlo **fuera de la captura de la demostración**.

```bash
kubectl -n mp2-hpa get hpa,pods > evidencias/local/hpa-final.txt
kubectl -n mp2-hpa describe hpa cpu-demo > evidencias/local/hpa-descripcion.txt
```

## Explicación para el profesor

El Deployment solicita `100m` de CPU por Pod. El HPA apunta al 50 % de esa
solicitud: aproximadamente `50m` por Pod, **no** al 50 % de la CPU total del nodo
ni al 50 % del límite de `500m`.

La regla orientativa es:

```text
réplicas deseadas = ceil(réplicas actuales × utilización actual / utilización objetivo)
```

Con dos réplicas y utilización media de 90 %, el cálculo orientativo es
`ceil(2 × 90 / 50) = 4`. El controlador además considera disponibilidad de
métricas, tolerancia, estado de los Pods, estabilización y los límites 1 a 4.
HPA cambia **Pods**, mientras el autoscaler del clúster cambia **nodos**.
[Funcionamiento del HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

El servicio CPU ejecuta una operación acotada por petición. Cuatro bucles
concurrentes generan carga dentro del namespace. El endpoint de salud no hace
ese trabajo, evitando reinicios provocados por la propia prueba.

## Problemas frecuentes

- `TARGETS <unknown>`: espera a metrics-server y revisa `kubectl top pods`.
- No escala: verifica carga activa, CPU requests y que no estés mirando otro contexto.
- Pods Pending: revisa recursos libres; el HPA no crea capacidad física.
- No baja inmediatamente: espera métricas recientes y estabilización; confirma que no quede otro generador activo.

## Detener Minikube

```bash
export MINIKUBE_HOME="$PWD/.tools/minikube-home"
export KUBECONFIG="$PWD/.kube/minikube.config"
.tools/minikube -p mp2-hpa stop
# Si usas Minikube instalado en PATH, cambia .tools/minikube por minikube.
```

Detener conserva el laboratorio local. `minikube delete -p mp2-hpa` lo elimina;
conserva las evidencias antes de hacerlo.

## Repetir una sesión después del apagado

El Job generador tiene un límite de cinco minutos y puede quedar vencido. Ejecuta `bash scripts/14-reset-hpa-load.sh` antes de cada nueva ronda: reemplaza solo ese Job y lo deja suspendido. Después, `bash scripts/09-verify-hpa.sh` observa la subida y bajada automáticas. Los resultados recientes y el incidente del Job vencido se describen en [RESULTADOS.md](RESULTADOS.md).

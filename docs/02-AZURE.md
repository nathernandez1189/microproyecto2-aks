# Activar Azure y desplegar el microproyecto

AKS se creó por Portal y se comprobó desde CLI local y Cloud Shell el 9 de septiembre de 2026. El 14 de septiembre se repitieron las pruebas desde el Mac y luego se detuvo conservando el disco. [RESULTADOS.md](RESULTADOS.md) distingue las fechas.

Esta guía documenta una **primera instalación**. Para el entorno existente, usa [08-REACTIVACION-Y-DEMO.md](08-REACTIVACION-Y-DEMO.md). No vuelvas a activar Students ni crees otro AKS si ya dispones de ellos.

## Activar Azure for Students

1. Abre [Azure for Students](https://azure.microsoft.com/es-es/free/students/).
2. Inicia sesión con la cuenta de Microsoft que utilizarás para el proyecto y completa la verificación académica con tu correo de UAO. No uses el correo de Educastur mostrado en el PDF histórico.
3. Completa personalmente la verificación, los datos solicitados y la aceptación de condiciones. No compartas contraseñas ni códigos.
4. En el portal, abre **Suscripciones** y comprueba que **Azure for Students** aparece activa. Registra su identificador en tu `.env` local.
5. Revisa el crédito disponible y las condiciones mostradas para tu cuenta. La página oficial anuncia USD 100 por 12 meses para estudiantes elegibles; no significa que todos los servicios sean gratuitos.

La interfaz puede cambiar. Sigue los nombres actuales de las opciones del portal
si no coinciden con las capturas de 2020 del adjunto.

## Preparar herramientas y configuración

Cloud Shell ya dispone de Azure CLI y kubectl. Para cumplir la segunda forma de
verificación también utiliza una terminal **fuera de Cloud Shell**, en tu computador.
En macOS, con Homebrew instalado: `brew install azure-cli kubectl`.
Consulta la [instalación oficial](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos).

```bash
export AZURE_CONFIG_DIR="$PWD/.azure"
az login
cp -n .env.example .env
# Edita .env con tu suscripción, región y un nombre único alfanumérico para ACR.
bash scripts/00-check-azure.sh
```

La política observada el 9 de septiembre no permitía `eastus2`; autorizaba
`chilecentral`, `brazilsouth`, `northcentralus`, `canadacentral` y `westus`.
La configuración validada por el formulario usa `chilecentral`: las consultas encontraron máquinas DS2 v2 disponibles y cuota suficiente para dos nodos.
`az account list-locations` enumera
regiones globales; **no garantiza** que tu suscripción permita crear el tamaño
de máquina elegido. Revisa las restricciones de `az vm list-skus`, la cuota total
regional y la cuota de la familia de máquinas.

Si un proveedor necesario figura `NotRegistered`, regístralo en **Suscripciones >
Proveedores de recursos**, o usa `az provider register --namespace Microsoft.Compute --wait`
cambiando el nombre por el proveedor que falte. Repite la consulta hasta verificarlo.

## Crear el clúster desde Azure Portal

El enunciado exige el portal: conserva capturas de **Revisar y crear** y del
despliegue terminado. Los scripts no sustituyen esta parte.

| Campo | Configuración propuesta para este laboratorio |
|---|---|
| Suscripción | Azure for Students activa |
| Grupo de recursos | `rg-microproyecto2`, exclusivo para este trabajo |
| Modalidad | AKS administrado de configuración manual, preset Dev/Test |
| Nivel de precios del control plane | Free, si está disponible; las máquinas y otros recursos se cobran |
| Nombre | `aks-microproyecto2` |
| Región | Una región permitida con cuota y capacidad comprobadas |
| Kubernetes | Versión estable y soportada que ofrezca el portal |
| Grupo de nodos | Linux Ubuntu, modo System, mínimo dos nodos, escalado manual |
| Tamaño | Configuración validada en el portal: `Standard_DS2_v2`, 2 vCPU y 7 GiB por nodo |
| Arquitectura de nodos | x86-64, compatible con las imágenes `linux/amd64` que publican los scripts |
| Red | Configuración admitida por el portal; Azure CNI Overlay si está disponible |
| Identidad | Identidad administrada; mantener la autenticación ofrecida por el portal |
| Monitoreo | Habilitar Container Insights según la siguiente sección; evitar duplicar workspaces |

En la sesión del 9 de septiembre de 2026, el portal aceptó dos `Standard_DS2_v2` y el despliegue terminó con ambos nodos Ready. Esta es una configuración observada en esa fecha, no una garantía de disponibilidad futura. Revisa requisitos, cuota y capacidad si creas otro clúster.
[Requisitos de grupos de sistema](https://learn.microsoft.com/en-us/azure/aks/use-system-pools).

La cuota observada de la familia DSv2 era de 4 vCPU y la regional de 6. Dos nodos consumían la cuota de familia; un nodo adicional para actualización requeriría ampliarla. La decisión actual es conservar AKS detenido entre ensayos. Consulta costos antes de reactivarlo.

Para este laboratorio pequeño se permite compartir el grupo de sistema con las
aplicaciones si no tiene un taint que las excluya. Es una decisión de costo para
la práctica. Una arquitectura productiva debería separar las cargas de usuario.
No añadas automáticamente otros grupos: revisa el total final de máquinas y costo.

Antes de **Crear**, registra tamaño, nodos, región, versión, redes y estimación que
muestre el portal. Después comprueba **Provisioning state: Succeeded** y los dos
nodos. Guarda los parámetros para recrear el clúster más adelante.
[Guía oficial de creación por portal](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal).

## Verificar desde dos lugares diferentes

En tu computador, desde la raíz del proyecto:

```bash
bash scripts/01-connect.sh cli-local
```

En **Cloud Shell Bash**, utiliza una copia del repositorio y un `.env` completado allí:

```bash
bash scripts/01-connect.sh cloud-shell
```

Guarda ambos archivos de salida y una captura de cada terminal donde se distinga
el entorno. No basta ejecutar dos veces el mismo comando en la misma terminal.
Si la autenticación requiere `kubelogin`, sigue el aviso de AKS y su documentación
de acceso; no descargues credenciales de administrador como solución automática.
El script usa `.kube/aks.config` para no sobrescribir el contexto personal.

## Publicar imágenes y desplegar

```bash
bash scripts/02-publish-images.sh
bash scripts/03-deploy.sh
docker compose stop
bash scripts/04-open-apps.sh
```

`02` crea ACR Basic si no existe y publica imágenes `linux/amd64`. El flujo elige buildx local en Chile Central por la restricción de ACR Tasks observada durante el laboratorio. En otras regiones puede usar ACR Tasks. La construcción requiere Docker en el modo local; Azure puede consumir crédito. La alternativa manual es:

```bash
set -a; source .env; set +a
az acr login --name "$ACR_NAME"
REGISTRY=$(az acr show -n "$ACR_NAME" --query loginServer -o tsv)
docker buildx build --platform linux/amd64 -f apps/classifier/Dockerfile -t "$REGISTRY/mp2-classifier:$IMAGE_TAG" --push .
docker buildx build --platform linux/amd64 -f apps/planner/Dockerfile -t "$REGISTRY/mp2-planner:$IMAGE_TAG" --push .
bash scripts/03-deploy.sh
```

El script configura `AcrPull` para la identidad de kubelet en un ACR con permisos
RBAC. Si el registro usa ABAC, `--attach-acr` no aplica: asigna el rol
**Container Registry Repository Reader** a esa identidad según la guía oficial,
y adapta la publicación para no intentar `--attach-acr`.
[Integración ACR y AKS](https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration).

Para una revisión de código posterior usa una etiqueta nueva en `.env`, por
ejemplo `IMAGE_TAG=v2`, y repite publicación y despliegue. No reutilices `v1`
esperando que Kubernetes descargue otra imagen: `IfNotPresent` puede conservar
la imagen anterior. Un registro por digest permite mayor trazabilidad en una
versión futura.

En otra terminal, con los túneles activos:

```bash
curl --fail -F img=@tests/fixtures/dog.jpg http://localhost:8081/predict
curl --fail http://localhost:8082/readyz
python3 -m unittest discover -s tests -v
bash scripts/06-evidence.sh
```

Aunque el navegador muestra `localhost`, las aplicaciones están dentro de AKS;
el túnel solo transporta las peticiones. Corrobóralo con el nombre de Pod devuelto
por `/predict`, los Pods del clúster y los registros de Azure.

## Demostrar el volumen en AKS

1. Crea una tarea desde el tablero y guarda `/api/tasks`.
2. En una terminal nueva: `export KUBECONFIG="$PWD/.kube/aks.config"`.
3. Ejecuta `kubectl -n microproyecto2 rollout restart deployment/planner` y después `kubectl -n microproyecto2 rollout status deployment/planner --timeout=300s`.
4. Vuelve a ejecutar los túneles si el del tablero se cerró. Confirma que la misma tarea permanece.
5. Conserva la salida de `kubectl -n microproyecto2 get pods,pvc -o wide` antes y después.

## Control del crédito y eliminación definitiva

Para cerrar una sesión conservando el progreso, sigue el apagado de la guía 08. Los pasos de eliminación siguientes son una alternativa definitiva, no la rutina de ensayo.

Revisa costos de nodos, discos, red de salida, ACR y registros. La configuración
usa Services ClusterIP, pero AKS puede crear recursos de red para su salida. El
nivel Free del control plane no elimina estos cargos. Un presupuesto avisa;
no es un interruptor automático de consumo.

Antes de borrar, guarda evidencias y exporta tareas con `curl --fail
http://localhost:8082/api/tasks > tareas-respaldo.json`. Conserva ese archivo en
privado si usaste datos personales. Para una copia SQLite consistente puedes usar
su API de backup; no copies solo el archivo `.db` mientras haya escrituras WAL.

```bash
bash scripts/06-evidence.sh
bash scripts/07-delete-azure.sh
```

La limpieza pide escribir el nombre exacto del grupo, elimina **todos sus recursos**
y verifica también el grupo administrado de nodos. Usa solo el grupo exclusivo
del microproyecto. Revisa recursos creados fuera de él. Detener AKS puede dejar
discos, registro y otros conceptos facturables; no equivale a destruirlo.

Para recrear: repite la creación **por portal**, luego scripts `01` a `06`.
Las tareas de demostración se volverán a crear; el código y los pesos se recuperan
mediante el proceso de construcción.

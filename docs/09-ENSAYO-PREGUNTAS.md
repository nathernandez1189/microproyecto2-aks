# Ensayo de sustentación — Microproyecto 2 Azure

Primero intenta responder sin mirar. Después compara con la respuesta modelo y explica una prueba que mostrarías.

## 1. ¿Qué hicieron en este proyecto?
Desplegamos dos aplicaciones en un clúster AKS de dos nodos: un clasificador de fotografías y un organizador de actividades. Comprobamos su funcionamiento, persistencia y monitoreo. Como extra, demostramos autoescalado de pods en Minikube local.

## 2. ¿Qué diferencia tiene frente a Minikube?
La práctica anterior corría localmente. Aquí las aplicaciones principales se ejecutan en infraestructura de Azure mediante AKS. El HPA adicional sigue siendo un laboratorio local separado.

## 3. ¿Qué es AKS y qué administra Microsoft?
AKS es Kubernetes administrado por Azure. Microsoft administra el plano de control; nosotros configuramos aplicaciones, accesos, recursos y almacenamiento. No significa que Microsoft diseñe o corrija automáticamente nuestra aplicación.

## 4. ¿Cuántos nodos y réplicas tienes?
AKS tiene dos nodos. El clasificador utiliza dos réplicas y Planner una. Son conceptos distintos: el nodo ofrece recursos y el pod ejecuta la aplicación. El extra HPA tiene otro clúster local con un nodo.

## 5. ¿Imagen, contenedor, pod y Deployment son lo mismo?
La imagen es el paquete. El contenedor ejecuta ese paquete. El pod agrupa los contenedores que Kubernetes ejecuta juntos. El Deployment mantiene la cantidad deseada de pods y su configuración.

## 6. ¿Para qué usaste ACR?
Para guardar las imágenes Docker que AKS descarga y ejecuta. El Dockerfile contiene las instrucciones para construirlas; ACR almacena el resultado.

## 7. ¿Por qué construiste para amd64 si tu Mac es ARM?
Porque las imágenes deben coincidir con la arquitectura de los nodos de destino. Los nodos de este AKS son amd64; el Mac y el Minikube local usan ARM64.

## 8. ¿Entrenaste el modelo de inteligencia artificial?
No. Usamos MobileNetV3 Small preentrenado en ImageNet-1K. Preprocesamos una fotografía y hacemos inferencia: calculamos predicciones con un modelo que ya fue entrenado.

## 9. ¿Qué significa la puntuación 75,8 %?
Es una puntuación softmax del modelo para esa categoría entre las 1000 disponibles. No demuestra que la aplicación tenga una exactitud general del 75,8 % ni garantiza que esa predicción sea correcta.

## 10. ¿Qué ocurre con una fotografía inválida?
La aplicación valida formato y tamaño. Por ejemplo, una solicitud sin el archivo requerido devuelve 400 y una demasiado grande devuelve 413. Eso es una validación esperada, no necesariamente una caída del servidor.

## 11. ¿Qué hace Campus Planner y qué base utiliza?
Permite crear, consultar, actualizar y eliminar actividades: CRUD. Usa Flask con SQLite. El archivo de la base está en un disco persistente de Azure, no en MySQL ni en Azure SQL.

## 12. ¿Cómo sabes que los datos son persistentes?
Creamos una tarea, cambiamos el pod y comprobamos que el nuevo pod tenía otro UID, el mismo volumen y la misma tarea. Recargar una página por sí solo no demuestra que los datos sobrevivan al cambio de pod.

## 13. ¿Un PVC es un respaldo?
No. Un PVC permite utilizar almacenamiento independiente del pod. Un respaldo es otra copia para recuperar información. Si se elimina o daña el volumen, persistencia por sí sola no basta. También guardamos una copia SQLite y comprobamos su integridad.

## 14. ¿Por qué Planner tiene una réplica?
Usa SQLite en un archivo y está diseñado con una réplica y estrategia Recreate. No lo presentamos como base distribuida; puede tener una interrupción breve al reemplazar su pod. Para escalarlo necesitaríamos revisar la arquitectura y la base de datos.

## 15. ¿Por qué abres localhost si está en Azure?
Porque kubectl port-forward crea un túnel autenticado desde mi Mac hacia un pod de AKS. Localhost es la entrada del túnel. Cerrar el túnel no apaga el pod. Tampoco demuestra balanceo entre réplicas, porque selecciona un pod.

## 16. ¿Por qué Cloud Shell y CLI local?
Porque el profesor exige comprobar ambos accesos. Cloud Shell es una terminal alojada por Azure; Warp es una terminal de mi computador. Ambas deben consultar el mismo clúster y mostrar sus dos nodos.

## 17. ¿Qué diferencia hay entre métricas y logs?
Las métricas son medidas como CPU, memoria o cantidad de solicitudes. Los logs describen operaciones concretas. Usamos Container Insights y Log Analytics de Azure Monitor, con consultas KQL. kubectl top es un complemento, no reemplaza mostrar Azure Monitor.

## 18. ¿Cómo investigas un error?
Reviso estado de pods y eventos, después logs y métricas del intervalo afectado. Distingo una solicitud inválida 4xx de un error de servidor 5xx. No doy por hecho que el clúster falló solo porque una solicitud recibió 400.

## 19. ¿Cómo funciona el HPA?
Observa una métrica y ajusta réplicas automáticamente. En el laboratorio va de 1 a 4 pods según CPU y vuelve a 1 al retirar la carga. El objetivo es 50% de los 100m de CPU solicitados por pod, aproximadamente 50m; no es 50% de toda la máquina.

## 20. ¿Por qué puede mostrar más del 100 % de CPU?
El porcentaje del HPA se calcula respecto a la solicitud de CPU. Si un pod solicita 100m y usa 400m, está usando 400% de su solicitud. No significa que el computador supere el 100% de su capacidad física.

## 21. ¿Por qué no baja inmediatamente al quitar la carga?
Necesita métricas actualizadas y respeta una ventana de estabilización. Esperamos y comprobamos la reducción automática; no la forzamos con kubectl scale para hacerla pasar por HPA.

## 22. ¿Qué diferencia hay entre escalado manual, HPA y autoscaler del clúster?
El manual fija réplicas por una orden nuestra. HPA modifica pods según métricas. El autoscaler del clúster modifica la cantidad de nodos. En el extra demostramos HPA, no crecimiento automático de máquinas.

## 23. ¿Dos nodos garantizan que las réplicas estén separadas?
No. Hay que revisar la columna NODE y las reglas de planificación. Tener dos nodos no demuestra por sí solo alta disponibilidad de toda la solución, y Planner sigue teniendo una réplica.

## 24. ¿Por qué Chile Central y no cualquier región?
La suscripción restringe regiones y hay que comprobar cuota y capacidad. Elegimos una región permitida donde se pudo desplegar el tamaño requerido. Listar todas las regiones no garantiza permiso para crear cualquier recurso.

## 25. ¿Qué pasa al cerrar el navegador o detener AKS?
Cerrar el navegador no detiene Azure. Detener AKS detiene su cómputo y conserva la configuración y almacenamiento del proyecto. Otros recursos conservados pueden generar cargos. El profesor recomienda destruir para controlar costos; nosotros conservamos detenido el entorno para mantener los datos y reactivarlo.

## Retos prácticos que pueden pedir

- Mostrar los dos nodos desde Warp y Cloud Shell.
- Enviar otra fotografía y explicar una predicción equivocada sin inventar certeza.
- Crear una tarea y demostrar que permanece después de reemplazar el pod.
- Explicar un registro 400 generado deliberadamente al omitir la fotografía.
- Identificar qué pod atendió una solicitud y relacionarlo con los logs.
- Generar carga, observar el aumento del HPA y esperar su reducción.

## Apertura de la exposición

“En este proyecto llevamos dos aplicaciones a Azure usando Kubernetes. Una clasifica fotografías con un modelo preentrenado y la otra administra actividades con datos persistentes. Demostramos el acceso desde dos terminales, revisamos el funcionamiento y utilizamos monitoreo para observar la actividad. Como extra, comprobamos que Kubernetes puede aumentar y reducir automáticamente réplicas según la carga.”

## Forma de responder

Usa tres partes: qué es, cómo lo usamos y qué prueba lo demuestra. Si no recuerdas un valor, consúltalo en la configuración o terminal; no lo inventes.

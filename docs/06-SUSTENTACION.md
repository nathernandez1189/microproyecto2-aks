# Guía de sustentación individual

MIGUEL ANGEL DIUZA, JUAN OSPINA TENORIO y NATALIA HERNANDEZ PIEDRAHITA deben poder presentar todo
el proyecto. La distribución sugerida sirve para preparar y revisar, no para que
alguien desconozca el resto del proyecto.

## Apertura para adaptar con tus propias palabras

“El proyecto despliega dos aplicaciones en Kubernetes: un clasificador de imágenes
y un tablero académico con persistencia. Voy a mostrar el clúster, procesar una
imagen, comprobar que los datos sobreviven al reemplazo de un Pod y relacionar
esas acciones con los registros de Azure Monitor. El punto extra demuestra cómo
HPA aumenta y reduce Pods cuando cambia la carga.”

Solo usa “en AKS” cuando realmente estés conectado al clúster de Azure.

## Recorrido sugerido

| Minuto orientativo | Demostración | Idea que debes explicar |
|---|---|---|
| 0 a 1 | Arquitectura y portal | Qué administra Azure y qué configuras tú |
| 1 a 2 | Cloud Shell y CLI local | Nodos Ready y ambos entornos de acceso |
| 2 a 4 | Clasificador | Preprocesamiento, inferencia, softmax y limitaciones |
| 4 a 6 | Campus Planner | Operaciones, PVC y reemplazo del Pod |
| 6 a 8 | Azure Monitor | Diferencia entre estado, métrica y registro |
| 8 a 10 | HPA local | CPU requests, réplicas y estabilización |

Es un guion de ensayo, no una duración confirmada por el profesor. Inicia el
laboratorio y la recolección de métricas antes del turno. La bajada del HPA tarda;
puedes iniciarla y mostrar otra evidencia mientras termina.

## Preguntas que cada integrante debe responder

**1. ¿Qué es AKS?** Un servicio administrado de Kubernetes. Azure opera el control
plane; tú defines cargas, acceso, nodos y configuración del proyecto dentro del
modelo de responsabilidad compartida.

**2. ¿Dos nodos son dos Pods?** No. Un nodo es una máquina del clúster; un Pod es
una unidad de ejecución programada sobre un nodo. Cada nodo puede alojar varios Pods.

**3. ¿Qué hace un Deployment?** Mantiene el estado deseado de sus réplicas mediante
ReplicaSets y permite actualizar o reemplazar Pods. No guarda automáticamente sus datos.

**4. ¿Por qué usar Service si el Pod tiene IP?** La IP del Pod puede cambiar. El
Service aporta un punto de acceso y selecciona Pods mediante etiquetas.

**5. ¿Qué hace un Namespace?** Agrupa y delimita recursos. No equivale por sí solo
a una barrera de red o a un clúster independiente.

**6. ¿Qué sucede con la imagen cargada?** Se valida, se decodifica, se corrige la
orientación EXIF, se convierte a RGB y se transforma según los pesos del modelo.
El tensor pasa por MobileNetV3 y softmax; se devuelven las cinco clases con mayor
puntuación. La imagen no se guarda en disco.

**7. ¿Entrenaron el modelo?** No. Se despliega un modelo preentrenado de TorchVision.
El aporte consiste en la aplicación, empaquetado, despliegue, pruebas y operación.

**8. ¿Por qué no usaron el ejemplo exactamente?** El documento lo presenta como
sugerencia. Se eligió una alternativa con dependencias fijadas y pesos incluidos
en la imagen. Cambian biblioteca y conjunto de etiquetas: ImageNet tiene 1.000
clases, mientras el ejemplo CIFAR-10 tiene diez. No son resultados equivalentes.

**9. ¿Un 90 % implica 90 % de certeza real?** No. Es el valor softmax relativo a
las clases conocidas. Puede ser alto incluso para una imagen fuera del dominio.

**10. ¿Readiness, liveness y startup son iguales?** Startup protege el inicio lento;
readiness decide si el Pod está listo para recibir tráfico; liveness permite
reiniciar un contenedor que dejó de responder. Una readiness fallida no debe
interpretarse automáticamente como reinicio.

**11. ¿Requests y limits?** Requests se usan para asignar recursos y, en CPU,
para calcular utilización del HPA. Limits acotan consumo: CPU puede sufrir
throttling y memoria puede terminar en OOMKilled.

**12. ¿Por qué el clasificador tiene dos réplicas?** No guarda estado y puede
replicarse. La distribución por nodos es una preferencia con `ScheduleAnyway`;
debe comprobarse, no asumirse como garantía de alta disponibilidad.

**13. ¿Por qué Planner tiene una sola réplica?** Usa SQLite sobre un volumen
ReadWriteOnce y estrategia Recreate. No está diseñado para múltiples escritores
en distintos Pods. Para escalarlo migraríamos a una base compartida apropiada,
como PostgreSQL, y diseñaríamos sus conexiones y migraciones.

**14. ¿ReadWriteOnce significa exactamente un Pod?** Significa montaje de escritura
desde un nodo. No es por sí solo una restricción universal de un único Pod. La
réplica única y la estrategia de este proyecto evitan escritores simultáneos.

**15. ¿El PVC es una copia de seguridad?** No. Mantiene datos fuera del ciclo del
Pod. Eliminar el PVC o los recursos de Azure puede eliminar el disco según su
política. Necesitamos exportaciones o respaldos separados.

**16. ¿Qué diferencia hay entre log y métrica?** El log registra un evento concreto;
la métrica resume una magnitud a lo largo del tiempo. Usamos request_id para
correlacionar una petición y las vistas de Azure para observar consumo.

**17. ¿Por qué HPA no escala?** Revisaría contexto, métricas disponibles, requests,
carga, condiciones del HPA y capacidad del clúster. `<unknown>` no significa 0 %.

**18. ¿Por qué no baja inmediatamente?** Hay muestreo, tolerancia y una ventana de
estabilización que evita oscilaciones rápidas.

**19. ¿HPA crea máquinas?** No. Modifica réplicas de Pods. El autoscaler del clúster
puede modificar nodos, sujeto a límites, cuotas y capacidad.

**20. ¿Por qué borrar AKS?** Los nodos y servicios asociados consumen crédito.
Guardamos configuración, código y evidencias, y recreamos el entorno antes de la
sustentación. Free se refiere al nivel elegido del control plane, no a todo el sistema.

## Cambios en vivo para practicar

Usa primero un entorno de ensayo y explica la predicción antes del comando.
Para los comandos de AKS establece `export KUBECONFIG="$PWD/.kube/aks.config"`.

**Aumentar el clasificador a tres réplicas**

```bash
kubectl -n microproyecto2 scale deployment/classifier --replicas=3
kubectl -n microproyecto2 rollout status deployment/classifier
kubectl -n microproyecto2 get pods -l app=classifier -o wide
kubectl -n microproyecto2 scale deployment/classifier --replicas=2
```

Esto es escalado manual. El HPA se demuestra por separado.

**Reemplazar un Pod sin borrar el Deployment**

```bash
POD=$(kubectl -n microproyecto2 get pod -l app=classifier -o jsonpath='{.items[0].metadata.name}')
kubectl -n microproyecto2 delete pod "$POD"
kubectl -n microproyecto2 get pods -l app=classifier -w
```

El controlador crea un reemplazo. Puede ser necesario reiniciar port-forward si
su Pod seleccionado fue eliminado. No confundas esa caída del túnel con la caída
de todas las réplicas.

**Diagnosticar un problema**

```bash
kubectl -n microproyecto2 get pods
kubectl -n microproyecto2 describe pod NOMBRE_DEL_POD
kubectl -n microproyecto2 logs NOMBRE_DEL_POD
kubectl -n microproyecto2 get events --sort-by=.metadata.creationTimestamp
```

**Cambiar el umbral del HPA local**

```bash
export KUBECONFIG="$PWD/.kube/minikube.config"
kubectl -n mp2-hpa patch hpa cpu-demo --type=json -p '[{"op":"replace","path":"/spec/metrics/0/resource/target/averageUtilization","value":70}]'
# Restaurar al terminar:
kubectl -n mp2-hpa patch hpa cpu-demo --type=json -p '[{"op":"replace","path":"/spec/metrics/0/resource/target/averageUtilization","value":50}]'
```

Un objetivo mayor suele requerir menos réplicas para la misma carga, sin eliminar
los límites y condiciones del controlador.

## Preparación cruzada

Como reparto de estudio sugerido, Miguel prepara Azure y redes; Juan, aplicaciones
y HPA; Natalia, persistencia, monitoreo y evidencias. Después intercambian temas.
Cada persona debe completar el ensayo completo y justificar un cambio sin depender
de las otras. Este reparto no certifica contribuciones realizadas ni cambia la inscripción oficial.

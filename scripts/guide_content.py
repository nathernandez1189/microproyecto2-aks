"""Contenido editorial de la guía. Los resultados se toman del proyecto real."""
AUTHORS = ['JUAN OSPINA TENORIO', 'MIGUEL ANGEL DIUZA', 'NATALIA HERNANDEZ PIEDRAHITA']
PAGES = []
def page(title, subtitle, *blocks):
    PAGES.append(dict(title=title, subtitle=subtitle, blocks=list(blocks)))
def p(text): return ('p', text)
def h(text): return ('h', text)
def note(title, text): return ('note', title, text)
def table(headers, rows, widths): return ('table', headers, rows, widths)
def code(text): return ('code', text)
def ref(text): return ('ref', text)
def diagram(kind): return ('diagram', kind)

page('Guía de ejecución\ndel microproyecto 2',
     'Kubernetes en Azure con clasificación de imágenes, persistencia y monitoreo.',
     ('cover',),
     p('Una guía para <b>entender, ejecutar y justificar</b> el proyecto. Explica la función de cada componente, las decisiones de diseño, las pruebas que debes realizar y las respuestas que debes poder construir con tus propias palabras.'),
     note('Estado de esta edición · 14 de septiembre de 2026',
          '<b>AKS comprobado:</b> dos nodos, 12 pruebas HTTP, persistencia y monitoreo reales. HPA local repitió el ciclo 1 a 4 a 1. Tras el ensayo del 14 de septiembre se detuvo AKS conservando el disco; Minikube y Docker también quedaron detenidos.'),
     p('<b>Equipo:</b> los tres integrantes de esta portada fueron confirmados para la entrega. La sustentación es individual; cada persona debe comprender el proyecto completo y verificar su horario en la plataforma del curso.'),
     ref('Universidad Autónoma de Occidente · Computación en la Nube · Material de preparación y documentación técnica.'))

page('Cómo usar esta guía', 'Primero comprende la idea; después ejecuta y reúne evidencia.',
     p('Cada sección combina <b>qué se hace, por qué se hace y cómo comprobarlo</b>. Los comandos son instrucciones para ejecutar desde la carpeta del proyecto. Un comando escrito en este documento no demuestra que ya se haya ejecutado.'),
     table(['Ruta de lectura', 'Páginas', 'Qué podrás explicar'], [
         ['Comprender el proyecto', '3 a 6', 'Problema, objetivos, rúbrica, arquitectura y conceptos.'],
         ['Justificar las aplicaciones', '7 a 12', 'Modelo, API, base de datos, contenedores y Kubernetes.'],
         ['Ejecutar de forma ordenada', '13 a 17', 'Pruebas locales, Azure, conexión y despliegue.'],
         ['Observar y comprobar', '18 a 21', 'Monitoreo, consultas, HPA y resultados reales.'],
         ['Operar y sustentar', '22 a 27', 'Costos, errores, guion, preguntas y cambios en vivo.'],
         ['Entregar y cerrar', '28 a 30', 'Evidencias, conclusiones, límites y fuentes.']], [48,24,98]),
     h('Tres estados que debes distinguir'),
     p('<b>Implementado:</b> existe código o configuración. <b>Comprobado:</b> una prueba real produjo el resultado registrado. <b>Pendiente:</b> falta ejecutar o verificar en el entorno requerido. Por ejemplo, una aplicación implementada y probada en Docker todavía puede estar pendiente de demostración en AKS.'),
     h('Dónde está el material'),
     code('apps/          Aplicaciones y contenedores\nk8s/           Manifiestos, ajuste AKS y laboratorio HPA\nscripts/       Pasos de ejecución y recolección de evidencia\nmonitoring/    Configuración de registros y consultas KQL\ntests/         Pruebas HTTP e imagen de demostración\ndocs/          Guías y decisiones\nevidencias/    Resultados locales y pruebas reales de Azure'),
     note('Regla práctica', 'No avances porque una pantalla se vea bien. Avanza cuando puedas explicar el resultado y repetir la comprobación. Conserva el entorno, el momento, la acción y el resultado de cada evidencia.'))

page('Problema, propósito y objetivos', 'El proyecto estudia cómo operar aplicaciones, además de hacerlas funcionar.',
     h('El problema que se aborda'),
     p('Una aplicación puede funcionar en un computador y fallar al trasladarse a otro por diferencias de dependencias, configuración o almacenamiento. Además, al reiniciar un contenedor pueden perderse datos si se guardan únicamente dentro de él. Cuando surge un error, hace falta saber qué ocurrió y en qué componente.'),
     p('El microproyecto usa dos aplicaciones complementarias para estudiar estos problemas: una procesa imágenes sin conservar archivos; la otra guarda tareas académicas. Ambas se empaquetan en contenedores y se preparan para ejecutarse en Kubernetes administrado por Azure.'),
     h('Objetivo general'),
     p('<b>Implementar y demostrar un entorno de laboratorio en AKS</b> con al menos dos nodos, un clasificador de imágenes, una aplicación con persistencia y monitoreo, justificando sus decisiones de despliegue y operación.'),
     table(['Objetivo específico', 'Cómo se verifica'], [
         ['Reproducir la ejecución', 'Construir las imágenes y ejecutar las mismas pruebas HTTP.'],
         ['Administrar las cargas con Kubernetes', 'Mostrar Deployments, Pods, Services y nodos Ready.'],
         ['Conservar los datos del tablero', 'Reemplazar el Pod y recuperar la misma tarea desde el PVC.'],
         ['Relacionar uso y comportamiento', 'Encontrar peticiones y consumo en Azure Monitor.'],
         ['Entender el escalado automático', 'Observar HPA local aumentar y reducir réplicas.']], [76,94]),
     h('Por qué estas dos aplicaciones'),
     p('Visión AI representa una carga de cálculo: recibe una imagen y devuelve predicciones. Campus Planner representa una carga con estado: crea, consulta, actualiza y elimina información. La diferencia permite justificar por qué el clasificador se replica y el tablero conserva una sola réplica.'),
     note('Explicación sencilla para sustentar', '“Elegimos dos aplicaciones con necesidades distintas para demostrar que Kubernetes no se configura igual para una tarea de cálculo que para una aplicación que debe conservar datos”.'))

page('Qué exige y cómo se cumple', 'La evidencia debe responder directamente a cada punto del enunciado.',
     table(['Criterio', 'Valor', 'Implementación y prueba necesaria'], [
         ['Clúster AKS', '1,0', 'Creación por Azure Portal, mínimo dos nodos y verificación desde Cloud Shell y CLI local.'],
         ['Clasificador', '1,0', 'Visión AI debe procesar una fotografía dentro de un Pod de AKS.'],
         ['Aplicación de interés', '1,0', 'Campus Planner debe funcionar en AKS; la persistencia añade una demostración técnica verificable.'],
         ['Monitoreo', '1,0', 'Usar servicios de Azure para mostrar consumo y registros de las aplicaciones.'],
         ['Pregunta individual', '1,0', 'Cada persona explica conceptos, decisiones y cambios solicitados.'],
         ['Extra elegido: HPA', '+0,5', 'Aumento y reducción automáticos de Pods. El enunciado permite hacerlo localmente.']], [39,15,116]),
     p('Los valores se transcriben del documento de la asignatura. El profesor define la calificación y cómo aplica el extra. Se eligió <b>HPA</b>; no se presenta Kubeflow como una funcionalidad implementada.'),
     h('Qué procede del enunciado'),
     p('AKS por portal, dos nodos, clasificador, segunda aplicación, monitoreo, verificación desde dos entornos y sustentación individual. El ejemplo de clasificación con MXNet se presenta como una sugerencia, no como una biblioteca obligatoria.'),
     h('Qué se añadió al diseño'),
     p('Pruebas automatizadas, validación de entradas, registros estructurados, sondas de salud, límites de recursos, un volumen persistente y guías de diagnóstico. Estas mejoras permiten explicar el comportamiento con evidencia; no reemplazan ninguno de los puntos de Azure.'),
     note('No confundir', 'Dos réplicas del clasificador son dos Pods, no dos nodos. Dos terminales locales tampoco equivalen a verificar desde Cloud Shell y desde el computador.'),
     ref('Fuente del alcance: documento adjunto “2025-03 Microproyecto2.doc” y anuncio del curso compartido por la usuaria.'))

page('Arquitectura del proyecto', 'Una vista lógica del entorno desplegado y comprobado en Azure.',
     diagram('architecture'),
     p('<b>Recorrido de una solicitud:</b> el navegador accede a un puerto local; kubectl abre un túnel autenticado hacia un Pod seleccionado a partir de su Service. La aplicación procesa la petición y devuelve una respuesta. El tablero consulta su base de datos en el volumen persistente.'),
     p('<b>Recorrido de una imagen de contenedor:</b> el código se construye y se publica en Azure Container Registry. Los nodos descargan esa imagen para iniciar los contenedores. ACR almacena las imágenes; no ejecuta las aplicaciones.'),
     p('<b>Recorrido de la observación:</b> las aplicaciones escriben eventos JSON en stdout. El agente de monitoreo los recopila; Log Analytics permite buscarlos con KQL. Las vistas de Azure complementan esos eventos con información del clúster.'),
     note('Alcance del dibujo', 'Los dos nodos son la capacidad del clúster. La ubicación de cada Pod debe comprobarse con get pods -o wide. La distribución del clasificador es preferente, no una garantía. El túnel port-forward selecciona un Pod y no demuestra balanceo entre las dos réplicas.'),
     ref('Diseño propio basado en k8s/base, scripts/02 a 05 y monitoring/. Despliegue real comprobado el 9 de septiembre de 2026.'))

page('Kubernetes explicado sin enredos', 'Relaciona cada concepto con un objeto concreto de este proyecto.',
     table(['Concepto', 'Qué significa aquí'], [
         ['Imagen y contenedor', 'La imagen es el paquete de aplicación y dependencias. El contenedor es una ejecución de ese paquete.'],
         ['Nodo', 'Máquina que aporta CPU y memoria y ejecuta Pods. El proyecto requiere al menos dos en AKS.'],
         ['Pod', 'Unidad de ejecución programada sobre un nodo. Aquí contiene un contenedor de una aplicación.'],
         ['Deployment', 'Declara qué imagen usar y cuántas réplicas mantener. Su controlador crea o reemplaza Pods.'],
         ['Service', 'Nombre y acceso interno estable que selecciona Pods por etiquetas, como app=classifier.'],
         ['Namespace', 'Agrupación lógica. Las aplicaciones usan microproyecto2; el laboratorio HPA usa mp2-hpa.'],
         ['PVC y volumen', 'El PVC solicita almacenamiento. El volumen asociado conserva el archivo de tareas fuera del Pod.'],
         ['Control plane', 'Coordina el estado deseado. En AKS lo administra Azure; el equipo configura sus cargas.']], [38,132]),
     h('Ejemplo: se elimina un Pod del clasificador'),
     p('El Deployment sigue declarando dos réplicas. Su controlador detecta que falta una y crea un reemplazo. El nuevo Pod tendrá otro nombre o identificador. La imagen y el Deployment no desaparecen porque se elimine una ejecución.'),
     h('Responsabilidad compartida'),
     p('Azure administra el servicio de Kubernetes, pero eso no escribe la aplicación, valida las fotografías ni diseña la persistencia. El equipo sigue siendo responsable de sus imágenes, permisos, configuración, pruebas y consumo de recursos.'),
     note('Frase que ayuda', '“Kubernetes compara lo que declaramos con lo que está ejecutándose e intenta corregir la diferencia. Declarar el estado deseado no elimina la necesidad de observar si pudo cumplirlo”.'),
     ref('Base conceptual: [S1] Deployments; aplicación concreta: k8s/base/classifier.yaml y planner.yaml.'))

page('Visión AI: qué hace y por qué', 'Clasificación real de imágenes con un modelo preentrenado.',
     h('La necesidad y la elección'),
     p('Visión AI recibe una fotografía y muestra cinco etiquetas ordenadas por puntuación. Se eligió MobileNetV3 Small para una demostración de inferencia en CPU, sin añadir una GPU al laboratorio. Esta es una decisión de alcance; no se ha medido una comparación de rendimiento entre varios modelos.'),
     p('La implementación fija PyTorch 2.8.0 y TorchVision 0.23.0 y carga los pesos IMAGENET1K_V1. Trabaja con <b>1.000 categorías ImageNet, en inglés</b>. El ejemplo sugerido en el enunciado usa MXNet y diez categorías CIFAR-10: sus etiquetas y resultados no son equivalentes. [S3]'),
     table(['Paso', 'Qué ocurre en el código'], [
         ['1. Recibir y validar', 'El campo multipart debe llamarse img. Se comprueba el archivo decodificado, formato, tamaño de petición y píxeles.'],
         ['2. Preparar', 'Se corrige orientación EXIF, se convierte a RGB y se aplican las transformaciones asociadas a los pesos.'],
         ['3. Inferir', 'El tensor entra al modelo en modo de evaluación y sin cálculo de gradientes. No se modifica el modelo.'],
         ['4. Ordenar', 'Softmax produce puntuaciones relativas; topk selecciona las cinco mayores.'],
         ['5. Responder', 'La API devuelve etiquetas, puntuaciones, tiempo medido, dimensiones y nombre del Pod.']], [40,130]),
     h('Por qué el modelo se incluye al construir la imagen'),
     p('Los pesos se descargan durante el build de Docker. El contenedor usa la copia incluida, por lo que cada inicio no depende de volver a descargar el modelo. Un bloqueo protege la inferencia y Torch usa un hilo de CPU para hacer más predecible el consumo del laboratorio.'),
     note('Cómo justificarlo', '“Nuestro trabajo integra y despliega un modelo preentrenado. Demostramos el servicio HTTP, el contenedor y su operación en Kubernetes; no afirmamos haber entrenado la red desde cero”.'),
     ref('Archivos: apps/classifier/app.py, download_model.py y Dockerfile. Fuente del modelo: [S3].'))

page('Cómo comprobar el clasificador', 'Una predicción visible debe poder relacionarse con su API y su Pod.',
     p('Abre http://localhost:8081 con el entorno correspondiente en ejecución. Usa primero tests/fixtures/dog.jpg y después imágenes adicionales. Para evitar el límite de petición, prepara archivos JPEG, PNG o WebP de menos de 4 MB; el límite total configurado es 5 MB, incluido el contenido multipart.'),
     code('curl --fail -F img=@tests/fixtures/dog.jpg \\\n  http://localhost:8081/predict'),
     table(['Dato', 'Resultado local guardado', 'Qué significa'], [
         ['Primera etiqueta', 'Samoyed', 'Predicción para esta imagen de prueba.'],
         ['Puntuación', '0,757887 ≈ 75,79 %', 'Puntuación softmax, no certeza universal.'],
         ['Medida de tiempo', '13,15 ms', 'Una observación local; no es rendimiento de AKS.'],
         ['Dimensiones', '1546 × 1213', 'Tamaño de la imagen después de corregir orientación.']], [35,58,77]),
     p('La lista completa local fue Samoyed, Arctic fox, Pomeranian, wallaby y Great Pyrenees. El archivo evidencias/local/08-prediccion-real.json conserva la respuesta. No copies su nombre de contenedor como si fuera un Pod de Azure.'),
     h('Prueba de error controlado'),
     code('curl -i -X POST http://localhost:8081/predict\ncurl --fail http://localhost:8081/readyz'),
     p('La primera petición debe responder 400 por falta de imagen; la segunda debe seguir respondiendo 200. Así demuestras que una entrada incorrecta se rechaza sin hacer caer el servicio. Un archivo de un formato no admitido puede producir 415; una petición demasiado grande, 413.'),
     h('Interpretación honesta del resultado'),
     p('Una sola foto acertada demuestra funcionamiento, no precisión global. El modelo puede equivocarse, especialmente con dibujos, documentos o categorías fuera de su dominio. El valor inference_ms incluye transformaciones y espera del bloqueo; no incluye toda la comunicación del navegador.'),
     note('Evidencia de AKS obtenida', 'La respuesta 04-inferencia.json registra Samoyed con puntuación 0,757887 y 19,52 ms de inferencia en classifier-74999b7f6-whkqc. Los recursos y las capturas se conservan en evidencias/azure/. Es una observación, no una medición de precisión global.'))

page('Campus Planner: aplicación con datos', 'Un tablero académico permite demostrar operaciones y persistencia.',
     h('Qué resuelve'),
     p('El tablero organiza actividades por título, asignatura y estado. Se puede crear una tarea, verla en la lista, pasarla a en curso o completada y eliminarla. Los contadores de la interfaz se calculan con las tareas obtenidas de la API.'),
     table(['Acción', 'Ruta HTTP', 'Respuesta esperada'], [
         ['Consultar', 'GET /api/tasks', '200 con lista tasks.'],
         ['Crear', 'POST /api/tasks', '201 con la tarea y su id.'],
         ['Cambiar estado', 'PATCH /api/tasks/{id}', '200 con el nuevo estado.'],
         ['Eliminar', 'DELETE /api/tasks/{id}', '204 sin cuerpo.'],
         ['Comprobar disponibilidad', 'GET /readyz', '200 si una consulta a SQLite funciona.']], [35,76,59]),
     h('Cómo se guarda la información'),
     p('La tabla tasks tiene id, title, course, status y created_at. El archivo se almacena en /data/planner.db; /data se monta desde un volumen. SQLite simplifica el laboratorio porque no exige administrar un servidor de base de datos separado.'),
     p('Las consultas usan parámetros para tratar las entradas como datos. El código valida títulos de 1 a 120 caracteres y asignaturas de 1 a 60. Los estados admitidos son pendiente, en-curso y completada. Un id inexistente produce 404; una entrada inválida, 400.'),
     h('Por qué una réplica y estrategia Recreate'),
     p('La aplicación no se diseñó para múltiples escritores distribuidos. Recreate termina la ejecución anterior antes de iniciar la nueva; una réplica reduce problemas de concurrencia con el archivo SQLite. A cambio, puede haber una interrupción breve al actualizar o reemplazar el Pod.'),
     note('Límite del alcance', 'Es un tablero compartido de laboratorio, sin cuentas ni autorización individual. Usa datos de ejemplo. Para múltiples usuarios reales harían falta autenticación, autorización, respaldos y un diseño de base de datos adecuado.'),
     ref('La justificación describe la implementación existente de apps/planner/app.py y k8s/base/planner.yaml.'))

page('Persistencia: demostrar, no asumir', 'La prueba consiste en cambiar el Pod y conservar la misma información.',
     p('En AKS, el PVC planner-data solicita 1 GiB mediante la StorageClass managed-csi. El disco es independiente de la ejecución del Pod. ReadWriteOnce permite escritura desde un nodo; no significa por sí solo que únicamente un Pod pueda acceder. Aquí se complementa con una réplica y Recreate. [S2]'),
     table(['Momento', 'Acción', 'Qué guardar'], [
         ['Antes', 'Crear una tarea y consultar /api/tasks.', 'Identificador, título y estado.'],
         ['Antes', 'Consultar Pod y PVC.', 'UID del Pod y nombre del volumen.'],
         ['Cambio', 'Reiniciar el Deployment de planner.', 'Esperar a que la nueva ejecución esté lista.'],
         ['Después', 'Abrir de nuevo el túnel si se cerró y consultar tareas.', 'Misma tarea, nuevo UID y mismo PVC.']], [23,81,66]),
     code('export KUBECONFIG="$PWD/.kube/aks.config"\nkubectl -n microproyecto2 get pods -l app=planner -o wide\nkubectl -n microproyecto2 get pvc planner-data\ncurl --fail http://localhost:8082/api/tasks\n\nkubectl -n microproyecto2 rollout restart deployment/planner\nkubectl -n microproyecto2 rollout status deployment/planner \\\n  --timeout=300s\nkubectl -n microproyecto2 get pods -l app=planner -o wide'),
     p('Para comparar el UID puedes usar la vista detallada del Pod con kubectl describe pod. Reabre el acceso con scripts/04-open-apps.sh si el túnel quedó asociado al Pod anterior. Después consulta /api/tasks y comprueba el mismo id.'),
     h('Qué prueba y qué no prueba'),
     p('El resultado demuestra persistencia frente al reemplazo del Pod en ese entorno. No demuestra respaldo, recuperación ante pérdida del disco ni alta disponibilidad. Borrar el PVC o el grupo de recursos puede eliminar los datos según la política de recuperación.'),
     note('Frase para sustentar', '“La información sobrevive porque el archivo vive en un volumen independiente del Pod. Si borramos el volumen, esa protección deja de existir; por eso persistencia y respaldo son necesidades diferentes”.'))

page('Contenedores y seguridad del laboratorio', 'Cada medida responde a una necesidad concreta del proyecto.',
     p('Las aplicaciones usan Flask para las rutas HTTP y Gunicorn como servidor de ejecución del contenedor. El Dockerfile describe la imagen; Docker Compose permite probarla localmente. Kubernetes usará imágenes publicadas con la arquitectura de CPU de sus nodos.'),
     table(['Decisión implementada', 'Razón y límite'], [
         ['Usuario UID 10001', 'La aplicación no necesita ejecutarse como root. Reduce privilegios dentro del contenedor.'],
         ['Archivos de solo lectura', 'La aplicación escribe únicamente donde lo necesita: /tmp y /data en el tablero.'],
         ['Sin elevación y sin capabilities', 'Se evita dar capacidades del sistema que las rutas HTTP no requieren.'],
         ['Sin token de ServiceAccount', 'Las aplicaciones no llaman a la API de Kubernetes; no necesitan ese token montado.'],
         ['Entradas validadas', 'Se rechazan imágenes o tareas inválidas antes de continuar el procesamiento.'],
         ['Services ClusterIP y túnel local', 'La demostración no publica directamente las aplicaciones en Internet.'],
         ['Registros con identificadores', 'Permiten investigar peticiones sin guardar fotografías ni títulos de tareas en los logs de aplicación.']], [59,111]),
     h('Reproducción y versiones'),
     p('Las versiones principales de la aplicación están fijadas. Algunas dependencias transitivas y la imagen base pueden cambiar: eso limita una reproducción idéntica en el futuro. Guardar digests, hashes y el inventario de versiones daría mayor precisión a una entrega posterior.'),
     h('Qué queda fuera'),
     p('No se configuraron un dominio público, TLS externo, inicio de sesión para usuarios ni límites de peticiones por persona. Los controles del contenedor mejoran el laboratorio, pero no convierten el tablero en un producto listo para publicación pública.'),
     note('Arquitecturas diferentes', 'Las pruebas locales se hicieron en Apple Silicon con imágenes ARM64. Los nodos DS2 v2 requieren linux/amd64. El flujo de publicación prepara esa arquitectura; su ejecución en AKS se comprobó y se repitió el 14 de septiembre.'))

page('Manifiestos: recursos, salud y réplicas', 'Estos valores explican cómo Kubernetes debe ejecutar las aplicaciones.',
     table(['Aplicación', 'Réplicas', 'Requests por Pod', 'Limits por Pod'], [
         ['Clasificador', '2', '250m CPU / 384Mi', '1 CPU / 1Gi'],
         ['Planner', '1', '100m CPU / 64Mi', '500m CPU / 256Mi'],
         ['CPU demo local', '1 a 4', '100m CPU / 64Mi', '500m CPU / 128Mi']], [37,24,55,54]),
     p('1000m equivalen a un núcleo. Los requests de las aplicaciones suman <b>600m y 832Mi</b> con la configuración base: 2 × 250m + 100m y 2 × 384Mi + 64Mi. A eso se añaden Kubernetes, monitoreo y otros procesos. El total de recursos de las máquinas no queda íntegramente disponible para las aplicaciones.'),
     p('Los requests ayudan al planificador a ubicar los Pods. Los limits acotan consumo; alcanzar el límite de CPU puede producir throttling y superar el de memoria puede terminar el contenedor. Los valores elegidos son iniciales y deben contrastarse con observaciones en AKS.'),
     table(['Sonda', 'Pregunta que responde', 'Uso en el proyecto'], [
         ['startup', '¿Terminó de iniciar?', 'Da tiempo al modelo y a la base antes de las demás comprobaciones.'],
         ['readiness', '¿Puede recibir tráfico?', '/readyz comprueba disponibilidad; en Planner consulta SQLite.'],
         ['liveness', '¿Sigue respondiendo?', '/healthz permite detectar falta de respuesta y reiniciar si corresponde.']], [28,55,87]),
     h('Leer un fragmento de YAML'),
     code('spec:\n  replicas: 2\n  selector:\n    matchLabels: {app: classifier}\n  template:\n    metadata:\n      labels: {app: classifier}'),
     p('replicas declara cuántas ejecuciones mantener. Las etiquetas relacionan el Deployment con sus Pods y el Service con sus destinos. Cambiar una etiqueta sin adaptar el selector puede dejar un Service sin destinos.'),
     ref('Sondas: [S4]. Valores exactos: k8s/base/classifier.yaml, planner.yaml y k8s/hpa/demo.yaml.'))

page('Ejecutar primero en el computador', 'Esta etapa detecta errores de aplicación antes de consumir crédito de Azure.',
     h('1. Preparar la terminal'),
     p('Abre Docker Desktop y una terminal dentro de microproyecto2-aks. Debes ver compose.yaml al listar la carpeta. Las pruebas HTTP usan Python 3 y no requieren instalar PyTorch en el computador: el modelo vive dentro del contenedor.'),
     code('docker compose up -d --build --wait\ndocker compose ps\npython3 -m unittest discover -s tests -v'),
     p('<b>Qué hace:</b> construye las imágenes, inicia ambos servicios y espera sus comprobaciones de salud. <b>Qué esperar:</b> dos servicios saludables y las 12 pruebas aprobadas. La primera construcción descarga dependencias y pesos; puede tardar más que los siguientes inicios.'),
     h('2. Recorrer las interfaces'),
     p('Abre <b>http://localhost:8081</b> para Visión AI y <b>http://localhost:8082</b> para Campus Planner. Procesa la imagen de prueba; crea una actividad, cambia su estado y recarga el tablero. Explica qué llamada a la API respalda cada acción.'),
     h('3. Probar persistencia local'),
     code('curl --fail http://localhost:8082/api/tasks\ndocker compose up -d --force-recreate planner\ncurl --fail http://localhost:8082/api/tasks'),
     p('Espera a que Planner vuelva a estar saludable antes de la segunda consulta. La misma tarea debe permanecer en el volumen de Docker. Esta prueba es local; debe repetirse posteriormente con el PVC de AKS.'),
     h('4. Cerrar o reabrir sin borrar tareas'),
     code('docker compose stop\n# Para continuar otra sesión:\ndocker compose up -d --wait'),
     note('Cuidado con los puertos y los datos', 'Antes de abrir túneles a AKS, detén Compose para liberar 8081 y 8082. docker compose down conserva el volumen; añadir -v lo elimina. No uses esa opción para una simple pausa.'),
     ref('Opcional: scripts/10-test-kubernetes-local.sh ensaya los manifiestos en Minikube; tampoco sustituye la evidencia de AKS.'))

page('Azure: estado de la cuenta y cuotas', 'Lo observado en esta suscripción determina la configuración viable.',
     table(['Comprobación del 9 de septiembre de 2026', 'Resultado registrado'], [
         ['Suscripción', 'Azure for Students activa.'],
         ['Crédito mostrado', 'USD 100 antes de crear recursos; vence el 9 de septiembre de 2027. El saldo posterior debe consultarse.'],
         ['Acceso desde el computador', 'Azure CLI 2.90.0 instalada e inicio de sesión completado.'],
         ['Proveedores', 'Compute, ContainerService, Network, ContainerRegistry, OperationalInsights e Insights registrados.'],
         ['Regiones permitidas por política', 'Chile Central, Brazil South, North Central US, Canada Central y West US.'],
         ['Opción encontrada', 'Chile Central, Standard_DS2_v2, cuota de familia 4 vCPU y regional 6 vCPU.']], [82,88]),
     h('Por qué no basta escoger una región conocida'),
     p('Son comprobaciones distintas: la política permite una región; la cuota limita cuántos recursos admite la suscripción; la disponibilidad indica si un tamaño se ofrece para esa cuenta. Aun con esas condiciones, el aprovisionamiento real puede fallar por capacidad del momento.'),
     p('En North Central US aparecían tamaños modernos disponibles, pero su familia tenía cuota cero. La solicitud automática de ampliar DASv5 a 6 vCPU fue rechazada. La revisión de las cinco regiones encontró DS2 v2 con cuota en Chile Central. Esta búsqueda justifica la región elegida.'),
     h('Configuración local del proyecto'),
     p('El archivo .env ya fue preparado en este computador; consérvalo. Contiene los nombres y la suscripción, no contraseñas. En una copia nueva, crea .env a partir de .env.example y completa tus valores. Las sesiones de Azure están aisladas en .azure/ y quedan fuera del paquete para compartir.'),
     code('bash scripts/00-check-azure.sh'),
     note('Estado exacto', 'AKS fue creado por Azure Portal. Se comprobaron dos nodos Ready, Kubernetes 1.35.7 y ambas aplicaciones en Chile Central. La conexión local y la sesión real de Cloud Shell están documentadas en evidencias/azure/.'),
     ref('Evidencia de preparación: evidencias/azure/00-preparacion-portal.md. El PDF de activación adjunto es histórico; la cuenta ya está activa.'))

page('Crear AKS desde Azure Portal', 'El portal es parte del requisito del curso y debe quedar evidenciado.',
     p('En Azure Portal busca Kubernetes services, inicia la creación de un clúster y configura el laboratorio. Si retomas el formulario preparado, verifica sus valores antes de continuar. Si lo reconstruyes, usa esta ficha; los nombres de las opciones pueden cambiar. [S5]'),
     table(['Campo', 'Configuración preparada', 'Justificación'], [
         ['Nombre y grupo', 'aks-microproyecto2 / rg-microproyecto2', 'Identificación y limpieza de recursos exclusivos.'],
         ['Región', 'Chile Central', 'Disponibilidad y cuota observadas para esta cuenta.'],
         ['Preset y plan', 'Dev/Test / Free', 'Laboratorio; Free no elimina el costo de las máquinas.'],
         ['Versión', '1.35.7 ofrecida por el portal', 'Volver a comprobar compatibilidad al recrear.'],
         ['Grupo de nodos', 'System, Ubuntu, DS2 v2', 'Opción que pasó la validación del formulario.'],
         ['Cantidad y zonas', '2, manual, sin zonas', 'Cumple el mínimo y mantiene fijo el número de nodos.'],
         ['Red', 'Azure CNI Overlay y LB Standard', 'Configuración preparada para conectividad del laboratorio.'],
         ['Acceso e identidad', 'Identidad administrada y RBAC de Kubernetes', 'Permisos para administrar y consumir las imágenes.'],
         ['Registros', 'Activar después con script 05', 'Usar un workspace dentro del grupo exclusivo.']], [30,69,71]),
     p('El grupo de infraestructura preparado es MC_rg-microproyecto2_aks-microproyecto2_chilecentral. Evita agregar grupos de nodos o servicios opcionales por accidente. Al editar, vuelve a verificar que el resumen conserve <b>dos nodos</b> y el tamaño esperado.'),
     h('Validación no es creación'),
     p('Guarda la configuración en Revisar y crear. Solo después de aceptar el consumo previsto, crea el recurso, espera Provisioning state: Succeeded y verifica los nodos. Una validación favorable no prueba que las máquinas ya existan.'),
     note('Cuota y actualizaciones', 'La documentación general y el preset muestran requisitos diferentes; se conserva la validación observada sin afirmar equivalencia universal. Dos DS2 v2 consumen la cuota de familia. El grupo System exige maxUnavailable=0; un nodo temporal de actualización requeriría más cuota. [S6]'))

page('Conectar desde dos entornos', 'Cloud Shell y la terminal local deben mostrar el mismo clúster real.',
     h('En el computador'),
     p('Después de que AKS termine de crearse, ejecuta el script de conexión desde la carpeta del proyecto. Reutiliza la sesión local de Azure y descarga la configuración en .kube/aks.config para no mezclarla con otros contextos.'),
     code('bash scripts/01-connect.sh cli-local\nexport KUBECONFIG="$PWD/.kube/aks.config"\nkubectl config current-context\nkubectl get nodes -o wide'),
     p('El script guarda evidencias/azure/01-nodos-cli-local.txt y comprueba que existan al menos dos nodos con condición Ready=True. Si solo hay uno o alguno no está listo, no da el requisito por cumplido.'),
     h('En Cloud Shell Bash'),
     p('Abre Cloud Shell desde Azure Portal. Utiliza una copia del proyecto obtenida del repositorio publicado o cargando el paquete. Completa allí su .env con la misma suscripción y nombres. No copies las carpetas de credenciales del computador; Cloud Shell usa su propio acceso.'),
     code('cd microproyecto2-aks\nbash scripts/01-connect.sh cloud-shell\nexport KUBECONFIG="$PWD/.kube/aks.config"\nkubectl get nodes -o wide'),
     p('Guarda 01-nodos-cloud-shell.txt y una captura donde sea visible que la terminal pertenece al portal. Compara el nombre del clúster y los nodos con la salida local. El argumento cloud-shell solo etiqueta el archivo: debes ejecutarlo realmente desde ese entorno.'),
     table(['Observación', 'Interpretación'], [
         ['Ready en dos nodos', 'El plano de control reconoce dos nodos listos.'],
         ['Mismos nodos desde ambos lugares', 'Se administró el mismo clúster por dos entornos de acceso.'],
         ['kubectl responde', 'El contexto, la autenticación y la conectividad permiten la consulta.']], [64,106]),
     note('Contextos separados', 'AKS usa .kube/aks.config. El extra local usa .kube/minikube.config. Antes de un cambio, confirma el contexto. Cambiar una variable en una terminal no la cambia automáticamente en las demás.'),
     ref('Conexión documentada por Microsoft: [S5]. Comportamiento exacto de la comprobación: scripts/01-connect.sh.'))

page('Publicar imágenes y desplegar', 'Construir, almacenar y ejecutar son pasos diferentes.',
     h('1. Publicar en Azure Container Registry'),
     code('bash scripts/02-publish-images.sh'),
     p('El script crea ACR Basic en el grupo exclusivo si no existe, con usuario administrador desactivado y permisos RBAC. Asocia el registro a AKS y construye mp2-classifier:v1 y mp2-planner:v1 para linux/amd64. El registro preparado tiene un nombre único guardado en .env.'),
     p('La identidad de kubelet debe poder descargar las imágenes mediante AcrPull en este modo. Si el registro utiliza ABAC, el flujo y el rol cambian; el script se detiene para evitar aplicar la configuración equivocada. [S7]'),
     h('2. Preparar y aplicar los manifiestos'),
     code('bash scripts/03-deploy.sh'),
     p('El ajuste de AKS selecciona managed-csi para el PVC. El script reemplaza los nombres de imagen por las rutas del registro, crea el namespace, solicita una validación al servidor, aplica los recursos y espera los Deployments. Consulta después Pods, Services y PVC.'),
     h('3. Abrir el acceso y comprobar'),
     code('docker compose stop\nbash scripts/04-open-apps.sh\n# Deja esa terminal abierta; en otra terminal:\npython3 -m unittest discover -s tests -v'),
     p('El script abre 8081 para el clasificador y 8082 para el tablero, vinculados a 127.0.0.1. Aunque el navegador muestre localhost, las respuestas proceden de AKS si los túneles apuntan a su contexto. Corrobóralo con el Pod devuelto y los logs; la URL sola no identifica el entorno.'),
     h('Si ACR Tasks está restringido'),
     p('ACR Tasks rechazó la construcción en Chile Central. Se construyeron y publicaron ambas imágenes con buildx local para linux/amd64. El script 02 selecciona ahora esa ruta automáticamente en Chile. ACR almacena las imágenes y los nodos AKS las ejecutan.'),
     note('Cambios posteriores', 'Usa una nueva etiqueta, por ejemplo v2, al publicar una revisión. Con IfNotPresent, reutilizar v1 puede conservar una imagen anterior en los nodos. Guarda qué versión produjo cada evidencia.'),
     ref('Scripts 02, 03 y 04; k8s/overlays/aks; integración oficial ACR-AKS: [S7].'))

page('Monitoreo: qué observar y por qué', 'Una aplicación que responde también debe poder investigarse.',
     h('Tres fuentes complementarias'),
     table(['Fuente', 'Qué responde', 'Uso en la demostración'], [
         ['Estado de Kubernetes', '¿Está ejecutándose y disponible?', 'Pods, Deployments, eventos y reinicios.'],
         ['Métricas', '¿Cuánto consume o tarda?', 'CPU, memoria, número de peticiones y duración.'],
         ['Registros', '¿Qué petición o evento ocurrió?', 'Ruta, código HTTP, duración, request_id y Pod.']], [37,59,74]),
     h('Activar el servicio de Azure'),
     code('bash scripts/05-monitoring.sh'),
     p('Log Analytics y Container Insights están habilitados con intervalo de un minuto, filtro microproyecto2 y retención de 30 días. Se añadió streams al archivo para Azure CLI 2.90. La consulta devolvió 11 solicitudes reales en la primera verificación con datos. [S8]'),
     h('Demostración ordenada'),
     p('<b>1.</b> Abre AKS → Monitoring → Insights y elige el intervalo de la prueba. <b>2.</b> Procesa varias imágenes y crea una tarea. <b>3.</b> Envía una petición sin imagen para obtener un 400. <b>4.</b> Consulta Logs en el workspace correcto y relaciona una petición con su Pod. <b>5.</b> Explica el comportamiento observado, incluso si un pico breve no es visible por la agregación.'),
     code('curl -i -X POST http://localhost:8081/predict\nexport KUBECONFIG="$PWD/.kube/aks.config"\nkubectl top nodes\nkubectl -n microproyecto2 top pods'),
     h('Lo que no se recopila automáticamente'),
     p('Las aplicaciones exponen /metrics en formato Prometheus, pero la configuración actual no despliega Prometheus administrado ni un recolector para ese endpoint. No afirmes que sus contadores ya están en Azure. Las evidencias principales usan Container Insights y ContainerLogV2.'),
     note('Cómo interpretar un error', 'Un 400 por imagen ausente indica validación de una petición incorrecta, no caída del clúster. Un 5xx requiere investigar la aplicación. Un Pod reiniciado necesita correlacionar eventos y registros, no solo mirar el código HTTP.'))

page('KQL: convertir logs en explicación', 'Ejecuta cada consulta por separado dentro del workspace de Log Analytics.',
     h('Encontrar solicitudes de las aplicaciones'),
     code('ContainerLogV2\n| where TimeGenerated > ago(1h)\n| where PodNamespace == "microproyecto2"\n| extend e = parse_json(tostring(LogMessage))\n| where tostring(e.event) == "http_request"\n| project TimeGenerated, PodName, path=tostring(e.path),\n          status=toint(e.status),\n          duration_ms=todouble(e.duration_ms),\n          request_id=tostring(e.request_id)\n| order by TimeGenerated desc'),
     p('<b>where</b> filtra por tiempo, namespace y tipo de evento. <b>extend</b> interpreta el texto JSON. <b>project</b> elige las columnas de interés. <b>order by</b> muestra primero los registros recientes. Los nombres de campos corresponden a apps/common/observability.py.'),
     h('Qué debes explicar de una fila'),
     p('Identifica la ruta /predict, el código de respuesta, el Pod que atendió la solicitud y su duración. La cabecera X-Request-ID permite relacionar una respuesta HTTP con un evento de aplicación. Los logs omiten las comprobaciones de salud para reducir ruido.'),
     table(['Medida o situación', 'Lectura correcta'], [
         ['duration_ms', 'Duración medida en el servidor; no equivale a todo el tiempo del navegador.'],
         ['p95_ms', 'Percentil calculado sobre la muestra consultada. Con pocas peticiones es poco representativo.'],
         ['Consulta vacía', 'Puede deberse a filtros, rango temporal, falta de ingesta o ausencia real del evento.'],
         ['Reinicios', 'Compara el inventario y el periodo. Un Pod nuevo es otro objeto.']], [41,129]),
     h('Si no aparecen datos'),
     p('Comprueba workspace, clúster, namespace e intervalo; revisa que el add-on y los agentes estén activos; genera nuevas peticiones y espera la ingesta. Una tabla inexistente no significa “cero errores”. monitoring/queries.kql incluye además agrupación por minuto, p95, inventario y eventos Warning.'),
     note('Evidencia real guardada', '05-consulta-1.json contiene solicitudes recuperadas desde Log Analytics, con ruta, estado, duración, Pod e identificador. 05-consulta-2.json resume la actividad. Repite python3 scripts/12-query-monitoring.py para exportar la ventana reciente.'))

page('HPA: entender y ejecutar el extra', 'Se demuestra en Minikube para separar el aprendizaje del gasto de Azure.',
     p('Horizontal Pod Autoscaler ajusta el número de réplicas según una métrica. El laboratorio usa una aplicación de carga CPU distinta de Planner: evita escalar horizontalmente una base SQLite que no fue diseñada para ello. No se requiere Kubeflow para la alternativa elegida.'),
     table(['Parámetro del laboratorio', 'Valor y razón'], [
         ['Contexto y namespace', 'mp2-hpa: separa este ejercicio del clúster de Azure.'],
         ['Réplicas', 'Mínimo 1, máximo 4: crecimiento visible y acotado.'],
         ['CPU request', '100m por Pod: referencia del porcentaje de utilización.'],
         ['Objetivo', '50 % de CPU sobre el request; aproximadamente 50m.'],
         ['Bajada', 'Ventana de estabilización configurada de 60 segundos.'],
         ['Generador', 'Job inicialmente suspendido, límite de ejecución 300 segundos.']], [57,113]),
     code('bash scripts/08-hpa-local.sh\nexport KUBECONFIG="$PWD/.kube/minikube.config"\nkubectl config current-context\nkubectl -n mp2-hpa get hpa,pods\nkubectl -n mp2-hpa top pods\nbash scripts/14-reset-hpa-load.sh\nbash scripts/09-verify-hpa.sh'),
     p('El primer script prepara Minikube, metrics-server y la aplicación. El script 14 renueva solo el Job vencido. El script 09 observa una réplica inicial, inicia carga, espera cuatro réplicas disponibles, suspende la carga y espera el regreso a una. Guarda evidencias/local/03-hpa-ciclo.txt. No modifica réplicas manualmente durante esa comprobación.'),
     h('Ejemplo numérico para explicar el mecanismo'),
     p('Una aproximación de la decisión es redondear hacia arriba: réplicas actuales × utilización actual / objetivo. Si hay 2 réplicas, la utilización media es 100 % y el objetivo 50 %, la propuesta básica es 4. El controlador también considera límites, disponibilidad de métricas, tolerancia y estabilización. [S9]'),
     note('Dos diferencias importantes', 'HPA cambia Pods; el autoscaler del clúster cambia nodos. kubectl scale es escalado manual y no demuestra HPA. El valor <unknown> indica que no hay una medida utilizable; no significa CPU en cero.'))

page('Pruebas y resultados comprobados', 'Pruebas históricas del 9 y repetición del 14 de septiembre de 2026.',
     table(['Comprobación real', 'Resultado', 'Evidencia local'], [
         ['HTTP en Docker', '12 pruebas aprobadas.', '01-pruebas-http.txt'],
         ['Inferencia de la foto de ejemplo', 'Samoyed como primera etiqueta.', '08-prediccion-real.json'],
         ['Aplicaciones en Kubernetes local', '2 Pods de clasificación y 1 de Planner.', '04-kubernetes-aplicaciones.txt'],
         ['HTTP contra Kubernetes local', 'Las mismas 12 pruebas aprobadas.', '04-kubernetes-aplicaciones.txt'],
         ['Persistencia al reemplazar Pod', 'Nuevo UID, mismo PVC y tarea conservada.', '04-kubernetes-aplicaciones.txt'],
         ['Ciclo HPA', '1 réplica → 4 disponibles → 1.', '03-hpa-ciclo.txt']], [60,66,44]),
     h('Qué cubren las 12 pruebas HTTP'),
     p('Las seis del clasificador comprueban disponibilidad del modelo, inferencia, imagen ausente, archivo inválido, exceso de tamaño y métricas. Las seis del tablero comprueban CRUD, caracteres especiales tratados como datos, validación, estados o ids inválidos, interfaz y cabeceras, y disponibilidad de SQLite.'),
     h('Observación del HPA guardada'),
     p('En la repetición del 14 de septiembre de 2026 (Colombia), la carga empezó a las 01:45:34 UTC del día 15. Hubo cuatro réplicas disponibles a las 01:46:44 y una a las 01:49:27. El Job vencido se renovó antes del ciclo; no se forzaron réplicas manualmente.'),
     h('Demostración en Azure completada'),
     p('AKS se creó por Portal y Cloud Shell se comprobó el 9 de septiembre. El 14 se repitió la CLI local: dos nodos Ready, imágenes AMD64 y 12 pruebas aprobadas en 19,804 s. Planner conservó la tarea y el PVC al cambiar de Pod. KQL devolvió solicitudes; scripts/11 y 12 repiten estas pruebas.'),
     note('Cómo justificar las pruebas', '“No probamos solo que abra la página. Comprobamos respuestas correctas, entradas inválidas, persistencia y comportamiento bajo carga. Los resultados locales prepararon la ejecución y las pruebas se repitieron en Azure”.'),
     ref('La relación detallada se conserva en docs/RESULTADOS.md y tests/test_http.py.'))

page('Costos, conservación y destrucción', 'El crédito se cuida limitando el tiempo de uso y verificando la limpieza.',
     p('El portal mostró USD 196,37 al mes por una máquina DS2 v2 en Chile Central. Tomando 730 horas como referencia, dos máquinas equivalen aproximadamente a <b>USD 0,538 por hora</b>. Son estimaciones de máquinas observadas el 9 de septiembre de 2026, no una factura ni un total garantizado.'),
     table(['Tiempo encendido', 'Solo dos máquinas, estimado'], [
         ['1 hora', 'USD 0,54'], ['4 horas', 'USD 2,15'],
         ['24 horas', 'USD 12,91'], ['7 días continuos', 'USD 90,38']], [79,91]),
     p('Se añaden discos, red, direcciones o balanceador, ACR y datos de monitoreo, según uso y facturación. Pedir 1 GiB en un PVC no implica que el proveedor facture exactamente 1 GiB. Un presupuesto puede avisar y la información de costos puede tardar; no es un corte inmediato de consumo.'),
     h('Antes de eliminar'),
     code('mkdir -p privadas\ncurl --fail http://localhost:8082/api/tasks \\\n  > privadas/tareas-respaldo.json\nbash scripts/06-evidence.sh'),
     p('Guarda también capturas del portal, salidas de KQL, imágenes de prueba y configuración. tareas-respaldo.json es una exportación de las tareas; esta aplicación no incorpora un comando automático para restaurar todos sus campos. Usa datos de ejemplo y conserva el archivo fuera de publicaciones innecesarias.'),
     h('Eliminar únicamente el grupo del microproyecto'),
     code('bash scripts/07-delete-azure.sh'),
     p('El script enumera recursos, pide escribir ELIMINAR seguido del nombre exacto del grupo y elimina sus recursos. Comprueba después que tanto el grupo dedicado como el administrado de nodos ya no existan. Revisa en el portal recursos externos y consumo pendiente.'),
     note('Recreación para la sustentación', 'Guardar código y manifiestos permite recrear; no conserva por sí solo los datos eliminados. Reconstruye por portal aproximadamente un día antes, valida disponibilidad de nuevo y repite las pruebas. Detener AKS puede dejar conceptos facturables: no equivale a destruirlo.'))

page('Diagnóstico: del síntoma a la causa', 'Antes de cambiar algo, identifica el contexto y observa el estado.',
     code('export KUBECONFIG="$PWD/.kube/aks.config"\nkubectl config current-context\nkubectl -n microproyecto2 get pods,pvc\nkubectl -n microproyecto2 get events \\\n  --sort-by=.metadata.creationTimestamp'),
     table(['Síntoma', 'Qué revisar', 'Corrección razonable'], [
         ['QuotaExceeded o tamaño no disponible', 'Familia, región, política y capacidad.', 'Elegir opción permitida o resolver cuota; no reducir a un nodo.'],
         ['ImagePullBackOff', 'Nombre y etiqueta de imagen, ACR, identidad y conectividad.', 'Corregir referencia o permiso de descarga.'],
         ['exec format error', 'Arquitectura de la imagen.', 'Reconstruir para linux/amd64 en los nodos elegidos.'],
         ['Pod Pending', 'Eventos del Pod, recursos y estado del PVC.', 'Resolver la condición concreta de planificación o almacenamiento.'],
         ['CrashLoopBackOff', 'Logs, causa de salida y memoria.', 'Corregir el fallo; reiniciar sin diagnóstico suele repetirlo.'],
         ['PVC Pending', 'StorageClass, eventos y disponibilidad de disco.', 'Verificar managed-csi y el motivo que informa el proveedor.'],
         ['localhost no responde', 'Compose, puertos, contexto y túnel.', 'Liberar 8081/8082 o reabrir port-forward.'],
         ['No hay logs en Azure', 'Workspace, add-on, filtros y tiempo de ingesta.', 'Generar peticiones y confirmar que el agente las recopila.'],
         ['HPA muestra <unknown>', 'metrics-server, requests y contexto local.', 'Esperar métricas válidas y leer las condiciones del HPA.']], [42,60,68]),
     p('Para profundizar usa kubectl describe pod NOMBRE_DEL_POD y kubectl logs NOMBRE_DEL_POD dentro del namespace correcto. Si el contenedor reinició, logs --previous puede ayudar cuando existe un registro de la ejecución anterior.'),
     note('Cómo responder al profesor', '“Primero observo el estado y los eventos; después formulo una causa posible y hago una corrección pequeña. Vuelvo a ejecutar la misma prueba para comprobar si realmente la resolví”.'))

page('Guion sencillo de sustentación', 'La secuencia enlaza una necesidad, una decisión y una prueba.',
     h('Apertura para adaptar con tus palabras'),
     p('“El proyecto prepara dos aplicaciones para AKS. Una clasifica fotografías sin guardar archivos y otra administra tareas que deben persistir. Voy a mostrar el clúster, ejecutar ambas aplicaciones, reemplazar un Pod para comprobar los datos y relacionar las acciones con monitoreo. El extra muestra HPA en un entorno local”.'),
     p('Cuando el despliegue real esté terminado, puedes sustituir “prepara” por “despliega”. La presentación debe describir el estado que realmente puedas mostrar ese día.'),
     table(['Ensayo orientativo', 'Qué mostrar', 'Idea central'], [
         ['0 a 1 minuto', 'Arquitectura y AKS en el portal.', 'Qué administra Azure y qué configura el equipo.'],
         ['1 a 2', 'Cloud Shell y CLI local.', 'Mismo clúster, al menos dos nodos Ready.'],
         ['2 a 4', 'Fotografía y respuesta del clasificador.', 'Inferencia, predicciones y Pod que responde.'],
         ['4 a 6', 'Tarea antes y después del reemplazo.', 'Persistencia fuera del ciclo del Pod.'],
         ['6 a 8', 'CPU/memoria y una fila de KQL.', 'Una observación real con contexto.'],
         ['8 a 10', 'Ciclo HPA local.', 'Cambio automático de réplicas por CPU.']], [31,75,64]),
     h('Preparación con los tres nombres de esta guía'),
     p('Como reparto de estudio sugerido, Miguel puede explicar Azure y redes; Juan, las aplicaciones y el HPA; Natalia, persistencia, monitoreo y evidencias. Después intercambien temas. <b>Las tres personas deben poder recorrer todo el proyecto</b>; el reparto no limita la responsabilidad individual ni certifica contribuciones ya realizadas.'),
     note('Tiempo y coordinación', 'Este recorrido de diez minutos es para ensayar, no una duración confirmada del turno. Inicia el HPA y el monitoreo con anticipación; la reducción de réplicas y la ingesta de datos pueden tardar.'))

page('Preguntas conceptuales: fundamentos', 'Respuestas breves que debes poder desarrollar con un ejemplo propio.',
     h('1. ¿Qué aporta AKS?'), p('Proporciona Kubernetes administrado. Azure opera el control plane; nosotros declaramos aplicaciones, nodos y permisos y comprobamos sus resultados.'),
     h('2. ¿Cuál es la diferencia entre nodo y Pod?'), p('El nodo es la máquina; el Pod es una unidad de ejecución dentro del clúster. Un nodo puede alojar varios Pods.'),
     h('3. ¿Por qué usar un Deployment?'), p('Permite declarar la imagen y el número de réplicas, y mantenerlas mediante controladores. Reemplaza ejecuciones que faltan; no respalda sus archivos.'),
     h('4. ¿Por qué un Service?'), p('Selecciona Pods mediante etiquetas y proporciona acceso interno estable. Las direcciones de los Pods pueden cambiar cuando se reemplazan.'),
     h('5. ¿Qué aporta un Namespace?'), p('Organiza recursos del proyecto y permite aplicar controles a ese ámbito. Por sí solo no constituye una barrera de red.'),
     h('6. ¿Qué diferencia una imagen de un contenedor?'), p('La imagen es el paquete construido. El contenedor es una ejecución de ese paquete con recursos y configuración de operación.'),
     h('7. ¿Qué significan requests y limits?'), p('Requests orientan la asignación de recursos; limits acotan consumo. En el HPA de CPU, el request también es la referencia de utilización.'),
     h('8. ¿Readiness reinicia el contenedor?'), p('Una readiness fallida indica que no debe recibir tráfico a través del Service. Liveness puede provocar reinicio; startup protege la inicialización.'),
     h('9. ¿Dos réplicas garantizan alta disponibilidad?'), p('No por sí solas. Hay que comprobar ubicación, capacidad, acceso y dependencias. Nuestro tablero y su disco siguen teniendo límites de disponibilidad.'),
     h('10. ¿Por qué la URL sigue siendo localhost en AKS?'), p('Porque el navegador entra por un túnel local. La aplicación está en Azure si el contexto del túnel es AKS; se confirma con Pods y registros.'))

page('Preguntas conceptuales: decisiones', 'La respuesta debe explicar tanto el beneficio como el límite.',
     h('11. ¿Entrenamos el modelo?'), p('No. Usamos pesos preentrenados. El aporte del proyecto es la integración, el empaquetado, la ejecución y la observación del servicio.'),
     h('12. ¿Por qué cambiar el ejemplo MXNet?'), p('Es una sugerencia del enunciado. Elegimos otra implementación de clasificación, documentando que ImageNet tiene 1.000 clases y el ejemplo CIFAR-10 tiene diez.'),
     h('13. ¿75,79 % significa certeza real?'), p('No. Es una puntuación relativa producida por softmax para esa imagen y las categorías del modelo. No mide precisión global ni garantiza el acierto.'),
     h('14. ¿Por qué Planner tiene una réplica?'), p('Usa SQLite sobre un volumen y no fue diseñado para escritores distribuidos. Recreate evita superponer la versión anterior y la nueva; puede haber interrupción.'),
     h('15. ¿ReadWriteOnce equivale a un único Pod?'), p('No. Limita escritura desde un nodo y puede permitir varios Pods en ese nodo. Nuestra configuración de una réplica limita la ejecución del tablero.'),
     h('16. ¿Un PVC es un respaldo?'), p('No. Separa datos del Pod. Borrar el volumen puede perderlos; hacen falta exportaciones o copias independientes para recuperación.'),
     h('17. ¿Qué diferencia un log de una métrica?'), p('El log describe un evento concreto; la métrica expresa una magnitud o agregado. Juntos ayudan a relacionar una petición con su consumo y resultado.'),
     h('18. ¿HPA crea máquinas?'), p('No. Ajusta réplicas de Pods. El autoscaler del clúster puede cambiar nodos; el proyecto mantiene dos nodos de Azure y demuestra HPA local.'),
     h('19. ¿Por qué HPA no baja de inmediato?'), p('Las métricas se muestrean y el controlador usa estabilización. El valor configurado de 60 segundos no garantiza una reducción exactamente a los 60 segundos.'),
     h('20. ¿Por qué destruir el clúster?'), p('Las máquinas y recursos asociados consumen crédito mientras se conservan según su facturación. Guardamos evidencias y configuración para recrear antes de sustentar.'))

page('Cambios en vivo para practicar', 'Predice el efecto, realiza el cambio y comprueba el resultado.',
     h('Ejercicio 1. Escalar manualmente el clasificador'),
     code('export KUBECONFIG="$PWD/.kube/aks.config"\nkubectl -n microproyecto2 scale deployment/classifier --replicas=3\nkubectl -n microproyecto2 rollout status deployment/classifier\nkubectl -n microproyecto2 get pods -l app=classifier -o wide\n# Restaurar el estado declarado para la demostración:\nkubectl -n microproyecto2 scale deployment/classifier --replicas=2'),
     p('<b>Predicción:</b> Kubernetes intentará crear un tercer Pod si hay recursos. <b>Explicación:</b> es escalado manual de Pods; el número de nodos no cambia por este comando. Una réplica Pending no debe contarse como disponible.'),
     h('Ejercicio 2. Reemplazar ejecuciones del clasificador'),
     code('kubectl -n microproyecto2 rollout restart deployment/classifier\nkubectl -n microproyecto2 rollout status deployment/classifier\nkubectl -n microproyecto2 get pods -l app=classifier -o wide'),
     p('<b>Predicción:</b> se reemplazan Pods usando la estrategia de actualización del Deployment. <b>Comprobación:</b> aparecen nuevos nombres o UIDs y vuelve a haber dos réplicas disponibles. Si el túnel dependía de una ejecución reemplazada, ábrelo de nuevo.'),
     h('Ejercicio 3. Provocar un error de cliente'),
     code('curl -i -X POST http://localhost:8081/predict\ncurl --fail http://localhost:8081/healthz'),
     p('<b>Predicción:</b> 400 y luego 200. <b>Comprobación:</b> el registro muestra la petición inválida sin caída del servicio. Explica por qué ese error forma parte de una validación correcta.'),
     h('Ejercicio 4. Interpretar otro objetivo de HPA'),
     p('Antes de modificarlo, explica qué ocurriría al subir el objetivo de 50 % a 70 % para la misma carga: la propuesta básica suele ser menor. docs/06-SUSTENTACION.md contiene los comandos para cambiarlo y restaurarlo. Hazlo en el contexto local, no en AKS.'),
     note('Criterio de éxito', 'No basta memorizar el comando. Debes señalar qué objeto cambia, qué esperas observar, qué condición podría impedirlo y cómo regresas a la configuración del proyecto.'))

page('Evidencias y entrega organizada', 'Una entrega revisable conecta requisitos, archivos y resultados.',
     table(['ID', 'Qué entregar como evidencia', 'Condición de aceptación'], [
         ['A01', 'Portal: configuración y creación terminada.', 'Nombre, región, dos nodos y estado correcto.'],
         ['A02 / A03', 'Cloud Shell y CLI local.', 'Mismo clúster, origen visible, dos nodos Ready.'],
         ['A04 / A05', 'Clasificador, API y recursos.', 'Foto procesada en AKS, Pod y dos réplicas disponibles.'],
         ['A06 / A07', 'Tablero y prueba del PVC.', 'Operaciones correctas y tarea conservada con nuevo Pod.'],
         ['A08 / A09', 'Gráficos de Azure y consulta KQL.', 'Clúster, intervalo y petición identificables.'],
         ['A10', 'Error 400 controlado.', 'Respuesta inválida explicada y servicio saludable.'],
         ['X01 a X03', 'HPA antes, durante y después.', 'Subida y bajada automáticas, sin scale manual.'],
         ['E01', 'GitHub y Classroom.', 'Archivos finales accesibles y entrega confirmada.']], [26,81,63]),
     h('Qué acompañar a cada captura'),
     p('Escribe una frase con entorno, acción y resultado observado. Ejemplo de estructura: “En AKS se reemplazó el Pod del tablero; su UID cambió y la tarea con id ___ permaneció en el mismo PVC”. No inventes valores para completar una plantilla.'),
     h('Qué incluir en el paquete'),
     p('README, aplicaciones, manifiestos, scripts, consultas, pruebas, guía y resultados reales. Revisa las evidencias antes de publicarlas. Excluye .env, .azure, .kube, contraseñas, tokens, cachés y bases de datos. El ZIP usa solo archivos registrados en Git y evidencia revisada en evidencias/publicables; los originales privados permanecen locales.'),
     h('Antes del turno'),
     p('Comprueba la inscripción y el año en el Excel oficial; revisa el enlace de reunión aplicable; publica los scripts y confirma Classroom con anticipación. El anuncio indica Google Meet para horarios previos a clase y el Webex habitual para la franja de clase. La guía no modificó esos sitios ni confirma una entrega realizada.'))

page('Justificación final y límites', 'Una conclusión sólida reconoce qué demuestra el proyecto y qué falta.',
     h('Justificación integral para adaptar'),
     p('“La solución combina una carga sin estado y una carga con persistencia para mostrar decisiones diferentes de operación. El clasificador puede replicarse porque no conserva fotografías entre peticiones; el tablero necesita un volumen porque sus tareas deben sobrevivir al reemplazo de su ejecución. Los contenedores reúnen las dependencias y Kubernetes declara cómo mantener cada aplicación”.'),
     p('“Las pruebas HTTP verifican casos correctos e incorrectos. Las sondas comprueban disponibilidad y los registros permiten relacionar una petición con su Pod. El monitoreo de Azure completa la demostración con solicitudes reales del entorno remoto. HPA se estudia por separado en local para entender el mecanismo sin aumentar el consumo del clúster de Azure”.'),
     h('Qué se puede concluir hoy'),
     p('<b>El despliegue y los registros de Azure están comprobados.</b> Dos nodos, ambas aplicaciones, 12 pruebas HTTP y persistencia se verificaron durante el ensayo. Luego se detuvo AKS conservando datos. GitHub reúne el código; la entrega académica y la sustentación se confirman por separado.'),
     table(['Límite actual', 'Mejora futura con una necesidad concreta'], [
         ['Tablero sin cuentas', 'Autenticación y autorización antes de ofrecerlo a usuarios reales.'],
         ['SQLite y una réplica', 'Base compartida y diseño de concurrencia si se necesita escalar.'],
         ['Acceso por túnel', 'TLS, dominio y controles de acceso si se publica un servicio.'],
         ['Una imagen de prueba conocida', 'Conjunto de evaluación diverso para medir calidad del modelo.'],
         ['Dependencias parcialmente fijadas', 'Digests y hashes para mayor reproducibilidad.'],
         ['Cuota pequeña y sesiones cortas', 'Capacidad para actualizaciones y resiliencia si el servicio debe permanecer activo.']], [66,104]),
     note('Autoría y comprensión', 'Explica el código que entregas y documenta fuentes y ayuda recibida según las reglas del curso. La guía ofrece argumentos y ejercicios; la sustentación individual requiere comprensión personal y resultados propios.'))

page('Fuentes y mapa de respaldo', 'Consulta las fuentes oficiales y el código al ampliar una explicación.',
     p('El alcance se obtuvo del archivo “2025-03 Microproyecto2.doc” y del anuncio compartido. “ActivarAzureStudents.pdf” se conservó como referencia histórica. Las decisiones y resultados de esta guía se contrastaron con el código y las evidencias locales; las páginas siguientes son referencias técnicas, no pruebas del despliegue del equipo.'),
     ('sources',),
     h('Archivos que respaldan las afirmaciones del proyecto'),
     table(['Tema', 'Ubicación principal'], [
         ['Modelo y validación de imagen', 'apps/classifier/app.py y download_model.py'],
         ['Tablero, SQL y operaciones', 'apps/planner/app.py'],
         ['Recursos, sondas y volumen', 'k8s/base/ y k8s/overlays/aks/'],
         ['Eventos y consultas', 'apps/common/observability.py y monitoring/'],
         ['Pruebas ejecutadas', 'tests/test_http.py y evidencias/local/'],
         ['Estado real de avance', 'docs/RESULTADOS.md y evidencias/azure/']], [66,104]),
     ref('Edición actualizada: 14 de septiembre de 2026. Las versiones, cuotas, disponibilidad y precios observados deben comprobarse de nuevo al recrear el entorno.'))

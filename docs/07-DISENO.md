# Decisiones de diseño y límites

## Modelo y dependencia del ejemplo

Se utiliza MobileNetV3 Small con pesos `IMAGENET1K_V1` de TorchVision. La aplicación
no modifica ni entrena esos pesos. PyTorch 2.8.0 y TorchVision 0.23.0 constituyen la
pareja de versiones elegida y fijada en Docker; no se afirma que sean las últimas.
Los pesos se descargan en la construcción y se reutilizan al iniciar cada Pod.

El ejemplo sugerido por el enunciado usa MXNet y CIFAR-10. Aquí hay 1.000 etiquetas
ImageNet, en inglés, y sus transformaciones oficiales. Una foto de un caballo
puede no producir la etiqueta genérica `horse`, por lo que la demostración incluye
una imagen de prueba con resultado verificable y recomienda más fotos propias.
[Modelo y transformaciones](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.mobilenet_v3_small.html).

## Operación

Gunicorn usa un proceso por contenedor. El clasificador emplea un bloqueo para
la inferencia y un hilo de CPU de Torch para mantener consumo predecible. El
segundo hilo HTTP permite atender comprobaciones de salud mientras hay una
inferencia. Las métricas Prometheus son por proceso/Pod y se reinician al reiniciarlo.

La aplicación valida tipo decodificado de archivo, tamaño total de petición y
cantidad de píxeles. El límite de 5 MB incluye el pequeño sobrecosto multipart,
por lo que un archivo exactamente en el límite puede rechazarse. Se recomienda
usar fotografías de menos de 4 MB para la demostración.

SQLite usa consultas parametrizadas y modo WAL. La aplicación es un tablero
compartido de laboratorio: no incorpora cuentas, autorización por usuario ni
gestión de datos personales. Sus datos deben ser de ejemplo.

## Seguridad y alcance del acceso

Los contenedores de las aplicaciones corren como UID 10001 y no montan tokens de
ServiceAccount. Se utiliza sistema de archivos de solo lectura, capabilities
eliminadas y seccomp RuntimeDefault. `/tmp` y el directorio de datos del tablero
son las excepciones de escritura necesarias.

Los Services son ClusterIP. El acceso de la demostración usa túneles vinculados
a 127.0.0.1. No se configura un sitio público, TLS externo, autenticación de
usuarios ni rate limiting. No debe publicarse el tablero a Internet como si fuera
un producto terminado. Para una futura versión pública habría que diseñar esos
controles y una base de datos apropiada.

## Recursos y disponibilidad

El clasificador solicita 250m y 384Mi por Pod, con límite de una CPU y 1Gi. Son
valores iniciales que se deben contrastar con mediciones en AKS. La primera
inferencia puede costar más que las siguientes; el tiempo mostrado incluye la
transformación y la espera del bloqueo, además de la operación del modelo.

El tablero solicita 100m y 64Mi, con límite 500m y 256Mi. Su PVC de 1Gi usa
`managed-csi` en AKS, correspondiente al aprovisionamiento de Azure Disk. El costo
real depende de las unidades de facturación del proveedor, no solo de pedir 1Gi.

La afinidad de distribución es preferente. El tablero tiene un punto único de
ejecución, interrupciones durante Recreate y dependencia del disco. No se afirma
alta disponibilidad productiva. El laboratorio HPA muestra el mecanismo, no una
prueba de capacidad del sistema completo.

## Autoría y uso de herramientas

Los integrantes deben revisar, ejecutar, adaptar y comprender el material antes
de entregarlo. Documenten la ayuda y las fuentes según las reglas del curso.
No atribuyan a los integrantes entrenamiento del modelo, capturas de Azure ni
resultados que no hayan obtenido. La calidad de la sustentación depende de su
comprensión y demostración personal, no únicamente de la apariencia del proyecto.

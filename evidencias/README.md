# Evidencias verificadas y compartibles

Los originales se conservan en este computador en `evidencias/local/` y `evidencias/azure/`. Esas carpetas no se publican íntegramente porque pueden contener datos de cuenta, red o capturas sin revisar. Las copias siguientes fueron revisadas para esta entrega; no se inventaron respuestas para completar una demostración.

| Archivo | Fecha de la ejecución | Qué acredita |
|---|---|---|
| [01-nodos-cli](publicables/01-nodos-cli-20260914.txt) | 14/09/2026 Colombia | Dos nodos Ready, Kubernetes 1.35.7, desde el Mac |
| [02-pruebas-aks](publicables/02-pruebas-aks-20260914.txt) | 14/09/2026 Colombia | 12 pruebas HTTP, nuevo UID del Pod, mismo PVC, misma tarea |
| [03-hpa-ciclo](publicables/03-hpa-ciclo-20260914.txt) | 14/09/2026 Colombia | Una réplica, cuatro disponibles y regreso a una sin escalado manual |
| [04-cloud-shell](publicables/04-cloud-shell-20260909.txt) | 09/09/2026 UTC | Fragmento de la terminal Cloud Shell con dos nodos Ready; evidencia histórica |
| [05-docker-http](publicables/05-docker-http-20260909.txt) | 09/09/2026 | 12 pruebas del ensayo local en Docker |
| [06-monitoreo](publicables/06-resumen-monitoreo.json) | 14/09/2026 Colombia | Conteos derivados de las cuatro consultas guardadas de Log Analytics |
| [07-apagado](publicables/07-apagado-aks.json) | Cierre de la sesión del 14/09 | AKS Stopped / Succeeded |

Los registros de la noche del 14 en Colombia aparecen como 15 de septiembre en UTC. Las IP internas, rutas personales y prefijos generados del pool se ocultan; los tiempos, estados y resultados se conservan. El fragmento Cloud Shell respeta los saltos de línea de la captura de accesibilidad.

[MANIFIESTO-SHA256.json](publicables/MANIFIESTO-SHA256.json) identifica fuentes locales, tratamiento y hashes. Un hash permite comprobar que un archivo no cambió; no reemplaza mostrar el sistema funcionando.

El registro de AKS incluye un Pod antiguo en Error. Se conservó esa observación: fue diagnosticado como Preempting, archivado y retirado posteriormente; la prueba del nuevo Pod y persistencia fue satisfactoria. La consulta de monitoreo incluye avisos, no una afirmación de cero errores. Ver [RESULTADOS.md](../docs/RESULTADOS.md).

Las capturas originales del portal y los respaldos privados permanecen locales para revisión presencial. No se ha publicado la base SQLite ni la exportación completa de tareas.

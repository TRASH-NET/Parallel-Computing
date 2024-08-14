# Análisis de Resultados
Los resultados de la ejecución del script con diferentes configuraciones de hilos y procesos muestran una clara diferencia en el tiempo de ejecución y la eficiencia de cada enfoque. A continuación, se presenta un análisis detallado de los resultados y las conclusiones obtenidas.
## Hilos (Threads)
Los resultados muestran una clara mejora en el tiempo de ejecución al aumentar el número de trabajadores hasta 32. La reducción del tiempo es significativa cuando se pasa de 1 a 8 trabajadores, lo que indica un buen aprovechamiento de la concurrencia para tareas de I/O. Sin embargo, la mejora se vuelve marginal a partir de 16 trabajadores, y la diferencia entre 16 y 32 trabajadores no es tan pronunciada, aunque sigue existiendo. Esto sugiere que el sistema está cerca de su límite de eficiencia para este tipo de tarea con hilos.

## Procesos (Processes)
En el caso de los procesos, también se observa una mejora inicial significativa en el tiempo de ejecución al aumentar el número de trabajadores. Sin embargo, a partir de 16 trabajadores, el tiempo de ejecución no mejora y, de hecho, tiende a empeorar. Esto podría deberse a la sobrecarga de crear y gestionar múltiples procesos en comparación con hilos, que son más ligeros en términos de recursos del sistema.

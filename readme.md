# Exploración Azure Speech para transcripción de entrevistas

## Scripts:
Dentro de la carpeta de scripts se encuentra el archivo `transcripcion.py` que a su vez tiene dos funciones:
* `transcribir_texto` tiene los siguientes parámetros:
    - `archivo_audio` (str): la ubicación del archivo a transcribir.
    - `lenguaje` (str, 'es-CO' por default) : el lenguaje origen del audio.
    - `mostrar_avance` (bool). Si se selecciona como ```True``` se muestra la identificación de cada una de las partes del audio.

La salida de esta función es una lista es `List[Tuple]`, donde cada una de las tuplas es `Tuple[str, Int, Int]`, siendo el texto transcrito la primera posición, la segunda posición el momento en el que comienza a transcribirse, y la última posición la duración, todo dado en ticks o diez-millonésimas de segundos (10**-7 seg).

* `guardar_transcripcion` tiene los siguientes parámetros:
    - `list_transcripcion` (List[Tuple]) : es el resultado de la función `transcribir_texto`. 
    - `archivo_salida` (str) : es el nombre que se le dará al texto de salida.
    - `guardar_con_tiempos` (bool) : Si se selecciona como ```True```, se exporta el tiempo con el intervalo en el que aparece. En caso contrario, se guarda el texto de corrido. 

## Entrevistas:
Entrevistas reales hechas a personas en el parque de Arví. Son la clase de conversaciones que tendrían que poder transcribirse. Todas son cortas, de no más de 2 minutos.

## Transcripciones:
Son las transcripciones hechas a todas las entrevistas de la carpeta. En este paso todavía no se había implementado el modelo de reconocimiento de speakers.
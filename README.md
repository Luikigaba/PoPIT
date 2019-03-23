# PoPIT

Este repositorio del proyecto PoPIT incluye los códigos necesarios para hacer la descarga las fotografías multiespectrales del satélite Sentinel-2 de la ESA, su correspondiente transformación y manipulación, y finalmente el desarrollo del modelo con técnicas de Machine Learning.

## Descarga de datos

Se tiene tanto un cuaderno donde se ha hecho el prototipado de código para la la manipulación y descarga de los datos, y después un script final para ejecutar en consola para descargar los datos.

## Manipulación de datos

Hay dos códigos de R para unificar y juntar los datos de las estaciones de control ambiental de Madrid, descargados a mano, y los datos de las imágenes multiespectrales. Así se crean las tablas finales usadas en el entrenamiento.

## Modelado

Un script de R usado para el cruce final de las tablas y desarrollo del algoritmo de Machine Learning final. Se ha utilizado validación cruzada para probar los modelos y la evaluación final sobre datos de test no vistos en el entrenamiento.

Entrenando un modelo para predecir la concentración de NOx, se ha obtenido un NMAE de 0.20.


## Resultado

Se aplica el modelo a la siguiente imagen de Sevilla, usando sus 11 bandas espectrales correspondientes:

![alt text](http://i66.tinypic.com/2qi2w4p.png)

Se obtiene el siguiente mapeo de de concentración de NOx sobre la ciudad:

![alt text](http://i65.tinypic.com/rtkjet.png)

Superponiendo las dos imágenes, se obtiene el siguiente mapa de concentración de NOx sobre Sevilla, visualizable en web:

![alt text](http://i63.tinypic.com/2hd74fq.jpg)

"""
TODO: rellenar

Asignatura: GIW
Práctica 2
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

import csv
from pprint import pprint
### Formato CSV
def lee_fichero_accidentes(ruta):
    with open("AccidentesBicicletas_2021.csv", 'r', newline='', encoding='utf8') as fich:
     ejemploLector = csv.reader(fich)
    for linea in ejemploLector:
        print(f"Linea #{ejemploLector.line_num} {linea}")

def accidentes_por_distrito_tipo(datos):
    ...

def dias_mas_accidentes(datos):
    ...

def puntos_negros_distrito(datos, distrito, k):
    ...


#### Formato JSON
def leer_monumentos(ruta):
    ...

def codigos_postales(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, direccion, distancia):
    ...

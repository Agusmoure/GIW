"""
TODO: rellenar

Asignatura: GIW
Práctica 2
Grupo: 08
Autores: Autores: Carlos Rondon Arevalo
         Pablo Padial Iniesta
         David Llanes Martín
         Agustín Moure Rodríguez 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

import csv
from pprint import pp
from collections import defaultdict
### Formato CSV
def lee_fichero_accidentes(ruta):
        with open(ruta, 'r', newline='',encoding='utf8') as fich:
            ejemploLector = csv.DictReader(fich, delimiter=';')
            for linea in ejemploLector:
                 print(f"{linea}")

def contar_accidentes(datos):
    contador = defaultdict(int)
    for accidente in datos:
        distrito = accidente.get('distrito')
        tipo_accidente = accidente.get('tipo_accidente')
        contador[(distrito, tipo_accidente)] += 1
    return dict(contador)

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

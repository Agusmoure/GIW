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
import json
import pprint
from collections import Counter
from geopy.geocoders import Nominatim
from geopy import distance
def leer_monumentos(ruta):
    with open(ruta, 'r',newline='',encoding='utf8')as fich:
        json_dict=json.load(fich)
    return json_dict["@graph"]


def codigos_postales(monumentos):
    postal_code_monuments= [monumento["address"]["postal-code"] for monumento in monumentos ]
    return Counter(postal_code_monuments).most_common() 

def busqueda_palabras_clave(monumentos, palabras):
    lista=[]
    for monumento in monumentos:
        words=True
        for palabra in palabras:
            desc_and_title=monumento["organization"]["organization-desc"]+" "+monumento["title"]
            if palabra.lower() not in desc_and_title.lower() :
                words=False
        if(words):
            lista.append((monumento["title"],monumento["address"]["district"]["@id"]))
    return lista


def busqueda_distancia(monumentos, direccion, distancia):
    geolocator = Nominatim(user_agent="GIW_pr2")
    lista=[]
    dir=geolocator.geocode(direccion,addressdetails=True)
    for monumento in monumentos:
        if "location" not in monumento:
            #TODO Preguntar si los que no tienen location hay que sacar su direccion mediante calle y localizacion porque hay alguno que no tienen esas cosas tambien me parece
            continue
        lugar=(monumento["location"]["latitude"],monumento["location"]["longitude"])
        distancia_al_monumento=distance.distance((dir.latitude,dir.longitude), lugar).km
        if distancia_al_monumento<distancia:
            lista.append((monumento["title"],monumento["id"],distancia_al_monumento))
            #Sacado de la documentación de sort si estan a la misma distancia mantiene el orden de aparición
            lista.sort(key=lambda monumento:monumento[2])
    return lista

"""
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
from collections import Counter
import json
from geopy.geocoders import Nominatim
from geopy import distance
### Formato CSV
def lee_fichero_accidentes(ruta):
    """
    Lee un fichero CSV y devuelve una lista de diccionarios del archivo leido
    """
    with open(ruta, 'r', newline='',encoding='utf8') as fich:
        ejemplo_lector = csv.DictReader(fich, delimiter=';')
        datos=list(ejemplo_lector)
    return datos

def contar_accidentes(datos):
    """
    Dada una lista de diccionarios de accidentes, devuelve un diccionario
    con clave tupla(distrito, tipo accidente) y valor cantidad de accidentes de ese tipo
    """
    contador = {}
    for accidente in datos:
        distrito = accidente.get('distrito')
        tipo_accidente = accidente.get('tipo_accidente')
        #Coge el valor actual del diccionario
        #con clave(distrito,tipo_accidente) si non existe devuelve 0
        # ya sea 0 o el valor le suma 1
        cantidad=contador.get((distrito,tipo_accidente),0)+1
        contador[(distrito, tipo_accidente)] = cantidad
    return contador


def dias_mas_accidentes(datos):
    """
    Dias con mas accidentes
    """

    fechas={dato.get('fecha') for dato in datos}
    cantidad=Counter(fechas).most_common()
    #Coje todos los valores que mas se repiten
    resultado={pareja for pareja in cantidad if pareja[1]==cantidad[0][1]}

    return resultado

def puntos_negros_distrito(datos, distrito, k):
    """
    Toma como parámetros un lista de diccionario de accidentes, distrito
    y el top de valores de retorno (k) y devuelve la localización con mas
    accidentes.
    """
    accidentes=[accidente['localizacion'] for accidente in datos
                 if accidente.get('distrito')==distrito]
    contador=Counter(accidentes)
    repes=contador.most_common(k)
    #Ordena primero en funcion de mayor numero y en caso de empate
    #lexicograficamente mayor
    repes.sort(key=lambda x:(x[1],x[0]),reverse=True)
    return repes

def leer_monumentos(ruta):
    """
    Toma como parámetro la ruta de un fichero .json y devuelve una 
    lista de monumentos.
    """
    with open(ruta, 'r',newline='',encoding='utf8')as fich:
        json_dict=json.load(fich)
    #Eliminamos informacion innecesaria
    return json_dict["@graph"]

def codigos_postales(monumentos):
    """
    Toma como parámetro una lista de monumentos y devuelve una lista
    de parejas (codigo_postal, numero_de_monumentos) ordenados por
    codigo postal con mas monumentos
    """
    postal_code_monuments= [monumento["address"]["postal-code"] for monumento in monumentos ]
    return Counter(postal_code_monuments).most_common()

def busqueda_palabras_clave(monumentos, palabras):
    """
    Busca aquellos monumentos que contengan todas las palabras
    que se reciben por parametro o bien
    en su descripcion o bien en su titulo
    """
    conjunto=set()
    for monumento in monumentos:
        words=True
        for palabra in palabras:
            desc_and_title=monumento["organization"]["organization-desc"]+" "+monumento["title"]
            if palabra.lower() not in desc_and_title.lower() :
                words=False
                break
        if words:
            if "district" not in monumento["address"]:
                text=''
            else:
                text=monumento["address"]["district"]["@id"]
            conjunto.add((monumento["title"],text))
    return conjunto

def busqueda_distancia(monumentos, direccion, distancia):
    """
    Determina todos los monumentos a una distancia menor a la pasada
    con respecto a la direccion proporcionada.Siempre y cuando
    el monumento exista en la lista
    """
    geolocator = Nominatim(user_agent="GIW_pr2")
    origin=geolocator.geocode(direccion,addressdetails=True)
    lista=[]
    for monumento in monumentos:
        if "location" not in monumento:
            continue
        lugar=(monumento["location"]["latitude"],monumento["location"]["longitude"])
        distancia_al_monumento=distance.distance((origin.latitude,origin.longitude), lugar).km
        if distancia_al_monumento<distancia:
            lista.append((monumento["title"],monumento["id"],distancia_al_monumento))
            #Sacado de la documentación de sort
            # si estan a la misma distancia mantiene el orden de aparición
            lista.sort(key=lambda monumento:monumento[2])
    return lista

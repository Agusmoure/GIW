"""

Asignatura: GIW
Práctica 5
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
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

URL = 'https://books.toscrape.com/'


# APARTADO 1 #
def explora_categoria(url):
    """ A partir de la URL de la página principal de una categoría, devuelve el nombre
        de la categoría y el número de libros """
    category_request=requests.get(url,timeout=60)
    # Corregimos el encoding
    category_request.encoding = category_request.apparent_encoding
    html = category_request.text
    soup = BeautifulSoup(html, 'html.parser')
    #Se ha visto el patron de que siempre
    #siempre el 1º strong es el nombre
    #y el segundo cuantos libros hay en total
    etiquetas=soup.find_all("strong")
    return (etiquetas[0].text,int(etiquetas[1].text))

def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    request = requests.get(URL,timeout=60)
    # Corregimos el encoding
    request.encoding = request.apparent_encoding
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    etiquetas = soup.find_all("div",{'class':"side_categories"})
    enlaces=etiquetas[0].find_all("a")
    #Descartamos la primera porque siempre es books
    return {explora_categoria(URL+enlace.attrs["href"])for enlace in enlaces[1:]}


# APARTADO 2 #
def url_categoria(nombre):
    """ Devuelve la URL de la página principal de una categoría a partir de su nombre (ignorar
        espacios al principio y final y también diferencias en mayúsculas/minúsculas) """
    request = requests.get(URL,timeout=60)
    # Corregimos el encoding
    request.encoding = request.apparent_encoding
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    #https://www.geeksforgeeks.org/beautifulsoup-search-by-text-inside-a-tag/
    etiquetas = soup.find_all(lambda tag: tag.name=="a"
                               and tag.text.strip().lower()==nombre.strip().lower())
    if len(etiquetas)==0:
        return None
    return URL+etiquetas[0].attrs["href"]


def number_from_text(texto):
    """
    Devuelve el numero que representa el texto 
    que llega por parametro
    """
    numeros={
        'one':1,
        'two':2,
        'three':3,
        'four':4,
        'five':5
    }
    return numeros.get(texto.lower(),None)

def libros_de_la_pagina(soup):
    """
    Devuelve un conjunto con todos los libros que se ven 
    """
    etiquetas=soup.find_all("article",{'class':"product_pod"})
    libros=set()
    for etiqueta in etiquetas:
        #Siempre las estrellas son la primera P
        p_etiqueta=etiqueta.find("p")
        # Esta p no es la misma que la primera
        precio=etiqueta.find("p",{'class':"price_color"}).text[1:]
        titulo=etiqueta.find("h3").find("a").attrs["title"]
        libro_actual=(titulo,float(precio),number_from_text(p_etiqueta.attrs["class"][1]))
        libros.add(libro_actual)
    return libros

def todas_las_paginas(url):
    """ Sigue la paginación recopilando todas las URL *absolutas* atravesadas
     y los libros que se encuentran en esta """
    lista=[url]
    request = requests.get(url,timeout=60)
    request.encoding = request.apparent_encoding  # Corregimos el encoding
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    conjunto=libros_de_la_pagina(soup)
    boton_siguiente=soup.find("li",{'class':"next"})
    if boton_siguiente is None:
        return lista, conjunto
    pagina_siguiente=boton_siguiente.find("a").attrs["href"]
    siguiente_url=urljoin(url,pagina_siguiente)
    return lista+todas_las_paginas(siguiente_url)[0],conjunto | todas_las_paginas(siguiente_url)[1]

def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve un conjunto de tuplas 
        (titulo, precio, valoracion), donde el precio será un número real y la 
        valoración un número natural """
    cat_url=url_categoria(nombre)
    if cat_url is None:
        return set()
    return todas_las_paginas(cat_url)[1]

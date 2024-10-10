"""

Asignatura: GIW
Práctica 3
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

import xml.sax
import xml.dom.minidom
import html
from geopy.geocoders import Nominatim
from geopy import distance
class ManejadorNombres(xml.sax.ContentHandler):
    """
    Clase encargada de manejar el ejercicio 1
    """
    def __init__(self):
        """
        metodo constructor
        """
        super().__init__()
        self.is_name=False
        self.names=[]
        self.current_name=""

    def startElement(self, name, attrs):
        """
        Se llama al comienzo de cada elemento del XML
        """
        if name=="name":
            self.is_name=True


    def characters(self, content):
        """
        Se llama para ver el contenido de cada elemento,
        No tiene porque llamarse una sola vez
        """
        if self.is_name:
            self.current_name+=content

    def endElement(self, name):
        """
        Se llama al final de cada elemento del XML
        """
        if name=="name" :
            self.is_name=False
            self.names.append(html.unescape(self.current_name).strip())
            self.current_name=""

    def get_names(self,sorted_list):
        """
        Devuelve una lista con los nombres encontrados en el xml
        """
        if sorted_list :
            self.names.sort()
        return self.names

def nombres_restaurantes(filename):
    """
    Llama a Sax con el manejadorNombres y devuelve la lista de nombres ordenada alfabeticamente
    """
    manejador=ManejadorNombres()
    parser = xml.sax.make_parser()
    parser.setContentHandler(manejador)
    parser.parse(filename)
    return manejador.get_names(True)

class ManejadorSubcategorias(xml.sax.ContentHandler):
    """
    Clase encargada de manejar el ejercicio 2
    """
    def __init__(self):
        """
        metodo constructor
        """
        super().__init__()
        self.is_categoria=False
        self.is_subcategoria=False
        self.subcategorias=set()
        self.save_category=False
        self.save_subcategory=False
        self.current_category=""
        self.current_subcategory=""

    def startElement(self, name, attrs):
        """
        Se llama al comienzo de cada elemento del XML
        """
        if name=="categoria":
            self.is_categoria=True
        if name=="subcategoria":
            self.is_subcategoria=True
        if self.is_subcategoria:
            for _,value in attrs.items():
                if value=="SubCategoria":
                    self.save_subcategory=True
        elif self.is_categoria:
            for _,value in attrs.items():
                if value=="Categoria":
                    self.save_category=True

    def characters(self, content):
        """
        Se llama para ver el contenido de cada elemento,
        No tiene porque llamarse una sola vez
        """
        if self.save_subcategory:
            self.current_subcategory+=content
        elif self.save_category:
            self.current_category+=content

    def endElement(self, name):
        """
        Se llama al final de cada elemento del XML
        """
        if self.current_subcategory!="":
            aux=f"{self.current_category} > {self.current_subcategory}"
            self.subcategorias.add(aux)
        if name=="categoria":
            self.is_categoria=False
            self.current_category=""
        if name=="subcategoria":
            self.is_subcategoria=False
            self.current_subcategory=""
        self.save_category=False
        self.save_subcategory=False

    def get_subcategories(self):
        """
        Devuelve un conjunto con las subcategorias encontrados en el xml
        """
        return self.subcategorias

def subcategorias(filename):
    """
    Llama a Sax con el manejadorSubcategorias y devuelve un conjunto con lo encontrado
    """
    manejador=ManejadorSubcategorias()
    parser = xml.sax.make_parser()
    parser.setContentHandler(manejador)
    parser.parse(filename)
    return manejador.get_subcategories()

def rellenar_campo(service, diccionario, campo, xml_name):
    """
    Rellena un campo basico
    """
    data=None
    if len(service.getElementsByTagName(xml_name)[0].childNodes)>0:
        node=service.getElementsByTagName(xml_name)[0].childNodes[0]
        data=html.unescape(node.data)
    diccionario[campo]=data

def rellenar_diccionario(service):
    """
    Rellena el diccionario pedido para el ejercicio 3
    """
    dictionary={}
    rellenar_campo(service,dictionary,"name","name")
    rellenar_campo(service,dictionary,"descripcion","body")
    rellenar_campo(service,dictionary,"email","email")
    rellenar_campo(service,dictionary,"web","web")
    rellenar_campo(service,dictionary,"phone","phone")
    dictionary["horario"]=None
    extra_data=service.getElementsByTagName("extradata")[0]
    for item in extra_data.getElementsByTagName("item"):
        if item.hasAttribute("name")and item.getAttribute("name")=="Horario":
            dictionary["horario"]=html.unescape(item.childNodes[0].data)
            break
    return dictionary

def info_restaurante(filename, name):
    """
    Devuelve la informacion
    """
    arbol_dom=xml.dom.minidom.parse(filename)
    services=arbol_dom.documentElement.getElementsByTagName("service")
    for service in services:
        aux=service.getElementsByTagName("name")[0]
        current_name=html.unescape(aux.childNodes[0].data).strip()
        if current_name!=name:
            continue
        return rellenar_diccionario(service)
    return None

def busqueda_cercania(filename, lugar, n):
    """
    Busca todos los restaurantes en un radio de n km
    desde lugar
    """
    arbol_dom=xml.dom.minidom.parse(filename)
    services=arbol_dom.documentElement.getElementsByTagName("service")
    geolocator = Nominatim(user_agent="GIW_pr2")
    origin=geolocator.geocode(lugar,addressdetails=True)
    lista=[]
    for service in services:
        lugar=(service.getElementsByTagName("latitude")[0].childNodes[0].data,
                service.getElementsByTagName("longitude")[0].childNodes[0].data)
        distancia_al_restaurante=distance.distance((origin.latitude,origin.longitude), lugar).km
        if distancia_al_restaurante<n:
            nombre=html.unescape(service.getElementsByTagName("name")[0].childNodes[0].data)
            lista.append((distancia_al_restaurante,
                          nombre))
    lista.sort(key=lambda restaurante:restaurante[0])
    return lista

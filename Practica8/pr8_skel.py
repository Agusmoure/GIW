"""
TODO: rellenar

Asignatura: GIW
Práctica 8
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

###
### <DEFINIR AQUÍ LAS CLASES DE MONGOENGINE>
###
import math

from mongoengine import connect, Document, EmbeddedDocument, EmbeddedDocumentField, StringField, \
  IntField, ListField, ValidationError

class Usuario(DynamicDocument):
    dni=StringField()
    nombre=StringField()
    apellido1=StringField()
    apellido2=StringField()
    f_nac=StringField()
    tarjetas=ListField()
    pedidos=ListField()

class Tarjeta(Document):
    nombre=StringField()
    numero=IntField()
    mes=IntField()
    year=IntField()
    cvv=IntField()

class Pedido(Document):
    total=IntField()
    fecha=StringField()
    lineas=ListField()


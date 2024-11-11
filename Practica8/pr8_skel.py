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
  IntField, ListField, ValidationError,FloatField,ComplexDateTimeField,ReferenceField

class Tarjeta(Document):
    nombre=StringField(required=True,min_length=2)
    numero=StringField(required=True,min_length=16,max_length=16)
    mes=StringField(required=True,min_length=2,max_length=2)
    year=StringField(required=True,min_length=2,max_length=2)
    cvv=StringField(required=True,min_length=3,max_length=3)
    def clean(self):
        self.validate(clean=False)
        number_wout_space=self.numero.replace(" ","")
        if len(number_wout_space)!=16:
            raise ValidationError("La tarjeta no tiene suficientes dígitos")
        try:
            int(number_wout_space)
        except:
            raise ValidationError("La tarjeta no es un número")
        mes_wout_space=self.mes.replace(" ","")
        if len(mes_wout_space)!=2:
            raise ValidationError("El mes no tiene suficientes dígitos")
        try:
            int(mes_wout_space)
        except:
            raise ValidationError("El mes no es un número")
        year_wout_space=self.year.replace(" ","")
        if len(year_wout_space)!=2:
            raise ValidationError("El año no tiene suficientes dígitos")
        try:
            int(year_wout_space)
        except:
            raise ValidationError("El año no es un número")
        cvv_wout_space=self.cvv.replace(" ","")
        if len(cvv_wout_space)!=3:
            raise ValidationError("El cvv no tiene suficientes dígitos")
        try:
            int(year_wout_space)
        except:
            raise ValidationError("El cvv no es un número")

class Producto(Document):
    codigo_barras=StringField(required=True,unique=True)
    nombre=StringField(required=True,min_length=2)
    categoria_principal=IntField(required=True)
    categorias_secundarias=ListField(IntField())

class Linea(EmbeddedDocument):
    num_items=IntField(required=True,min_value=0)
    precio_item=FloatField(required=True,min_value=0)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True,min_value=0)
    producto=ReferenceField(Producto, required=False)

class Pedido(Document):
    total=FloatField(required=True,min_value=0)
    fecha=ComplexDateTimeField(required=True)
    lineas=ListField(EmbeddedDocumentField(Linea),required=True)

class Usuario(Document):
    dni=StringField(primary_key=True,min_length=9,max_length=9,regex="[0-9]{8}[A-Z]")#lo podemos asumir? o ponemos required=True, unique=True
    nombre=StringField(required=True,min_length=2)
    apellido1=StringField(required=True,min_length=2)
    apellido2=StringField()
    f_nac=StringField(required=True)
    tarjetas=ListField(ReferenceField(Tarjeta))
    pedidos=ListField(EmbeddedDocumentField(Pedido))

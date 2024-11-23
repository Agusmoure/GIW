"""
Asignatura: GIW
Práctica 8
Grupo: 08
Autores: Carlos Rondon Arevalo
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

###
### <DEFINIR AQUÍ LAS CLASES DE MONGOENGINE>
###

from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, \
  IntField, ListField, ValidationError,FloatField,ComplexDateTimeField,ReferenceField
from datetime import datetime

class Tarjeta(EmbeddedDocument):
    """
    Tarjeta con la que se pagan los pedidos
    """
    nombre=StringField(required=True,min_length=2)
    numero=StringField(required=True,min_length=16,max_length=16,regex="[0-9]{16}")
    mes=StringField(required=True,min_length=2,max_length=2,regex="^(0[1-9]|1[0-2])$")
    year=StringField(required=True,min_length=2,max_length=2,regex="[0-9]{2}")
    cvv=StringField(required=True,min_length=3,max_length=3,regex="[0-9]{3}")
    def clean(self):
        self.validate(clean=False)

class Producto(Document):
    """
    Producto a comprar
    """
    codigo_barras=StringField(required=True,unique=True,
                              min_length=13,max_length=13,regex="[0-9]{13}")
    nombre=StringField(required=True,min_length=2)
    categoria_principal=IntField(required=True,min_value=0)
    categorias_secundarias=ListField(IntField(min_value=0),default=[],required=False)
    def get_nombre(self):
        """
        Devuelve el nombre del producto
        """
        return self.nombre
    def clean(self):
        self.validate(clean=False)

        last_digit=self.codigo_barras[-1]
        barcode_wot_last=self.codigo_barras[:-1]
        #https://es.wikipedia.org/wiki/European_Article_Number
        digits = [int(i) for i in reversed(barcode_wot_last)]
        digit_expected= (10 - (3 * sum(digits[0::2]) + (sum(digits[1::2])))) % 10
        if int(last_digit)!=digit_expected:
            raise ValidationError("El digito control es incorrecto")
        if len(self.categorias_secundarias)>0:
            if self.categoria_principal!=self.categorias_secundarias[0]:
                raise ValidationError("La categoria principal no es la primera secundaria")

class Linea(EmbeddedDocument):
    """
    Linea del producto en el ticket
    """
    num_items=IntField(required=True,min_value=0)
    precio_item=FloatField(required=True,min_value=0)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True,min_value=0)
    producto=ReferenceField(Producto, required=True)
    def get_total(self):
        """
        Devuelve el total
        """
        return self.total
    def get_producto(self):
        """
        Devuelve el producto
        """
        return self.producto
    def clean(self):
        self.validate(clean=False)
        if self.precio_item*self.num_items!=self.total:
            raise ValidationError("El total no coincide con lo que debería")
        if self.nombre_item!=self.producto.get_nombre():
            raise ValidationError("Los nombres no coinciden")

class Pedido(Document):
    """
    Pedido de una persona
    """
    total=FloatField(required=True,min_value=0)
    fecha=ComplexDateTimeField(required=True)
    lineas=ListField(EmbeddedDocumentField(Linea),required=True)
    def clean(self):
        self.validate(clean=False)
        if self.total!=sum(linea.get_total() for linea in self.lineas):
            raise ValidationError("El precio no es el que debería")
        productos_pedido=[linea.get_producto() for linea in self.lineas]
        if len(productos_pedido)!=len(set(productos_pedido)):
            raise ValidationError("Hay más de una linea con el mismo producto")

class Usuario(Document):
    """
    Usuario 
    """
    dni=StringField(primary_key=True,min_length=9,max_length=9,
                    regex="[0-9]{8}[A-Z]")
    nombre=StringField(required=True,min_length=2)
    apellido1=StringField(required=True,min_length=2)
    apellido2=StringField(required=False)
    f_nac=StringField(required=True,min_length=10,max_length=10,
                      regex="[0-9]{4}-[0-9]{2}-[0-9]{2}")
    tarjetas=ListField(EmbeddedDocumentField(Tarjeta),required=False)
    pedidos=ListField(ReferenceField(Pedido,reverse_delete_rule=4),required=False)
    def clean(self):
        self.validate(clean=False)
        letras_validacion="TRWAGMYFPDXBNJZSQVHLCKE"
        letra_a_validar=self.dni[-1]
        numero_dni=int(self.dni[:-1])
        letra_correcta = letras_validacion[numero_dni % 23]
        if letra_correcta != letra_a_validar:
            raise ValidationError("El DNI no es válido")
        if not datetime.strptime(self.f_nac, "%Y-%m-%d"):
            raise ValidationError("La fecha de nacimiento no es válida")

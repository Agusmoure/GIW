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

from mongoengine import  Document, EmbeddedDocument, EmbeddedDocumentField, StringField, \
  IntField, ListField, ValidationError,FloatField,ComplexDateTimeField,ReferenceField

class Tarjeta(EmbeddedDocument):
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
            mes_number=int(mes_wout_space)
            if(mes_number<1 or mes_number>12):
                raise ValidationError("El valor del mes no es válido")
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
            int(cvv_wout_space)
        except:
            raise ValidationError("El cvv no es un número")

class Producto(Document):
    codigo_barras=StringField(required=True,unique=True,min_length=13,max_length=13)
    nombre=StringField(required=True,min_length=2)
    categoria_principal=IntField(required=True,min_value=0)
    categorias_secundarias=ListField(IntField(min_value=0),default=[])
    def get_nombre(self):
        return self.nombre
    def clean(self):
        self.validate(clean=False)
        codigo_wout_space=self.codigo_barras.replace(" ","")
        if len(codigo_wout_space)!=13:
            raise ValidationError("El codigo de barras no tiene suficientes dígitos")
        try:
            int(codigo_wout_space)
        except:
            raise ValidationError("El codigo no es un número")
        last_digit=codigo_wout_space[-1]
        barcode_wot_last=codigo_wout_space[:-1]
        #https://es.wikipedia.org/wiki/European_Article_Number
        digits = [int(i) for i in reversed(barcode_wot_last)]
        digit_expected= (10 - (3 * sum(digits[0::2]) + (sum(digits[1::2])))) % 10
        if int(last_digit)!=digit_expected:
            raise ValidationError("El digito control es incorrecto")
        if len(self.categorias_secundarias)>0:
            if self.categoria_principal!=self.categorias_secundarias[0]:
                raise ValidationError("La categoria principal no es la primera secundaria")

class Linea(EmbeddedDocument):
    num_items=IntField(required=True,min_value=0)
    precio_item=FloatField(required=True,min_value=0)
    nombre_item=StringField(required=True,min_length=2)
    total=FloatField(required=True,min_value=0)
    #DUDA qué pasa si se elimina un producto?
    producto=ReferenceField(Producto, required=True)
    def get_total(self):
        return self.total
    def get_producto(self):
        return self.producto
    def clean(self):
        self.validate(clean=False)
        if self.precio_item*self.num_items!=self.total:
            raise ValidationError("El total no coincide con lo que debería")
        if self.nombre_item!=self.producto.get_nombre():
            raise ValidationError("Los nombres no coinciden")

class Pedido(Document):
    total=FloatField(required=True,min_value=0)
    fecha=ComplexDateTimeField(required=True)
    lineas=ListField(EmbeddedDocumentField(Linea),required=True)
    def clean(self):
        self.validate(clean=False)
        if self.total!=sum([linea.get_total() for linea in self.lineas]):
            raise ValidationError("El precio no es el que debería")
        productos_pedido=[linea.get_producto() for linea in self.lineas]
        if len(productos_pedido)!=len(set(productos_pedido)):
            raise ValidationError("Hay más de una linea con el mismo producto")

class Usuario(Document):
    dni=StringField(primary_key=True,min_length=9,max_length=9,regex="[0-9]{8}[A-Z]")#lo podemos asumir? o ponemos required=True, unique=True
    nombre=StringField(required=True,min_length=2)
    apellido1=StringField(required=True,min_length=2)
    apellido2=StringField(required=False)
    f_nac=StringField(required=True,min_length=10,max_length=10,regex="[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]")
    tarjetas=ListField(EmbeddedDocumentField(Tarjeta),required=False)
    pedidos=ListField(ReferenceField(Pedido,reverse_delete_rule=4),required=False)
    def clean(self):
        self.validate(clean=False)

        letras_validacion={
            0:'T', 8:'P', 16:'Q',
            1:'R', 9:'D', 17:'V',
            2:'W', 10:'X', 18:'H',
            3:'A', 11:'B', 19:'L',
            4:'G', 12:'N', 20:'C',
            5:'M', 13:'J', 21:'K',
            6:'Y', 14:'Z', 22:'E',
            7:'F', 15:'S',
        }
        letra_a_validar=self.dni[-1]
        numero_dni=int(self.dni[:-1])
        if letras_validacion.get(numero_dni%23,"")!=letra_a_validar:
            raise ValidationError("El DNI no es válido")

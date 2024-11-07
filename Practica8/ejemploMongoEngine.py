""""
Enrique Martin <emartinm@ucm.es>
Definición de ODM en MongoEngine
"""

import math

from mongoengine import connect, Document, EmbeddedDocument, EmbeddedDocumentField, StringField, \
  IntField, ListField, ValidationError


class Libro(EmbeddedDocument):
    """ Libro anidado dentro de las asignaturas """
    isbn = StringField(primary_key=True, regex='^[0-9]{13}$')
    titulo = StringField(required=True, min_length=5)
    autor = StringField(required=True, min_length=3)
    editorial = StringField(required=False)

    def __str__(self):
        """ Genera la cadena de texto para imprimirlo por pantalla """
        return (f'Libro(isbn={self.isbn}, titulo={self.titulo}, autor={self.autor}, '
                f'editorial={self.editorial if "editorial" in self else None}')


class Asignatura(Document):
    """ Información de las asignaturas """
    nombre = StringField(required=True)
    codigo = IntField(primary_key=True)
    temario = ListField(StringField(), required=False)
    bibliografia = EmbeddedDocumentField(Libro, required=False)

    def __str__(self):
        """ Genera la cadena de texto para imprimirlo por pantalla """
        return (f'Asignatura(codigo={self.codigo},\n'
                f'           nombre={self.nombre},\n'
                f'           temario={self.temario if "temario" in self else None})\n'
                f'           bibliografia={self.bibliografia if "bibliografia" in self else None})')

    def clean(self):
        """ Los códigos de asignatura deben ser números primos """
        self.validate(clean=False)
        for n in range(2, math.ceil(math.sqrt(self.codigo))):
            if self.codigo % n == 0:
                raise ValidationError(f"Código de asignatura no es numero primo: {self.codigo}")


if __name__ == "__main__":
    db = connect('ej_mongoengine')
    db.drop_database('ej_mongoengine')  # Borra datos antiguos

    python_book = Libro(isbn='9781593276034',
                        titulo='Python Crash Course',
                        autor='Eric Matthes',
                        editorial='No Starch Press')

    giw = Asignatura(nombre="GIW",
                     codigo=7,
                     temario=["web scraping", "REST", "seguridad"],
                     bibliografia=python_book)
    giw.profesor = "Enrique"  # Añadimos un campo en tiempo de ejecución
    # Ojo: notad que pylint lo detecta -> W0201: Attribute 'profesor' defined outside __init_
    print(giw.profesor)  # No lanza error
    giw.save()
    print()

    bd = Asignatura(nombre="BD", codigo=11)
    bd.save()

    for asig in Asignatura.objects:
        print(asig.codigo, asig.nombre)
    print()

    asig1 = Asignatura.objects.get(codigo=7)
    print(asig1)
    # print(asig1.profesor) # AttributeError: 'Asignatura' object has no attribute 'profesor'
    print()

    asig2 = Asignatura.objects.get(nombre='BD')
    print(asig2)
    print()

    asigs = Asignatura.objects(codigo__gt=10)  # Asignaturas con codigo > 25
    print(len(asigs))

    # Excepciones de get()
    ######################
    # asig3 = Asignatura.objects.get(codigo__gt=0)
    #     MultipleObjectsReturned: 2 or more items returned, instead of 1
    # asig3 = Asignatura.objects.get(codigo__gt=30)
    #     DoesNotExist: Asignatura matching query does not exist.
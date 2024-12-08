"""
Tests de unidad de la app. Se ejecutan con:
$ python manage.py test
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from opiniones.models import Opinion

class ModelsTest(TestCase):
    """ Ejemplo: tests de los modelos """

    def test_modelo_opinion(self):
        """ Comprueba la validación personalizada de Opinion """
        op = Opinion(puntuacion=2, texto="Muy malo")
        with self.assertRaises(ValidationError):
            op.full_clean()

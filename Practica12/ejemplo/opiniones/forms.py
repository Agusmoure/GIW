"""
Definición de formularios para validación
"""
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """Formulario para autenticar usuarios"""
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)


class OpinionForm(forms.Form):
    """Formulario para añadir opiniones"""
    puntuacion = forms.IntegerField(min_value=0, max_value=10, required=True, label="Tu puntuación")
    texto = forms.CharField(max_length=200, label='Tu comentario')

    def clean_texto(self):
        """Limpieza personalizada: texto en minúsculas"""
        return self.cleaned_data['texto'].lower()

    def clean(self):
        """ Validación de varios campos: puntuacion y texto """
        cleaned_data = super().clean()
        puntuacion_clean = cleaned_data.get("puntuacion")
        texto_clean = cleaned_data.get("texto")

        if (puntuacion_clean and texto_clean and puntuacion_clean < 5 and
                len(texto_clean.split()) < 5):
            raise ValidationError(
                "Puntuación negativa (<5) poco motivada. Es necesario incluir 5 o más palabras.")

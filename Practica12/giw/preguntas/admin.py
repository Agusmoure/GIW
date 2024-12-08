# Register your models here.

from django.contrib import admin
from preguntas.models import Pregunta
from preguntas.models import Respuesta

# Register your models here.
admin.site.register(Pregunta)
admin.site.register(Respuesta)
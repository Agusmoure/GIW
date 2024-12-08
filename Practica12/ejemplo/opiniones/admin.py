"""
Fichero para registrar qué objetos se manejaran en la interfaz de administración
"""

from django.contrib import admin
from opiniones.models import Opinion

# Register your models here.
admin.site.register(Opinion)

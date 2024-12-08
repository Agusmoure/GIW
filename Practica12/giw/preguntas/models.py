from django.db import models
from django.conf import settings

# Create your models here.

class Pregunta(models.Model):

    ident = models.BigAutoField(primary_key=True)

    titulo = models.CharField(max_length=250)
    texto = models.TextField(max_length=5000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def num_respuestas(self):
        return self.respuesta_set.count()

    def __str__(self):
        return self.titulo

class Respuesta(models.Model):

    ident = models.BigAutoField(primary_key=True)

    texto = models.TextField(max_length=5000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto[:50]
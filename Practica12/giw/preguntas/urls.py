"""
Definición de las rutas de la app, enlazando las funciones que las manejan
"""
from django.urls import path
from preguntas import views

app_name = "preguntas"

urlpatterns = [
    path('', views.lista_preguntas, name='lista_preguntas'),
    path('<int:pk>/', views.detalle_pregunta, name='detalle_pregunta'),
    path('<int:pk>/respuesta/', views.agregar_pregunta, name='agregar_pregunta'),
    path('login/', views.loginfunct, name='login'),
    path('logout/', views.logoutfunct, name='logout'),
    path('nueva/', views.agregar_pregunta, name='agregar_pregunta'),
]

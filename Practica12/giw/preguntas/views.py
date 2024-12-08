# Create your views here.

"""
Fichero con las funciones que manejan las peticiones HTTP
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from django.core.exceptions import ValidationError

from preguntas.forms import PreguntaForm, RespuestaForm, LoginForm
from preguntas.models import Pregunta, Respuesta

@require_GET
def lista_preguntas(request):
    """ Muestra la lista de preguntas, ordenadas por fecha (más nuevas primero) """
    preguntas = Pregunta.objects.order_by('-fecha_creacion')
    form = PreguntaForm() if request.user.is_authenticated else None
    return render(request, "lista_preguntas.html", {'preguntas': preguntas, 'form': form})


@login_required(login_url='preguntas:login')
@require_http_methods(["POST"])
def agregar_pregunta(request):
    """ Recibe un formulario y crea una nueva pregunta """
    form = PreguntaForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    titulo_f = form.cleaned_data['titulo']
    texto_f = form.cleaned_data['texto']

    pregunta = Pregunta(titulo=titulo_f, texto=texto_f, autor=request.user)

    try:
        pregunta.full_clean()
        pregunta.save()
    except ValidationError:
        return HttpResponseBadRequest("Pregunta mal formada")

    return redirect(reverse('preguntas:lista_preguntas'))


@login_required(login_url='preguntas:login')
@require_http_methods(["GET", "POST"])
def detalle_pregunta(request, pk):
    """ Muestra el detalle de una pregunta y permite añadir respuestas """
    pregunta = get_object_or_404(Pregunta, pk=pk)
    respuestas = pregunta.respuesta_set.order_by('-fecha_creacion')

    if request.method == "GET":
        form = RespuestaForm()
        return render(request, "detalle_pregunta.html", {'pregunta': pregunta, 'respuestas': respuestas, 'form': form})

    form = RespuestaForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    texto_f = form.cleaned_data['texto']

    respuesta = Respuesta(texto=texto_f, autor=request.user, pregunta=pregunta)

    try:
        respuesta.full_clean()
        respuesta.save()
    except ValidationError:
        return HttpResponseBadRequest("Respuesta mal formada")

    return redirect(reverse('preguntas:detalle_pregunta', kwargs={'pk': pk}))


@require_http_methods(["GET", "POST"])
def loginfunct(request):
    """ Muestra el formulario (GET) o realiza la autenticación (POST) """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('preguntas:lista_preguntas'))

    return render(request, "login.html", {
        'login_form': form,
        'error_message': "Usuario o contraseña incorrectos"
    })

    
@require_GET
def logoutfunct(request):

    logout(request)
    return redirect(reverse('preguntas:lista_preguntas'))

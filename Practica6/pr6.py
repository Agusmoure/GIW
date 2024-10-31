"""
Asignatura: GIW
Práctica 6
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

from datetime import datetime
import requests
def inserta_usuarios(datos, token):
    """ Inserta todos los usuarios de la lista
    devuelve cantidad de usuarios insertados correctamente """
    usuarios_insertados = 0
    for usuario in datos:
        response = requests.post('https://gorest.co.in/public/v2/users',
                                headers={'Authorization': f'Bearer {token}'},
                                data=usuario,timeout=600)
        if response.status_code == 201:
            usuarios_insertados += 1
    return usuarios_insertados

def get_ident_email(email, token):
    """ Devuelve el identificador del usuario cuyo email sea *exactamente* el pasado como parámetro.
        En caso de que ese usuario no exista devuelve None """
    response=requests.get('https://gorest.co.in/public/v2/users',
                            headers={'Authorization':f'Bearer {token}'},
                            timeout=600)
    users=response.json()
    for user in users:
        if user["email"]==email:
            return user["id"]
    return None

def borra_usuario(email, token):
    """ Elimina el usuario cuyo email sea *exactamente* el pasado como parámetro.
        En caso de éxito en el borrado devuelve True.
        Si no existe tal usuario devolverá False """
    user_id = get_ident_email(email,token)
    if user_id is None:
        return False
    response=requests.delete(f'https://gorest.co.in/public/v2/users/{user_id}',
                            headers={'Authorization':f'Bearer {token}'},
                            timeout=600)
    return response.status_code==204

def inserta_todo(email, token, title, due_on, status='pending'):
    """ Inserta un nuevo ToDo para el usuario con email exactamente igual al pasado.
    Si el ToDo ha sido insertado con éxito devolverá True, en otro caso devolverá False """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return False
    response = requests.post(f'https://gorest.co.in/public/v2/users/{user_id}/todos',
                            headers={'Authorization': f'Bearer {token}'},
                            data = {'title': title,
                                    'due_on': due_on,
                                    'status': status},
                            timeout=600
                            )
    return response.status_code == 201

def lista_todos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo
    asociados al usuario con el email pasado como parámetro """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return []
    response = requests.get(f'https://gorest.co.in/public/v2/users/{user_id}/todos',
                            headers={'Authorization': f'Bearer {token}'},
                            timeout=600)
    if response.status_code == 200:
        return response.json()
    return []

def lista_todos_no_cumplidos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el email
    pasado como parámetro que están pendientes (status=pending) y cuya fecha tope (due_on)
    es anterior a la fecha y hora actual.
    Para comparar las fechas solo hay que tener en cuenta el dia, la hora y los minutos;
    es decir, ignorar los segundos, microsegundos y el uso horario """
    user_id = get_ident_email(email, token)
    if user_id is None:
        return []
    todos = lista_todos(email, token)
    ahora = datetime.now().replace(second=0, microsecond=0)
    tareas_no_cumplidas = []
    for tarea in todos:
        if tarea['status'] == 'pending':
            fecha_due = datetime.strptime(tarea['due_on'][:16], '%Y-%m-%dT%H:%M')
            if fecha_due > ahora:
                tareas_no_cumplidas.append(tarea)
    return tareas_no_cumplidas

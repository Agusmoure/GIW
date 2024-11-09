"""
TODO: rellenar

Asignatura: GIW
Práctica X
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

from flask import Flask, request
app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###
# DUDA: Detecta pylint como constantes pero no son constantes
# DUDA: if demasiados largos pero en if no permite multilinea
asignaturas=[]
id_actual=0
def comprueba_horario(horario):
    """
    Devuelve si el horario es correcto
    y en caso de error cual es el fallo tambien
    """
    #Tiene exactamente las claves necesarias
    if len(horario)!=3:
        return False,"Algun horario no tiene suficientes claves o tiene mas de estas"
    #las claves son las necesarias
    if "dia" not in horario or "hora_inicio" not in horario or "hora_final" not in horario:
        return False, "Alguna de las claves del horario esta mal"
    #el valor de las claves son correctas
    if not isinstance(horario["dia"],str) or isinstance(horario["hora_inicio"],bool) or not isinstance(horario["hora_inicio"],int) or isinstance(horario["hora_final"],bool) or not isinstance(horario["hora_final"],int):
        return False,"Algun tipo del horario es incorrecto"
    return True, ""
def comprueba_asignatura(asignatura):
    """
    Devuelve si la asignatura es correcta
    en caso de no serlo devuelve el error tambien
    """
    #Solo tiene 3 claves
    if len(asignatura)!=3:
        return False,"numero de claves incorrecto"
    #Las claves son exactamente las necesarias
    if "nombre" not in asignatura or "numero_alumnos" not in asignatura or "horario" not in asignatura:
        return False,"alguna clave es erronea"
    #los valores de las claves son correctos
    if not isinstance(asignatura["nombre"],str) or isinstance(asignatura["numero_alumnos"],bool) or not isinstance(asignatura["numero_alumnos"],int) or not isinstance(asignatura["horario"],list):
        return False,"tipos incorrectos"
    for fecha in asignatura["horario"]:
        correcta,mensaje=comprueba_horario(fecha)
        if not correcta:
            return False,mensaje
    return True, ""
def get_asignatura_codigo(codigo):
    """
    Devuelve si ha encontrado la asignatura con el codigo asociado
    en caso positivo tambien devuelve la asignatura
    """
    found=False
    asig_encontrada={}
    for asignatura in asignaturas:
        if asignatura["id"]==codigo:
            found=True
            asig_encontrada=asignatura
            break
    return found,asig_encontrada
#Seccion de /asignaturas
@app.route('/asignaturas',methods=['DELETE'])
def delete_all():
    """
    Elimina todas las asignaturas
    """
    asignaturas.clear()
    return ('',204)

@app.route('/asignaturas', methods=['POST'])
def post_asignatura():
    """
    Si la asignatura esta bien formada la añade 
    {
        "id": int,
        "nombre": str,
        "numero_alumnos": int,
        "horario: [
            {
                "dia": str,
                "hora_inicio": int,
                "hora_final": int
            }
        ]

    """
    asignatura=request.get_json()
    correcta, mensaje=comprueba_asignatura(asignatura)
    if not correcta:
        return (mensaje, 400)
    #https://stackoverflow.com/questions/35309042/python-how-to-set-global-variables-in-flask
    global id_actual
    asignatura["id"]= id_actual
    asignaturas.append(asignatura)
    id_actual+=1
    return ({"id":asignatura["id"]},201)

@app.route('/asignaturas',methods=["GET"])
def get_global():
    """
    Devuelve las asignaturas pedidas
    """
    params=request.args
    #si no tiene parametros devuelve para evitar perder tiempo comparando
    if len(params)==0:
        response={"asignaturas":["/asignaturas/"+str(asignatura["id"])
                                    for asignatura in asignaturas]}
        return(response,200)
    #argumentos validos
    validos=("page","per_page","alumnos_gte")
    #Confirmamos que todos los parametros sean validos
    for param in params:
        if param not in validos:
            return("",400)
    #confirmamos que si viene page entonces vienen per_page y viceversa
    page_and_per_page= "page" in params and "per_page" in params
    page_and_per_page =page_and_per_page or ("per_page"not in params and "page" not in params)
    if not page_and_per_page:
        return ('',400)
    restantes=asignaturas
    #si hay numero de alum descartamos los que no cumplen
    if "alumnos_gte"in params:
        restantes=[asignatura for asignatura in asignaturas
                    if asignatura["numero_alumnos"]>=int(params["alumnos_gte"])]
    #si hay que ordenar por pagina selecionamos los necesarios
    if "page" in params:
        page=int(params["page"])
        per_page=int(params["per_page"])
        start=per_page*(page-1)
        end=start+per_page
        if start<=len(restantes):
            if end<len(restantes):
                restantes=restantes[start:end]
            else:
                restantes=restantes[start:]
        else:
            restantes=[]
    response={"asignaturas":["/asignaturas/"+str(asignatura["id"]) for asignatura in restantes]}
    if len(asignaturas)==len(restantes):
        return(response,200)
    return(response,206)

#Seccion de /asignaturas/X
@app.route('/asignaturas/<int:numero>',methods=["DELETE"])
def delete_asignatura(numero):
    """
    Elimina una asignatura
    """
    found,asignatura=get_asignatura_codigo(numero)
    if found:
        asignaturas.remove(asignatura)
        return("",204)
    return("",404)

@app.route('/asignaturas/<int:numero>',methods=["GET"])
def get_asignatura(numero):
    """
    Obtiene una asignatura
    """
    found, asignatura=get_asignatura_codigo(numero)
    if found:
        return(asignatura,200)
    return("",404)

@app.route('/asignaturas/<int:numero>',methods=["PUT"])
def put_asignatura(numero):
    """
    Cambia todos los datos de una asignatura
    """
    found,asignatura=get_asignatura_codigo(numero)
    if not found:
        return("",404)
    asignatura_nueva=request.get_json()
    correcta,mensaje=comprueba_asignatura(asignatura_nueva)
    if not correcta:
        return(mensaje,400)
    asignatura_nueva["id"]=asignatura["id"]
    asignaturas.remove(asignatura)
    asignaturas.append(asignatura_nueva)
    return("",200)
@app.route('/asignaturas/<int:numero>',methods=["PATCH"])
def patch_asignatura(numero):
    """
    Actualiza uno de los datos de la asignatura
    """
    found,asignatura=get_asignatura_codigo(numero)
    if not found:
        return("",404)
    validas=("nombre","horario","numero_alumnos")
    if len(request.get_json().keys())!=1:
        return ("",400)
    #keys no es una lista sino una dict_key si no no podemos acceder al
    #valor mediante [0]
    clave=list(request.get_json().keys())[0]
    if clave not in validas:
        return("",400)
    asignatura[clave]=request.get_json()[clave]
    return("",200)

#seccion de /asignaturas/X/horario
@app.route('/asignaturas/<int:numero>/horario',methods=["GET"])
def get_horario(numero):
    """
    Devuelve el horario de una asignatura
    """
    found,asignatura=get_asignatura_codigo(numero)
    if not found:
        return("",404)
    return ({"horario":asignatura["horario"]},200)
if __name__ == '__main__':
    # Activa depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    app.run()

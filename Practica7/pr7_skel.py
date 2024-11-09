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

from flask import Flask, request, session, render_template
app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###
# DUDA: Detecta pylint como constantes pero no son constantes
asignaturas=[]
id_actual=0
@app.route('/asignaturas',methods=['DELETE'])
def delete_all():
    """
    Elimina todas las asignaturas
    """
    asignaturas.clear()
    return ('',204)

def comprueba_horario(horario):
    """
    Devuelve si el horario es correcto
    y en caso de error cual es el fallo
    """
    if len(horario)!=3:
        return False,"Algun horario no tiene suficientes claves o tiene mas de estas"
    if "dia" not in horario or "hora_inicio" not in horario or "hora_final" not in horario:
        return False, "Alguna de las claves del horario esta mal"
    if not isinstance(horario["dia"],str) or isinstance(horario["hora_inicio"],bool) or not isinstance(horario["hora_inicio"],int) or isinstance(horario["hora_final"],bool) or not isinstance(horario["hora_final"],int):
        return False,"Algun tipo del horario es incorrecto"
    return True, ""
def comprueba_asignatura(asignatura):
    """
    Devuelve si la asignatura es correcta
    en caso de no serlo devuelve el error
    """
    if len(asignatura)!=3:
        return False,"numero de claves incorrecto"
    if "nombre" not in asignatura or "numero_alumnos" not in asignatura or "horario" not in asignatura:
        return False,"alguna clave es erronea"
    if not isinstance(asignatura["nombre"],str) or isinstance(asignatura["numero_alumnos"],bool) or not isinstance(asignatura["numero_alumnos"],int) or not isinstance(asignatura["horario"],list):
        return False,"tipos incorrectos"
    for fecha in asignatura["horario"]:
        correcta,mensaje=comprueba_horario(fecha)
        if not correcta:
            return False,mensaje
    return True, ""
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
    if len(params)==0:
        response={"asignaturas":["/asignaturas/"+str(asignatura["id"])
                                    for asignatura in asignaturas]}
        return(response,200)
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
        print(start)
        print(end)
        print("peticion")
        if start<=len(restantes):
            if end<len(restantes):
                restantes=restantes[start:end]
            else:
                restantes=restantes[start:]
        else:
            restantes=[]
    response={"asignaturas":["/asignaturas/"+str(asignatura["id"]) for asignatura in restantes]}
    print("restantes:")
    print(response)
    if len(asignaturas)==len(restantes):
        return(response,200)
    return(response,206)
if __name__ == '__main__':
    # Activa depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'

    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'

    app.run()

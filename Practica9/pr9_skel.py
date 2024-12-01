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
from mongoengine import connect, Document, StringField, EmailField
import bcrypt
from urllib.parse import unquote
import pyotp
import pyotp.utils
import qrcode
import base64
from io import BytesIO
# Resto de importaciones


app = Flask(__name__)
records=connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **
class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#
from pprint import pprint
def from_form_get_dict(form):

    splited=form.split('&')
    dicc={}
    for pareja in splited:
        pareja=pareja.split('=')
        dicc[pareja[0]]=pareja[1]
    return dicc

def signup_validation(request):
#TODO en lugar de hacer un dict podriamos hacer una segunda funcion directamente un user eso hace las cosas mas eficientes
    dicc=from_form_get_dict(request.get_data(as_text=True))
    nick = dicc.get("nickname")
    full_name = dicc.get("full_name")
    password = dicc.get("password")
    passwordrpt = dicc.get("password2")
    email = unquote(dicc.get("email"))
    country=dicc.get("country")
    print(email)
    aux=User.objects(user_id=nick)
    if len(aux)>0 :
        msg = 'El usuario ya existe'
        print(msg)
        #TODO es necesario hacer templates o se puede hacer asi?
        return False,msg,409,None

    if password != passwordrpt:
        msg = 'Las contraseñas no coinciden'
        print(msg)
        return False,msg,400,None
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user =User( user_id=nick,full_name=full_name, country= country,email=  email, passwd=hashed.decode('utf-8') )
    user.save()
    return True,f"Bienvenido usuario {full_name}",201,user 
        # render_template('Welcome.html.jinja', name=full_name)
        # print("user created")
        # return("Usuario creado",201)

@app.route('/signup', methods=['POST'])
def signup():
    could_create,msg,code,user=signup_validation(request)
    return (msg,code)

@app.route('/change_password', methods=['POST'])
def change_password():
    dicc=from_form_get_dict(request.get_data(as_text=True))
    nick = dicc.get("nickname")
    password = dicc.get("old_password")
    newPassword = dicc.get("new_password")
    
    nick_found = User.objects(user_id= nick)
    print(nick_found)
    if len(nick_found)<=0:
        return("Usuario o contraseña incorrectos",409)
    #TODO preguntar si debemos ignorar este caso
    if password is newPassword:
        return ("La nueva contraseña no puede ser la antigua contraseña",400)
    user=nick_found[0]
    if not bcrypt.checkpw(password.encode('utf-8'),user.passwd.encode('utf-8')):
        return("Usuario o contraseña incorrectos",409)
    hashed = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
    User.objects(user_id=nick).update(set__passwd=hashed.decode('utf-8'))
    return (f"La contraseña de {nick} ha sido modificada",201)

def login_validation(request):
    dicc=from_form_get_dict(request.get_data(as_text=True))
    nick = dicc.get("nickname")
    password = dicc.get("password")
    totp=dicc.get("topt",None)
    users = User.objects(user_id= nick)
    if len(users)>0:
        user=users[0]
        passwordcheck = user.passwd.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            if totp is None:
                return True,f'Bienvenido {user.full_name}',200
            else:
                totp_generated=pyotp.TOTP(user.totp_secret)
                if totp_generated.verify(totp):
                    return True,f'Bienvenido {user.full_name}',200

    return False, "Usuario o contraseña incorrectos",400

@app.route('/login', methods=['POST'])
def login():
    login_correct,msg,code=login_validation(request)
    return (msg,code)
##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR

# Mediante la biblioteca pyotp creamos un codigo en base 32 y lo almacenamos con el usuario,
# tras ello se genera una url teniendo en cuenta el nickname del usuario y su numero secreto,
# con la biblioteca de qrcode convertimos esa url en un codigo qr, y posteriormente mediante base64
# guardamos los bytes que forman la imagen para pasarselo a la web y que esta genere el código qr


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    could_create,msg,code,user=signup_validation(request)
    if not could_create:
        return (msg,code)
    random_32=pyotp.random_base32()
    User.objects(user_id=user.user_id).update(set__totp_secret=random_32)
    uri= pyotp.utils.build_uri(random_32,user.user_id)   
    qr=qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_img_bytes = base64.b64encode(buffered.getvalue()).decode()
    return render_template("QR.html.jinja",name=user.full_name,image=f"data:image/png;base64, {qr_img_bytes}") 
    #return (f"Usuario: {user.user_id}, secreto:{random_32}",201)

@app.route('/login_totp', methods=['POST'])
def login_totp():
    login_correct,msg,code=login_validation(request)
    if not login_correct:
        return (msg,code)
    return (msg,code)

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

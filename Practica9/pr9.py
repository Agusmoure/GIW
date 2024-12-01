"""


Asignatura: GIW
Práctica 9
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

from urllib.parse import unquote
import base64
from io import BytesIO
from flask import Flask, request, render_template
from mongoengine import connect, Document, StringField, EmailField
import bcrypt
import pyotp
import pyotp.utils
import qrcode

app = Flask(__name__)
records=connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **
class User(Document):
    """
    Clase de usuario
    """
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)

def from_form_get_dict(form):
    """
    Devuelve un diccionario desde un form
    """
    splited=form.split('&')
    dicc={}
    for pareja in splited:
        pareja=pareja.split('=')
        dicc[pareja[0]]=pareja[1]
    return dicc

def signup_validation(request_arg):
    """
    Valida la creacion de un usuario devolviendo,
    si lo consigue,
    el mensaje,
    el codigo de servidor,
    el usuario en caso de conseguirlo
    """
    dicc=from_form_get_dict(request_arg.get_data(as_text=True))
    nick = dicc.get("nickname")
    full_name = dicc.get("full_name")
    password = dicc.get("password")
    passwordrpt = dicc.get("password2")
    email = unquote(dicc.get("email"))
    country=dicc.get("country")
    aux=User.objects(user_id=nick)
    if len(aux)>0 :
        msg = 'El usuario ya existe'
        return False,msg,409,None

    if password != passwordrpt:
        msg = 'Las contraseñas no coinciden'
        print(msg)
        return False,msg,400,None
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user =User( user_id=nick,full_name=full_name, country= country
                ,email=  email, passwd=hashed.decode('utf-8') )
    user.save()
    return True,f"Bienvenido usuario {full_name}",201,user

@app.route('/signup', methods=['POST'])
def signup():
    """
    Contola el servidor en la peticion post a signup
    """
    could_create,msg,code,user=signup_validation(request)
    if could_create:
        return render_template("Welcome.html.jinja",name=user.full_name),code
    return render_template("Fail.html.jinja",msg=msg),code

@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Gestiona si puede cambiar la contraseña o no
    """
    dicc=from_form_get_dict(request.get_data(as_text=True))
    nick = dicc.get("nickname")
    password = dicc.get("old_password")
    new_password = dicc.get("new_password")
    nick_found = User.objects(user_id= nick)
    print(nick_found)
    if len(nick_found)<=0:
        return render_template("Fail.html.jinja",msg="Usuario o contraseña incorrectos"),400
    if password is new_password:
        # TODO: DUDA ignorar este caso?
        return render_template("Fail.html.jinja",
                                msg="La nueva contraseña no puede ser la antigua contraseña"),400
    user=nick_found[0]
    if not bcrypt.checkpw(password.encode('utf-8'),user.passwd.encode('utf-8')):
        return render_template("Fail.html.jinja",
                msg="Usuario o contraseña incorrectos"),400
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    User.objects(user_id=nick).update(set__passwd=hashed.decode('utf-8'))
    return render_template("PasswordChange.html.jinja",nick=nick),200

def login_validation(request_arg):
    """
    Valida el login
    """
    dicc=from_form_get_dict(request_arg.get_data(as_text=True))
    nick = dicc.get("nickname")
    password = dicc.get("password")
    totp=dicc.get("totp",None)
    print(dicc)
    users = User.objects(user_id= nick)
    if len(users)>0:
        user=users[0]
        passwordcheck = user.passwd.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            if totp is None:
                return True,f'Bienvenido {user.full_name}',200,user
            totp_generated=pyotp.TOTP(user.totp_secret)
            if totp_generated.verify(totp):
                return True,f'Bienvenido {user.full_name}',200,user

    return False, "Usuario o contraseña incorrectos",400,None

@app.route('/login', methods=['POST'])
def login():
    """Gestiona la peticion post de login"""
    could_login,msg,code,user=login_validation(request)
    if not could_login:
        return render_template("Fail.html.jinja",msg=msg),code
    return render_template("WelcomeLogin.html.jinja",name=user.full_name),code

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
    """Gestiona la peticion Post a signup_totp"""
    could_create,msg,code,user=signup_validation(request)
    if not could_create:
        return render_template("Fail.html.jinja",msg=msg)
    random_32=pyotp.random_base32()
    User.objects(user_id=user.user_id).update(set__totp_secret=random_32)
    uri= pyotp.utils.build_uri(random_32,user.user_id)
    qr_code=qrcode.make(uri)
    buffered = BytesIO()
    qr_code.save(buffered, format="PNG")
    qr_img_bytes = base64.b64encode(buffered.getvalue()).decode()
    return render_template("QR.html.jinja",nick=user.user_id,secret=random_32,
                            image=f"data:image/png;base64, {qr_img_bytes}"),code

@app.route('/login_totp', methods=['POST'])
def login_totp():
    """Gestiona la peticion post a login_totp"""
    login_correct,msg,code,user=login_validation(request)
    if not login_correct:
        return render_template("Fail.html.jinja",msg=msg),code
    return render_template("WelcomeLogin.html.jinja",name=user.full_name),code

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

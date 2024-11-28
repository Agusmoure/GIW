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
# Resto de importaciones


app = Flask(__name__)
connect('giw_auth')


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


@app.route('/signup', methods=['POST'])
def signup():
    nick = request.args.get("nickname");
    full_name = request.args.get("full_name");
    password = request.args.get("password");
    passwordrpt = request.args.get("password2");
    email = request.args.get("email");

    nick_exist = records.find_one({"nickname": nick})
    if (nick_exist):
    	msg = 'El usuario ya existe';
    	render_template('signup', message=msg);

    if password != password2:
    	msg = 'Las contraseñas no coinciden';
    	render_template('signup', message=msg);
    else:
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		user = {'user_id': nick, 'full_name': full_name, 
		'country': country, 'email': email, 'passwd': hashed }
		records.insert_one(user)

		return render_template('welcome.html', name=full_name);

	return render_template('login.html')




@app.route('/change_password', methods=['POST'])
def change_password():
    nick = request.form.get("nickname")
    password = request.form.get("old_password")
    newPassword = request.form.get("new_password")
       
    nick_found = records.find_one({"nickname": nick})
        if nick_found:
            nick_val = nick_found['nickname']
            passwordcheck = nick_found['password']
      
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                hashed = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
				records.update_one({nickname: nick}, {passwd: hashed});


                return render_template('passchanged.html', name=nick)
        else:
            message = 'Usuario o contraseña incorrectos'
            return render_template('change_pass.html', message=message)
 	return render_template('change_pass.html')
           
@app.route('/login', methods=['POST'])
def login():
    nick = request.form.get("nickname")
    password = request.form.get("password")

       
    nick_found = records.find_one({"nickname": nick})
        if nick_found:
            email_val = nick_found['email']
            passwordcheck = nick_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                return render_template('welcome.html', name=nick_found['full_name']);
            else:
                message = 'Contraseña incorrecta'
                return render_template('login.html', message=message)
        else:
            message = 'Usuario incorrecto'
            return render_template('login.html', message=message)
    return render_template('login.html')
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    ...
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    ...
  

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

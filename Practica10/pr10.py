"""

Asignatura: GIW
Práctica 10
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

import base64
import json
import secrets

from flask import Flask, request, session
import requests

app = Flask(__name__)

# Credenciales
CLIENT_ID = '542634645519-b1nf875cu02igg3q1qlcfqtqs1dr1dft.apps.googleusercontent.com'
CLIENT_SECRET = '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'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

def get_google_endpoints():
    """Obtiene los endpoints de autorización y token de Google."""
    response = requests.get(DISCOVERY_DOC, timeout=10)
    discovery_data = response.json()
    return discovery_data["authorization_endpoint"], discovery_data["token_endpoint"]

@app.route('/login_google', methods=['GET'])
def login_google():
    """Inicia sesión con Google"""
    state = secrets.token_urlsafe(16)
    session['state'] = state

    auth_endpoint, _ = get_google_endpoints()
    auth_url = (
        f"{auth_endpoint}?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"scope=openid%20email&"
        f"state={state}&"
        f"redirect_uri={REDIRECT_URI}"
    )
    return f"""
    <html>
        <head>
            <title>Login con Google</title>
        </head>
        <body>
            <h1>Inicia sesión con Google</h1>
            <a href="{auth_url}">
                <button>Login con Google</button>
            </a>
        </body>
    </html>
    """


@app.route('/token', methods=['GET'])
def token():
    """Procesa el token de Google después del inicio de sesión"""
    code = request.args.get("code")
    state = request.args.get("state")

    if state != session.get('state'):
        return "Error: el token CSRF no coincide", 400

    _, token_endpoint = get_google_endpoints()
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_endpoint, data=token_data, timeout=10)
    token_json = token_response.json()
    id_token = token_json.get("id_token")

    if not id_token:
        return "Error: No se pudo obtener el id_token", 400

    payload = id_token.split(".")[1]
    resto = len(payload) % 4
    payload += "=" * (4 - resto)
    decoded_payload = base64.urlsafe_b64decode(payload).decode("utf-8")
    user_info = json.loads(decoded_payload)

    email = user_info.get("email", "desconocido")
    return f"<h1>Bienvenido {email}</h1>"


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

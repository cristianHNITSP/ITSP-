from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

# Verificar si el archivo usuarios.json existe
if not os.path.exists('usuarios.json'):
    with open('usuarios.json', 'w') as file:
        json.dump([], file)

try:
    with open('usuarios.json', 'r') as file:
        usuarios = json.load(file)
except FileNotFoundError:
    usuarios = []

bp = Blueprint('auth', __name__, url_prefix='/auth')

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import json
import os

# Verificar si el archivo usuarios.json existe
if not os.path.exists('usuarios.json'):
    with open('usuarios.json', 'w') as file:
        json.dump([], file)

try:
    with open('usuarios.json', 'r') as file:
        usuarios = json.load(file)
except FileNotFoundError:
    usuarios = []

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar si el nombre de usuario ya existe
        for user in usuarios:
            if user['username'] == username:
                return render_template('auth/register.html', error_username='El nombre de usuario ya existe.')

        # Agregar el nuevo usuario a la lista de usuarios
        usuarios.append({"username": username, "email": email, "password": generate_password_hash(password)})

        # Guardar la lista de usuarios en el archivo JSON
        try:
            with open('usuarios.json', 'w') as file:
                json.dump(usuarios, file, indent=4)
        except Exception as e:
            return render_template('auth/register.html', error_register='Error al guardar los datos: {}'.format(e))
        
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Cargar los usuarios desde el archivo JSON
        try:
            with open('usuarios.json', 'r') as file:
                usuarios = json.load(file)
        except FileNotFoundError:
            usuarios = []

        # Buscar el usuario en la lista de usuarios
        for user in usuarios:
            if user.get('username') == username:
                stored_password_hash = user.get('password')
                # Verificar si la contraseña ingresada coincide con la contraseña almacenada
                if check_password_hash(stored_password_hash, password):
                    # Inicio de sesión exitoso
                    return redirect(url_for('index'))  # Redirigir a la página principal después del inicio de sesión

        # Si el nombre de usuario no existe o la contraseña es incorrecta, mostrar mensaje de error
        error_message = 'Nombre de usuario o contraseña incorrectos.'
        return render_template('auth/login.html', error_message=error_message)

    # Si se realiza una solicitud GET, renderizar la página de inicio de sesión
    return render_template('auth/login.html')
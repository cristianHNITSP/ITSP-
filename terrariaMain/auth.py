from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
#import json
#import os
import pyodbc

# Verificar si el archivo usuarios.json existe
#if not os.path.exists('usuarios.json'):
#    with open('usuarios.json', 'w') as file:
#        json.dump([], file)

#try:
#    with open('usuarios.json', 'r') as file:
#        usuarios = json.load(file)
#except FileNotFoundError:
#    usuarios = []

#bp = Blueprint('auth', __name__, url_prefix='/auth')

# Verificar si el archivo usuarios.json existe
#if not os.path.exists('usuarios.json'):
#    with open('usuarios.json', 'w') as file:
#        json.dump([], file)

#try:
#    with open('usuarios.json', 'r') as file:
#        usuarios = json.load(file)
#except FileNotFoundError:
#    usuarios = []

bp = Blueprint('auth', __name__, url_prefix='/auth')
logged_in = False

@bp.route('/register', methods=['GET', 'POST'])
def register():
    error_message_email = None
    error_message_username = None

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Obtener la conexión desde la aplicación
        connection_string = current_app.config['CONNECTION_STRING']

        # Verificar si el correo electrónico ya está registrado en la base de datos
        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tb_users_data WHERE i_email = ?", email)
                existing_email = cursor.fetchone()
                if existing_email:
                    error_message_email = 'El correo electrónico ya está registrado.'
                    return render_template('auth/register.html', error_message_register=error_message_email)

        # Verificar si el nombre de usuario ya existe en la base de datos
        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tb_users_data WHERE i_names = ?", username)
                existing_user = cursor.fetchone()
                if existing_user:
                    error_message_username = 'El nombre de usuario ya existe.'
                    return render_template('auth/register.html', error_message_register=error_message_username)

        # Si no hay errores, proceder con el registro
        if not error_message_email and not error_message_username:
            # Hashear la contraseña antes de guardarla en la base de datos
            hashed_password = generate_password_hash(password)

            # Intentar conectarse a la base de datos y agregar el nuevo usuario
            try:
                with pyodbc.connect(connection_string) as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO tb_users_data (i_email, i_names, i_passwords) VALUES (?, ?, ?)", email, username, hashed_password)
                        connection.commit()
                        return redirect(url_for('auth.login'))
            except pyodbc.Error as e:
                # Manejar cualquier error de la base de datos
                error_message_email = 'Error en el registro: {}'.format(str(e))
                return render_template('auth/register.html', error_message_register=error_message_email)

    return render_template('auth/register.html')


import json
import os
import random
import string

# Directorio donde se guardará el archivo JSON
SESSIONS_DIR = 'sessions'
SESSIONS_FILE = 'active_sessions.json'

# Verificar y crear el directorio si no existe
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

# Ruta completa del archivo JSON
SESSIONS_PATH = os.path.join(SESSIONS_DIR, SESSIONS_FILE)

# Función para cargar las sesiones desde el archivo JSON
def load_sessions():
    if os.path.exists(SESSIONS_PATH):
        with open(SESSIONS_PATH, 'r') as file:
            return json.load(file)
    else:
        # Si el archivo no existe, devuelve una lista vacía
        return []

# Función para guardar las sesiones en el archivo JSON
def save_sessions(sessions):
    with open(SESSIONS_PATH, 'w') as file:
        json.dump(sessions, file)

# Verificar si el archivo JSON existe al inicio y crear uno nuevo si no existe
if not os.path.exists(SESSIONS_PATH):
    save_sessions([])

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            connection_string = current_app.config['CONNECTION_STRING']
            with pyodbc.connect(connection_string) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT i_passwords, i_is_authenticated FROM tb_users_data WHERE i_names = ?", username)
                    row = cursor.fetchone()

                    if row:
                        stored_password_hash, is_authenticated = row
                        if check_password_hash(stored_password_hash, password):
                            if is_authenticated:
                                error_message = 'El usuario ya ha iniciado sesión.'
                                print(error_message)
                                return render_template('auth/login.html', error_message=error_message)

                            # Verificar si hay otro usuario autenticado en la misma máquina
                            cursor.execute("SELECT COUNT(*) FROM tb_users_data WHERE i_is_authenticated = 1")
                            num_authenticated_users = cursor.fetchone()[0]

                            if num_authenticated_users > 0:
                                error_message = 'Ya hay otro usuario iniciado sesión en esta máquina.'
                                print(error_message)
                                return render_template('auth/login.html', error_message=error_message)

                            # Generar una clave especial
                            special_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

                            # Marcar al usuario como autenticado en la base de datos
                            cursor.execute("UPDATE tb_users_data SET i_is_authenticated = 1 WHERE i_names = ?", username)
                            connection.commit()

                            # Cargar sesiones existentes
                            sessions = load_sessions()

                            # Agregar la sesión activa al formato requerido
                            sessions.append({"username": username, "KEY_SESSION": special_key})

                            # Guardar las sesiones en el archivo JSON
                            save_sessions(sessions)

                            # Renderizar la página de inicio después de iniciar sesión exitosamente
                            return render_template('index.html', logged_in=True, username=username, special_key=special_key)
                        else:
                            # Llamar a la función especial con el usuario y el estado de inicio de sesión
                            return render_template('index.html', logged_in=False)
        except pyodbc.Error as e:
            error_message = 'Error al autenticar el usuario: {}'.format(str(e))
            return render_template('auth/login.html', error_message=error_message)

        error_message = 'Nombre de usuario o contraseña incorrectos.'
        return render_template('auth/login.html', error_message=error_message, has_error=error_message is not None, on_login_page=True)

    return render_template('auth/login.html', on_login_page=True)

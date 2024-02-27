from flask import (Blueprint, render_template, request, url_for, redirect, flash)
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

from flask import (Blueprint, render_template, request, url_for, redirect, flash)
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

# Verificar si el archivo usuarios.json existe
if not os.path.exists('usuarios.json'):
    with open('usuarios.json', 'w') as file:
        json.dump({}, file)

try:
    with open('usuarios.json', 'r') as file:
        usuarios = json.load(file)
except FileNotFoundError:
    usuarios = {}

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('usuarios.json', 'r') as file:
            data = json.load(file)

        if username in data:
            return render_template('auth/register.html', error='El nombre de usuario ya existe')

        # Agregar el nuevo usuario al archivo JSON
        with open('usuarios.json', 'w') as file:
            data[username] = password
            json.dump(data, file)
        
        return render_template('auth/register.html')

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    return render_template('auth/login.html', username=username, password=password)
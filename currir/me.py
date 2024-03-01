from flask import Blueprint, render_template

bp = Blueprint('sobremi', __name__, url_prefix='/sobremi')

@bp.route('/infperso')
def inf ():
    return render_template('me/sobremi.html')

@bp.route('/mispasi')
def pasiones ():
    return render_template('me/pasi.html')

@bp.route('/miformacion')
def formacion ():
    return render_template('me/formacion.html')

@bp.route('/contacto')
def contacto ():
    return render_template('me/contacto.html')
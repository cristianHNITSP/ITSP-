from flask import Blueprint

bp = Blueprint('works', __name__, url_prefix='/works')

@bp.route('/list')
def list ():
    return"lista de trabajos"

@bp.route('/create')
def create ():
    return"crear tareas"


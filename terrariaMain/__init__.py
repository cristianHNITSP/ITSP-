from flask import Flask, render_template, send_from_directory

def create_app():
    app = Flask(__name__)

    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRETE_KEY = 'dev',
        CONNECTION_STRING = 'DRIVER={SQL Server};SERVER=IDEAPAD_CRIS;DATABASE=db_users;UID=sa;PWD=pwd_prac'
        )

    #registrar blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import account
    app.register_blueprint(account.bp)

    #insertar img en el server local
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/')
    def index ():
        return render_template('index.html')
    
    return app
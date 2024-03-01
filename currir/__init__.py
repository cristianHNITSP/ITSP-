from flask import Flask, render_template, send_from_directory

def create_app():
    app = Flask(__name__)

    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRETE_KEY = 'dev'
    )

    #registrar blueprint
    from . import me
    app.register_blueprint(me.bp) 

    from . import auth
    app.register_blueprint(auth.bp) 

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/')
    def index ():
        return render_template('index.html')
    
    return app
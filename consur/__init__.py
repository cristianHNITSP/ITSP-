from flask import Flask

def create_app():
    app = Flask(__name__)

    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRETE_KEY = 'dev'
    )

    @app.route('/')
    def index ():
        return 'Hola mundo :)'
    
    return app
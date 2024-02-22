from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRETE_KEY = 'dev'
    )

    #registrar blueprint
    from . import works
    app.register_blueprint(works.bp) 

    from . import auth
    app.register_blueprint(auth.bp) 

    @app.route('/')
    def index ():
        return render_template('index.html')
    
    return app

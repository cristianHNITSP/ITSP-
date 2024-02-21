from flask import Flask, render_template #Es para importar flask

app = Flask(__name__) 

@app.route('/index')
def index():
    data={
        'titulo':'Mi primera plantilla',
        'mensaje':'Bienvenido al sitio web',
        'nombre':'Cristian Hernández Novelo'
    } #Declaración de diccionario
    return render_template('index.html',data=data)
app.run(debug=True)  


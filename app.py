#API EVENTICKONES
#Aplicación en python que muestra información desde un servicio web de la DISCOVERY API de ticketmaster

#Importamos lo que vamos a necesitar de flask
from flask import Flask, render_template,abort
# Importamos la libreria os del sistema para utilizar environ
import os 
# La aplicación nos va permitir mostrar la información del fichero books.json
# Por tanto, importamos json para leer el fichero 
import json 

# Definimos la variable app por Flask
app = Flask(__name__)

# Definimos la ruta principal de la página de incio 
@app.route('/',methods=["GET","POST"])
def inicio():
	return render_template("index.html")

#Probar en el entorno de desarrollo
app.run(debug=True)

#Para desplegar en heroku		
#port=os.environ["PORT"]
#app.run('0.0.0.0', int(port), debug=False)

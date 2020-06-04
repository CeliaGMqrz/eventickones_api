#API EVENTICKONES
#Aplicación en python que muestra información desde un servicio web de la DISCOVERY API de ticketmaster

#Importamos lo que vamos a necesitar de flask
from flask import Flask, render_template,abort,request
#Importamos la librería request
import requests
# Importamos la libreria os del sistema para utilizar environ
import os 
# Importamos json
import json
#Importar las fechas
from datetime import datetime

with open("paises.json") as fichero:
    info=json.load(fichero)

# Definimos la variable app por Flask
app = Flask(__name__)
#Guardamos la url base
url_base="https://app.ticketmaster.com/discovery/v2/"

# Definimos la ruta principal de la página de incio 
@app.route('/',methods=["GET","POST"])
def inicio():
    #En una variable key, guardamos por el diccionario os.environ nuestra key
    key=os.environ["apikey"]
    #Creamos el diccionario con los parámetros necesarios
    payload = {'apikey':key}
    #Guardamos la petición en una variable(urlbase + diccionario con parametros)
    r=requests.get(url_base+'events',params=payload)
    #Guardamos los paises a partir del fichero json
    paises=[]
    for i in info:
    	paises.append(str(i))
    #Si el método por el que accedimos es GET:
    if r.status_code == 200:
        #Guardamos el contenido en json
        contenido = r.json()
        if request.method=="GET":
            return render_template("index.html", paises=paises)
        else:
            abort(404)

#Probar en el entorno de desarrollo
app.run(debug=True)

#Para desplegar en heroku		
#port=os.environ["PORT"]
#app.run('0.0.0.0', int(port), debug=False)

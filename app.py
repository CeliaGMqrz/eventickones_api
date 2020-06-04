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

#Funcion que devuelve datos según el artista
def ev_artista (palabra_clave):
		    #Creamos el diccionario con los parámetros necesarios
		    payload = {'apikey':key,'keyword':palabra_clave}
		    #Guardamos la petición en una variable(urlbase + diccionario con parametros)
		    r=requests.get(url_base+'events',params=payload)
		    #Inicializamos las listas necesarias
		    nombres=[]
		    fechas=[]
		    horas=[]
		    salas=[]
		    direccion=[]
		    ciudades=[]
		    paises=[]
		    urls=[]
		    urls_sala=[]
		    numelementos=0
		    #Comprobamos que la peticion es correcta
		    if r.status_code == 200:
		        url_gestionada=r.url
		        #Guardamos el contenido en json
		        contenido = r.json()
		        # Si la palabra clave no está en la variable guardada imprime un mensaje
		        noms=[]
		        for i in contenido["_embedded"]["events"]:
		            noms.append(i["name"])
		        for nombre in noms:
		            if palabra_clave.upper() not in nombre.upper():
		                mensaje=("No hay eventos para esa búsqueda")
		                return mensaje
		        else:
		            #Para cada elemento en el contenido añadimos la informacion a las listas
		            for elem in contenido["_embedded"]["events"]:
		                #NOMBRES
		                nombres.append(elem["name"])
		                #CIUDADES
		                ciudades.append(elem["_embedded"]["venues"][0]["city"]["name"])
		                #PAISES
		                paises.append(elem["_embedded"]["venues"][0]["country"]["name"])
		                #SALAS
		                salas.append(elem["_embedded"]["venues"][0]["name"])
		                #DIRECCIONES
		                if "address" in elem["_embedded"]["venues"][0]:
		                    direccion.append(elem["_embedded"]["venues"][0]["address"]["line1"])
		                else:
		                    direccion.append("NO ESPECIFICADA")
		                #FECHAS
		                fechas.append(elem["dates"]["start"]["localDate"])
		                #HORAS: A veces la hora no esta especificada así que nos aseguramos de ello.
		                if "localTime" in elem["dates"]["start"]:
		                    horas.append(elem["dates"]["start"]["localTime"])
		                else:
		                    horas.append("NO ESPECIFICADA")
		                #URLS
		                urls.append(elem["url"])
		                urls_sala.append(elem["_embedded"]["venues"][0]["url"])
		                if elem["_embedded"]["venues"][0]["url"]:
		                    numelementos=numelementos+1
		            filtro=[nombres,paises,ciudades,salas,direccion,fechas,horas,urls,urls_sala,numelementos]
		        return filtro




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
            try:
                artista=request.form.get("name")
            except:
                abort(404)

            pais=request.form.get("pais")

            #Función que recibe el nombre del artista y devuelve todos los eventos proximos del mismo
            #Si lo que devuelve la funcion no es una lista devuelve un mensaje.
            if type(ev_artista(artista)) != list:
                return render_template("index.html", mensaje=(ev_artista(artista)))
            #Si no, impime el contenido
            else:
                #devuelve el filtro
                return render_template("index.html", filtro=(ev_artista(artista)))
    else:
        abort(404)

#Probar en el entorno de desarrollo
app.run(debug=True)

#Para desplegar en heroku		
#port=os.environ["PORT"]
#app.run('0.0.0.0', int(port), debug=False)

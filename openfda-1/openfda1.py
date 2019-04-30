import http.client
import json

headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection("api.fda.gov")  #Conexión con la pagina con toda la información de los medicamentos
conexion.request("GET", "/drug/label.json?limit=10", None, headers) #URL para poder buscar los medicamentos, estableciendo el limite en 10.
r1 = conexion.getresponse()
print(r1.status, r1.reason)
respuesta = r1.read().decode("utf-8")
conexion.close()

respuesta2 = json.loads(respuesta)

#Obtaining the id, purpose and manufacturer name from one drug
print("La ID del medicamento es:", respuesta2['results'][8]['id'])   #Si cambiamos el numero nos da los datos de cada medicamento que pongamos.
print("El medicamento sirve para:", respuesta2['results'][8]['purpose'])
print("El nombre del fabricante es:", respuesta2['results'][8]['openfda']['manufacturer_name'])  #los nombres de manufacter_name, id, purpose,... son los que vemos en la pagina open.fda


#Programa 2
#Obtenemos la ID de los 10 primeros medicamentos
n = 0
for elem in respuesta2["results"]:
	print("La ID del medicamento",n, "es:", elem["id"])
n += 1

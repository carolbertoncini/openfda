#Partiendo del código de openfda1.
import http.client
import json

headers = {"User-Agent": "http-client"}
consulta= "/?search=active_ingredient:acetylsalicylic&limit=10" #Buscamos a partir del ingrediente activo para obtener las aspirinas

conexion = http.client.HTTPSConnection( "api.fda.gov") #Establecemos conexion, lo leemos e interpretamos en json
conexion.request("GET", "/drug/label.json" + consulta, None, headers)

respuesta1 = conexion.getresponse()
aspirina = respuesta1.read().decode("utf-8")
conexion.close()

aspirinas = json.loads(aspirina)["results"]

for aspirina in aspirinas: #Imprimimos las ID los nombres de los fabricantes de aquellos productos con acetylsalicylico como ingrediente activo
    print("ID del medicamento relacionado con Aspirina: ", aspirina["id"])
    if aspirina["openfda"]:
        fabricante = aspirina["openfda"]["manufacturer_name"]
        print("El fabricante es: ",fabricante)
    else: #Para en el caso de que no se encuentre la información
print("El Fabricante no está disponible")

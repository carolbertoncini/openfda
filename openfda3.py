import http.client
import json
import socket

headers = {'User-Agent': 'http-client'}
servidor = "api.fda.gov"
consulta = "/drug/label.json"
limite= "?limit=10"

conexion= http.client.HTTPSConnection(servidor) #Se establece la conexion
conexion.request("GET", consulta + limite, None, headers)

respuesta1 = conexion.getresponse()
medicinas = respuesta1.read().decode("utf-8")
conexion.close()

resultados = json.loads(medicinas)["results"]

InfoCliente = "" #Lo creamos vacío para rellenarlo posteriormente con la información de los medicamentos
for medicina in resultados:
    openfda = medicina["openfda"]
    if openfda: #En caso de que esté en openfda
        marca = openfda["brand_name"] #Pasamos los datos a string
        marca = ",".join(marca)

        nombre_medicamento = openfda["substance_name"]
        nombre_medicamento = ",".join(nombre_medicamento)

        fabricante = openfda["manufacturer_name"]
        fabricante = ",".join(fabricante)

        InfoCliente = InfoCliente + marca + "\t"+ "-" + nombre_medicamento + "\t"+ "-" +fabricante + "\n" #Para poder escribirlo todo en la misma linea
    else: #En caso de que no esté, no tendremos en esa información y lo mostraremos en pantalla
        no_info = ("NO existe información\n")
        InfoCliente = InfoCliente + no_info


IP = "127.0.0.1"
PORT = 8080
MAX_OPEN_REQUEST = 5


def InfoDeCliente(clientsocket):
    #Tenemos el contenido en forma html
    contenido = """
    <html>
    <h1>Medication list</h1>
    <p> Marca -  Nombre Medicamento -  Fabricante <p>
    <body style="background-color: pink">
    <pre> """ + InfoCliente + """
    </pre>
    </html>
    """

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)

#SERVIDOR
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, PORT))
serversocket.listen(MAX_OPEN_REQUEST)

while True: #En caso de que funcione, se lanzará el servidor y se esperará a que se reciba la petición
    print("Waiting for the client on IP:", IP, " PORT:", PORT)
    (clientsocket, addressclient) = serversocket.accept()
    print("Request received:", addressclient)
    InfoDeCliente(clientsocket)
clientsocket.close()

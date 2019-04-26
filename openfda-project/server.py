import http.server
import socketserver
import json
import http.client

IP = "localhost"
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

URL = "api.fda.gov"

class OpenFDA_HTML():
    def html(self, list1):
        inicio = "<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"
        final = "</ul>" + "\n" + "</body>" + "\n" + "</html>"

        with open("drug.html", "w") as f:
            f.write(inicio)
            for elemento in list1:
                elemento1 = "<li>" + elemento + "</li>" + "\n"
                f.write(elemento1)
            f.write(final)


HTML = OpenFDA_HTML()


class OpenFDA_Client():
    def buscar_medicamento(self, medicamento, limit):
        headers = {"User-Agent": "http-client"}
        conexion = http.client.HTTPSConnection(URL)
        url_buscar_medicamento = "/drug/label.json?search=active_ingredient:" + medicamento + "&" + "limit=" + limit
        conexion.request("GET", url_buscar_medicamento, None, headers)
        respuesta1 = conexion.getresponse()
        drugs_raw = respuesta1.read().decode("utf-8")
        conexion.close()
        medicamento = json.loads(drugs_raw)
        medicamento1 = medicamento
        return medicamento1

    def buscar_fabricante(self, medicamento, limit):
        headers = {"User-Agent": "http-client"}
        conexion = http.client.HTTPSConnection(URL)
        url_buscar_fabricante = "/drug/label.json?search=openfda.manufacturer_name:" + medicamento + "&" + "limit=" + limit
        conexion.request("GET", url_buscar_fabricante, None, headers)
        respuesta1 = conexion.getresponse()
        drugs_raw = respuesta1.read().decode("utf-8")
        conexion.close()
        medicamento = json.loads(drugs_raw)
        medicamento1 = medicamento
        return medicamento1

    def buscar_listas(self, limit):
        headers = {"User-Agent": "http-client"}
        conexion = http.client.HTTPSConnection(URL)
        url_buscar_listas = "/drug/label.json?" + "limit=" + limit
        conexion.request("GET", url_buscar_listas, None, headers)
        respuesta1 = conexion.getresponse()
        drugs_raw = respuesta1.read().decode("utf-8")
        conexion.close()
        medicamento = json.loads(drugs_raw)
        medicamento1 = medicamento
        return medicamento1


Client = OpenFDA_Client()


class OpenFDA_Parser():
    def datos_medicamentos(self, medicamento_1, list1):
        for i in range(len(medicamento_1["results"])):
            if 'active_ingredient' in medicamento_1["results"][i]:
                list1.append(medicamento_1["results"][i]["active_ingredient"][0])
            else:
                list1.append("Unknown")

    def datos_fabricante(self, fabricante_1, list1):
        for i in range(len(fabricante_1["results"])):
            try:
                if "openfda" in fabricante_1["results"][i]:
                    list1.append(fabricante_1["results"][i]["openfda"]["manufacturer_name"][0])
            except KeyError:
                list1.append("Unknown")

    def datos_lista_medicamentos(self, medicamento_1, list1):
        for i in range(len(medicamento_1["results"])):
            try:
                if "openfda" in medicamento_1["results"][i]:
                    list1.append(medicamento_1["results"][i]["openfda"]["brand_name"][0])
            except KeyError:
                list1.append("Unknown")

    def datos_lista_fabricante(self, fabricante_1, list1):
        for i in range(len(fabricante_1["results"])):
            try:
                if "openfda" in fabricante_1["results"][i]:
                    list1.append(fabricante_1["results"][i]["openfda"]["manufacturer_name"][0])
            except KeyError:
                list1.append("Unknown")

    def warnings(self, warning_1, list1):
        for i in range(len(warning_1["results"])):
            if "warnings" in warning_1["results"][i]:
                list1.append(warning_1["results"][i]["warnings"][0])
            else:
                list1.append("Unknown")


Parser = OpenFDA_Parser()


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("search.html", "r") as f:
                    data = f.read()
                    self.wfile.write(bytes(data, "utf8"))

            elif "searchDrug" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []

                if "&" not in self.path:
                    limit = "10"
                    parametro = self.path.split("?")[1]
                    medicamento = parametro.split("&")[0].split("=")[1]

                    buscar = Client.buscar_medicamento(medicamento, limit)
                    Parser.datos_medicamentos(buscar, list1)

                elif "&" in self.path:
                    parametro = self.path.split("?")[1]
                    medicamento = parametro.split("&")[0].split("=")[1]
                    limit = parametro.split("&")[1].split("=")[1]

                    if not limit:
                        limit = "10"

                    buscar = Client.buscar_medicamento(medicamento, limit)
                    Parser.datos_medicamentos(buscar, list1)

                HTML.html(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "searchCompany" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []

                if "&" not in self.path:
                    limit = "10"
                    parametro = self.path.split("?")[1]
                    fabricante = parametro.split("&")[0].split("=")[1]

                    buscar = Client.buscar_fabricante(fabricante, limit)
                    Parser.datos_fabricante(buscar, list1)

                elif "&" in self.path:
                    parametro = self.path.split("?")[1]
                    fabricante = parametro.split("&")[0].split("=")[1]
                    limit = parametro.split("&")[1].split("=")[1]

                    if not limit:
                        limit = "10"

                    buscar = Client.buscar_fabricante(fabricante, limit)
                    Parser.datos_fabricante(buscar, list1)

                HTML.html(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listDrugs" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []
                parametro = self.path.split("?")[1]
                limit = parametro.split("=")[1]

                buscar = Client.buscar_listas(limit)
                Parser.datos_lista_medicamentos(buscar, list1)

                HTML.html(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listCompanies" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []
                parametro = self.path.split("?")[1]
                limit = parametro.split("=")[1]

                buscar = Client.buscar_listas(limit)
                Parser.datos_lista_fabricante(buscar, list1)

                HTML.html(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listWarnings" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []
                parametro = self.path.split("?")[1]
                limit = parametro.split("=")[1]

                buscar = Client.buscar_listas(limit)
                Parser.warnings(buscar, list1)

                HTML.html(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "secret" in self.path:
                self.send_response(401)
                self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone")
                self.end_headers()

            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header("Location", "http://localhost:8000/")
                self.end_headers()

            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("error.html", "r") as f:
                    file = f.read()
                self.wfile.write(bytes(file, "utf8"))

        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("error.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))

        return


Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()

import os
import socket
import threading

class WebServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un socket TCP
        self.server.bind((self.host, self.port)) # vincula el socket a la dirección y puerto
        self.server.listen() # Escucha conexiones entrantes
        print(f"Escuchando {self.host}:{self.port}")
        self.server_handler = threading.Thread(target=self.wait_for_connections)
        self.server_handler.daemon = True
        self.server_handler.start()

    def wait_for_connections(self):
        while True:
            client, addr = self.server.accept() # Acepta una conexión entrante
            client_handler = threading.Thread(target=self.handle_client, args=(client, addr)) # Crea un hilo para manejar el cliente
            client_handler.start()

    def stop(self):
        print("Deteniendo el servidor")
        self.server.stop()

    def handle_client(self, client, addr):
        with client:
            request = client.recv(1024).decode() # 1024 = buffer size (tamano del buffer)
            http_request = request.split()
            http_request = {
                "method": http_request[0],
                "path": http_request[1],
                "protocol": http_request[2]
            }
            print(f'Petición recibida: {http_request}')
            try:
                htdoc = http_request["path"] if http_request["path"] != "/" else "/index.html"
                resource = f"samples/htdocs{htdoc}"
                if not os.path.exists(resource):
                    self.send_response(client, 404, 'samples/htdocs/404.html')
                    return
                self.send_response(client, 200, resource)
            except Exception as e:
                print(f"Error: {e}")
                self.send_response(client, 500)

    def send_response(self, client, code, file=None):
        http_header = {
            200: "HTTP/1.1 200 OK",
            404: "HTTP/1.1 404 Not Found",
            500: "HTTP/1.1 500 Internal Server Error"
        }
        if file:
            with open(file, "r") as file:
                content = file.read()
        else:
            content = ''
        print(f"Enviando respuesta: {http_header[code]}")
        response = http_header[code] + "\n\n" + content
        client.sendall(response.encode())
        client.close()

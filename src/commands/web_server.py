from pynettools.web_server import WebServer

def main():
    server = WebServer("0.0.0.0", 8080)
    server.start()
    input("Presiona Enter para detener el servidor\n")
    server.stop()

if __name__ == "__main__":
    main()
import sys
from pynettools.web_server import WebServer

def main():

    args = sys.argv[1:] 
    if len(args) == 0:
        htdocs = 'samples/htdocs'
    else:
        htdocs = args[0]

    server = WebServer("0.0.0.0", 8080, htdocs)
    server.start()
    input("Presiona Enter para detener el servidor\n")
    server.stop()

if __name__ == "__main__":
    main()
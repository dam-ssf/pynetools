import sys
import os
from pynettools.ip import IP
from pynettools.netmask import Netmask

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"Uso: {prog} <ip>")
        sys.exit(1)

    if len(args) == 1:
        ip = args[0]
    else:
        print("Número de argumentos incorrecto")
        sys.exit(1)

    try:
        ip = IP(ip)
    except ValueError as e:
        print("Dirección IP no válida")
        sys.exit(1)

    print(f"{ip.to_bin()}")

if __name__ == '__main__':
    main()
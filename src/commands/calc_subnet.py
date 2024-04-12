import sys
import os
import math
from pynettools.network import Network
from pynettools.netmask import Netmask

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"Uso: {prog} [ <ip> <netmask> | <ip/cidr> ] <subnets>")
        sys.exit(1)

    try:

        if len(args) == 2:
            ip_cidr = args[0]
            network = Network(ip_cidr)
            count = int(args[1])
        elif len(args) == 3:
            ip = args[0]
            netmask = args[1]
            network = Network(ip, netmask)
            count = int(args[2])                
        else:
            raise ValueError("Los argumentos no son válidos")
        
        if count < 0:
            raise ValueError("El número de subredes no puede ser negativo")
        
        subnets = network.subnets(count)        

        print(f"Obteniendo {len(subnets['nets'])} subredes de {network.ip}/{network.netmask.get_cidr()} ... ")
        print(f"Se han necesitado {subnets['bits_for_subnets']} bits para {len(subnets['nets'])} subredes => calculadas 2^{subnets['bits_for_subnets']} = {subnets['real_subnets']} subredes  ...\n")

        for i, subnet in enumerate(subnets['nets']):
            print(f"* Subred {i + 1}:")
            print(subnet)

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
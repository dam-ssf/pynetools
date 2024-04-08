import sys
import os
from pynettools.network import Network
from pynettools.nic import get_nic
from pynettools.netmask import Netmask
import math

def calc_bits_for_subnets(subnets):
    if subnets == 0:
        return 0
    return math.ceil(math.log2(subnets))

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
            subnets = int(args[1])
        elif len(args) == 3:
            ip = args[0]
            netmask = args[1]
            network = Network(ip, netmask)
            subnets = int(args[2])                
        else:
            raise ValueError("Los argumentos no son válidos")
        
        if subnets < 0:
            raise ValueError("El número de subredes no puede ser negativo")

        bits_for_subnets = calc_bits_for_subnets(subnets)
        bits_host = 32 - network.netmask.get_cidr()
        real_subnets = 2 ** bits_for_subnets 

        if bits_for_subnets > bits_host:
            raise ValueError("No se pueden obtener tantas subredes")

        print(f"Obteniendo {subnets} subredes de {network.ip}/{network.netmask.get_cidr()} ... ")
        print(f"Se necesitan {bits_for_subnets} bits para {subnets} subredes => calculando 2^{bits_for_subnets} = {real_subnets} subredes  ...\n")

        for i in range(real_subnets):
            print(f"* Subred {i + 1}:")
            offset = i * 2 ** (bits_host - bits_for_subnets)
            subnet = Network(network.network + offset, Netmask(network.netmask.get_cidr() + bits_for_subnets))
            print(subnet)

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
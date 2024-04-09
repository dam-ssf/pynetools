import sys
import os
from pynettools.ip import IP
from pynettools.network import Network
from pynettools.nic import get_nic

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"Uso: {prog} [ <ip> <netmask> | <ip/cidr> | --nic <name> ]")
        sys.exit(1)

    try:

        if len(args) == 1:

            ip_cidr = args[0]
            network = Network(ip_cidr)

            if not IP.include_cidr(ip_cidr):
                print(f'AVISO: Usando máscara de red por defecto para la dirección IP especificada {network.netmask}')

        elif len(args) == 2:

            if args[0] == '--nic':
                nic_name = args[1]
                nic = get_nic(nic_name)
                network = Network(nic['ipv4'], nic['netmask'])
            else:
                ip = args[0]
                netmask = args[1]
                network = Network(ip, netmask)
                
        else:
            raise ValueError("Los argumentos no son válidos")
        
        print(network)

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
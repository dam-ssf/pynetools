import sys
import os
from pynettools.network import Network
from pynettools.ip import IP
from pynettools.netmask import Netmask

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"Uso: {prog} [<ip> <netmask>|<ip/cidr>]")
        sys.exit(1)

    try:
        if len(args) == 1:
            network = Network(args[0])
        elif len(args) == 2:
            network = Network(args[0], args[1])
        else:
            raise ValueError("Número de argumentos incorrecto")
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f'Dirección IP     : {network.ip}')
    print(f'IP decimal       : {network.ip.to_int()}')
    print(f'IP hexadecimal   : {hex(network.ip.to_int())}')
    print(f'IP binario       : {network.ip.to_bin()}')
    print(f'Dirección de red : {network.network}')
    print(f'Máscara de red   : {network.netmask}')
    print(f'Notación CIDR    : /{network.netmask.get_cidr()}')
    print(f'Clase de red     : {network.network.get_class()}')
    print(f'Tipo de red      : {network.network.get_type()}')
    print(f'Número de hosts  : {network.get_total_hosts()} (usables {network.get_usable_hosts()})')
    print(f'Primer host      : {network.get_first_host()}')
    print(f'Último host      : {network.get_last_host()}')
    print(f'Broadcast        : {network.get_broadcast()}')

if __name__ == '__main__':
    main()
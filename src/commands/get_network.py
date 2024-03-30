import sys
import os
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
        print(f'Rango de hosts   : {network.get_first_host()} - {network.get_last_host()}')
        print(f'Broadcast        : {network.get_broadcast()}')

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
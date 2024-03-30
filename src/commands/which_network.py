import sys
import os
from pynettools.ip import IP
from pynettools.netmask import Netmask

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) == 0:
        print(f"Uso: {prog} [<ip> <netmask>|<ip/cidr>]")
        sys.exit(1)

    if len(args) == 1 and IP.include_cidr(args[0]):
        ip, cidr = args[0].split('/')
        netmask = int(cidr)
    elif len(args) == 2:
        ip = args[0]
        netmask = args[1]
    else:
        print("Número de argumentos incorrecto")
        sys.exit(1)

    try:
        ip = IP(ip)
    except ValueError as e:
        print("Dirección IP no válida")
        sys.exit(1)

    try:
        netmask = Netmask(netmask)
    except ValueError as e:
        print("Máscara de red no válida")
        sys.exit(1)

    wildcard = netmask.get_wildcardmask()
    network = ip.get_network(netmask)
    host = ip.get_host(netmask)

    print(f"IP               :   {ip.to_bin()} ({ip})")
    print(f"Máscara de red   : & {netmask.to_bin()} ({netmask})")
    print(f"----------------     {'-' * 50}")
    print(f"Red              :   {network.to_bin()} ({network})")
    print()
    print(f"IP               :   {ip.to_bin()} ({ip})")
    print(f"Máscara wildcard : & {wildcard.to_bin()} ({wildcard})")
    print(f"----------------     {'-' * 50}")
    print(f"Host             :   {host.to_bin()} ({host})")

if __name__ == '__main__':
    main()
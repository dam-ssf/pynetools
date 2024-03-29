import sys
import re
from ip import IP
from get_netmask import get_netmask

def is_cidr(ip):
    return bool(re.match(r'\d+\.\d+\.\d+\.\d+/\d+', ip))

def main():

    args = sys.argv[1:]

    if len(args) == 0:
        print("Uso: python get_network.py [<ip> <netmask>|<cidr>]")
        sys.exit(1)

    if len(args) == 1 and is_cidr(args[0]):
        ip, bits = args[0].split('/')
        try:
            netmask = get_netmask(int(bits))
        except ValueError as e:
            print("Número de bits de la máscara de red incorrecto")
            sys.exit(1)
    else:
        ip = args[0]
        netmask = args[1]

    try:
        ip = IP(ip)
    except ValueError as e:
        print("Dirección IP no válida")
        sys.exit(1)
    try:
        netmask = IP(netmask)
    except ValueError as e:
        print("Máscara de red no válida")
        sys.exit(1)

    network = ip.get_network(netmask)

    print(f"  IP             : {ip.to_bin()} ({ip})")
    print(f"& Máscara de red : {netmask.to_bin()} ({netmask})")
    print(f"  --------------   {'-' * 50}")
    print(f"  Red            : {network.to_bin()} ({network})")

if __name__ == '__main__':
    main()
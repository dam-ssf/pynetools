import sys
import os
from pynettools.netmask import Netmask

def main():
    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]
    if len(args) == 0 or len(args) > 1:
        print(f"Uso: {prog} <bits>")
        sys.exit(1)
    bits = int(args[0])
    try:
        netmask = Netmask(bits)
        wildcard = netmask.get_wildcardmask()
    except ValueError as e:
        print(e)
        sys.exit(1)
    print(f'Máscara de red   : {netmask.to_bin()} ({netmask})')
    print(f'Máscara wildcard : {wildcard.to_bin()} ({wildcard})')

if __name__ == '__main__':
    main()
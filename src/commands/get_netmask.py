import sys
import os
from pynetools.netmask import get_netmask, get_wildcardmask

def main():
    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]
    if len(args) == 0 or len(args) > 1:
        print(f"Uso: {prog} <bits>")
        sys.exit(1)
    bits = int(args[0])
    try:
        netmask = get_netmask(bits)
        wildcard = get_wildcardmask(bits)
    except ValueError as e:
        print(e)
        sys.exit(1)
    print(f'Máscara de red   : {netmask.to_bin()} ({netmask})')
    print(f'Máscara wildcard : {wildcard.to_bin()} ({wildcard})')

if __name__ == '__main__':
    main()
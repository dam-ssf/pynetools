import sys
import os
from pynettools.mac import Mac

def main():

    prog = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    if len(args) != 1:
        print(f"Uso: {prog} <mac-address>")
        sys.exit(1)

    mac_str = args[0]
    if Mac.is_vendor(mac_str):
        mac_str = mac_str.replace('-', ':').upper() + ':00:00:00'

    mac = Mac(mac_str)
    vendor = mac.get_vendor()

    if not vendor:
        vendor = 'Proveedor desconocido'
        
    print(f'Dirección MAC      : {mac}')
    print(f'Proveedor (vendor) : {vendor}')

if __name__ == '__main__':    
    main()
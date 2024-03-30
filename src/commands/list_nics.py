import socket
import psutil
from pynettools.nic import get_nic, get_all_nics

def main():
    print("Mis interfaces de red son: ")
    for interface in get_all_nics():
        print("- ", interface)

if __name__ == '__main__':    
    main()
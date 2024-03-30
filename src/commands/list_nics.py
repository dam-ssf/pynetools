import socket
import psutil

def get_nic(interface):
    data = {
        'name': interface
    } 
    for snicaddr in psutil.net_if_addrs()[interface]:
        if snicaddr.family == socket.AF_INET:
            data['ipv4'] = snicaddr.address
            data['netmask'] = snicaddr.netmask
        elif snicaddr.family == psutil.AF_LINK:
            data['mac'] = snicaddr.address
    return data

def get_all_nics():
    return [ get_nic(interface) for interface in psutil.net_if_stats().keys() ]

def main():
    print("Mis interfaces de red son: ")
    for interface in get_all_nics():
        print("- ", interface)

if __name__ == '__main__':    
    main()
from pynettools.ip import IP
from pynettools.netmask import Netmask

class Network():

    def __init__(self, ip, netmask = None):
        if type(ip) is str and IP.include_cidr(ip):
            ip, cidr = ip.split('/')
            self.netmask = Netmask(int(cidr))
        elif type(netmask) is Netmask:
            self.netmask = netmask
        elif type(netmask) is str:
            self.netmask = Netmask(netmask)
        else:
            raise ValueError("Máscara de red inválida")        
        self.ip = IP(ip)
        self.network = self.ip.get_network(self.netmask)

    def get_first_host(self):
        return self.network + 1
    
    def get_last_host(self):
        return self.network + self.get_usable_hosts()
    
    def get_total_hosts(self):
        return 2 ** (32 - self.netmask.get_cidr())
    
    def get_usable_hosts(self):
        return self.get_total_hosts() - 2

    def get_broadcast(self):
        wildcard = self.netmask.get_wildcardmask()        
        return self.network | wildcard
    

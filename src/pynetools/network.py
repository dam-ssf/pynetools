from pynetools.ip import IP
from pynetools.get_netmask import get_netmask

class Network(IP):

    def __init__(self, ip):
        if not IP.include_cidr(ip):
            raise ValueError("Dirección de red inválida")
        ip, cidr = ip.split('/')
        self.netmask = IP(get_netmask(cidr))
        self.ip = IP(ip).get_network(self.netmask)

    def __init__(self, ip, netmask):
        super().__init__(ip)
        self.netmask = IP(netmask)

    def get_broadcast(self):
        broadcast = []
        for i in range(4):
            ip_part = int(self.ip[i])
            netmask_part = int(self.netmask.ip[i])
            broadcast.append(str(ip_part | ~netmask_part))
        return IP('.'.join(broadcast))

    def __or__(self, other):
        ip = []
        for i in range(4):
            ip.append(str(self.ip[i] | other.ip[i]))
        return IP('.'.join(ip))

    def __str__(self):
        ip_str = []
        for part in self.ip:
            ip_str.append(str(part))
        return '.'.join(ip_str) + '/' + str(self.netmask)

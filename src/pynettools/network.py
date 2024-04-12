import math
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
        elif not netmask:
            self.netmask = None
        else:
            raise ValueError(f"Máscara de red inválida: {netmask}")
        self.ip = IP(ip)
        if not self.netmask:
            self.netmask = Netmask.get_default_netmask(self.ip)
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
    
    def subnets(self, subnets):
        if subnets < 0:
            raise ValueError("El número de subredes no puede ser negativo")

        bits_for_subnets = Network.calc_bits_for_subnets(subnets)
        bits_host = self.netmask.gets_bits_host()
        real_subnets = 2 ** bits_for_subnets 

        if bits_for_subnets > bits_host:
            raise ValueError("No se pueden obtener tantas subredes")

        subnets = {
            "bits_for_subnets": bits_for_subnets,
            "bits_host": bits_host,
            "real_subnets": real_subnets,
            "nets": []
        }

        for i in range(real_subnets):
            offset = i * 2 ** (bits_host - bits_for_subnets)
            subnet = Network(self.network + offset, Netmask(self.netmask.get_cidr() + bits_for_subnets))
            subnets['nets'].append(subnet)
        
        return subnets
    
    def __str__(self) -> str:
        return f"""
Dirección IP     : {self.ip}
IP decimal       : {self.ip.to_int()}
IP hexadecimal   : {hex(self.ip.to_int())}
IP binario       : {self.ip.to_bin()}
Dirección de red : {self.network}
Máscara de red   : {self.netmask}
Notación CIDR    : /{self.netmask.get_cidr()}
Clase de red     : {self.network.get_class()}
Tipo de red      : {self.network.get_type()}
Número de hosts  : {self.get_total_hosts()} (usables {self.get_usable_hosts()})
Rango de hosts   : {self.get_first_host()} - {self.get_last_host()}
Broadcast        : {self.get_broadcast()}
        """
    
    @staticmethod
    def calc_bits_for_subnets(subnets):
        if subnets == 0:
            return 0
        return math.ceil(math.log2(subnets))

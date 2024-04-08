import re

class IP:

    def __init__(self, ip):
        if type(ip) is IP:
            self.ip = ip.ip
        elif type(ip) is int:
            self.ip = [ (ip >> 24) & 0xFF, (ip >> 16) & 0xFF, (ip >> 8) & 0xFF, ip & 0xFF ]
        elif type(ip) is str and IP.is_ip(ip):
            self.ip = [ int(part) for part in ip.split('.') ]
        else:
            raise ValueError(f'Dirección IP inválida: {ip}')
            
    def __or__(self, other):
        if not issubclass(type(other), IP):
            raise ValueError('Operando no válido')
        ip = []
        for i in range(4):
            ip_part = self.ip[i]
            other_part = other.ip[i]
            ip.append(ip_part | other_part)
        return IP('.'.join([ str(part) for part in ip ]))
    
    def __and__(self, other):
        if not issubclass(type(other), IP):
            raise ValueError('Operando no válido')
        ip = []
        for i in range(4):
            ip_part = self.ip[i]
            other_part = other.ip[i]
            ip.append(ip_part & other_part)
        return IP('.'.join([ str(part) for part in ip ]))
    
    def __invert__(self):
        ip = []
        for i in range(4):
            ip_part = self.ip[i]
            ip.append(~ip_part & 0xFF)
        return IP('.'.join([ str(part) for part in ip ]))
    
    def __add__(self, other):
        if type(other) is int:
            ip = self.to_int() + other
            return IP(ip)
        return self

    def to_bin(self):
        ip_bin = []
        for i in self.ip:
            part = bin(i)[2:]               # [2:] elimina 0b del inicio
            ip_bin.append(part.zfill(8))    # zfill(8) rellena con 0 a la izquierda
        return '.'.join(ip_bin)
    
    def get_class(self):
        if 1 <= self.ip[0] <= 126:
            return 'A'
        if self.ip[0] == 127:
            return 'Loopback'
        if 128 <= self.ip[0] <= 191:
            return 'B'
        if 192 <= self.ip[0] <= 223:
            return 'C'
        if 224 <= self.ip[0] <= 239:
            return 'D'
        if 240 <= self.ip[0] <= 255:
            return 'E'

    def get_type(self):
        if self.ip[0] == 10:
            return 'Privada'
        if self.ip[0] == 172 and 16 <= self.ip[1] <= 31:
            return 'Privada'
        if self.ip[0] == 192 and self.ip[1] == 168:
            return 'Privada'
        return 'Pública'
    
    def get_network(self, netmask):
        return self & netmask
    
    def get_host(self, netmask):
        return self & ~netmask

    def to_int(self):
        return (self.ip[0] << 24) + (self.ip[1] << 16) + (self.ip[2] << 8) + self.ip[3]
    
    def __str__(self) -> str:
        ip_str = []
        for part in self.ip:
            ip_str.append(str(part))
        return '.'.join(ip_str)
    
    @staticmethod
    def is_ip(ip):
        ip = ip.split('.')
        if len(ip) != 4:
            return False
        for i in ip:
            if not i.isdigit():
                return False
            if not 0 <= int(i) <= 255:
                return False
        return True

    @staticmethod
    def include_cidr(ip_cidr):
        return bool(re.match(r'\d+\.\d+\.\d+\.\d+/\d+', str(ip_cidr)))
    

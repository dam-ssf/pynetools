class IP:

    def __init__(self, ip):
        if not self._check_ip(ip):
            raise ValueError("Dirección IP inválida")
        self.ip = [ int(part) for part in ip.split('.') ]

    def to_bin(self):
        ip_bin = []
        for i in self.ip:
            part = bin(i)[2:]               # [2:] elimina 0b del inicio
            ip_bin.append(part.zfill(8))    # zfill(8) rellena con 0 a la izquierda
        return '.'.join(ip_bin)
    
    def _check_ip(self, ip):
        ip = ip.split('.')
        if len(ip) != 4:
            return False
        for i in ip:
            if not i.isdigit():
                return False
            if not 0 <= int(i) <= 255:
                return False
        return True
    
    def get_class(self):
        if 1 <= self.ip[0] <= 126:
            return 'A'
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
        network = []
        for i in range(4):
            ip_part = int(self.ip[i])
            netmask_part = int(netmask.ip[i])
            network.append(str(ip_part & netmask_part))
        return IP('.'.join(network))

    def __str__(self):
        ip_str = []
        for part in self.ip:
            ip_str.append(str(part))
        return '.'.join(ip_str)
from pynettools.ip import IP

class Netmask(IP):

    def __init__(self, netmask):
        if type(netmask) is int:
            if not 0 <= netmask <= 32:
                raise ValueError(f'Número de bits incorrecto en la máscara de red: {netmask}. Debe ser un valor entre 0 y 32')
            self.cidr = netmask
            netmask = Netmask.cidr_to_netmask(netmask)
        elif type(netmask) is str:
            self.cidr = Netmask.netmask_to_cidr(netmask)
        super().__init__(netmask)
        if not Netmask.is_netmask(str(self)):
            raise ValueError("Máscara de red inválida")

    def get_cidr(self):
        return self.cidr

    def get_wildcardmask(self):
        return ~self
    
    def gets_bits_host(self):
        return 32 - self.cidr

    @staticmethod
    def netmask_to_cidr(netmask):
        netmask = IP(netmask)
        bits = netmask.to_bin().count('1')
        return bits
    
    @staticmethod
    def cidr_to_netmask(bits):
        if not 0 <= bits <= 32:
            raise ValueError("Número de bits incorrecto")
        netmask = bits * '1' + (32 - bits) * '0'
        netmask = [ str(int(netmask[i:i+8], 2)) for i in range(0, 32, 8) ]
        netmask = '.'.join(netmask)
        return IP(netmask)

    @staticmethod
    def is_netmask(netmask):
        try:
            netmask = IP(netmask)
            return not '01' in netmask.to_bin().replace('.', '')
        except ValueError:
            return False
        
    @staticmethod
    def get_default_netmask(ip):
        match ip.get_class():
            case 'A':
                return Netmask('255.0.0.0')
            case 'B':
                return Netmask('255.255.0.0')
            case 'C':
                return Netmask('255.255.255.0')
            case _:
                return None

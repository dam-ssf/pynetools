from pynetools.ip import IP

def get_netmask(bits):
    if not 0 <= bits <= 32:
        raise ValueError("Número de bits incorrecto")
    netmask = bits * '1' + (32 - bits) * '0'
    netmask = [ str(int(netmask[i:i+8], 2)) for i in range(0, 32, 8) ]
    netmask = '.'.join(netmask)
    return IP(netmask)

def get_wildcardmask(bits):
    if not 0 <= bits <= 32:
        raise ValueError("Número de bits incorrecto")
    wildcard = bits * '0' + (32 - bits) * '1'
    wildcard = [ str(int(wildcard[i:i+8], 2)) for i in range(0, 32, 8) ]
    wildcard = '.'.join(wildcard)
    return IP(wildcard)
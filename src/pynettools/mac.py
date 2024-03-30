import re
import os
import sys

"""
Lista de proveedores (mac_vendors.txt) extraída de https://gist.github.com/aallan/b4bb86db86079509e6159810ae9bd3e4
"""
class Mac():

    vendors = []

    def __init__(self, mac):
        mac = mac.replace('-', ':').upper()
        if not Mac.is_mac(mac):
            raise ValueError("Dirección MAC inválida")
        self.mac = mac

    def get_vendor(self):
        mac_vendor_part = self.mac.split(':')[0:3]
        mac_vendor_part =  ''.join(mac_vendor_part).upper()
        pattern = re.compile(f"^{mac_vendor_part}\t(.+)$", re.IGNORECASE)
        vendor = None
        resources = sys.modules[__package__].__path__[0]
        with open(os.path.join(resources, 'mac_vendors.txt'), encoding='utf-8') as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    vendor = match.group(1)
                    break
            f.close()
        return vendor

    def __str__(self):
        return self.mac

    @staticmethod
    def is_mac(mac):
        return re.match(r'^([0-9A-F]{2}:){5}([0-9A-F]{2})$', mac)
    
    @staticmethod
    def is_vendor(mac):
        return re.match(r'^([0-9A-F]{2}[:-]){2}([0-9A-F]{2})$', mac)
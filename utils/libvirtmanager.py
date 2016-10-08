import xml.etree.ElementTree as ET

import libvirt


class LibvirtManager(object):
    DEFAULT_NETWORK = "default"

    def libvirt_connection(self, conf):
        self.conn = libvirt.open(conf.options['connection'])

    def domain_define(self, xml):
        return self.conn.defineXML(xml)

    def domain_list(self):
        return self.conn.listDefinedDomains()

    def network_get(self, name=DEFAULT_NETWORK):
        return self.conn.networkLookupByName(name)

    def domain_get_nics(self, domain):
        interfaces = []

        root = ET.fromstring(domain.XMLDesc())

        for iface in root.findall("./devices/interface"):
            new_if = {}
            for child in iface:
                new_if[child.tag] = child.attrib
            interfaces.append(new_if)

        return interfaces

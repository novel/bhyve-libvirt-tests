import logging
import unittest

from tests import base


logging.getLogger("paramiko").setLevel(logging.ERROR)


class DomainGenericTest(unittest.TestCase,
                        base.DomainTest):
    """Test for the most generic domain xml.

    Uses virtio-net, so requires to have
    ifconfig_vtnet0='DHCP' somewhere in /etc/rc.conf"""

    domain_xml_file = 'base.xml'

    def setUp(self):
        super(DomainGenericTest, self).setUp()
        self.prepare()

    def get_fixture_params(self):
        fixture_params = {}
        for param in ("disk_img", "cdrom_img"):
            fixture_params[param.upper()] = self.conf.options[param]
        fixture_params["NAME"] = self.name_generate('dom')
        fixture_params["UUID"] = self.uuid()
        return fixture_params


class DomainE1000Test(DomainGenericTest):
    """Test for domain with e1000 nic

    Requires ifconfig_em0='DHCP'"""

    domain_xml_file = 'e1000.xml'

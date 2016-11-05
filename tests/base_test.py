import logging
import unittest

from tests import base


logging.getLogger("paramiko").setLevel(logging.ERROR)


class DomainGenericTest(unittest.TestCase,
                        base.DomainTest):
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

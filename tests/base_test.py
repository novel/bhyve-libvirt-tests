import time
import logging
import unittest

import paramiko
import paramiko.client

from tests import base
from utils import config
from utils import fixtures
from utils.libvirtmanager import LibvirtManager


logging.getLogger("paramiko").setLevel(logging.ERROR)


class BaseTest(unittest.TestCase,
               base.BaseTestCase,
               LibvirtManager):
    WAIT_FOR_NEW_LEASE_TIMEOUT = 180
    WAIT_FOR_SSH_TIMEOUT = 180

    def setUp(self):
        self.conf = config.Config()
        self.libvirt_connection(self.conf)

    def test_foo(self):
        fixture_params = {}
        for param in ("disk_img", "cdrom_img"):
            fixture_params[param.upper()] = self.conf.options[param]
        fixture_params["NAME"] = self.name_generate('dom')
        fixture_params["UUID"] = self.uuid()
        domxml = fixtures.get('base.xml', fixture_params)

        dom = self.domain_define(domxml)
        self.addCleanup(dom.undefine)

        self.assertIn(dom.name(), self.domain_list())

        net = self.network_get()

        dom.create()
        self.addCleanup(dom.shutdown)

        self.assertEqual(dom.isActive(), 1)

        dom_nics = self.domain_get_nics(dom)
        mac = dom_nics[0]['mac']['address']

        lease_deadline = time.time() + self.WAIT_FOR_NEW_LEASE_TIMEOUT
        dom_ipaddr = None
        while time.time() < lease_deadline:
            try:
                dom_ipaddr = [l['ipaddr'] for l in net.DHCPLeases()
                              if l['mac'] == mac][0]
                break
            except IndexError:
                time.sleep(5)

        if not dom_ipaddr:
            raise Exception('Failed to obtain domain DHCP lease')

        ssh_client = paramiko.client.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
        ssh_client.connect(dom_ipaddr,
                           username=self.conf.options['domain_user'],
                           password=self.conf.options['domain_passwd'])
        stdin, stdout, stderr = ssh_client.exec_command("uname -a")

        cmd_output = stdout.read()  # noqa

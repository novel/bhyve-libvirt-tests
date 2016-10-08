import subprocess
import unittest

from tests import base
from utils import config
from utils.libvirtmanager import LibvirtManager


class BaseTest(unittest.TestCase,
               base.BaseTestCase,
               LibvirtManager):

    def setUp(self):
        self.conf = config.Config()
        self.libvirt_connection(self.conf)

    def test_hostname(self):
        hostname = self.conn.getHostname()

        self.assertEqual(hostname,
                         subprocess.check_output(["hostname"]).strip())

    def test_nodeinfo(self):
        info = self.conn.getInfo()

        # mem size
        physmem = int(float(self.sysctl_get("hw.physmem")) / 1024 / 1024)
        self.assertEqual(info[1], physmem)

        # number of CPUs
        self.assertEqual(info[2], int(self.sysctl_get("hw.ncpu")))

        # CPU freq; TODO: fallback for non-cpufreq(4) case
        self.assertEqual(info[3], int(self.sysctl_get("dev.cpu.0.freq")))

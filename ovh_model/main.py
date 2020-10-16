#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo

class OVHTopology(IPTopo):
    def build(self, *args, **kwargs):

        # INITIAL SETUP

        # Adding routers
        ovh_r1 = self.addRouter("ovh_r1")
        ovh_r2 = self.addRouter("ovh_r2")
        ovh_r3 = self.addRouter("ovh_r3")
        ovh_r4 = self.addRouter("ovh_r4")
        ovh_r5 = self.addRouter("ovh_r5")
        ovh_r6 = self.addRouter("ovh_r6")
        ovh_r7 = self.addRouter("ovh_r7")
        ovh_r8 = self.addRouter("ovh_r8")
        ovh_r9 = self.addRouter("ovh_r9")
        ovh_r10 = self.addRouter("ovh_r10")
        ovh_r11 = self.addRouter("ovh_r11")
        ovh_r12 = self.addRouter("ovh_r12")
        telia_r1 = self.addRouter("telia_r1")
        google_r1 = self.addRouter("google_r1")
        cogent_r1 = self.addRouter("cogent_r1")
        level3_r1 = self.addRouter("level3_r1")

        # Adding links
        self.addLink(ovh_r1, ovh_r2)
        self.addLink(ovh_r1, ovh_r3)
        self.addLink(ovh_r2, ovh_r4)
        self.addLink(ovh_r3, ovh_r4)
        self.addLink(ovh_r3, ovh_r6)
        self.addLink(ovh_r3, ovh_r5)
        self.addLink(ovh_r3, ovh_r9)
        self.addLink(ovh_r3, ovh_r7)
        self.addLink(ovh_r4, ovh_r5)
        self.addLink(ovh_r4, ovh_r6)
        self.addLink(ovh_r4, ovh_r8)
        self.addLink(ovh_r4, ovh_r12)
        self.addLink(ovh_r5, telia_r1)
        self.addLink(ovh_r6, telia_r1)
        self.addLink(ovh_r6, level3_r1)
        self.addLink(ovh_r7, ovh_r8)
        self.addLink(ovh_r7, ovh_r10)
        self.addLink(ovh_r8, ovh_r11)
        self.addLink(ovh_r9, ovh_r12)
        self.addLink(ovh_r9, ovh_r10)
        self.addLink(ovh_r12, ovh_r11)
        self.addLink(ovh_r12, google_r1)
        self.addLink(ovh_r12, cogent_r1)
        self.addLink(ovh_r12, level3_r1)

        # Setup the ASes
        self.addAS(1, (ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12))
        self.addAS(2, (telia_r1,))
        self.addAS(3, (cogent_r1,))
        self.addAS(4, (level3_r1,))

        super().build(*args, **kwargs)

if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

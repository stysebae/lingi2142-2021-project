#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, RouterConfig, set_rr, ebgp_session, SHARE

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

        # Adding deamons
        ovh_r1.addDaemon(BGP)
        ovh_r2.addDaemon(BGP)
        ovh_r3.addDaemon(BGP)
        ovh_r4.addDaemon(BGP)
        ovh_r5.addDaemon(BGP)
        ovh_r6.addDaemon(BGP)
        ovh_r7.addDaemon(BGP)
        ovh_r8.addDaemon(BGP)
        ovh_r9.addDaemon(BGP)
        ovh_r10.addDaemon(BGP)
        ovh_r11.addDaemon(BGP)
        ovh_r12.addDaemon(BGP)
        telia_r1.addDaemon(BGP)
        google_r1.addDaemon(BGP)
        cogent_r1.addDaemon(BGP)
        level3_r1.addDaemon(BGP)

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
        self.addLink(ovh_r10, ovh_r11)
        self.addLink(ovh_r10, google_r1)
        self.addLink(ovh_r10, cogent_r1)
        self.addLink(ovh_r11, ovh_r12)
        self.addLink(ovh_r11, level3_r1)
        self.addLink(ovh_r11, cogent_r1)
        self.addLink(ovh_r11, google_r1)

        # Setup the ASes
        self.addAS(1, (ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12))
        self.addAS(2, (telia_r1,))
        self.addAS(3, (cogent_r1,))
        self.addAS(4, (level3_r1,))
        self.addAS(5, (google_r1,))

        # Configure the RR
        set_rr(self, rr=ovh_r7, peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12])
        set_rr(self, rr=ovh_r8, peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r9, ovh_r10, ovh_r11, ovh_r12])

        # Adding eBGP
        ebgp_session(self, ovh_r5, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, level3_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, google_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, cogent_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, level3_r1, link_type=SHARE)

        super().build(*args, **kwargs)

if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

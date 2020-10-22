#!/usr/bin/env python3

from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import OSPF, BGP, AS, set_rr, ebgp_session, SHARE

# CONSTANT VALUES

FRANKFURT_ID = ("b", "11")  # cf. docs/Addressing Plan.md
ROUBAIX_ID = ("c", "12")
STRASBOURG_ID = ("d", "13")
PARIS_ID = ("e", "14")

# Routers configuration
MAX_IPV4_PREFIX_LEN = 24  # /24 and /48 are default values for IPv4 and IPv6
MAX_IPV6_PREFIX_LEN = 48

# Links and Loopback addresses
IPV4_LO_PREFIX = IPV4_LINK_PREFIX = 32
IPV6_LO_PREFIX = IPV6_LINK_PREFIX = 128


class OVHTopology(IPTopo):
    """
    This class represents the topology of our OVH model (see ovh_model/img/model_preview.jpg).
    """

    def build(self, *args, **kwargs):
        # INITIAL SETUP

        # Adding routers

        ovh_r1 = self.addRouter("ovh_r1")  # ovh_r1 to ovh_r6: routers located in Frankfurt
        ovh_r2 = self.addRouter("ovh_r2")
        ovh_r3 = self.addRouter("ovh_r3")
        ovh_r4 = self.addRouter("ovh_r4")
        ovh_r5 = self.addRouter("ovh_r5")
        ovh_r6 = self.addRouter("ovh_r6")
        ovh_r7 = self.addRouter("ovh_r7")  # ovh_r7, ovh_r8: routers in Roubaix
        ovh_r8 = self.addRouter("ovh_r8")
        ovh_r9 = self.addRouter("ovh_r9")  # ovh_r9, ovh_r12: routers in Strasbourg
        ovh_r10 = self.addRouter("ovh_r10")  # ovh_r10, ovh_r11: routers in Paris
        ovh_r11 = self.addRouter("ovh_r11")
        ovh_r12 = self.addRouter("ovh_r12")
        telia_r1 = self.addRouter("telia_r1")
        google_r1 = self.addRouter("google_r1")
        cogent_r1 = self.addRouter("cogent_r1")
        level3_r1 = self.addRouter("level3_r1")

        # Adding subnets

        self.addSubnet(nodes=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6],
                       subnets=[self.get_ipv6_address(FRANKFURT_ID[0]), self.get_ipv4_address(FRANKFURT_ID[1])])
        self.addSubnet(nodes=[ovh_r7, ovh_r8],
                       subnets=[self.get_ipv6_address(ROUBAIX_ID[0]), self.get_ipv4_address(ROUBAIX_ID[1])])
        self.addSubnet(nodes=[ovh_r9, ovh_r12],
                       subnets=[self.get_ipv6_address(STRASBOURG_ID[0]), self.get_ipv4_address(STRASBOURG_ID[1])])
        self.addSubnet(nodes=[ovh_r10, ovh_r11],
                       subnets=[self.get_ipv6_address(PARIS_ID[0]), self.get_ipv4_address(PARIS_ID[1])])

        # Adding daemons
        ovh_r1.addDaemon(OSPF)
        ovh_r1.addDaemon(BGP)
        ovh_r2.addDaemon(OSPF)
        ovh_r2.addDaemon(BGP)
        ovh_r3.addDaemon(OSPF)
        ovh_r3.addDaemon(BGP)
        ovh_r4.addDaemon(OSPF)
        ovh_r4.addDaemon(BGP)
        ovh_r5.addDaemon(OSPF)
        ovh_r5.addDaemon(BGP)
        ovh_r6.addDaemon(OSPF)
        ovh_r6.addDaemon(BGP)
        ovh_r7.addDaemon(OSPF)
        ovh_r7.addDaemon(BGP)
        ovh_r8.addDaemon(OSPF)
        ovh_r8.addDaemon(BGP)
        ovh_r9.addDaemon(OSPF)
        ovh_r9.addDaemon(BGP)
        ovh_r10.addDaemon(OSPF)
        ovh_r10.addDaemon(BGP)
        ovh_r11.addDaemon(OSPF)
        ovh_r11.addDaemon(BGP)
        ovh_r12.addDaemon(OSPF)
        ovh_r12.addDaemon(BGP)
        telia_r1.addDaemon(OSPF)
        telia_r1.addDaemon(BGP)
        google_r1.addDaemon(OSPF)
        google_r1.addDaemon(OSPF)
        cogent_r1.addDaemon(OSPF)
        cogent_r1.addDaemon(BGP)
        level3_r1.addDaemon(OSPF)
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

        # Set AS-ownerships
        self.addOverlay(
            AS(1, (ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12)))
        self.addOverlay(AS(2, (telia_r1,)))
        self.addOverlay(AS(3, (cogent_r1,)))
        self.addOverlay(AS(4, (level3_r1,)))
        self.addOverlay(AS(5, (google_r1,)))

        # Configure the RRs
        set_rr(self, rr=ovh_r7,
               peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12])
        set_rr(self, rr=ovh_r8,
               peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r9, ovh_r10, ovh_r11, ovh_r12])

        # Adding eBGP
        ebgp_session(self, ovh_r5, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, level3_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, google_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, cogent_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, level3_r1, link_type=SHARE)

        super().build(*args, **kwargs)

    def get_ipv6_address(self, addr, lo=False):
        """

        """
        res = f"2023:{addr}::/{str(MAX_IPV6_PREFIX_LEN)}"
        if lo:
            res = f"2023:a:{addr}::1/{str(IPV6_LO_PREFIX)}"
        return res

    def get_ipv4_address(self, addr, lo=False):
        """

        """
        res = f"12.{addr}.0.0/{str(MAX_IPV4_PREFIX_LEN)}"
        if lo:
            res = f"12.10.{addr}.0/{str(IPV4_LO_PREFIX)}"
        return res


if __name__ == '__main__':
    net = IPNet(topo=OVHTopology(), max_v4_prefixlen=MAX_IPV4_PREFIX_LEN, max_v6_prefixlen=MAX_IPV6_PREFIX_LEN,
                allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

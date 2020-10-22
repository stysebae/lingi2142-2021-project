#!/usr/bin/env python3

"""
LINGI2142: Computer Networks: Configuration and Management
File: main.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file sets up in Mininet the part of the OVH's network that we have chosen.
"""

from mininet.log import lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import OSPF, BGP, set_rr, ebgp_session, SHARE, AF_INET6, AF_INET, OSPF6

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
        """
        Build the topology of our OVH network and set up it by adding routers, links, protocols, setting up routers
        reflectors, etc.
        """
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
        ovh_r10 = self.addRouter("ovh_r10")
        ovh_r11 = self.addRouter("ovh_r11")
        ovh_r12 = self.addRouter("ovh_r12")
        telia_r1 = self.addRouter("telia_r1")
        google_r1 = self.addRouter("google_r1")
        cogent_r1 = self.addRouter("cogent_r1")
        level3_r1 = self.addRouter("level3_r1")
        all_routers = [ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11,
                       ovh_r12, telia_r1, google_r1, cogent_r1, level3_r1]
        # Adding protocols to routers
        self.add_ospf(all_routers)
        self.add_bgp(all_routers, [ovh_r5, ovh_r6, ovh_r10, ovh_r11], [telia_r1], [google_r1], [cogent_r1], [level3_r1])
        # Adding ASes ownerships
        self.addAS(1,
                   (ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12))
        self.addAS(2, (telia_r1,))
        self.addAS(3, (cogent_r1,))
        self.addAS(4, (level3_r1,))
        self.addAS(5, (google_r1,))
        # Configuring RRs
        set_rr(self, rr=ovh_r7,
               peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12])
        set_rr(self, rr=ovh_r8,
               peers=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r9, ovh_r10, ovh_r11, ovh_r12])
        # Adding links
        # self.addLink(r1, r2, params1={"ip": "2001:2345:7::a/64"}, params2={"ip": "2001:2345:7::b/64"}, igp_metric=5)
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
        # Adding subnets
        """
        self.addSubnet(nodes=[ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6],
                       subnets=[self.get_ipv6_address(FRANKFURT_ID[0]), self.get_ipv4_address(FRANKFURT_ID[1])])
        self.addSubnet(nodes=[ovh_r7, ovh_r8],
                       subnets=[self.get_ipv6_address(ROUBAIX_ID[0]), self.get_ipv4_address(ROUBAIX_ID[1])])
        self.addSubnet(nodes=[ovh_r9, ovh_r12],
                       subnets=[self.get_ipv6_address(STRASBOURG_ID[0]), self.get_ipv4_address(STRASBOURG_ID[1])])
        self.addSubnet(nodes=[ovh_r10, ovh_r11],
                       subnets=[self.get_ipv6_address(PARIS_ID[0]), self.get_ipv4_address(PARIS_ID[1])])
        """
        # Adding eBGP sessions
        ebgp_session(self, ovh_r5, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, level3_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, google_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, cogent_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, level3_r1, link_type=SHARE)

        super().build(*args, **kwargs)

    def add_ospf(self, all_routers):
        """
        Add Open Shortest Path as Interior Gateway Protocol (IGP), both for IPv4 and IPv6.

        :param all_routers: (list of Routers)
        """
        for router in all_routers:
            router.addDaemon(OSPF)
            router.addDaemon(OSPF6)

    def add_bgp(self, all_routers, ovh_routers, telia_routers, google_routers, cogent_routers, level3_routers):
        """
        Add Border Gateway Protocol (BGP) to the routers and specify which prefixes they advertise.
        """
        family_ipv4 = AF_INET()
        family_ipv6 = AF_INET6()
        for router in all_routers:
            router.addDaemon(BGP, address_families=(family_ipv4, family_ipv6))
        for router in ovh_routers:
            router.addDaemon(BGP, family=AF_INET(redistribute=("ospf6", "connected"), ))
            router.addDaemon(BGP, family=AF_INET6(redistribute=("ospf6", "connected"), ))
        # Other ASes advertise specific prefixes
        for router in telia_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:beef::/32",), ))  # TODO: change IP address space
        for router in google_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:baef::/32",), ))
        for router in cogent_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:bbef::/32",), ))
        for router in level3_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:bcef::/32",), ))

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
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    net = IPNet(topo=OVHTopology(), max_v4_prefixlen=MAX_IPV4_PREFIX_LEN, max_v6_prefixlen=MAX_IPV6_PREFIX_LEN,
                allocate_IPs=True)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

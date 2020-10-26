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
from ipmininet.router.config import OSPF, BGP, set_rr, ebgp_session, SHARE, AF_INET6, AF_INET, OSPF6, AccessList, \
    bgp_peering, bgp_fullmesh

# CONSTANT VALUES

FRANKFURT_ID = ("b", "11")  # cf. docs/Addressing Plan.md
ROUBAIX_ID = ("c", "12")
STRASBOURG_ID = ("d", "13")
PARIS_ID = ("e", "14")

# Routers configuration
MAX_IPV4_PREFIX_LEN = 31  # /24 and /48 are default values for IPv4 and IPv6
MAX_IPV6_PREFIX_LEN = 48

# Links and Loopback addresses
IPV4_LO_PREFIX = IPV4_LINK_PREFIX = 32
IPV6_LO_PREFIX = IPV6_LINK_PREFIX = 128


class OVHTopology(IPTopo):

    class IPv4Address():
        def __init__(self, firstByte=10, secondByte=0, thirdByte=0, fourthByte=0, mask=24):
            self.firstByte = firstByte
            self.secondByte = secondByte
            self.thirdByte = thirdByte
            self.fourthByte = fourthByte
            self.mask = mask

        def __str__(self):
            return "{}.{}.{}.{}/{}".format(self.firstByte, self.secondByte, self.thirdByte, self.fourthByte, self.mask)

        def getFourthByte(self):
            return self.fourthByte

        def setHost(self, host):
            hostList = str(host).split(".")
            if len(hostList) == 3:
                self.secondByte = hostList[0]
                self.thirdByte = hostList[1]
                self.fourthByte = hostList[2]
            elif len(hostList) == 2:
                self.thirdByte = hostList[0]
                self.fourthByte = hostList[1]
            else:
                self.fourthByte = hostList[0]



    """
    This class represents the topology of our OVH model (see ovh_model/img/model_preview.jpg).
    """

    def build(self, *args, **kwargs):
        """
        Build the topology of our OVH network and set up it by adding routers, links, protocols, setting up routers
        reflectors, etc.
        """
        # Adding routers
        # r1 = self.addRouter('r1', lo_addresses=["2042:1::1/64", "10.1.1.1/24"])
        ovh_r1 = self.addRouter("ovh_r1", lo_addresses=["2023:a:1::1/128", self.IPv4Address(12, 10, 1, 1, 32).__str__()])  # ovh_r1 to ovh_r6: routers located in Frankfurt
        ovh_r2 = self.addRouter("ovh_r2", lo_addresses=["2023:a:1::2/128", self.IPv4Address(12, 10, 1, 2, 32).__str__()])
        ovh_r3 = self.addRouter("ovh_r3", lo_addresses=["2023:a:1::3/128", self.IPv4Address(12, 10, 1, 3, 32).__str__()])
        ovh_r4 = self.addRouter("ovh_r4", lo_addresses=["2023:a:1::4/128", self.IPv4Address(12, 10, 1, 4, 32).__str__()])
        ovh_r5 = self.addRouter("ovh_r5", lo_addresses=["2023:a:1::5/128", self.IPv4Address(12, 10, 1, 5, 32).__str__()])
        ovh_r6 = self.addRouter("ovh_r6", lo_addresses=["2023:a:1::6/128", self.IPv4Address(12, 10, 1, 6, 32).__str__()])
        ovh_r7 = self.addRouter("ovh_r7", lo_addresses=["2023:a:2::7/128", self.IPv4Address(12, 10, 2, 1, 32).__str__()])  # ovh_r7, ovh_r8: routers in Roubaix
        ovh_r8 = self.addRouter("ovh_r8", lo_addresses=["2023:a:2::8/128", self.IPv4Address(12, 10, 2, 2, 32).__str__()])
        ovh_r9 = self.addRouter("ovh_r9", lo_addresses=["2023:a:3::9/128", self.IPv4Address(12, 10, 3, 1, 32).__str__()])  # ovh_r9, ovh_r12: routers in Strasbourg
        ovh_r10 = self.addRouter("ovh_r10", lo_addresses=["2023:a:4::a/128", self.IPv4Address(12, 10, 4, 1, 32).__str__()])
        ovh_r11 = self.addRouter("ovh_r11", lo_addresses=["2023:a:4::b/128", self.IPv4Address(12, 10, 4, 2, 32).__str__()])
        ovh_r12 = self.addRouter("ovh_r12", lo_addresses=["2023:a:3::c/128", self.IPv4Address(12, 10, 3, 2, 32).__str__()])
        telia_r1 = self.addRouter("telia_r1", lo_addresses=["2023:a:5::d/128", self.IPv4Address(12, 10, 5, 1, 32).__str__()])
        google_r1 = self.addRouter("google_r1", lo_addresses=["2023:a:6::e/128", self.IPv4Address(12, 10, 6, 1, 32).__str__()])
        cogent_r1 = self.addRouter("cogent_r1", lo_addresses=["2023:a:7::f/128", self.IPv4Address(12, 10, 7, 1, 32).__str__()])
        level3_r1 = self.addRouter("level3_r1", lo_addresses=["2023:a:8::10/128", self.IPv4Address(12, 10, 8, 1, 32).__str__()])
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
        """
        There are 4 RR's configured in a two layer hierarchy, ovh_r7 is in the first layer and ovh_r3, ovh_r10 and ovh_r8 are in the second layer
        """
        peers_rr1 = [ovh_r3, ovh_r10, ovh_r8]
        peers_rr2 = [ovh_r1, ovh_r2, ovh_r5]
        peers_rr3 = [ovh_r9, ovh_r11, ovh_r12]
        peers_rr4 = [ovh_r4, ovh_r6]
        self.add_router_reflector(ovh_r7, peers_rr1)
        self.add_router_reflector(ovh_r3, peers_rr2)
        self.add_router_reflector(ovh_r10, peers_rr3)
        self.add_router_reflector(ovh_r8, peers_rr4)
        # Adding links
        self.add_ip_address_link(ovh_r1, ovh_r2, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 0, 31)))
        self.add_ip_address_link(ovh_r1, ovh_r3, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 2, 31)))
        self.add_ip_address_link(ovh_r2, ovh_r4, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 4, 31)))
        self.add_ip_address_link(ovh_r3, ovh_r4, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 6, 31)))
        self.add_ip_address_link(ovh_r3, ovh_r6, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 8, 31)))
        self.add_ip_address_link(ovh_r3, ovh_r5, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 10, 31)))
        self.add_ip_address_link(ovh_r3, ovh_r9, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 12, 31)))
        self.add_ip_address_link(ovh_r3, ovh_r7, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 14, 31)))
        self.add_ip_address_link(ovh_r4, ovh_r5, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 16, 31)))
        self.add_ip_address_link(ovh_r4, ovh_r6, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 18, 31)))
        self.add_ip_address_link(ovh_r4, ovh_r8, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 20, 31)))
        self.add_ip_address_link(ovh_r4, ovh_r12, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 22, 31)))
        self.add_ip_address_link(ovh_r5, telia_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 24, 31)))
        self.add_ip_address_link(ovh_r6, telia_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 26, 31)))
        self.add_ip_address_link(ovh_r6, level3_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 28, 31)))
        self.add_ip_address_link(ovh_r7, ovh_r8, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 30, 31)))
        self.add_ip_address_link(ovh_r7, ovh_r10, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 32, 31)))
        self.add_ip_address_link(ovh_r8, ovh_r11, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 34, 31)))
        self.add_ip_address_link(ovh_r9, ovh_r12, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 36, 31)))
        self.add_ip_address_link(ovh_r9, ovh_r10, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 38, 31)))
        self.add_ip_address_link(ovh_r10, ovh_r11, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 40, 31)))
        self.add_ip_address_link(ovh_r10, google_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 42, 31)))
        self.add_ip_address_link(ovh_r10, cogent_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 44, 31)))
        self.add_ip_address_link(ovh_r11, ovh_r12, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 46, 31)))
        self.add_ip_address_link(ovh_r11, level3_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 48, 31)))
        self.add_ip_address_link(ovh_r11, cogent_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 50, 31)))
        self.add_ip_address_link(ovh_r11, google_r1, (self.get_ipv6_address(11), self.IPv4Address(12, 11, 0, 52, 31)))
        # Adding eBGP sessions
        ebgp_session(self, ovh_r5, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, level3_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, google_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, cogent_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, level3_r1, link_type=SHARE)

        super().build(*args, **kwargs)

    def add_ip_address_link(self, router1, router2, ip_addr_router):
        """
        Add a link with IPv4 and IPv6 addresses on interface parameters.

        :param router1: (RouterDescription) First router attached to the link.
        :param router2: (RouterDescription) Second router attached to the link.
        :param ip_addr_router: (tuple of str) IP addresses (IPv6, IPv4) of routers.
        """
        link = self.addLink(router1, router2)
        firstRouter, secondRouter = ip_addr_router, ip_addr_router
        link[router1].addParams(ip=(firstRouter[0], firstRouter[1].__str__()))
        secondRouter[1].setHost(secondRouter[1].getFourthByte() + 1)
        link[router2].addParams(ip=(secondRouter[0], secondRouter[1].__str__()))

        link[router1].addParams(ospf_dead_int=8)
        link[router2].addParams(ospf_dead_int=8)
        link[router1].addParams(ospf_hello_int=6)
        link[router2].addParams(ospf_hello_int=6)
        return link

    def add_ospf(self, all_routers):
        """
        Add Open Shortest Path as Interior Gateway Protocol (IGP), both for IPv4 and IPv6.

        :param all_routers: (list of RouterDescription) A list of all routers contained in the network.
        """
        for router in all_routers:
            router.addDaemon(OSPF)
            router.addDaemon(OSPF6)

    def add_ospf_cost(self, router1, router2, ospf_cost_value):
        """
        Add an IPG metric to a link between two routers (default value: 1).

        :param router1: (RouterDescription) A first router.
        :param router2: (RouterDescription) A second router connected to the first one with an OSPF cost on this link.
        :param ospf_cost_value: (int) The (OSPF) IGP metric.
        """
        self.addLink(router1, router2, igp_cost=ospf_cost_value)

    def add_ospf_area(self, router1, router2, ospf_area_value):
        """
        Add an OSPF area of a link between two routers (default value: ‘0.0.0.0’).

        :param router1: (RouterDescription) A first router.
        :param router2: (RouterDescription) A second router connected to the first one with an OSPF area on this link.
        :param ospf_area_value: (str) The OSPF area of the link.
        """
        self.addLink(router1, router2, igp_area=ospf_area_value)

    def set_ospf_priority(self, link, router, priority_value):
        """
        Change the OSPF priority/chances of a router to be the Designated Router (DR).

        :param link: (LinkDescription) Link on which we want to set an IP address.
        :param router: (RouterDescription) Router connected to link on which apply IP addresses (on a given interface).
        :param priority_value: (int) Priority value (highest = best chances to be designated).
        """
        link[router].addParams(ospf_priority=priority_value)

    def set_ospf_hello_interval(self, link, router, hello_timer):
        """
        Change the OSPF hello interval timer.

        :param link: (LinkDescription) Link on which we want to set the timer.
        :param router: (RouterDescription) Router connected to link on which apply the hello timer (on a given
        interface).
        :param hello_timer: (int) Timer.
        """
        link[router].addParams(ospf_hello_int=hello_timer)

    def set_ospf_dead_interval(self, link, router, dead_timer):
        """
        Change the OSPF hello interval timer.

        :param link: (LinkDescription) Link on which we want to set the timer.
        :param router: (RouterDescription) Router connected to link on which apply the hello timer (on a given
        interface).
        :param dead_timer: (int) Timer.
        """
        link[router].addParams(ospf_dead_int=dead_timer)

    def add_bgp(self, all_routers, ovh_routers, telia_routers, google_routers, cogent_routers, level3_routers):
        """
        Add Border Gateway Protocol (BGP) to the routers and specify which prefixes they advertise (both for IPv4
        and IPv6).

        :param all_routers: (list of RouterDescription) A list of all routers contained in the network.
        :param ovh_routers: (list of RouterDescription) List of OVH's routers having an eBGP session which will
        redistribute prefixes advertised by other ASes.
        :param telia_routers: (list of RouterDescription) List of Telia's routers to which OVH routers are connected.
        :param google_routers: (list of RouterDescription) List of Google's routers to which OVH routers are connected.
        :param cogent_routers: (list of RouterDescription) List of Cogent's routers to which OVH routers are connected.
        :param level3_routers: (list of RouterDescription) List of Level3's routers to which OVH routers are connected.
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
            # TODO: family=AF_INET(networks=(...) or address_families=(_bgp.AF_INET(networks=('1.2.3.0/24',)),)?
            router.addDaemon(BGP, family=AF_INET(networks=("dead:beef::/32",), ))  # TODO: change IP address space
            router.addDaemon(BGP, family=AF_INET6(networks=("dead:beef::/32",), ))
        for router in google_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:baef::/32",), ))
            router.addDaemon(BGP, family=AF_INET6(networks=("dead:baef::/32",), ))
        for router in cogent_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:bbef::/32",), ))
            router.addDaemon(BGP, family=AF_INET6(networks=("dead:bbef::/32",), ))
        for router in level3_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:bcef::/32",), ))
            router.addDaemon(BGP, family=AF_INET6(networks=("dead:bcef::/32",), ))

    def set_bgp_local_pref(self, dest_router, local_pref_value, src_router):
        """
        Set the local-pref BGP attribute.

        :param dest_router: (RouterDescription) Destination router influenced by local-pref.
        :param local_pref_value: (int) Local-pref value (if high, it will be preferred).
        :param src_router: (RouterDescription) Source router influenced by local-pref.
        """
        al = AccessList(name='all',
                        entries=('any',))  # Add an access list to "any" (this can be an IP prefix or address instead)
        dest_router.get_config(BGP) \
            .set_local_pref(local_pref_value, from_peer=src_router, matching=(al,))

    def set_bgp_med(self, src_router, med_value, dest_router):
        """
        Set the MED BGP attribute.

        :param src_router: (RouterDescription) Source router whose link to dest_router has a MED value.
        :param med_value: (int) MED value (if high, it will be avoided if possible).
        :param dest_router: (RouterDescription) Destination router whose link to dest_router has a MED value.
        """
        al = AccessList(name='all',
                        entries=('any',))  # Add an access list to "any" (this can be an IP prefix or address instead)
        src_router.get_config(BGP) \
            .set_med(med_value, to_peer=dest_router, matching=(al,))

    def set_ibgp_session(self, router1, router2):
        """
        Register a BGP peering between two nodes router1 and router2.

        :param router1: (RouterDescription) First router.
        :param router2: (RouterDescription) Second router to peer.
        """
        bgp_peering(self, router1, router2)

    def set_ibgp_fullmesh(self, routers_list):
        """
        Set a full-mesh set of iBGP peering between a list of n routers (i.e. (n*(n-1)//2) iBGP peering).

        :param routers_list: (list of RouterDescription) Routers on which a full-mesh iBGP peering is set.
        """
        bgp_fullmesh(self, routers_list)

    def set_bgp_community(self, dest_router, community, src_router):
        """
        Set a BGP community.

        :param dest_router: (RouterDescription) Destination router on which BGP community will be applied.
        :param community: (str) The BGP community value.
        :param src_router: (RouterDescription) Source router influenced by the BGP community.
        """
        al = AccessList(name='all',
                        entries=('any',))  # Add an access list to "any" (this can be an IP prefix or address instead)
        dest_router.get_config(BGP) \
            .set_community(community, from_peer=src_router, matching=(al,))

    def add_router_reflector(self, router_reflector, clients_list):
        """
        Set a router reflector and configure its iBGP peering.

        :param router_reflector: (RouterDescription) Router designated as router reflector.
        :param clients_list: (list of RouterDescription) Clients of the router reflector.
        """
        set_rr(self, rr=router_reflector, peers=clients_list)

    def get_ipv6_address(self, addr, lo=False):
        """
        Get and return an IPv6 address range according to our addressing plan (see docs/Addressing Plan.cmd).
        """
        res = f"2023:{addr}::/{str(MAX_IPV6_PREFIX_LEN)}"
        if lo:
            res = f"2023:a:{addr}::1/{str(IPV6_LO_PREFIX)}"
        return res

    def get_ipv4_address(self, addr, lo=False):
        """
        Get and return an IPv4 address range according to our addressing plan (see docs/Addressing Plan.cmd).
        """
        res = self.IPv4Address(12, addr, 0, 0, MAX_IPV4_PREFIX_LEN)
        if lo:
            res = self.IPv4Address(12, 10, addr, 0, IPV4_LO_PREFIX)
        return res


if __name__ == '__main__':
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    net = IPNet(topo=OVHTopology(), max_v4_prefixlen=MAX_IPV4_PREFIX_LEN, max_v6_prefixlen=MAX_IPV6_PREFIX_LEN,
                allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

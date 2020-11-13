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
    bgp_peering, bgp_fullmesh, RouterConfig
from ipmininet.router.config.zebra import AccessListEntry, DENY, PERMIT

from ip_addresses import IPv4Address, IPv6Address
from announced_prefixes import GOOGLE_IPV4_ANNOUNCED_PREFIXES

# CONSTANT VALUES

# Links and Loopback addresses
IPV4_LO_PREFIX = 32
IPV4_LINK_PREFIX = IPV4_LO_PREFIX - 1
IPV6_LO_PREFIX = 128
IPV6_LINK_PREFIX = IPV6_LO_PREFIX - 1


class OVHTopology(IPTopo):
    """
    This class represents the topology of our OVH model (see ovh_model/img/).
    """

    def build(self, *args, **kwargs):
        """
        Build the topology of our OVH network and set up it by adding routers, links, protocols, setting up routers
        reflectors, etc.
        """
        # Adding routers
        # TODO: hello and dead intervals are wrong on loopback addresses! (Hello 10, Dead 40, Retransmit 5)
        # TODO: hello and dead intervals not configured on some interfaces (example: ovh_r11, eth3)
        ovh_r1 = self.addRouter("ovh_r1", config=RouterConfig, lo_addresses=[
            IPv6Address("2023", "a", "1", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 1, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r2 = self.addRouter("ovh_r2", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 1, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r3 = self.addRouter("ovh_r3", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "3", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 1, 3, IPV4_LO_PREFIX).__str__()])
        ovh_r4 = self.addRouter("ovh_r4", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "4", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 1, 4, IPV4_LO_PREFIX).__str__()])
        ovh_r5 = self.addRouter("ovh_r5", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "5", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 1, 5, IPV4_LO_PREFIX).__str__()])
        ovh_r6 = self.addRouter("ovh_r6", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "6", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 1, 6, IPV4_LO_PREFIX).__str__()])
        ovh_r7 = self.addRouter("ovh_r7", lo_addresses=[
            IPv6Address("2023", "a", "1", "0", "0", "0", "0", "7", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 2, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r8 = self.addRouter("ovh_r8", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "1", "0", "0", "0", "0", "8", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 2, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r9 = self.addRouter("ovh_r9", lo_addresses=[
            IPv6Address("2023", "a", "1", "0", "0", "0", "0", "9", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 3, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r10 = self.addRouter("ovh_r10", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "1", "0", "0", "0", "0", "a", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 4, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r11 = self.addRouter("ovh_r11", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "1", "0", "0", "0", "0", "b", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 4, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r12 = self.addRouter("ovh_r12", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "1", "0", "0", "0", "0", "c", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 3, 2, IPV4_LO_PREFIX).__str__()])
        telia_r1 = self.addRouter("telia_r1", config=RouterConfig,
                                  lo_addresses=[
                                      IPv6Address("2023", "a", "5", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                      IPv4Address(12, 10, 5, 1, IPV4_LO_PREFIX).__str__()])
        google_r1 = self.addRouter("google_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "6", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 6, 1, IPV4_LO_PREFIX).__str__()])
        cogent_r1 = self.addRouter("cogent_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "7", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 7, 1, IPV4_LO_PREFIX).__str__()])
        level3_r1 = self.addRouter("level3_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "8", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 8, 1, IPV4_LO_PREFIX).__str__()])
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
        # Configuring RRs (two-layers hierarchy)
        peers_rr1 = [ovh_r3, ovh_r10, ovh_r8]
        peers_rr2 = [ovh_r1, ovh_r2, ovh_r5]
        peers_rr3 = [ovh_r9, ovh_r11, ovh_r12]
        peers_rr4 = [ovh_r4, ovh_r6]
        self.add_router_reflector(ovh_r7, peers_rr1)
        self.add_router_reflector(ovh_r3, peers_rr2)
        self.add_router_reflector(ovh_r10, peers_rr3)
        self.add_router_reflector(ovh_r8, peers_rr4)
        # Adding links
        self.add_physical_link(ovh_r1, ovh_r2, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "0", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 0, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r1, ovh_r3, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 2, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r2, ovh_r4, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "4", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 4, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r3, ovh_r4, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "6", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 6, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r3, ovh_r6, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "8", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 8, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r3, ovh_r5, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "a", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 10, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r3, ovh_r9, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "b", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 12, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(ovh_r3, ovh_r7, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "c", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 14, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(ovh_r4, ovh_r5, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "10", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 16, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r4, ovh_r6, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "12", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 18, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r4, ovh_r8, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "14", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 20, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(ovh_r4, ovh_r12, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "16", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 22, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(ovh_r5, telia_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "18", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 24, IPV4_LINK_PREFIX)), igp_cost_value=21)
        self.add_physical_link(ovh_r6, telia_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1a", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 26, IPV4_LINK_PREFIX)), igp_cost_value=21)
        self.add_physical_link(ovh_r6, level3_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1b", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 28, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r7, ovh_r8, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1c", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 30, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r7, ovh_r10, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "20", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 32, IPV4_LINK_PREFIX)), igp_cost_value=3)
        self.add_physical_link(ovh_r8, ovh_r11, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "22", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 34, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r9, ovh_r12, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "24", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 36, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r9, ovh_r10, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "26", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 38, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(ovh_r10, ovh_r11, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "28", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 40, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r10, google_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2a", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 42, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(ovh_r10, cogent_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2b", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 44, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r11, ovh_r12, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2c", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 46, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(ovh_r11, level3_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "30", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 48, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r11, cogent_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "32", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 50, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r11, google_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "34", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 52, IPV4_LINK_PREFIX)), igp_cost_value=2)
        # Set BGP parameters (according to announced prefixes)
        al = AccessList(name="all", entries=("any",))
        # With Google (AS 15169)
        ovh_r11.get_config(BGP).set_local_pref(350, from_peer=google_r1, matching=(al,))
        google_r1.get_config(BGP).set_community("16276:34917", from_peer=ovh_r11, matching=(al,))
        # With Cogent (AS 174)
        ovh_r11.get_config(BGP).set_local_pref(80, from_peer=cogent_r1, matching=(al,))
        cogent_r1.get_config(BGP).set_community("16276:10817", from_peer=ovh_r11, matching=(al,))
        # With Level3 (AS 3356)
        ovh_r11.get_config(BGP).set_local_pref(100, from_peer=level3_r1, matching=(al,))
        level3_r1.get_config(BGP).set_community("16276:10217", from_peer=ovh_r11, matching=(al,))
        # Adding eBGP sessions
        ebgp_session(self, ovh_r5, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, telia_r1, link_type=SHARE)
        ebgp_session(self, ovh_r6, level3_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, google_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, cogent_r1, link_type=SHARE)
        ebgp_session(self, ovh_r11, level3_r1, link_type=SHARE)

        super().build(*args, **kwargs)

    def add_physical_link(self, router1, router2, ip_addr_routers, igp_cost_value=1, hello_timer=6, dead_timer=8):
        """
        Add a physical link with IPv4 and IPv6 addresses on interface parameters between two given routers.

        :param router1: (RouterDescription) First router attached to the link.
        :param router2: (RouterDescription) Second router attached to the link.
        :param ip_addr_routers: (tuple of str) IP addresses (IPv6, IPv4) of routers.
        :param igp_cost_value: (int) The (OSPF) IGP metric to add between the routers (default value: 1).
        :param hello_timer: (int) Interval (timer) in seconds for the OSPF hello messages.
        :param dead_timer: (int) Interval (timer) in seconds for the OSPF dead messages.
        """
        link = self.addLink(router1, router2, igp_cost=igp_cost_value)
        ip_addr_router1, ip_addr_router2 = ip_addr_routers, ip_addr_routers
        link[router1].addParams(ip=(ip_addr_router1[0].__str__(), ip_addr_router1[1].__str__()))
        ip_addr_router2[0].set_host(ip_addr_router2[0].increment(7))
        ip_addr_router2[1].set_host(ip_addr_router2[1].get_fourth_byte() + 1)
        link[router2].addParams(ip=(ip_addr_router2[0].__str__(), ip_addr_router2[1].__str__()))
        link[router1].addParams(ospf_dead_int=dead_timer)
        link[router2].addParams(ospf_dead_int=dead_timer)
        link[router1].addParams(ospf_hello_int=hello_timer)
        link[router2].addParams(ospf_hello_int=hello_timer)

    def add_ospf(self, all_routers):
        """
        Add Open Shortest Path as Interior Gateway Protocol (IGP), both for IPv4 and IPv6.

        :param all_routers: (list of RouterDescription) A list of all routers contained in the network.
        """
        for router in all_routers:
            router.addDaemon(OSPF)
            router.addDaemon(OSPF6)

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
        router_id = "1.1.1."
        i = 0
        for router in all_routers:
            router.addDaemon(BGP, address_families=(family_ipv4, family_ipv6))
        for router in ovh_routers:
            i += 1
            router.addDaemon(BGP, routerid=router_id + str(i), family=AF_INET(redistribute=("ospf", "connected"), ))
            router.addDaemon(BGP, routerid=router_id + str(i), family=AF_INET6(redistribute=("ospf6", "connected"), ))
        # Other ASes advertise specific prefixes
        for router in telia_routers:
            router.addDaemon(BGP, family=AF_INET(networks=("dead:beef::/32",), ))  # TODO: change IP address space
            router.addDaemon(BGP, family=AF_INET6(networks=("dead:beef::/32",), ))
        for router in google_routers:
            router.addDaemon(BGP, family=GOOGLE_IPV4_ANNOUNCED_PREFIXES)
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


if __name__ == '__main__':
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    net = IPNet(topo=OVHTopology(), use_v4=True, use_v6=True, allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

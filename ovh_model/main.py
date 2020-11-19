#!/usr/bin/env python3

"""
LINGI2142: Computer Networks: Configuration and Management
File: main.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file sets up in Mininet the part of the OVH's network that we have chosen.
"""
from typing import Union

from mininet.log import lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import OSPF, BGP, set_rr, ebgp_session, SHARE, AF_INET6, AF_INET, OSPF6, AccessList, \
    bgp_peering, bgp_fullmesh, RouterConfig
from ipmininet.router.config.zebra import AccessListEntry, DENY, PERMIT
from ipmininet.host.config import Named, ARecord, PTRRecord, AAAARecord
from ipaddress import ip_address

from ip_addresses import IPv4Address, IPv6Address
from announced_prefixes import GOOGLE_IPV4_ANNOUNCED_PREFIXES

# CONSTANT VALUES

# Links and Loopback addresses
from ovh_model.announced_prefixes import COGENT_IPV4_ANNOUNCED_PREFIXES, LEVEL3_IPV4_ANNOUNCED_PREFIXES

IPV4_LO_PREFIX = 32
IPV4_LINK_PREFIX = IPV4_LO_PREFIX - 1
IPV6_LO_PREFIX = 128
IPV6_LINK_PREFIX = IPV6_LO_PREFIX - 1

DOMAIN = "ovh.com"


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
        ovh_r1 = self.addRouter("ovh_r1", config=RouterConfig, lo_addresses=[
            IPv6Address("2023", "a", "c", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 12, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r2 = self.addRouter("ovh_r2", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "c", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 12, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r3 = self.addRouter("ovh_r3", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "c", "0", "0", "0", "0", "3", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 12, 3, IPV4_LO_PREFIX).__str__()])
        ovh_r4 = self.addRouter("ovh_r4", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "c", "0", "0", "0", "0", "4", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 12, 4, IPV4_LO_PREFIX).__str__()])
        ovh_r5 = self.addRouter("ovh_r5", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "c", "0", "0", "0", "0", "5", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 12, 5, IPV4_LO_PREFIX).__str__()])
        ovh_r6 = self.addRouter("ovh_r6", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "c", "0", "0", "0", "0", "6", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 12, 6, IPV4_LO_PREFIX).__str__()])
        ovh_r7 = self.addRouter("ovh_r7", lo_addresses=[
            IPv6Address("2023", "a", "d", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 13, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r8 = self.addRouter("ovh_r8", config=RouterConfig,
                                lo_addresses=[
                                    IPv6Address("2023", "a", "d", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                    IPv4Address(12, 10, 13, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r9 = self.addRouter("ovh_r9", lo_addresses=[
            IPv6Address("2023", "a", "e", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
            IPv4Address(12, 10, 14, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r10 = self.addRouter("ovh_r10", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "f", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 15, 1, IPV4_LO_PREFIX).__str__()])
        ovh_r11 = self.addRouter("ovh_r11", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "f", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 15, 2, IPV4_LO_PREFIX).__str__()])
        ovh_r12 = self.addRouter("ovh_r12", config=RouterConfig,
                                 lo_addresses=[
                                     IPv6Address("2023", "a", "e", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                     IPv4Address(12, 10, 14, 2, IPV4_LO_PREFIX).__str__()])
        telia_r1 = self.addRouter("telia_r1", config=RouterConfig,
                                  lo_addresses=[
                                      IPv6Address("2023", "a", "5", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                      IPv4Address(12, 10, 20, 1, IPV4_LO_PREFIX).__str__()])
        google_r1 = self.addRouter("google_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "6", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 21, 1, IPV4_LO_PREFIX).__str__()])
        cogent_r1 = self.addRouter("cogent_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "7", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 22, 1, IPV4_LO_PREFIX).__str__()])
        level3_r1 = self.addRouter("level3_r1", config=RouterConfig,
                                   lo_addresses=[
                                       IPv6Address("2023", "a", "8", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                       IPv4Address(12, 10, 23, 1, IPV4_LO_PREFIX).__str__()])
        all_routers = [ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11,
                       ovh_r12, telia_r1, google_r1, cogent_r1, level3_r1]
        # Adding protocols to routers
        self.add_ospf(all_routers)
        self.add_bgp(all_routers, [ovh_r5, ovh_r6, ovh_r10, ovh_r11], [telia_r1], [google_r1], [cogent_r1], [level3_r1])
        # Adding AS ownerships
        self.addAS(1,
                   (ovh_r1, ovh_r2, ovh_r3, ovh_r4, ovh_r5, ovh_r6, ovh_r7, ovh_r8, ovh_r9, ovh_r10, ovh_r11, ovh_r12))
        self.addAS(2, (telia_r1,))
        self.addAS(3, (cogent_r1,))
        self.addAS(4, (level3_r1,))
        self.addAS(5, (google_r1,))
        # Configuring RRs
        peers_rr1 = [ovh_r7, ovh_r8, ovh_r6] + [ovh_r1, ovh_r2, ovh_r4, ovh_r5]  # ovh_r3
        peers_rr2 = [ovh_r3, ovh_r8, ovh_r7] + [ovh_r1, ovh_r2, ovh_r4, ovh_r5]  # ovh_r6
        peers_rr3 = [ovh_r3, ovh_r8, ovh_r6] + [ovh_r9, ovh_r10, ovh_r11, ovh_r12]  # ovh_r7
        peers_rr4 = [ovh_r3, ovh_r7, ovh_r6] + [ovh_r9, ovh_r10, ovh_r11, ovh_r12]  # ovh_r8
        self.add_router_reflector(ovh_r3, peers_rr1)
        self.add_router_reflector(ovh_r6, peers_rr2)
        self.add_router_reflector(ovh_r7, peers_rr3)
        self.add_router_reflector(ovh_r8, peers_rr4)
        # DNS anycast
        ovh_webserver1 = self.addHost("webserver1")
        ovh_dns_resolver1 = self.addHost("resolver1")
        ovh_dns_resolver2 = self.addHost("resolver2")
        self.add_physical_link(ovh_r7, ovh_dns_resolver1, (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36",
                                                                       IPV6_LINK_PREFIX), IPv4Address(12, 11, 0, 54,
                                                                                                      IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r4, ovh_dns_resolver2, (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36",
                                                                       IPV6_LINK_PREFIX), IPv4Address(12, 11, 0, 54,
                                                                                                      IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r11, ovh_webserver1, (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "38",
                                                                     IPV6_LINK_PREFIX), IPv4Address(12, 11, 0, 56,
                                                                                                    IPV4_LINK_PREFIX)))
        ovh_dns_resolver1.addDaemon(Named)
        ovh_dns_resolver2.addDaemon(Named)
        self.addDNSZone(name=DOMAIN, dns_master=ovh_dns_resolver1, dns_slaves=[ovh_dns_resolver2],
                        nodes=[ovh_webserver1])
        reverse_domain_name_ipv6 = ip_address("2023::").reverse_pointer[-10:]  # adding a missing PTR record
        ptr_record_ipv6 = PTRRecord(
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "38", IPV6_LINK_PREFIX).__str__()[:-4],
            ovh_webserver1 + f".{DOMAIN}")
        self.addDNSZone(name=reverse_domain_name_ipv6, dns_master=ovh_dns_resolver1, dns_slaves=[ovh_dns_resolver2],
                        ns_domain_name=DOMAIN, records=[ptr_record_ipv6])
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
            IPv4Address(12, 11, 0, 24, IPV4_LINK_PREFIX)))
        self.add_physical_link(ovh_r6, telia_r1, (
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1a", IPV6_LINK_PREFIX),
            IPv4Address(12, 11, 0, 26, IPV4_LINK_PREFIX)))
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
        ebgp_session(self, ovh_r5, telia_r1)
        ebgp_session(self, ovh_r6, telia_r1)
        ebgp_session(self, ovh_r6, level3_r1)
        ebgp_session(self, ovh_r11, google_r1)
        ebgp_session(self, ovh_r11, cogent_r1)
        ebgp_session(self, ovh_r11, level3_r1)
        ebgp_session(self, ovh_r10, cogent_r1)
        ebgp_session(self, ovh_r10, google_r1)

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
        # Other AS advertise specific prefixes
        for router in google_routers:
            router.addDaemon(BGP, family=GOOGLE_IPV4_ANNOUNCED_PREFIXES)
        for router in cogent_routers:
            router.addDaemon(BGP, family=COGENT_IPV4_ANNOUNCED_PREFIXES)
        for router in level3_routers:
            router.addDaemon(BGP, family=LEVEL3_IPV4_ANNOUNCED_PREFIXES)

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

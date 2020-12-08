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
from ipmininet.iptopo import IPTopo, RouterDescription
from ipmininet.router.config import OSPF, BGP, set_rr, ebgp_session, AF_INET6, AF_INET, OSPF6, RouterConfig, CLIENT_PROVIDER, IPTables, IP6Tables, Rule
from ipmininet.host.config import Named, PTRRecord
from ipaddress import ip_address

from ip_addresses import IPv4Address, IPv6Address

# CONSTANT VALUES

IPV4_LO_PREFIX = 32
IPV4_LINK_PREFIX = IPV4_LO_PREFIX - 1
IPV4_SUBNET_PREFIX = 27
IPV6_LO_PREFIX = 128
IPV6_LINK_PREFIX = IPV6_LO_PREFIX - 1
IPV6_SUBNET_PREFIX = 48

DOMAIN = "ovh.com"

OVH_AS = 16276
GOOGLE_AS = 15169
COGENT_AS = 174
LEVEL3_AS = 3356
TELIA_AS = 1299

SUBNETS_IPV4 =   {"fra1_g1": "12.16.218.0/30", "fra1_g2": "12.16.218.4/30", "fra_sbb1": "12.16.218.8/30", "fra_sbb2": "12.16.218.12/30", "fra_1": "12.16.218.16/30", "fra_5": "12.16.218.20/30",
            "rbx_g1": "12.16.218.32/30", "rbx_g2": "12.16.218.36/30",
            "sbg_g1": "12.16.218.64/30", "sbg_g2": "12.16.218.68/30",
            "par_th2": "12.16.218.96/30", "par_gsw": "12.16.218.100/30",
            "telia": "123.3.2.0/30", "cogent": "125.3.2.0/30", "google": "124.3.2.0/30", "level3": "126.3.2.0/30"}

SUBNETS_IPV6 =   {"fra1_g1": "2023:c:1::/48", "fra1_g2": "2023:c:2::/48", "fra_sbb1": "2023:c:3::/48", "fra_sbb2": "2023:c:4::/48", "fra_1": "2023:c:5::/48", "fra_5": "2023:c:6::/48",
            "rbx_g1": "2023:d:1::/48", "rbx_g2": "2023:d:2::/48",
            "sbg_g1": "2023:e:1::/48", "sbg_g2": "2023:e:2::/48",
            "par_th2": "2023:f:1::/48", "par_gsw": "2023:f:2::/48",
            "telia": "2028:a:1::/48", "cogent": "2029:a:1::/48", "google": "2019:a:1::/48", "level3": "2020:a:1::/48"}

class RouterDesc(RouterDescription):
    def addInterfaceSupport(self):
        self.i = RouterInterfaces(self.__str__())

    def interfaces(self):
        return self.i


class RouterInterfaces():
    def __init__(self, router):
        self.intefaces = list()
        self.r = router

    def addInterface(self, router_name):
        count = len(self.intefaces)
        self.intefaces.append(self.Interface(self.r, router_name, count))

    def getInterfaces(self):
        return self.intefaces

    class Interface():
        def __init__(self, from_router, to_router, int_nbr):
            self.i = "{}-eth{}".format(from_router, int_nbr)
            self.peer_router = to_router

        def __str__(self):
            return self.i

        def getPeerRouter(self):
            return self.peer_router


class OVHTopology(IPTopo):
    """
    This class represents the topology of our OVH model (see ovh_model/img/).
    """

    def addRouter(self, router_name, lo_addresses: list):
        router = super().addRouter(router_name, config=RouterConfig, lo_addresses=lo_addresses)
        router.__class__ = RouterDesc
        router.addInterfaceSupport()
        host = self.addHost("h_{}".format(router_name))
        l = self.addLink(router, host)
        self.addSubnet(links=[l], subnets=[SUBNETS_IPV6[router_name], SUBNETS_IPV4[router_name]])
        return router

    def build(self, *args, **kwargs):
        """
        Build the topology of our OVH network and set up it by adding routers, links, protocols, setting up routers
        reflectors, etc.
        """
        # TODO: check IPv6 addresses
        # Adding routers
        fra1_g1 = self.addRouter("fra1_g1", [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 1, IPV4_LO_PREFIX).__str__()])
        fra1_g2 = self.addRouter("fra1_g2", [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 2, IPV4_LO_PREFIX).__str__()])
        fra_sbb1 = self.addRouter("fra_sbb1",   [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "3", IPV6_LO_PREFIX).__str__(),
                                                IPv4Address(12, 16, 216, 3, IPV4_LO_PREFIX).__str__()])
        fra_sbb2 = self.addRouter("fra_sbb2",   [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "4", IPV6_LO_PREFIX).__str__(),
                                                IPv4Address(12, 16, 216, 4, IPV4_LO_PREFIX).__str__()])
        fra_1 = self.addRouter("fra_1", [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "5", IPV6_LO_PREFIX).__str__(),
                                        IPv4Address(12, 16, 216, 5, IPV4_LO_PREFIX).__str__()])
        fra_5 = self.addRouter("fra_5", [IPv6Address("2023", "a", "c", "0", "0", "0", "0", "6", IPV6_LO_PREFIX).__str__(),
                                        IPv4Address(12, 16, 216, 6, IPV4_LO_PREFIX).__str__()])
        rbx_g1 = self.addRouter("rbx_g1",   [IPv6Address("2023", "a", "d", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 7, IPV4_LO_PREFIX).__str__()])
        rbx_g2 = self.addRouter("rbx_g2",   [IPv6Address("2023", "a", "d", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 8, IPV4_LO_PREFIX).__str__()])
        sbg_g1 = self.addRouter("sbg_g1",   [IPv6Address("2023", "a", "e", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 9, IPV4_LO_PREFIX).__str__()])
        sbg_g2 = self.addRouter("sbg_g2",   [IPv6Address("2023", "a", "e", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 10, IPV4_LO_PREFIX).__str__()])
        par_th2 = self.addRouter("par_th2", [IPv6Address("2023", "a", "f", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 11, IPV4_LO_PREFIX).__str__()])
        par_gsw = self.addRouter("par_gsw", [IPv6Address("2023", "a", "f", "0", "0", "0", "0", "2", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(12, 16, 216, 12, IPV4_LO_PREFIX).__str__()])
        telia = self.addRouter("telia", [IPv6Address("2299", "a", "5", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                        IPv4Address(123, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        google = self.addRouter("google",   [IPv6Address("2169", "a", "6", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(124, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        cogent = self.addRouter("cogent",   [IPv6Address("2174", "a", "7", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(125, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        level3 = self.addRouter("level3",   [IPv6Address("2356", "a", "8", "0", "0", "0", "0", "1", IPV6_LO_PREFIX).__str__(),
                                            IPv4Address(126, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        all_routers = [fra1_g1, fra1_g2, fra_sbb1, fra_sbb2, fra_1, fra_5, rbx_g1, rbx_g2, sbg_g1,
                       sbg_g2, par_th2, par_gsw, telia, google, cogent, level3]
        fra_routers = [fra1_g1, fra1_g2, fra_sbb1, fra_sbb2, fra_1, fra_5]  # In Frankfurt
        rbx_routers = [rbx_g1, rbx_g2]  # In Roubaix
        sbg_routers = [sbg_g1, sbg_g2]  # In Strasbourg
        par_routers = [par_th2, par_gsw]  # In Paris
        ovh_routers = fra_routers + rbx_routers + sbg_routers + par_routers

        sbg_web = self.addHost("sbg_web")  # for anycast
        self.addLink(sbg_web, sbg_g2)
        # TODO: change to Router (in order to set a loopback address)
        fra_server = self.addHost("fra_server")
        self.addLink(fra_server, fra_sbb2)
        rbx_server = self.addHost("rbx_server")
        self.addLink(rbx_server, rbx_g1)

        # Adding physical links
        self.add_physical_link(fra1_g1, fra1_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "0", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 0, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra1_g1, fra_sbb1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 2, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra1_g2, fra_sbb2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "4", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 4, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb1, fra_sbb2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "6", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 6, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb1, fra_5,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "8", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 8, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb1, fra_1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "a", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 10, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb1, sbg_g1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "b", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 12, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(fra_sbb1, rbx_g1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "c", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 14, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(fra_sbb2, fra_1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "10", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 16, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb2, fra_5,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "12", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 18, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb2, rbx_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "14", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 20, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(fra_sbb2, sbg_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "16", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 22, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(fra_1, telia,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "18", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 24, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_5, telia,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1a", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 26, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_5, level3,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1b", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 28, IPV4_LINK_PREFIX)))
        self.add_physical_link(rbx_g1, rbx_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "1c", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 30, IPV4_LINK_PREFIX)))
        self.add_physical_link(rbx_g1, par_th2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "20", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 32, IPV4_LINK_PREFIX)), igp_cost_value=3)
        self.add_physical_link(rbx_g2, par_gsw,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "22", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 34, IPV4_LINK_PREFIX)))
        self.add_physical_link(sbg_g1, sbg_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "24", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 36, IPV4_LINK_PREFIX)))
        self.add_physical_link(sbg_g1, par_th2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "26", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 38, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(par_th2, par_gsw,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "28", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 40, IPV4_LINK_PREFIX)))
        self.add_physical_link(par_th2, google,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2a", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 42, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(par_th2, cogent,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2b", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 44, IPV4_LINK_PREFIX)))
        self.add_physical_link(par_gsw, sbg_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2c", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 46, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(par_gsw, level3,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "30", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 48, IPV4_LINK_PREFIX)))
        self.add_physical_link(par_gsw, cogent,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "32", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 50, IPV4_LINK_PREFIX)))
        self.add_physical_link(par_gsw, google,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "34", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 52, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(rbx_g1, fra_server,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 54, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_sbb2, rbx_server,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 54, IPV4_LINK_PREFIX)))
        self.add_physical_link(sbg_g2, sbg_web,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "38", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 56, IPV4_LINK_PREFIX)))

        # Adding OSPF and BGP daemons to routers
        self.add_ospf(all_routers)
        self.add_bgp(all_routers, [fra_1, fra_5, par_th2, par_gsw], [telia], [google], [cogent], [level3])

        # OSPF Security
        # TODO

        # BGP Security
        # TODO

        # Adding AS ownerships
        self.addAS(OVH_AS,
                   (fra1_g1, fra1_g2, fra_sbb1, fra_sbb2, fra_1, fra_5, rbx_g1, rbx_g2, sbg_g1,
                    par_th2, par_gsw, sbg_g2))
        self.addAS(TELIA_AS, (telia,))
        self.addAS(COGENT_AS, (cogent,))
        self.addAS(LEVEL3_AS, (level3,))
        self.addAS(GOOGLE_AS, (google,))

        # Configuring RRs/iBGP sessions
        peers_fra_fr5_sbb1 = peers_fra_5 = [fra1_g1, fra1_g2, fra_sbb2, fra_1]
        peers_rbx_g1 = peers_rbx_g2 = [sbg_g1, par_th2, par_gsw, sbg_g2]
        set_rr(self, rr=fra_sbb1, peers=peers_fra_fr5_sbb1)
        set_rr(self, rr=fra_5, peers=peers_fra_5)
        set_rr(self, rr=rbx_g1, peers=peers_rbx_g1)
        set_rr(self, rr=rbx_g2, peers=peers_rbx_g2)
        self.addiBGPFullMesh(16276, routers=[fra_sbb1, fra_5, rbx_g1, rbx_g2])  # 4*3/2 iBGP sessions

        # Adding eBGP sessions
        ebgp_session(self, telia, fra_1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, telia, fra_5, link_type=CLIENT_PROVIDER)
        ebgp_session(self, level3, fra_5, link_type=CLIENT_PROVIDER)
        ebgp_session(self, google, par_gsw, link_type=CLIENT_PROVIDER)
        ebgp_session(self, cogent, par_gsw, link_type=CLIENT_PROVIDER)
        ebgp_session(self, level3, par_gsw, link_type=CLIENT_PROVIDER)
        ebgp_session(self, cogent, par_th2, link_type=CLIENT_PROVIDER)
        ebgp_session(self, google, par_th2, link_type=CLIENT_PROVIDER)

        # DNS anycast
        # TODO: to check
        fra_server.addDaemon(Named)
        rbx_server.addDaemon(Named)
        self.addDNSZone(name=DOMAIN, dns_master=fra_server, dns_slaves=[rbx_server],
                        nodes=[sbg_web])
        reverse_domain_name_ipv6 = ip_address("2023::").reverse_pointer[-10:]  # adding a missing PTR record
        ptr_record_ipv6 = PTRRecord(
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "38", IPV6_LINK_PREFIX).__str__()[:-4],
            sbg_web + f".{DOMAIN}")
        self.addDNSZone(name=reverse_domain_name_ipv6, dns_master=fra_server, dns_slaves=[rbx_server],
                        ns_domain_name=DOMAIN, records=[ptr_record_ipv6])
        super().build(*args, **kwargs)

    def add_physical_link(self, router1, router2, ip_addr_routers, igp_cost_value=1, hello_timer=3, dead_timer=12):
        """
        Add a physical link with IPv4 and IPv6 addresses on interface parameters between two given routers.

        :param router1: (RouterDescription) First router attached to the link.
        :param router2: (RouterDescription) Second router attached to the link.
        :param ip_addr_routers: (tuple of str) IP addresses (IPv6, IPv4) of routers.
        :param igp_cost_value: (int) The (OSPF) IGP metric to add between the routers (default value: 1).
        :param hello_timer: (int) Interval (timer) in seconds for the OSPF hello messages.
        :param dead_timer: (int) Interval (timer) in seconds for the OSPF dead messages.
        """
        link = self.addLink(router1, router2, igp_cost=igp_cost_value, password="{}-{}".format(router1.__str__(), router2.__str__()))
        ip_addr_router1, ip_addr_router2 = ip_addr_routers, ip_addr_routers
        link[router1].addParams(ip=(ip_addr_router1[0].__str__(), ip_addr_router1[1].__str__()))
        ip_addr_router2[0].set_host(ip_addr_router2[0].increment(7))
        ip_addr_router2[1].set_host(ip_addr_router2[1].get_fourth_byte() + 1)
        link[router2].addParams(ip=(ip_addr_router2[0].__str__(), ip_addr_router2[1].__str__()))
        link[router1].addParams(ospf_dead_int=dead_timer)
        link[router2].addParams(ospf_dead_int=dead_timer)
        link[router1].addParams(ospf_hello_int=hello_timer)
        link[router2].addParams(ospf_hello_int=hello_timer)
        if isinstance(router1, RouterDesc) and isinstance(router2, RouterDesc): # If both are routers
            router1.interfaces().addInterface(router2.__str__())
            router2.interfaces().addInterface(router1.__str__())

    def add_ospf(self, routers):
        """
        Add Open Shortest Path as Interior Gateway Protocol (IGP), both for IPv4 and IPv6.

        :param routers: (list of RouterDescription) A list of all routers contained in the network.
        """
        for router in routers:
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
        rules = [Rule("-A INPUT -p 89 -j DROP"), Rule("-A OUTPUT -p 89 -j DROP")] # Drop incomming and outgoing OSPF packets (for external AS)
        families = (AF_INET(redistribute=("connected",)), AF_INET6(redistribute=("connected",)))
        for router in all_routers:
            router.addDaemon(BGP, address_families=families)
        for router in ovh_routers:
            router.addDaemon(BGP, address_families=families)
            ovh_rules = list()
            for interface in router.interfaces().getInterfaces():
                if "_" not in interface.getPeerRouter(): # Check if it is a peer router
                    ovh_rules.append(Rule("-A INPUT -i {} -p 89 -j DROP".format(interface))) # Drop OSPF packets from other AS
                    ovh_rules.append(Rule("-A OUTPUT -o {} -p 89 -j DROP".format(interface))) # Drop OSPF packets to other AS
                    # Accept 30 connections before limiting a 2 connections per second
                    ovh_rules.append(Rule("-A INPUT -i {} -m limit --limit 2/s --limit-burst 30 -j ACCEPT".format(interface))) 
            router.addDaemon(IPTables, rules=ovh_rules)
            router.addDaemon(IP6Tables, rules=ovh_rules)
        # Other AS advertise specific prefixes
        for router in google_routers:
            router.addDaemon(BGP, address_families=families)
            router.addDaemon(IPTables, rules=rules)
            router.addDaemon(IP6Tables, rules=rules)
        for router in cogent_routers:
            router.addDaemon(BGP, address_families=families)
            router.addDaemon(IPTables, rules=rules)
            router.addDaemon(IP6Tables, rules=rules)
        for router in level3_routers:
            router.addDaemon(BGP, address_families=families)
            router.addDaemon(IPTables, rules=rules)
            router.addDaemon(IP6Tables, rules=rules)
        for router in telia_routers:
            router.addDaemon(BGP, address_families=families)
            router.addDaemon(IPTables, rules=rules)
            router.addDaemon(IP6Tables, rules=rules)


if __name__ == '__main__':
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    net = IPNet(topo=OVHTopology(), use_v4=True, use_v6=True, allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
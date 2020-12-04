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
from ipmininet.router.config import OSPF, BGP, set_rr, ebgp_session, AF_INET6, AF_INET, OSPF6, RouterConfig
from ipmininet.host.config import Named, PTRRecord
from ipaddress import ip_address

from ip_addresses import IPv4Address, IPv6Address

# CONSTANT VALUES

IPV4_LO_PREFIX = 32
IPV4_LINK_PREFIX = IPV4_LO_PREFIX - 1
IPV6_LO_PREFIX = 128
IPV6_LINK_PREFIX = IPV6_LO_PREFIX - 1

DOMAIN = "ovh.com"

OVH_AS = 16276
GOOGLE_AS = 15169
COGENT_AS = 174
LEVEL3_AS = 3356
TELIA_AS = 1299


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
        fra1_lim1_g1 = self.addRouter("fra1_lim1_g1",
                                      config=RouterConfig,
                                      lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "1",
                                                                IPV6_LO_PREFIX).__str__(),
                                                    IPv4Address(12, 16, 216, 1, IPV4_LO_PREFIX).__str__()])
        fra1_lim1_g2 = self.addRouter("fra1_lim1_g2",
                                      config=RouterConfig,
                                      lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "2",
                                                                IPV6_LO_PREFIX).__str__(),
                                                    IPv4Address(12, 16, 216, 2, IPV4_LO_PREFIX).__str__()])
        fra_fr5_sbb1 = self.addRouter("fra_fr5_sbb1",
                                      config=RouterConfig,
                                      lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "3",
                                                                IPV6_LO_PREFIX).__str__(),
                                                    IPv4Address(12, 16, 216, 3, IPV4_LO_PREFIX).__str__()])
        fra_fr5_sbb2 = self.addRouter("fra_fr5_sbb2",
                                      config=RouterConfig,
                                      lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "4",
                                                                IPV6_LO_PREFIX).__str__(),
                                                    IPv4Address(12, 16, 216, 4, IPV4_LO_PREFIX).__str__()])
        fra_1 = self.addRouter("fra_1",
                               config=RouterConfig,
                               lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "5",
                                                         IPV6_LO_PREFIX).__str__(),
                                             IPv4Address(12, 16, 216, 5, IPV4_LO_PREFIX).__str__()])
        fra_5 = self.addRouter("fra_5",
                               config=RouterConfig,
                               lo_addresses=[IPv6Address("2023", "a", "c", "0", "0", "0", "0", "6",
                                                         IPV6_LO_PREFIX).__str__(),
                                             IPv4Address(12, 16, 216, 6, IPV4_LO_PREFIX).__str__()])
        rbx_g1 = self.addRouter("rbx_g1",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "d", "0", "0", "0", "0", "1",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(12, 16, 216, 7, IPV4_LO_PREFIX).__str__()])
        rbx_g2 = self.addRouter("rbx_g2",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "d", "0", "0", "0", "0", "2",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(12, 16, 216, 8, IPV4_LO_PREFIX).__str__()])
        sbg_g1 = self.addRouter("sbg_g1",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "e", "0", "0", "0", "0", "1",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(12, 16, 216, 9, IPV4_LO_PREFIX).__str__()])
        sbg_g2 = self.addRouter("sbg_g2",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "e", "0", "0", "0", "0", "2",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(12, 16, 216, 10, IPV4_LO_PREFIX).__str__()])
        par_th2 = self.addRouter("par_th2",
                                 config=RouterConfig,
                                 lo_addresses=[IPv6Address("2023", "a", "f", "0", "0", "0", "0", "1",
                                                           IPV6_LO_PREFIX).__str__(),
                                               IPv4Address(12, 16, 216, 11, IPV4_LO_PREFIX).__str__()])
        par_gsw = self.addRouter("par_gsw",
                                 config=RouterConfig,
                                 lo_addresses=[IPv6Address("2023", "a", "f", "0", "0", "0", "0", "2",
                                                           IPV6_LO_PREFIX).__str__(),
                                               IPv4Address(12, 16, 216, 12, IPV4_LO_PREFIX).__str__()])
        telia = self.addRouter("telia",
                               config=RouterConfig,
                               lo_addresses=[IPv6Address("2023", "a", "5", "0", "0", "0", "0", "1",
                                                         IPV6_LO_PREFIX).__str__(),
                                             IPv4Address(123, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        google = self.addRouter("google",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "6", "0", "0", "0", "0", "1",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(124, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        cogent = self.addRouter("cogent",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "7", "0", "0", "0", "0", "1",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(125, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        level3 = self.addRouter("level3",
                                config=RouterConfig,
                                lo_addresses=[IPv6Address("2023", "a", "8", "0", "0", "0", "0", "1",
                                                          IPV6_LO_PREFIX).__str__(),
                                              IPv4Address(126, 3, 2, 1, IPV4_LO_PREFIX).__str__()])
        all_routers = [fra1_lim1_g1, fra1_lim1_g2, fra_fr5_sbb1, fra_fr5_sbb2, fra_1, fra_5, rbx_g1, rbx_g2, sbg_g1,
                       par_th2, par_gsw, sbg_g2, telia, google, cogent, level3]

        # Subnets
        # TODO

        # Hosts
        telia_host = self.addHost("telia_host")
        self.addLink(telia_host, telia)
        google_host = self.addHost("google_host")
        self.addLink(google_host, google)
        cogent_host = self.addHost("cogent_host")
        self.addLink(cogent_host, cogent)
        level3_host = self.addHost("level3_host")
        self.addLink(level3_host, level3)
        sbg_webserver = self.addHost("sbg_webserver")  # for anycast
        fra_dns_resolver = self.addHost("fra_dns_resolver")
        rbx_dns_resolver = self.addHost("rbx_dns_resolver")

        # Adding physical links
        self.add_physical_link(fra1_lim1_g1, fra1_lim1_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "0", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 0, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra1_lim1_g1, fra_fr5_sbb1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "2", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 2, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra1_lim1_g2, fra_fr5_sbb2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "4", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 4, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb1, fra_fr5_sbb2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "6", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 6, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb1, fra_5,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "8", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 8, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb1, fra_1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "a", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 10, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb1, sbg_g1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "b", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 12, IPV4_LINK_PREFIX)), igp_cost_value=2)
        self.add_physical_link(fra_fr5_sbb1, rbx_g1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "c", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 14, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(fra_fr5_sbb2, fra_1,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "10", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 16, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb2, fra_5,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "12", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 18, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb2, rbx_g2,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "14", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 20, IPV4_LINK_PREFIX)), igp_cost_value=5)
        self.add_physical_link(fra_fr5_sbb2, sbg_g2,
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
        self.add_physical_link(rbx_g1, fra_dns_resolver,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 54, IPV4_LINK_PREFIX)))
        self.add_physical_link(fra_fr5_sbb2, rbx_dns_resolver,
                               (IPv6Address("2023", "b", "0", "0", "0", "0", "0", "36", IPV6_LINK_PREFIX),
                                IPv4Address(12, 16, 217, 54, IPV4_LINK_PREFIX)))
        self.add_physical_link(sbg_g2, sbg_webserver,
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
                   (fra1_lim1_g1, fra1_lim1_g2, fra_fr5_sbb1, fra_fr5_sbb2, fra_1, fra_5, rbx_g1, rbx_g2, sbg_g1,
                    par_th2, par_gsw, sbg_g2))
        self.addAS(TELIA_AS, (telia,))
        self.addAS(COGENT_AS, (cogent,))
        self.addAS(LEVEL3_AS, (level3,))
        self.addAS(GOOGLE_AS, (google,))

        # Configuring RRs/iBGP sessions
        peers_fra_fr5_sbb1 = peers_fra_5 = [fra1_lim1_g1, fra1_lim1_g2, fra_fr5_sbb2, fra_1]
        peers_rbx_g1 = peers_rbx_g2 = [sbg_g1, par_th2, par_gsw, sbg_g2]
        set_rr(self, rr=fra_fr5_sbb1, peers=peers_fra_fr5_sbb1)
        set_rr(self, rr=fra_5, peers=peers_fra_5)
        set_rr(self, rr=rbx_g1, peers=peers_rbx_g1)
        set_rr(self, rr=rbx_g2, peers=peers_rbx_g2)
        self.addiBGPFUllMesh(16276, routers=[fra_fr5_sbb1, fra_5, rbx_g1, rbx_g2])  # 4*3/2 iBGP sessions

        # Adding eBGP sessions
        ebgp_session(self, fra_1, telia)
        ebgp_session(self, fra_5, telia)
        ebgp_session(self, fra_5, level3)
        ebgp_session(self, par_gsw, google)
        ebgp_session(self, par_gsw, cogent)
        ebgp_session(self, par_gsw, level3)
        ebgp_session(self, par_th2, cogent)
        ebgp_session(self, par_th2, google)

        # DNS anycast
        fra_dns_resolver.addDaemon(Named)
        rbx_dns_resolver.addDaemon(Named)
        self.addDNSZone(name=DOMAIN, dns_master=fra_dns_resolver, dns_slaves=[rbx_dns_resolver],
                        nodes=[sbg_webserver])
        reverse_domain_name_ipv6 = ip_address("2023::").reverse_pointer[-10:]  # adding a missing PTR record
        ptr_record_ipv6 = PTRRecord(
            IPv6Address("2023", "b", "0", "0", "0", "0", "0", "38", IPV6_LINK_PREFIX).__str__()[:-4],
            sbg_webserver + f".{DOMAIN}")
        self.addDNSZone(name=reverse_domain_name_ipv6, dns_master=fra_dns_resolver, dns_slaves=[rbx_dns_resolver],
                        ns_domain_name=DOMAIN, records=[ptr_record_ipv6])
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
            router.addDaemon(BGP)
        for router in cogent_routers:
            router.addDaemon(BGP)
        for router in level3_routers:
            router.addDaemon(BGP)


if __name__ == '__main__':
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    net = IPNet(topo=OVHTopology(), use_v4=True, use_v6=True, allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
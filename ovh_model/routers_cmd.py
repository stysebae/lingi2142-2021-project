#!/usr/bin/env python3

"""
LINGI2142: Computer Networks: Configuration and Management
File: routers_cmd.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file executes automatically FRRouting commands in order to configure routers.
"""

import pexpect
from os import sys
from main import GOOGLE_AS, TELIA_AS, LEVEL3_AS, COGENT_AS, OVH_AS

child = None
OSPF_PASSWORD = "OVH"

def send_command(command):
    child.sendline(command)
    child.sendline("")

def deny_reserved_addresses(local_router, peer_router, as_nbr):
    child.sendline("{} telnet localhost 2605".format(local_router))
    send_command("zebra")
    child.expect("{}>".format(local_router))
    send_command("enable")
    child.expect("{}#".format(local_router))
    send_command("configure terminal")

    send_command("ip prefix-list too-specific seq 5 permit 0.0.0.0/0 le 24")
    send_command("ip prefix-list ipv4-martians seq 5 deny 0.0.0.0/8 le 32")
    send_command("ip prefix-list ipv4-martians seq 10 deny 127.0.0.0/8 le 32")
    send_command("ip prefix-list ipv4-martians seq 15 deny 169.254.0.0/16 le 32")
    send_command("ip prefix-list ipv4-martians seq 20 deny 198.18.0.0/15 le 32")
    send_command("ip prefix-list ipv4-martians seq 25 deny 192.0.0.0/24 le 32")
    send_command("ip prefix-list ipv4-martians seq 30 deny 10.0.0.0/8 le 32")
    send_command("ip prefix-list ipv4-martians seq 35 deny 172.16.0.0/12 le 32")
    send_command("ip prefix-list ipv4-martians seq 40 deny 192.168.0.0/16 le 32")
    send_command("ip prefix-list ipv4-martians seq 45 deny 255.255.255.255/32")

    send_command("router bgp {}".format(as_nbr))
    send_command("bgp log-neighbor-changes")
    send_command("address-family ipv4 unicast")

    send_command("neighbor {} prefix-list ipv4-martians in".format(peer_router))
    send_command("neighbor {} prefix-list ipv4-martians out".format(peer_router))
    send_command("neighbor {} prefix-list too-specific in".format(peer_router))
    send_command("neighbor {} maximum-prefix 200".format(peer_router))
    send_command("neighbor {} ttl-security hops 2".format(peer_router)) # We have access to all routers maximum 2 hops away
    send_command("neighbor {} remove-private-as replace-as".format(peer_router))

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def activate_ospf_password(local_router, nbr_interfaces, password):
    child.sendline("{} telnet localhost ospfd".format(local_router))
    send_command("zebra")
    child.expect("{}>".format(local_router))
    send_command("enable")
    child.expect("{}#".format(local_router))

    for i in range(nbr_interfaces):
        send_command("configure terminal")
        send_command("router ospf")
        send_command("interface {}-eth{}".format(local_router, i))
        send_command("ip ospf message-digest-key 1 md5 {}".format(password))
        send_command("ip ospf authentication message-digest")
        send_command("end")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def set_password(local_router, peer_router, as_nbr, password):
    child.sendline("{} telnet localhost 2605".format(local_router))
    send_command("zebra")
    child.expect("{}>".format(local_router))
    send_command("enable")
    child.expect("{}#".format(local_router))
    send_command("configure terminal")
    send_command("router bgp {}".format(as_nbr))

    send_command("neighbor {} password {}".format(peer_router, password))

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def set_password_routers(routers, ip, as_nbr, password):
    set_password(routers[0], ip[0], as_nbr[0], password)
    set_password(routers[1], ip[1], as_nbr[1], password)

def advertise_google():
    child.sendline("google telnet localhost 2605")
    send_command("zebra")
    child.expect("google>")
    send_command("enable")
    child.expect("google#")
    send_command("configure terminal")

    send_command("router bgp {}".format(GOOGLE_AS))
    send_command("address-family ipv6")
    send_command("network 2001:4860::/32")
    send_command("network 2404:6800::/32")
    send_command("network 2404:f340::/32")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def advertise_cogent():
    child.sendline("cogent telnet localhost 2605")
    send_command("zebra")
    child.expect("cogent>")
    send_command("enable")
    child.expect("cogent#")
    send_command("configure terminal")

    send_command("router bgp {}".format(COGENT_AS))
    send_command("address-family ipv6")
    send_command("network 2001:550:1:100::/56")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def advertise_level3():
    child.sendline("level3 telnet localhost 2605")
    send_command("zebra")
    child.expect("level3>")
    send_command("enable")
    child.expect("level3#")
    send_command("configure terminal")

    send_command("router bgp {}".format(LEVEL3_AS))
    send_command("address-family ipv6")
    send_command("network 2620:123:d001::/48")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

def advertise_telia():
    child.sendline("telia telnet localhost 2605")
    send_command("zebra")
    child.expect("telia>")
    send_command("enable")
    child.expect("telia#")
    send_command("configure terminal")

    send_command("router bgp {}".format(TELIA_AS))
    send_command("address-family ipv6")
    send_command("network 2a0e:1c80:a::/48")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")

if __name__ == "__main__":
    child = pexpect.spawn('./main.py', encoding='utf-8')
    child.logfile_read = sys.stdout
    child.expect("mininet>")
    print("Please wait for a second 'mininet>' to appears")
    child.logfile_read = None
    deny_reserved_addresses("par_gsw", "12.16.217.53", OVH_AS) # google
    deny_reserved_addresses("par_gsw", "12.16.217.49", OVH_AS) # level3
    deny_reserved_addresses("par_gsw", "12.16.217.51", OVH_AS) # cogent
    deny_reserved_addresses("fra_1", "12.16.217.25", OVH_AS) # telia
    deny_reserved_addresses("fra_5", "12.16.217.27", OVH_AS) # telia
    deny_reserved_addresses("fra_5", "12.16.217.29", OVH_AS) # level3

    set_password_routers(["par_gsw", "google"], ["12.16.217.53", "12.16.217.52"], [OVH_AS, GOOGLE_AS], "aaa") # par_gsw <-> google
    set_password_routers(["par_gsw", "level3"], ["12.16.217.49", "12.16.217.48"], [OVH_AS, LEVEL3_AS], "bbb") # par_gsw <-> level3
    set_password_routers(["par_gsw", "cogent"], ["12.16.217.51", "12.16.217.50"], [OVH_AS, COGENT_AS], "ccc") # par_gsw <-> cogent
    set_password_routers(["fra_1", "telia"], ["12.16.217.25", "12.16.217.24"], [OVH_AS, TELIA_AS], "ddd") # fra_1 <-> telia
    set_password_routers(["fra_5", "telia"], ["12.16.217.27", "12.16.217.26"], [OVH_AS, TELIA_AS], "eee") # fra_5 <-> telia
    set_password_routers(["fra_5", "level3"], ["12.16.217.29", "12.16.217.28"], [OVH_AS, LEVEL3_AS], "fff") # fra_5 <-> level3

    activate_ospf_password("fra1_g1", 3, OSPF_PASSWORD)
    activate_ospf_password("fra1_g2", 3, OSPF_PASSWORD)
    activate_ospf_password("fra_sbb1", 7, OSPF_PASSWORD)
    activate_ospf_password("fra_sbb2", 9, OSPF_PASSWORD)
    activate_ospf_password("fra_1", 4, OSPF_PASSWORD)
    activate_ospf_password("fra_5", 5, OSPF_PASSWORD)
    activate_ospf_password("rbx_g1", 6, OSPF_PASSWORD)
    activate_ospf_password("rbx_g2", 4, OSPF_PASSWORD)
    activate_ospf_password("sbg_g1", 4, OSPF_PASSWORD)
    activate_ospf_password("sbg_g2", 6, OSPF_PASSWORD)
    activate_ospf_password("par_th2", 6, OSPF_PASSWORD)
    activate_ospf_password("par_gsw", 7, OSPF_PASSWORD)

    advertise_google()
    advertise_cogent()
    advertise_level3()
    advertise_telia()

    child.interact()


#!/usr/bin/env python3

import pexpect
from os import sys

child = None

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
    send_command("neighbor {} remove-private-as".format(peer_router))

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
    child.sendline("google_r1 telnet localhost 2605")
    send_command("zebra")
    child.expect("google_r1>")
    send_command("enable")
    child.expect("google_r1#")
    send_command("configure terminal")

    """send_command("interface lo")
    send_command("ip address 8.8.8.8/24")"""

    send_command("router bgp 5")
    send_command("network 8.8.8.0 mask 255.255.255.0")

    send_command("end")
    send_command("exit")
    child.expect("mininet>")


if __name__ == "__main__":
    child = pexpect.spawn('./main.py', encoding='utf-8')
    child.logfile_read = sys.stdout
    child.expect("mininet>")
    print("Please wait for a second 'mininet>' to appears")
    child.logfile_read = None
    deny_reserved_addresses("ovh_r11", "12.11.0.53", 1) # google
    deny_reserved_addresses("ovh_r11", "12.11.0.49", 1) # level3
    deny_reserved_addresses("ovh_r11", "12.11.0.51", 1) # cogent
    deny_reserved_addresses("ovh_r5", "12.11.0.25", 1) # telia
    deny_reserved_addresses("ovh_r6", "12.11.0.27", 1) # telia
    deny_reserved_addresses("ovh_r6", "12.11.0.29", 1) # level3

    set_password_routers(["ovh_r11", "google_r1"], ["12.11.0.53", "12.11.0.52"], [1, 5], "aaa") # ovh_r11 <-> google_r1
    set_password_routers(["ovh_r11", "level3_r1"], ["12.11.0.49", "12.11.0.48"], [1, 4], "bbb") # ovh_r11 <-> level3_r1
    set_password_routers(["ovh_r11", "cogent_r1"], ["12.11.0.51", "12.11.0.50"], [1, 3], "ccc") # ovh_r11 <-> cogent_r1
    set_password_routers(["ovh_r5", "telia_r1"], ["12.11.0.25", "12.11.0.24"], [1, 2], "ddd") # ovh_r5 <-> telia_r1
    set_password_routers(["ovh_r6", "telia_r1"], ["12.11.0.27", "12.11.0.26"], [1, 2], "eee") # ovh_r6 <-> telia_r1
    set_password_routers(["ovh_r6", "level3_r1"], ["12.11.0.29", "12.11.0.28"], [1, 4], "fff") # ovh_r6 <-> level3_r1

    advertise_google()

    child.interact()


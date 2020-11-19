"""
LINGI2142: Computer Networks: Configuration and Management
File: announced_prefixes.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file displays IP addresses which are advertised by peers (Google, Cogent, Telia and Level3).
"""

from ipmininet.router.config import AF_INET6, AF_INET

GOOGLE_IPV4_ANNOUNCED_PREFIXES = AF_INET(networks=("8.8.8.0/24",), )
COGENT_IPV4_ANNOUNCED_PREFIXES = AF_INET(networks=("98.159.96.0/22",), )
LEVEL3_IPV4_ANNOUNCED_PREFIXES = AF_INET(networks=("98.159.96.0/22",), )
ROOT_SERVERS = AF_INET(networks=("192.33.4.0/24", "192.112.36.0/24",), )

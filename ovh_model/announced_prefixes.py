"""
LINGI2142: Computer Networks: Configuration and Management
File: announced_prefixes.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file displays IP addresses which are advertised by peers (Google, Cogent, Telia and Level3).
"""

from ipmininet.router.config import AF_INET6, AF_INET

#TODO: to continue
GOOGLE_IPV4_ANNOUNCED_PREFIXES = AF_INET(networks=(
"8.8.8.0/24", "8.8.4.0/24", "8.35.200.0/21", "8.35.192.0/21", "8.34.216.0/21", "8.34.208.0/21", "74.125.72.0/22",
"74.125.71.0/24", "74.125.70.0/24", "74.125.69.0/24", "74.125.68.0/24", "74.125.6.0/24", "74.125.44.0/22",
"74.125.39.0/24", "74.125.38.0/24", "74.125.31.0/24", "74.125.30.0/24", "74.125.29.0/24", "74.125.28.0/24",
"74.125.26.0/24", "74.125.250.0/24", "74.125.25.0/24", "74.125.24.0/24", "74.125.238.0/24", "74.125.236.0/24",),)

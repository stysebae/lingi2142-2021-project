# Addressing Plan

## IPv4

- Each city has its own subnet.
- We use the public IP addresses range 12.0.0.0, as following:

  | Location           | IP Addresses range | Loopback Addresses |
  |--------------------|--------------------|--------------------|
  | *Loopback Addresses* | 12.10.c.x/32       |                    |
  | Frankfurt          | 12.11.0.0/29       | 12.10.1.x/32       |
  | Roubaix            | 12.12.0.0/31       | 12.10.2.x/32       |
  | Strasbourg         | 12.13.0.0/31       | 12.10.3.x/32       |
  | Paris              | 12.14.0.0/31       | 12.10.4.x/32       |

  A few comments about this choice:
  - the format of the loopback addresses is 12.10.c.x/32 where *c* indicates the city ID and *x* the interface ID. Because we do not need more than one loopback address, its mask is /32.
  - We use /29 mask for Frankfurt because this subnet contains more routers than the others cities (6 vs. 2).

## IPv6

- Same spirit as for IPv4: each city has its own subnet composed of public addresses, but with IPv6 we may have 3 differents types of addresses (unicast, anycast and multicast) and we are not constrained with the number of available IP addresses like in IPv4: an IPv6 address consists of 64 bits of "network number" and 64 bits of "host number" (it is able to address 2^40 networks and 2^50 hosts).
- We use **IPv6 global unicast addresses**. According to [RFC3587](https://www.ietf.org/rfc/rfc3587.txt?number=3587) and [RFC4291](https://www.ietf.org/rfc/rfc4291.txt?number=4291), such addresses have the following format:

  | n bits            | m bits    | 128-n-m bits |
  |-------------------|-----------|--------------|
  | global routing ID | subnet ID | interface ID |

  where the global routing prefix is a value assigned to a site (i.e. a cluster of subnets/links), the subnet ID is an identifier of a subnet within the site and interface ID is used to identify interfaces on a link (and required to be unique within a subnet prefix).

  In practice, we use IP addresses in the range of the 2000::/3 prefix delegated by the IANA:

  | 3 bits | 45 bits           | 16 bits   | 64 bits      |
  |--------|-------------------|-----------|--------------|
  | 001    | global routing ID | subnet ID | interface ID |

  [RFC3177](https://tools.ietf.org/html/rfc3177) recommends to use /64 when it is known that one and only one subnet is needed, which is the case here. We have then:

  | Location           | IP Addresses range    | Loopback Addresses      |
  |--------------------|-----------------------|-------------------------|
  | *Loopback Addresses* | 2023:​​a:C::x/128 |                         |
  | Frankfurt          | 2023:​b::/64 | 2023:​a:​b::x/128 |
  | Roubaix            | 2023:​c::/64 | 2023:​a:​c::x/128 |
  | Strasbourg         | 2023:​d::/64 | 2023:​a:​d::x/128 |
  | Paris              | 2023:​e::/64 | 2023:​a:​e::x/128 |

  where *C* indicates the city (and not the 12 hexadecimal value!) and *x* designates the interface ID.

## References

- [Cisco's IPv4 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-smart-business-architecture/sba_ipAddr_dg.pdf)
- [Cisco's IPv6 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-government/sbaBN_IPv6addrG.pdf)
- [Designing an IPv4 Addressing Scheme](https://docs.oracle.com/cd/E23823_01/html/816-4554/ipplan-5.html)
- [RIPE's IPv6 Address Types](https://www.ripe.net/manage-ips-and-asns/ipv6/ipv6-address-types)
- [RFC3177: IAB/IESG Recommendations on IPv6 Address Allocations to Sites](https://tools.ietf.org/html/rfc3177)
- [RFC3587: IPv6 Global Unicast Address Format](https://tools.ietf.org/html/rfc3587)
- [RFC4291: IP Version 6 Addressing Architecture](https://tools.ietf.org/html/rfc4291)
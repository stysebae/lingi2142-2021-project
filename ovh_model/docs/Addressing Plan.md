# Addressing Plan

## IPv4

- Each city has its own subnet.
- 10.0.0.0 range for the most flexibility (instead of 192.168.0.0 range), because it allows a lot of hosts in the same range and it is also a private IPv4 range (see [RFC1918](https://www.ietf.org/rfc/rfc1918.txt?number=1918)). A Network Address Translation (NAT) is then required before the users can connect to the Internet.
- 256 IPv4 addresses (the first byte is set, we cannot change it) with a /16 mask and 65534 (i.e. 2^16-2) host addresses
- We reserve a dedicated subnet for the loopback addresses (10.10.0.0/16). Each other subnet can contain up to 256 loopback addresses (10.10.x.0/24, where *x* indicates the city):

| Location           | IP Addresses range | Loopback Addresses |
|--------------------|--------------------|--------------------|
| *Loopback Addresses* | 10.10.0.0/16       |                    |
| Frankfurt          | 10.11.0.0/16       | 10.10.1.0/24       |
| Roubaix            | 10.12.0.0/16       | 10.10.2.0/24       |
| Strasbourg         | 10.13.0.0/16       | 10.10.3.0/24       |
| Paris              | 10.14.0.0/16       | 10.10.4.0/24       |

## IPv6

- Same spirit as for IPv4: each city has its own subnet composed of private addresses and a bigger part of them is dedicated to host addresses.
- According to [RFC4193](https://www.ietf.org/rfc/rfc4193.txt?number=4193), the address block fc00::/7 is equivalent to the IPv4 10.0.0.0/8 private space and has the following format:

  | 7 bits | 1 | 40 bits   | 16 bits   | 64 bits      |
  |--------|---|-----------|-----------|--------------|
  | Prefix | L | Global ID | Subnet ID | Interface ID |

  In practice the block fd00::/8 is used for /48 prefixes and the global ID is formed thanks to a pseudo-random bit string generator algorithm, whose code is described in RFC4193. Here, we use fd59:f581:6faf::/48 (the global ID was generated via [this tool](https://www.ultratools.com/tools/rangeGenerator)).
- /64 prefix is a common choice for the traditional LAN/WAN interfaces of network devices. With the prefix fd59:f581:6faf::/48, we have thus a range from fd59:f581:6faf::/64 to fd59:f581:6faf:ffff::/64.
- We follow the same idea as IPv4 addressing plan for the subnets and loopbacks addresses:

| Location           | IP Addresses range    | Loopback Addresses      |
|--------------------|-----------------------|-------------------------|
| *Loopback Addresses* | fd59:f581:6faf:a::/64 |                         |
| Frankfurt          | fd59:f581:6faf:b::/64 | fd59:f581:6faf:a:1::/64 |
| Roubaix            | fd59:f581:6faf:c::/64 | fd59:f581:6faf:a:2::/64 |
| Strasbourg         | fd59:f581:6faf:d::/64 | fd59:f581:6faf:a:3::/64 |
| Paris              | fd59:f581:6faf:e::/64 | fd59:f581:6faf:a:4::/64 |


## References

- [Cisco's IPv4 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-smart-business-architecture/sba_ipAddr_dg.pdf)
- [Cisco's IPv6 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-government/sbaBN_IPv6addrG.pdf)
- [Designing an IPv4 Addressing Scheme](https://docs.oracle.com/cd/E23823_01/html/816-4554/ipplan-5.html)
- [UltraTools's IPv6 Address Range Generator](https://www.ultratools.com/tools/rangeGenerator)
- [RIPE's IPv6 Address Types](https://www.ripe.net/manage-ips-and-asns/ipv6/ipv6-address-types)
- [Wikipedia "Unique local address" article](https://en.wikipedia.org/wiki/Unique_local_address)
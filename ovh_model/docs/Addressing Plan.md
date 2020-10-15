# Addressing Plan

## IPv4

**TODO: adresses 10.0.0... sont des adresses privées (IANA, cf. RFC1918)**

- Each city has its own subnet
- 10.0.0.0 range for the most flexibility (instead of 192.168.0.0 range), because it allows a lot of hosts in the same range
- 256 IPv4 addresses (the first byte is set, we cannot change it) with a /16 mask and 65534 (i.e. 2^16-2) host addresses
- The first 2540 IPv4 addresses of each subnet are reserved for the loopback addresses of the routers (from 10.xxx.0.1 to 10.xxx.9.254, up to 10.xxx.10.0)

| Location   	| IP Addresses range 	| Loopbacks Addresses 	|
|------------	|--------------------	|---------------------	|
| Frankfurt  	| 10.10.0.0/16       	| Up to 10.10.9.254   	|
| Roubaix    	| 10.11.0.0/16      	| Up to 10.11.9.254   	|
| Strasbourg 	| 10.12.0.0/16      	| Up to 10.12.9.254   	|
| Paris      	| 10.13.0.0/16      	| Up to 10.13.9.254   	|

## IPv6

**TODO: 2001:0db8::::: est l'équivalent IPv6 de 192.168.0.0!**

- Same spirit as for IPv4: each cityhas its own subnet and a bigger part of addresses is dedicated to host addresses
- the IPv6 prefix acts as the network identifier and is represented using the prefix-length format like an IPv4 address under CIDR notation. The major difference is that an IPv4 host uses generally one IP address, but an IPv6 host can have more than one IP address:
  - unicast: 1 address <-> 1 interface;
  - anycast: 1 address <-> 2, ..., *n* interfaces;
  - multicast: 1 address <-> 2, ..., *n* (closest) interfaces;
- /64 prefix is a common choice for the traditional LAN/WAN interfaces of network devices


| Location   	| IP Addresses range 	        | Loopbacks Addresses 	|
|------------	|--------------------	       |---------------------	|
| Frankfurt  	| 2001:0db8:::::/64       	    | Up to 10.10.9.254   	|
| Roubaix    	| 2001:0db8:::::/64       	     | Up to 10.11.9.254   	|
| Strasbourg 	| 2001:0db8:::::/64      	    | Up to 10.12.9.254   	|
| Paris      	| 2001:0db8:::::/64      	    | Up to 10.13.9.254   	|

## References

- [Cisco's IPv4 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-smart-business-architecture/sba_ipAddr_dg.pdf)
- [Cisco's IPv6 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-government/sbaBN_IPv6addrG.pdf)
- [Designing an IPv4 Addressing Scheme](https://docs.oracle.com/cd/E23823_01/html/816-4554/ipplan-5.html)
- [RIPE's IPv6 Address Types](https://www.ripe.net/manage-ips-and-asns/ipv6/ipv6-address-types)
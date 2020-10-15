# Addressing Plan

(based on [Cisco's IPv4 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-smart-business-architecture/sba_ipAddr_dg.pdf))
(based on [Cisco's IPv6 Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-government/sbaBN_IPv6addrG.pdf))

## IPv4

- Each city has its own subnet
- 10.0.0.0 range for the most flexibility (instead of 192.168.0.0 range), because it allows a lot of hosts in the same range
- 256 IPv4 addresses with a /16 mask (the firt byte is set, we can't change it) and 65024 (254 x 256) host addresses
- The first 2540 IPv4 addresses of each subnet are reserved for the loopback addresses of the routers (from 10.xxx.0.1 to 10.xxx.9.254, up to 10.xxx.10.0)

| Location   	| IP Addresses range 	| Loopbacks Addresses 	|
|------------	|--------------------	|---------------------	|
| Frankfurt  	| 10.10.0.0/16       	| Up to 10.10.9.254   	|
| Roubaix    	| 10.11.0.0/16      	| Up to 10.11.9.254   	|
| Strasbourg 	| 10.12.0.0/16      	| Up to 10.12.9.254   	|
| Paris      	| 10.13.0.0/16      	| Up to 10.13.9.254   	|

## IPv6

- Same spirit as for IPv4

| Location   	| IP Addresses range 	|
|------------	|--------------------	|
| Frankfurt  	| 2001:a::/64       	|
| Roubaix    	| 2001:b::/64       	|
| Strasbourg 	| 2001:c::/64       	|
| Paris      	| 2001:d::/64       	|

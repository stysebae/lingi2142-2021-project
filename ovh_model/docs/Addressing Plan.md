# Addressing Plan

(based on [Cisco's IP Addressing Guide](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise/design-zone-smart-business-architecture/sba_ipAddr_dg.pdf))

## IPv4

- Each city has its own subnet
- 10.0.0.0 range for the most flexibility (instead of 192.168.0.0 range), because it allows a lot of hosts in the same range
- 2097150 (2^21-2) IPv4 addresses with a /11 mask and 1048574 (2^20-2) loopback addresses: 1048574 IPv4 addresses left for routers and hosts and 2046 subnets

| Location   	| IP Addresses range 	| Loopbacks Addresses 	|
|------------	|--------------------	|---------------------	|
| Frankfurt  	| 10.0.0.0/11       	| 10.0.0.0/12        	|
| Roubaix    	| 10.32.0.0/11      	| 10.32.0.0/12       	|
| Strasbourg 	| 10.64.0.0/11      	| 10.64.0.0/12       	|
| Paris      	| 10.96.0.0/11      	| 10.96.0.0/12       	|

## IPv6
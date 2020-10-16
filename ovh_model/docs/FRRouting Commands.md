# FRRouting Commands

## Reminder: some IPMininet useful commands

- `nodes`: displays nodes
- `links` or `net`: displays links
- `<node|switch|controller> cmd`: executes `cmd` on the specified node (e.g.: `ovh_r1 ifconfig -a`)
- `<node1> ping -c <node2>`: tests connectivity between `node1` and `node2`
- `dump`: displays all information about the nodes

## Connection to FRRouting daemons

To access to the configuration of FRRouting (within the IPMininet CLI), you have to use `telnet` to connect to FRRouting daemons.

A different port is used to access to every routing daemon. This small table shows the port associated to its default daemon:

| Port     | State | Service | Comments                                             |
|----------|-------|---------|------------------------------------------------------|
| 2601/tcp | open  | zebra   | controls the Routing Information Base (RIB) of each daemon                      |
| 2605/tcp | open  | bgpd    | show information related to the configuration of BGP |
| 2606/tcp | open  | ospf6d  | same but for OSPFv3 (OSPF for IPv6)                  |

To use it, type the following command: `[noecho] <node> telnet localhost XXXX` where XXXX is either 2601, 2605 or 2606 (for example: `noecho ovh_r1 telnet localhost 2606`). A new CLI interface will be shown. Type `zebra` as password in order to have the FRRouting CLI.

The commands listed below assume that you are using FRRouting CLI.

## RIB

- `show ip route`: shows all the routes contained in the RIB

## BGP

- `show bgp summary`: outputs a summary of the status of the BGP sessions on the local router.

## OSPF

(Commands known via `<node> telnet localhost 2606`)

- `show ip ospf`: general information about OSPF on the router
- `show ip ospf database`: information about the link state database
- `show ip ospf route`: shows the OSPF topology table
- `show ip ospf route summary`: gives a summary of the OSPF routes
- `show ip ospf neighbor`: displays OSPF-neighbor information on a per-interface basis
- `show ip ospf interface`: provides information about each of the router’s interfaces.
- `show ip ospf spf tree`: ASCII representation of the shortest path tree

## References

- [Cisco's IP Routing: OSPF Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-cfg.html)
- [FRRouting User Guide](http://docs.frrouting.org/en/stable-7.1/)
- [Exploring OSPFv3 routing with IPMininet](http://blog.computer-networking.info/ipmininet-ospfv3/)
- [Exploring BGP with IPMininet](http://blog.computer-networking.info/bgp-mininet/)
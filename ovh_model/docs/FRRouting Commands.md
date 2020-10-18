# FRRouting Commands

## Reminder: some IPMininet useful commands

- `nodes`: displays nodes
- `links` or `net`: displays links
- `<NODE|SWITCH|CONTROLLER> cmd`: executes `cmd` on the specified node (e.g.: `ovh_r1 ifconfig -a`)
- `<NODE1> ping -c X <NODE2>`: tests connectivity between `NODE1` and `NODE2` (where `X` is an integer)
- `dump`: displays all information about the nodes

## Connection to FRRouting daemons

To access to the configuration of FRRouting (within the IPMininet CLI), you have to use `telnet` to connect to FRRouting daemons.

A different port is used to access to every routing daemon. This small table shows the port associated to its default daemon:

| Port     | State | Service | Comments                                             |
|----------|-------|---------|------------------------------------------------------|
| 2601/tcp | open  | zebra   | controls the Routing Information Base (RIB) of each daemon                      |
| 2605/tcp | open  | bgpd    | show information related to the configuration of BGP |
| 2606/tcp | open  | ospf6d  | same but for OSPFv3 (OSPF for IPv6)                  |

To use it, type the following command: `[noecho] <NODE> telnet localhost XXXX` where XXXX is either 2601, 2605 or 2606 (for example: `noecho ovh_r1 telnet localhost 2606`). A new CLI interface will be shown. Type `zebra` as password in order to have the FRRouting CLI.

The commands listed below assume that you are using FRRouting CLI.

## RIB

(Commands known via `<node> telnet localhost 2601`)

- `show ip route`: shows all the routes contained in the RIB

## BGP

(Commands known via `<node> telnet localhost 2605`)

TODO

- `router bgp <AS_NBR>`: activates BGP on the router an set his AS number
- `network <SUBNET_IP/MASK>`: chooses the network on which advertise BGP
- `neighbor <NEIGHBOR_IP> remote-as <REMOTE_AS_NBR>`: defines the neighbor as a member of remote AS
- `neighbor <NEIGHBOR_IP> prefix-list <PREFIX_NAME> in`: sets the ingoing filter for the interface
- `neighbor <NEIGHBOR_IP> prefix-list <PREFIX_NAME> out`: sets the outgoing filter for the interface
- `neighbor <NEIGHBOR_IP> update-source <INTERFACE_NAME>`: sets the loopback addresss of the neighbor (the interface as to be set previously by : "interface loopback 0 \n ip adress LOOPBACK_IP 255.255.255.255")
- `set community <COMMUNITY>`: sets the BGP community value
- `set local-preference <X>`: sets the local-pref on the link
- `show bgp summary`: outputs a summary of the status of the BGP sessions on the local router.

## OSPF

(Commands known via `<node> telnet localhost 2606`)

### Enabling

We can enable OSPF on each router by the following steps:

- `enable`: enters in EXEC mode (e.g.: `ovh_r1#`)
- `configure terminal`: enters in global configuration mode
- `router ospf <PID>`: enables OSPF on the router
- `network <IP_ADDRESS WILDCARD_MASK> area <AREA_NBR>`: sets the interface (`IP_ADDRESS WILDCARD_MASK`) on which OSPF will run and his area number (`AREA_NBR`)
- `end`: exits router configuration mode

### Configuring OSPF Interface Parameters

After `enable` and `configure terminal`, **we have to specify the interface number (that we would like to configure) via `interface`**. Then, we can configure these differents parameters (once finished, type `end`):

- `ip address <IP_ADDRESS SUBNET_MASK>`: changes the IP address to `IP_ADDRESS SUBNET_MASK` on the selected interface
- `ip ospf cost <X>`: defines the cost `X` of the link connected at the selected interface
- `neighbor <NEIGHBOR_IP COST>`: defines a specific cost (`NEIGHBOR_IP COST`) to reach a given neighbor (otherwise, neighbors will assume the cost of the interface based on the `ip ospf cost` command)
- `ip ospf priority <X>`: changes the chances/priority (to `X`) of the router to be the OSPF designated router (who act as the main point of contact for the network segment)

#### "Hello" and "Dead" Intervals

OSPF uses hello packets and two timers to check if a neighbor is still alive or not. One timer is the "hello timer" which defines the frequency at which we have to send the hello packet and the second is the "dead interval" wich defines how long we should wait for hello packets before we declare the neighbor dead. A router send hello packet to his neighbors to tell them he is still alive.

We can change the value of the two timers with the commands (after `enable`, `configure terminal` and `interface` commands!):

- `ip ospf hello-interval <X>` (where `X` is the interval in seconds)
- `ip ospf dead-interval <X>` (where `X` is the interval in seconds)

### Debugging Commands:

- `show ip ospf`: general information about OSPF on the router
- `show ip ospf database`: information about the link state database
- `show ip ospf route`: show the OSPF topology table
- `show ip ospf route summary`: give a summary of the OSPF routes
- `show ip ospf neighbor`: display OSPF-neighbor information on a per-interface basis
- `show ip ospf interface`: provide information about each of the router’s interfaces.
- `show ip ospf spf tree`: ASCII representation of the shortest path tree

## References

- [Cisco's IP Routing: BGP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16/irg-xe-16-book.html)
- [Cisco's IP Routing: OSPF Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-cfg.html)
- [FRRouting User Guide](http://docs.frrouting.org/en/stable-7.1/)
- [Exploring OSPFv3 routing with IPMininet](http://blog.computer-networking.info/ipmininet-ospfv3/)
- [Exploring BGP with IPMininet](http://blog.computer-networking.info/bgp-mininet/)

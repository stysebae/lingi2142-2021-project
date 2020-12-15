# Anycast DNS

In our network, we have:
- one web server attached to `sbg_g2`
- one DNS resolver attached to `fra_sbb2` (`fra_server`)
- another DNS resolver attached to `rbx_g1` (`rbx_server`)

`rbx_server` and `fra_server` shares the same IPv4 and IPv6 addresses:
```
mininet> rbx_server ifconfig
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 2023:a:c::7  prefixlen 128  scopeid 0x0<global>
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 82  bytes 5758 (5.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 82  bytes 5758 (5.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
rbx_server-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.16.217.55  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 fe80::4461:6fff:fe57:a6c7  prefixlen 64  scopeid 0x20<link>
        inet6 2023:b::37  prefixlen 127  scopeid 0x0<global>
        ether 46:61:6f:57:a6:c7  txqueuelen 1000  (Ethernet)
        RX packets 365  bytes 44246 (44.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 332  bytes 26436 (26.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

mininet> fra_server ifconfig
fra_server-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.16.217.55  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 2023:b::37  prefixlen 127  scopeid 0x0<global>
        inet6 fe80::7492:53ff:fe0a:877e  prefixlen 64  scopeid 0x20<link>
        ether 76:92:53:0a:87:7e  txqueuelen 1000  (Ethernet)
        RX packets 348  bytes 40257 (40.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 313  bytes 24972 (24.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        inet6 2023:a:c::7  prefixlen 128  scopeid 0x0<global>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 2  bytes 78 (78.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 78 (78.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Their respective resolvers, `rbx_g1` and `fra_sbb2` also share the same IPv4 and IPv6 addresses:

```
rbx_g1-eth4: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.16.217.54  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 fe80::e8e0:1eff:fe56:1d29  prefixlen 64  scopeid 0x20<link>
        inet6 2023:b::36  prefixlen 127  scopeid 0x0<global>
        ether ea:e0:1e:56:1d:29  txqueuelen 1000  (Ethernet)
        RX packets 350  bytes 27830 (27.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 389  bytes 46096 (46.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

fra_sbb2-eth7: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.16.217.54  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 fe80::303d:24ff:fee5:63f  prefixlen 64  scopeid 0x20<link>
        inet6 2023:b::36  prefixlen 127  scopeid 0x0<global>
        ether 32:3d:24:e5:06:3f  txqueuelen 1000  (Ethernet)
        RX packets 329  bytes 26176 (26.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 368  bytes 41765 (41.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

The DNS zone (`/tmp/named_fra_server.ovh.com.zone.cfg`) is configured as follows:

```
$TTL 172800
@       IN      SOA     ovh.com. sysadmin.ovh.com. (
1 ; serial
86400 ; refresh timer
7200 ; retry timer
3600000 ; retry timer
172800 ; minimum ttl
)

ovh.com.   60   IN      NS      fra_server.ovh.com.
ovh.com.   60   IN      NS      rbx_server.ovh.com.
sbg_web   60    IN      A       12.16.218.72
sbg_web   60    IN      AAAA    2023:e:2::4
fra_server   60 IN      A       12.16.217.55
fra_server   60 IN      AAAA    2023:b::37
rbx_server   60 IN      A       12.16.217.55
rbx_server   60 IN      AAAA    2023:b::37
```

## Tests

### IPv4

- `fra_1` tries to reach `fra_server` and `rbx_server`:

```
mininet> fra_1 ping 12.16.217.55
PING 12.16.217.55 (12.16.217.55) 56(84) bytes of data.
^C
--- 12.16.217.55 ping statistics ---
14 packets transmitted, 0 received, 100% packet loss, time 13304ms
```

There are some issue when using IPv4 with the BGP daemon, however it works with IPv6 !
Traceroute doesn't work either.

### IPv6

- `fra_1` tries to reach 2023:b::7 (`fra_server` or `rbx_server`):

```
mininet> fra_1 ping6 -c 3 2023:b::37
PING 2023:b::37(2023:b::37) 56 data bytes
64 bytes from 2023:b::37: icmp_seq=1 ttl=62 time=0.175 ms
64 bytes from 2023:b::37: icmp_seq=2 ttl=62 time=0.147 ms
64 bytes from 2023:b::37: icmp_seq=3 ttl=62 time=0.151 ms

--- 2023:b::37 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2032ms
rtt min/avg/max/mdev = 0.147/0.157/0.175/0.019 ms

```

- Using `traceroute6`, we have the following outputs:

```
mininet> fra_1 traceroute6 2023:b::37
traceroute to 2023:b::37 (2023:b::37) from 2023:b::b, 30 hops max, 24 byte packets
 1  fra_sbb1 (2023:b::a)  0.163 ms  0.134 ms  0.102 ms
 2  fra_sbb2 (2023:b::7)  0.448 ms  9.097 ms  0.361 ms
 3  fra_server (2023:b::37)  0.309 ms  0.208 ms  1.021 ms
```

### UDP

We use the command `dig @server name type_record` to check if our anycast DNS works with UDP.

```
mininet> fra1_g1 dig @12.16.217.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46356
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 51cf6b2b89bd17f7fa21091f5fae8256b4f6043813bbb559 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; ANSWER SECTION:
ovh.com.		172800	IN	SOA	ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.		60	IN	NS	fra_server.ovh.com.
ovh.com.		60	IN	NS	rbx_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 12:55:50 UTC 2020
;; MSG SIZE  rcvd: 245
```
```
mininet> fra1_g1 dig @fra_server ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @fra_server ovh.com ANY
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52727
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 04f127ac592fbb01da028e1b5fae83869dd158e0bea3e035 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; ANSWER SECTION:
ovh.com.		172800	IN	SOA	ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.		60	IN	NS	rbx_server.ovh.com.
ovh.com.		60	IN	NS	fra_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55

;; Query time: 0 msec
;; SERVER: 2023:b::37#53(2023:b::37)
;; WHEN: Fri Nov 13 13:00:54 UTC 2020
;; MSG SIZE  rcvd: 245
```
```
mininet> fra1_g1 dig @12.16.217.55 sbg_web.ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 sbg_web.ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52893
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 297a8881ec913a6ac5a8a3485fae828fc25d47ec9de0bb8c (good)
;; QUESTION SECTION:
;sbg_web.ovh.com.		IN	ANY

;; ANSWER SECTION:
sbg_web.ovh.com.	60	IN	A	12.16.218.72
sbg_web.ovh.com.	60	IN	AAAA	2023:e:2::4

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	rbx_server.ovh.com.
ovh.com.		60	IN	NS	fra_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 12:56:47 UTC 2020
;; MSG SIZE  rcvd: 255
```

```
mininet> sbg_g2 dig @12.16.217.55 sbg_web.ovh.com AAAA

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 sbg_web.ovh.com AAAA
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 26775
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: be278ac172635c7d62ee11b35fae83a6836d54f74bcb4581 (good)
;; QUESTION SECTION:
;sbg_web.ovh.com.		IN	AAAA

;; ANSWER SECTION:
sbg_web.ovh.com.	60	IN	AAAA	2023:e:2::4

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	fra_server.ovh.com.
ovh.com.		60	IN	NS	rbx_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 13:01:26 UTC 2020
;; MSG SIZE  rcvd: 239
```

(Sometimes, no answer is given, with a message of size 64).

With IPv6, however, the configuration file of the in-addr.arpa.zone is not created for some unknown reason. Then the 
`dig` command cannot give an answer, as shown here:

```
mininet> sbg_g2 dig @2023:b::37 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @2023:b::37 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 59260
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 2a005eaa76a809867fe66ce25fae8456ac59f8e2cfd6f362 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; Query time: 0 msec
;; SERVER: 2023:b::37#53(2023:b::37)
;; WHEN: Fri Nov 13 13:04:22 UTC 2020
;; MSG SIZE  rcvd: 64
```

- Sending a UDP packet with `netcat` (and capturing it with `tcpdump`):

```
mininet> xterm fra_server
mininet> xterm rbx_server
mininet> xterm sbg_g2
xterm fra_server> tcpdump -w tcpdump_fra_server_udp.pcap -i any udp port 53 -v
xterm rbx_server> tcpdump -w tcpdump_rbx_server_udp.pcap -i any udp port 53 -v
xterm sbg_g2> nc -u 12.16.217.55 53
Hello DNS server! (UDP, IPv4)
xterm sbg_g2> nc -u 2023:b::37 53
Hello DNS server! (UDP, IPv6)
```

Results: 4 packets received by `fra_server`, nothing for `rbx_server` (see `pcap/tcpdump_fra_server_udp.pcap` and 
`pcap/tcpdump_rbx_server_udp.pcap`).

### TCP

- Querying DNS name servers with additional parameter `+tcp`:

```
mininet> fra_5 dig @12.16.217.55 ovh.com ANY +vc

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 ovh.com ANY +vc
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63788
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 8b5ae7906ef6b345638652425fae9c1d356bbea681341382 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; ANSWER SECTION:
ovh.com.		172800	IN	SOA	ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.		60	IN	NS	fra_server.ovh.com.
ovh.com.		60	IN	NS	rbx_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 14:45:49 UTC 2020
;; MSG SIZE  rcvd: 245
```

```
mininet> fra_5 dig @12.16.217.55 ovh.com ANY +tcp

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 ovh.com ANY +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52415
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 916861948cebd0907f6b2a285fae9c55f931bce1a552f546 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; ANSWER SECTION:
ovh.com.		172800	IN	SOA	ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.		60	IN	NS	fra_server.ovh.com.
ovh.com.		60	IN	NS	rbx_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 14:46:45 UTC 2020
;; MSG SIZE  rcvd: 245
```

```
mininet> fra_5 dig @12.16.217.55 sbg_web.ovh.com AAAA +tcp

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.16.217.55 sbg_web.ovh.com AAAA +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4910
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: aaf521932d5d72ec100cf5a75fae9cfd482bd09fbab2fe1e (good)
;; QUESTION SECTION:
;sbg_web.ovh.com.		IN	AAAA

;; ANSWER SECTION:
sbg_web.ovh.com.	60	IN	AAAA	2023:e:2::4

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	fra_server.ovh.com.
ovh.com.		60	IN	NS	rbx_server.ovh.com.

;; ADDITIONAL SECTION:
fra_server.ovh.com.	60	IN	A	12.16.217.55
rbx_server.ovh.com.	60	IN	A	12.16.217.55
fra_server.ovh.com.	60	IN	AAAA	2023:b::37
rbx_server.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.16.217.55#53(12.16.217.55)
;; WHEN: Fri Nov 13 14:49:33 UTC 2020
;; MSG SIZE  rcvd: 239
```

With IPv6, it does not work for the same reason as for UDP:

```
mininet> fra_5 dig @2023:b::37 ovh.com ANY +tcp

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @2023:b::37 ovh.com ANY +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 13306
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 6eaa284525426807ea87179f5fae9d6b948a5d928ebe2902 (good)
;; QUESTION SECTION:
;ovh.com.			IN	ANY

;; Query time: 0 msec
;; SERVER: 2023:b::37#53(2023:b::37)
;; WHEN: Fri Nov 13 14:51:23 UTC 2020
;; MSG SIZE  rcvd: 64
```

- Sending a TCP packet with `netcat` (and capturing it with `tcpdump`):

```
mininet> xterm fra_server
mininet> xterm rbx_server
mininet> xterm sbg_g2
xterm fra_server> tcpdump -w tcpdump_fra_server_tcp.pcap -i any tcp -v
xterm rbx_server> tcpdump -w tcpdump_rbx_server_tcp.pcap -i any tcp -v
xterm sbg_g2> nc 12.16.217.55 53
Hello DNS server! (TCP, IPv4)
xterm sbg_g2> nc 2023:b::37 53
Hello DNS server! (TCP, IPv6)
```

Results (see `pcap/tcpdump_fra_server_tcp.pcap` and `pcap/tcpdump_rbx_server_tcp.pcap`):
- 259 packets captured and 556 packets received by filter for `fra_server`;
- 203 packets captured and 426 packets received by filter for `rbx_server`

but only TCP establishment connection.
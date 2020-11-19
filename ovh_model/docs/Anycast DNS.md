# Anycast DNS

In our network, we have:
- one web server attached to `ovh_r11`
- one DNS resolver attached to `ovh_r7` (`resolver1`)
- another DNS resolver attached to `ovh_r4` (`resolver2`)

![OVH Initial Model](../img/technical_overview.png)

`resolver1` and `resolver2` shares the same IPv4 and IPv6 addresses:
```
mininet> resolver1 ifconfig
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 2  bytes 78 (78.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 78 (78.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
resolver1-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.11.0.55  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 2023:b::37  prefixlen 127  scopeid 0x0<global>
        inet6 fe80::e870:66ff:fe32:6f48  prefixlen 64  scopeid 0x20<link>
        ether ea:70:66:32:6f:48  txqueuelen 1000  (Ethernet)
        RX packets 91  bytes 7226 (7.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 81  bytes 7988 (7.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

mininet> resolver2 ifconfig
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 82  bytes 5758 (5.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 82  bytes 5758 (5.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
resolver2-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.11.0.55  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 2023:b::37  prefixlen 127  scopeid 0x0<global>
        inet6 fe80::946a:3bff:fe8c:b3e7  prefixlen 64  scopeid 0x20<link>
        ether 96:6a:3b:8c:b3:e7  txqueuelen 1000  (Ethernet)
        RX packets 46  bytes 3800 (3.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 45  bytes 3642 (3.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Their respective resolvers, `ovh_r4` and `ovh_r7` also share the same IPv4 and IPv6 addresses:

```
ovh_r4-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.11.0.54  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 fe80::e86d:bbff:fe3c:1a7a  prefixlen 64  scopeid 0x20<link>
        inet6 2023:b::36  prefixlen 127  scopeid 0x0<global>
        ether ea:6d:bb:3c:1a:7a  txqueuelen 1000  (Ethernet)
        RX packets 8  bytes 752 (752.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 1132 (1.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ovh_r7-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 12.11.0.54  netmask 255.255.255.254  broadcast 0.0.0.0
        inet6 2023:b::36  prefixlen 127  scopeid 0x0<global>
        inet6 fe80::2cc6:f7ff:fe57:8d33  prefixlen 64  scopeid 0x20<link>
        ether 2e:c6:f7:57:8d:33  txqueuelen 1000  (Ethernet)
        RX packets 10  bytes 892 (892.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 1232 (1.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

The DNS zone (`/tmp/named_resolver1.ovh.com.zone.cfg`) is configured as follows:

```
$TTL 172800
@	IN	SOA	ovh.com. sysadmin.ovh.com. (
1 ; serial
86400 ; refresh timer
7200 ; retry timer
3600000 ; retry timer
172800 ; minimum ttl
)

ovh.com.   60	IN	NS	resolver1.ovh.com.
ovh.com.   60	IN	NS	resolver2.ovh.com.
webserver1   60	IN	A	12.11.0.57
webserver1   60	IN	AAAA	2023:b::39
resolver1   60	IN	A	12.11.0.55
resolver1   60	IN	AAAA	2023:b::37
resolver2   60	IN	A	12.11.0.55
resolver2   60	IN	AAAA	2023:b::37
```

## Tests

### IPv4

- `ovh_r12` tries to reach `resolver1` and `resolver2`:

```
mininet> ovh_r12 ping -c 3 12.11.0.55
PING 12.11.0.55 (12.11.0.55) 56(84) bytes of data.
64 bytes from 12.11.0.55: icmp_seq=1 ttl=63 time=0.065 ms
64 bytes from 12.11.0.55: icmp_seq=2 ttl=63 time=0.102 ms
64 bytes from 12.11.0.55: icmp_seq=3 ttl=61 time=0.139 ms
--- 12.11.0.55 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2038ms
rtt min/avg/max/mdev = 0.065/0.102/0.139/0.030 ms

mininet> ovh_r12 ping -c 3 resolver1
PING 12.11.0.55 (12.11.0.55) 56(84) bytes of data.
64 bytes from 12.11.0.55: icmp_seq=1 ttl=61 time=0.076 ms
64 bytes from 12.11.0.55: icmp_seq=2 ttl=61 time=0.124 ms
64 bytes from 12.11.0.55: icmp_seq=3 ttl=61 time=0.130 ms
--- 12.11.0.55 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2000ms
rtt min/avg/max/mdev = 0.076/0.110/0.130/0.024 ms

mininet> ovh_r12 ping -c 3 resolver2
PING 12.11.0.55 (12.11.0.55) 56(84) bytes of data.
64 bytes from 12.11.0.55: icmp_seq=1 ttl=61 time=0.035 ms
64 bytes from 12.11.0.55: icmp_seq=2 ttl=63 time=0.105 ms
64 bytes from 12.11.0.55: icmp_seq=3 ttl=63 time=0.103 ms
--- 12.11.0.55 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.035/0.081/0.105/0.032 ms
```

- Using `traceroute`, we have the following outputs (here, `resolver2` is closer to `ovh_r12` than `resolver1`):

```
mininet> ovh_r12 traceroute 12.11.0.55
traceroute to 12.11.0.55 (12.11.0.55), 30 hops max, 60 byte packets
 1  ovh_r9 (12.11.0.36)  0.060 ms  0.045 ms  0.020 ms
 2  ovh_r3 (12.11.0.12)  0.033 ms  0.026 ms  0.018 ms
 3  ovh_r7 (12.11.0.15)  0.035 ms  0.023 ms  0.021 ms
 4  resolver2 (12.11.0.55)  0.098 ms  0.037 ms  0.027 ms

mininet> ovh_r12 traceroute resolver1
traceroute to 12.11.0.55 (12.11.0.55), 30 hops max, 60 byte packets
 1  ovh_r4 (12.11.0.22)  0.021 ms  0.006 ms  0.004 ms
 2  resolver2 (12.11.0.55)  0.034 ms  0.009 ms  0.005 ms

mininet> ovh_r12 traceroute resolver1
traceroute to 12.11.0.55 (12.11.0.55), 30 hops max, 60 byte packets
 1  ovh_r9 (12.11.0.36)  0.049 ms  0.012 ms  0.007 ms
 2  ovh_r3 (12.11.0.12)  0.024 ms  0.012 ms  0.018 ms
 3  ovh_r7 (12.11.0.15)  0.027 ms  0.015 ms  0.014 ms
 4  resolver2 (12.11.0.55)  0.028 ms  0.019 ms  0.018 ms

mininet> ovh_r12 traceroute resolver2
traceroute to 12.11.0.55 (12.11.0.55), 30 hops max, 60 byte packets
 1  ovh_r9 (12.11.0.36)  0.021 ms  0.005 ms  0.004 ms
 2  ovh_r3 (12.11.0.12)  0.013 ms  0.007 ms  0.006 ms
 3  ovh_r7 (12.11.0.15)  0.013 ms  0.010 ms  0.013 ms
 4  resolver2 (12.11.0.55)  0.019 ms  0.010 ms  0.009 ms

mininet> ovh_r12 traceroute resolver2
traceroute to 12.11.0.55 (12.11.0.55), 30 hops max, 60 byte packets
 1  ovh_r4 (12.11.0.22)  0.033 ms  0.010 ms  0.009 ms
 2  resolver2 (12.11.0.55)  0.022 ms  0.012 ms  0.010 ms
```

### IPv6

- `ovh_r12` tries to reach 2023:b::37 (`resolver1` or `resolver2`):

```
mininet> ovh_r12 ping6 -c 3 2023:b::37
PING 2023:b::37(2023:b::37) 56 data bytes
64 bytes from 2023:b::37: icmp_seq=1 ttl=61 time=0.276 ms
64 bytes from 2023:b::37: icmp_seq=2 ttl=61 time=0.228 ms
64 bytes from 2023:b::37: icmp_seq=3 ttl=61 time=0.180 ms

--- 2023:b::37 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2016ms
rtt min/avg/max/mdev = 0.180/0.228/0.276/0.039 ms
```

- Using `traceroute6`, we have the following outputs:

```
mininet> ovh_r12 traceroute6 2023:b::37
traceroute to 2023:b::37 (2023:b::37) from 2023:b::17, 30 hops max, 24 byte packets
 1  ovh_r4 (2023:b::16)  0.158 ms  0.036 ms  0.018 ms
 2  resolver2 (2023:b::37)  0.021 ms  0.019 ms  0.014 ms
```

### UDP

We use the command `dig @server name type_record` to check if our anycast DNS works with UDP.

```
mininet> ovh_r1 dig @12.11.0.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY
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
ovh.com.		60	IN	NS	resolver1.ovh.com.
ovh.com.		60	IN	NS	resolver2.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 12:55:50 UTC 2020
;; MSG SIZE  rcvd: 245
```
```
mininet> ovh_r1 dig @resolver1 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @resolver1 ovh.com ANY
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
ovh.com.		60	IN	NS	resolver2.ovh.com.
ovh.com.		60	IN	NS	resolver1.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55

;; Query time: 0 msec
;; SERVER: 2023:b::37#53(2023:b::37)
;; WHEN: Fri Nov 13 13:00:54 UTC 2020
;; MSG SIZE  rcvd: 245
```
```
mininet> ovh_r1 dig @12.11.0.55 webserver1.ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 webserver1.ovh.com ANY
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
;webserver1.ovh.com.		IN	ANY

;; ANSWER SECTION:
webserver1.ovh.com.	60	IN	A	12.11.0.57
webserver1.ovh.com.	60	IN	AAAA	2023:b::39

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	resolver2.ovh.com.
ovh.com.		60	IN	NS	resolver1.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 12:56:47 UTC 2020
;; MSG SIZE  rcvd: 255
```

```
mininet> ovh_r12 dig @12.11.0.55 webserver1.ovh.com AAAA

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 webserver1.ovh.com AAAA
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
;webserver1.ovh.com.		IN	AAAA

;; ANSWER SECTION:
webserver1.ovh.com.	60	IN	AAAA	2023:b::39

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	resolver1.ovh.com.
ovh.com.		60	IN	NS	resolver2.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 13:01:26 UTC 2020
;; MSG SIZE  rcvd: 239
```

(Sometimes, no answer is given, with a message of size 64).

With IPv6, however, the configuration file of the in-addr.arpa.zone is not created for some unknown reason. Then the 
`dig` command cannot give an answer, as shown here:

```
mininet> ovh_r12 dig @2023:b::37 ovh.com ANY

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
mininet> xterm resolver1
mininet> xterm resolver2
mininet> xterm ovh_r12
xterm resolver1> tcpdump -w tcpdump_resolver1_udp.pcap -i any udp port 53 -v
xterm resolver2> tcpdump -w tcpdump_resolver2_udp.pcap -i any udp port 53 -v
xterm ovh_r12> nc -u 12.11.0.55 53
Hello DNS server! (UDP, IPv4)
xterm ovh_r12> nc -u 2023:b::37 53
Hello DNS server! (UDP, IPv6)
```

Results: 4 packets received by `resolver1`, nothing for `resolver2` (see `pcap/tcpdump_resolver1_udp.pcap` and 
`pcap/tcpdump_resolver2_udp.pcap`).

### TCP

- Querying DNS name servers with additional parameter `+tcp`:

```
mininet> ovh_r6 dig @12.11.0.55 ovh.com ANY +vc

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY +vc
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
ovh.com.		60	IN	NS	resolver1.ovh.com.
ovh.com.		60	IN	NS	resolver2.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 14:45:49 UTC 2020
;; MSG SIZE  rcvd: 245
```

```
mininet> ovh_r6 dig @12.11.0.55 ovh.com ANY +tcp

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY +tcp
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
ovh.com.		60	IN	NS	resolver1.ovh.com.
ovh.com.		60	IN	NS	resolver2.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 14:46:45 UTC 2020
;; MSG SIZE  rcvd: 245
```

```
mininet> ovh_r6 dig @12.11.0.55 webserver1.ovh.com AAAA +tcp

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 webserver1.ovh.com AAAA +tcp
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
;webserver1.ovh.com.		IN	AAAA

;; ANSWER SECTION:
webserver1.ovh.com.	60	IN	AAAA	2023:b::39

;; AUTHORITY SECTION:
ovh.com.		60	IN	NS	resolver1.ovh.com.
ovh.com.		60	IN	NS	resolver2.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.	60	IN	A	12.11.0.55
resolver2.ovh.com.	60	IN	A	12.11.0.55
resolver1.ovh.com.	60	IN	AAAA	2023:b::37
resolver2.ovh.com.	60	IN	AAAA	2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 14:49:33 UTC 2020
;; MSG SIZE  rcvd: 239
```

With IPv6, it does not work for the same reason as for UDP:

```
mininet> ovh_r6 dig @2023:b::37 ovh.com ANY +tcp

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
mininet> xterm resolver1
mininet> xterm resolver2
mininet> xterm ovh_r12
xterm resolver1> tcpdump -w tcpdump_resolver1_tcp.pcap -i any tcp -v
xterm resolver2> tcpdump -w tcpdump_resolver2_tcp.pcap -i any tcp -v
xterm ovh_r12> nc 12.11.0.55 53
Hello DNS server! (TCP, IPv4)
xterm ovh_r12> nc 2023:b::37 53
Hello DNS server! (TCP, IPv6)
```

Results (see `pcap/tcpdump_resolver1_tcp.pcap` and `pcap/tcpdump_resolver2_tcp.pcap`):
- 259 packets captured and 556 packets received by filter for `resolver1`;
- 203 packets captured and 426 packets received by filter for `resolver2`

but only TCP establishment connection.
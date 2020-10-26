# Announced Prefixes

List of prefixes announced by the peers (25 per peer) of ASes 1299, 15169, 174 and 3356.



## Important Prefixes

### Root Servers

- 199.9.14.0/24:
```
199.9.14.0/24      via 198.27.73.102 on eth0 [rbx_g1_nc5 2020-10-22 from 94.23.122.41] * (100/0) [AS394353i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 20080 394353 394353
	BGP.next_hop: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.med: 1
	BGP.local_pref: 300
	BGP.community: (16276,38659) (20080,1000) (20080,1013) (20080,5000)
	BGP.originator_id: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.cluster_list: 94.23.122.41 94.23.122.12 178.32.135.101
                   via 198.27.73.102 on eth0 [rbx_g2_nc5 2020-10-22 from 94.23.122.46] (100/0) [AS394353i]
```

- 192.58.128.0/24 (local-pref higher than the previous one):

```
192.58.128.0/24    via 198.27.73.102 on eth0 [rbx_g1_nc5 2020-10-22 from 94.23.122.41] * (100/0) [AS26415i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 52320 53087 53087 53087 53087 53087 53087 262773 26415 26415 26415
	BGP.next_hop: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.med: 1
	BGP.local_pref: 330
	BGP.atomic_aggr: 
	BGP.aggregator: 186.232.192.202 AS26415
	BGP.community: (0,6939) (16276,39659)
	BGP.originator_id: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.cluster_list: 94.23.122.41 94.23.122.12 178.32.135.101
                   via 198.27.73.102 on eth0 [rbx_g2_nc5 2020-10-22 from 94.23.122.46] (100/0) [AS26415i]
```

- 193.0.14.0/24 (local-pref higher than the previous one):

```
193.0.14.0/24      via 198.27.73.102 on eth0 [rbx_g1_nc5 2020-10-22 from 94.23.122.41] * (100/0) [AS25152i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 7738 28186 25152
	BGP.next_hop: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.med: 1
	BGP.local_pref: 350
	BGP.community: (7738,50171) (16276,32659)
	BGP.originator_id: 198.27.73.102 (mia-mi1-bb1-a9.fl.us)
	BGP.cluster_list: 94.23.122.41 94.23.122.12 178.32.135.101
                   via 198.27.73.102 on eth0 [rbx_g2_nc5 2020-10-22 from 94.23.122.46] (100/0) [AS25152i]
```

- 192.33.4.0/24 (RR = **par-gsw-pb1-nc5**/`ovh_r10` and next AS in the AS path **AS 174**/`cogent_r1`):

```
192.33.4.0/24      unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS2149i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 174 2149
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 80
	BGP.atomic_aggr: 
	BGP.aggregator: 38.28.4.7 AS2149
	BGP.community: (174,21101) (16276,10817)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-04 from 94.23.122.46] (100/-) [AS2149i]
```

- 202.12.27.0/24 (**par-th2-sbb1-nc5**/`ovh_r10` as BGP next-hop and RR):

```
202.12.27.0/24     unreachable [rbx_g1_nc5 2020-10-24 from 94.23.122.41] * (100/-) [AS7500i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 7500
	BGP.next_hop: 54.36.50.200 (par-th2-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 300
	BGP.atomic_aggr: 
	BGP.aggregator: 202.12.27.66 AS7500
	BGP.community: (16276,31417)
	BGP.originator_id: 54.36.50.200 (par-th2-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-10-24 from 94.23.122.46] (100/-) [AS7500i]
```

- 192.112.36.0/24 (BGP next-hop: **par-gsw-pb2-nc5**/`ovh_r11` to reach **AS 3356** - Level3/`level3_r1` -):

```
192.112.36.0/24    unreachable [rbx_g1_nc5 2020-10-24 from 94.23.122.41] * (100/-) [AS5927i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 3356 3910 721 27065 5927
	BGP.next_hop: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 80
	BGP.atomic_aggr: 
	BGP.aggregator: 199.252.154.96 AS5927
	BGP.community: (209,90) (209,209) (209,41010) (3356,2) (3356,86) (3356,500) (3356,666) (3356,2064) (3910,3910) (3910,41010) (16276,10217) (65000,64990)
	BGP.originator_id: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-10-24 from 94.23.122.46] (100/-) [AS5927i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 3356 3910 721 27065 5927
	BGP.next_hop: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 80
	BGP.atomic_aggr: 
	BGP.aggregator: 199.252.154.96 AS5927
	BGP.community: (209,90) (209,209) (209,41010) (3356,2) (3356,86) (3356,500) (3356,666) (3356,2064) (3910,3910) (3910,41010) (16276,10217) (65000,64990)
	BGP.originator_id: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.46 54.36.50.100 54.36.50.195
```

- 199.7.83.0/24:

```
199.7.83.0/24      via 178.32.135.242 on eth0 [rbx_g1_nc5 2020-10-13 from 94.23.122.41] * (100/0) [AS20144i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 32098 20144
	BGP.next_hop: 178.32.135.242 (dfw-da2-bb1-a9.tx.us)
	BGP.med: 1
	BGP.local_pref: 340
	BGP.community: (16276,37158)
	BGP.originator_id: 178.32.135.242 (dfw-da2-bb1-a9.tx.us)
	BGP.cluster_list: 94.23.122.41 94.23.122.12 178.32.135.101
                   via 178.32.135.242 on eth0 [rbx_g2_nc5 2020-10-13 from 94.23.122.46] (100/0) [AS20144i]
```

### Others (DNS Servers, ...)

- Apple:

```
17.0.0.0/8         via 178.32.135.251 on eth0 [rbx_g1_nc5 2020-10-16 from 94.23.122.41] * (100/0) [AS714i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 714
	BGP.next_hop: 178.32.135.251 (pao-sv8-bb1-a9.ca.us)
	BGP.med: 1
	BGP.local_pref: 320
	BGP.community: (16276,31756)
	BGP.originator_id: 178.32.135.251 (pao-sv8-bb1-a9.ca.us)
	BGP.cluster_list: 94.23.122.41 94.23.122.12 178.32.135.101
                   via 178.32.135.251 on eth0 [rbx_g2_nc5 2020-10-22 from 94.23.122.46] (100/0) [AS714i]
```

- Google (without surprise, will reach **AS 15169**/`google_r1` ;  **par-gsw-pb1-nc5**/`ovh_r11` as BGP next-hop):

```
8.8.8.0/24         unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.122.46] (100/-) [AS15169i]
```

- 1.1.1.0/24:

```
1.1.1.0/24         unreachable [rbx_g1_nc5 2020-10-22 from 94.23.122.41] * (100/-) [AS13335i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 13335
	BGP.next_hop: 80.249.211.140 (ams-ix.as13335.net)
	BGP.med: 0
	BGP.local_pref: 300
	BGP.aggregator: 141.101.65.1 AS13335
	BGP.community: (16276,30202)
	BGP.originator_id: 94.23.122.25 (ams-5-a9.nl.eu)
	BGP.cluster_list: 94.23.122.41 94.23.122.12
                   unreachable [rbx_g2_nc5 2020-10-22 from 94.23.122.46] (100/-) [AS13335i]
```

## Telia (AS 1299)

- 96.17.4.0/22
- 96.16.192.0/21
- 95.101.133.0/24
- 92.241.220.0/22
- 92.241.216.0/22
- 92.241.192.0/20
- 91.149.32.0/20
- 84.254.68.0/22
- 80.91.248.0/21
- 80.91.240.0/20
- 80.239.224.0/19
- 80.239.192.0/19
- 80.239.160.0/19
- 80.239.128.0/19
- 72.247.64.0/21
- 72.246.240.0/22
- 62.115.0.0/16
- 5.154.160.0/21
- 46.230.224.0/20
- 46.230.216.0/21
- 46.230.208.0/21
- 46.230.208.0/20
- 46.230.192.0/20
- 46.230.176.0/20

## Google (AS 15169)

- 8.8.8.0/24
- 8.8.4.0/24
- 8.35.200.0/21
- 8.35.192.0/21
- 8.34.216.0/21
- 8.34.208.0/21
- 74.125.72.0/22
- 74.125.71.0/24
- 74.125.70.0/24
- 74.125.69.0/24
- 74.125.68.0/24
- 74.125.6.0/24
- 74.125.44.0/22
- 74.125.39.0/24
- 74.125.38.0/24
- 74.125.31.0/24
- 74.125.30.0/24
- 74.125.29.0/24
- 74.125.28.0/24
- 74.125.26.0/24
- 74.125.250.0/24
- 74.125.25.0/24
- 74.125.24.0/24
- 74.125.238.0/24
- 74.125.236.0/24

## Cogent (AS 174)

- 98.159.96.0/22
- 92.240.5.0/24
- 91.229.58.0/24
- 91.229.180.0/24
- 91.220.175.0/24
- 91.208.170.0/24
- 91.208.105.0/24
- 91.198.26.0/24
- 91.189.104.0/21
- 91.132.12.0/22
- 91.108.200.0/22
- 88.214.52.0/22
- 85.255.84.0/24
- 85.208.124.0/22
- 84.54.58.0/24
- 84.54.56.0/23
- 83.171.254.0/23
- 82.138.83.0/24
- 82.138.64.0/18
- 82.129.9.0/24
- 82.129.66.0/23
- 82.129.65.0/24
- 82.129.6.0/23
- 82.129.44.0/24
- 82.129.4.0/24

## Level3 (AS 3356)

- 99.193.251.0/24
- 98.159.39.0/24
- 98.159.38.0/24
- 98.159.33.0/24
- 98.159.32.0/24
- 98.159.239.0/24
- 98.159.234.0/24
- 98.159.226.0/24
- 92.119.149.0/24
- 92.119.12.0/22
- 91.207.153.0/24
- 91.207.152.0/24
- 91.149.254.0/24
- 91.149.252.0/23
- 91.149.232.0/23
- 91.149.230.0/24
- 91.149.228.0/23
- 91.149.222.0/23
- 91.149.218.0/23
- 89.167.241.0/24
- 89.167.240.0/24
- 89.167.232.0/24
- 89.167.224.0/24
- 89.167.219.0/24
- 89.167.175.0/24
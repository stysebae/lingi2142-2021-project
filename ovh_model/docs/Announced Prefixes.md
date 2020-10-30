# Announced Prefixes

List of prefixes announced by the peers (25 per peer) of ASes 1299, 15169, 174 and 3356.



## Important Prefixes

### Root Servers

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

### Others (DNS Servers, ...)

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

## Telia (AS 1299)

Rq: Reach those addresses through London (so is it useful to keep those addresses?)

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

All these IP addresses through Paris (**par-gsw-pb1-nc5.fr.eu**).

- 8.8.8.0/24:
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
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 8.8.4.0/24:
```
8.8.4.0/24         unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 8.35.200.0/21:
```
8.35.200.0/21      unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 8.35.192.0/21:
```
8.35.192.0/21      unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 8.34.216.0/21:
```
8.34.216.0/21      unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 8.34.208.0/21:
```
8.34.208.0/21      unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 74.125.72.0/22:
```
74.125.72.0/22     unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
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
- 74.125.29.0/24:
```
74.125.29.0/24     unreachable [rbx_g1_nc5 2020-08-05 from 94.23.122.41] * (100/-) [AS15169i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 15169
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 350
	BGP.community: (16276,34917)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-08-05 from 94.23.12
```
- 74.125.28.0/24
- 74.125.26.0/24
- 74.125.250.0/24
- 74.125.25.0/24
- 74.125.24.0/24
- 74.125.238.0/24
- 74.125.236.0/24

## Cogent (AS 174)

- 98.159.96.0/22:
```
98.159.96.0/22     unreachable [rbx_g1_nc5 2020-09-08 from 94.23.122.41] * (100/-) [AS174i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 174
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 80
	BGP.community: (174,21001) (174,22013) (16276,10817)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-09-15 from 94.23.12
```
- 92.240.5.0/24
- 91.229.58.0/24:
```
91.229.58.0/24     unreachable [rbx_g1_nc5 2020-09-24 from 94.23.122.41] * (100/-) [AS174i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 174
	BGP.next_hop: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 80
	BGP.community: (174,21101) (174,22007) (16276,10817)
	BGP.originator_id: 54.36.50.197 (par-gsw-pb1-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-09-24 from 94.23.12
```
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

- 99.193.251.0/24:
```
99.193.251.0/24    unreachable [rbx_g1_nc5 2020-10-29 from 94.23.122.41] * (100/-) [AS3356i]
	Type: BGP unicast univ
	BGP.origin: IGP
	BGP.as_path: 3356
	BGP.next_hop: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.med: 0
	BGP.local_pref: 100
	BGP.community: (3356,3) (3356,22) (3356,100) (3356,123) (3356,575) (3356,2003) (16276,10217)
	BGP.originator_id: 54.36.50.198 (par-gsw-pb2-nc5.fr.eu)
	BGP.cluster_list: 94.23.122.41 54.36.50.100 54.36.50.195
                   unreachable [rbx_g2_nc5 2020-10-29 from 94.23.12
```
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
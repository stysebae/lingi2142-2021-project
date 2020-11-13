# Debugging DNS

- **Enable BIND query logging** on the VM: `sudo rndc querylog` (disable it via the same command)

- **Remove all config files** related to a previous config: `cd /tmp && sudo rm /tmp/**`
- **Run IPMininet** script (via `tmux` or `tmux a`) and send these queries:

```
mininet> ovh_r1 dig @12.11.0.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 9710
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: cf4cae976d84d2864f806b895fae7aca712952c0c784c6d4 (good)
;; QUESTION SECTION:
;ovh.com.                       IN      ANY

;; ANSWER SECTION:
ovh.com.                172800  IN      SOA     ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.                60      IN      NS      resolver2.ovh.com.
ovh.com.                60      IN      NS      resolver1.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.      60      IN      A       12.11.0.55
resolver2.ovh.com.      60      IN      A       12.11.0.55
resolver1.ovh.com.      60      IN      AAAA    2023:b::37
resolver2.ovh.com.      60      IN      AAAA    2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 12:23:38 UTC 2020
;; MSG SIZE  rcvd: 245
```

and sometimes:

```
mininet> ovh_r1 dig @12.11.0.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 56222
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 3a7150188a8c08f513677f7a5fae7b457bd5271d437c9a9b (good)
;; QUESTION SECTION:
;ovh.com.                       IN      ANY

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 12:25:41 UTC 2020
;; MSG SIZE  rcvd: 64
```

```
mininet> ovh_r2 dig @12.11.0.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45493
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 70345da7338de682071923375fae7b79bf3e4a83b03f7123 (good)
;; QUESTION SECTION:
;ovh.com.                       IN      ANY

;; ANSWER SECTION:
ovh.com.                172800  IN      SOA     ovh.com. sysadmin.ovh.com. 1 86400 7200 3600000 172800
ovh.com.                60      IN      NS      resolver2.ovh.com.
ovh.com.                60      IN      NS      resolver1.ovh.com.

;; ADDITIONAL SECTION:
resolver1.ovh.com.      60      IN      A       12.11.0.55
resolver2.ovh.com.      60      IN      A       12.11.0.55
resolver1.ovh.com.      60      IN      AAAA    2023:b::37
resolver2.ovh.com.      60      IN      AAAA    2023:b::37

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 12:26:33 UTC 2020
;; MSG SIZE  rcvd: 245
```

and sometimes:

```
mininet> ovh_r2 dig @12.11.0.55 ovh.com ANY

; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> @12.11.0.55 ovh.com ANY
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 55296
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: fb7d39ed3ca0dd8d34ba73725fae5c81169103b7383a90d3 (good)
;; QUESTION SECTION:
;ovh.com.                       IN      ANY

;; Query time: 0 msec
;; SERVER: 12.11.0.55#53(12.11.0.55)
;; WHEN: Fri Nov 13 10:14:25 UTC 2020
;; MSG SIZE  rcvd: 64
```

- Associated **logs** in `/tmp` on the VM (`CTRL+B, then D` to leave the tmux session with IPMininet script):

```
vagrant@vagrant:/tmp$ cat named_resolver1.log 
13-Nov-2020 12:21:44.780 warning: /tmp/named_resolver1.55.0.11.12.in-addr.arpa.zone.cfg:13: ignoring out-of-zone data (57.0.11.12.in-addr.arpa)
vagrant@vagrant:/tmp$ cat named_resolver2.log 
13-Nov-2020 12:21:44.822 warning: /tmp/named_resolver2.55.0.11.12.in-addr.arpa.zone.cfg:13: ignoring out-of-zone data (57.0.11.12.in-addr.arpa)
13-Nov-2020 12:21:44.825 error: dns_master_load: file format mismatch (not raw)
13-Nov-2020 12:21:44.825 error: zone 2.ip6.arpa/IN: loading from master file /tmp/named_resolver2.2.ip6.arpa.zone.cfg failed: not implemented
13-Nov-2020 12:21:44.825 warning: zone 2.ip6.arpa/IN: unable to load from '/tmp/named_resolver2.2.ip6.arpa.zone.cfg'; renaming file to '/tmp/db-vvEqtBXK' for failure analysis and retransferring.
13-Nov-2020 12:21:44.826 error: dns_master_load: file format mismatch (not raw)
13-Nov-2020 12:21:44.826 error: zone ovh.com/IN: loading from master file /tmp/named_resolver2.ovh.com.zone.cfg failed: not implemented
13-Nov-2020 12:21:44.826 warning: zone ovh.com/IN: unable to load from '/tmp/named_resolver2.ovh.com.zone.cfg'; renaming file to '/tmp/db-VLhBjpVD' for failure analysis and retransferring.
```

**Warning**: `/tmp/named_resolver1.55.0.11.12.in-addr.arpa.zone.cfg:13: ignoring out-of-zone data (57.0.11.12.in-addr.arpa)` and `/tmp/named_resolver2.55.0.11.12.in-addr.arpa.zone.cfg:13: ignoring out-of-zone data (57.0.11.12.in-addr.arpa)`

cf. `/tmp/named_*` files
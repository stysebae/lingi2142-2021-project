# Anycast DNS

In our network, we have:
- one web server attached to `ovh_r11`
- one DNS resolver attached to `ovh_r7` (`resolver1`)
- another DNS resolver attached to `ovh_r4` (`resolver2`)

`resolver1` and `resolver2` shares the same IPv4 and IPv6 addresses:

![DNS resolver 1 IP addresses](../img/resolver1_ip.png)
![DNS resolver 2 IP addresses](../img/resolver2_ip.png)

On the link where they are attached to their respective resolvers, `ovh_r7` and `ovh_r4` also share the same IPv4 and 
IPv6 addresses:

![ovh_r7 IP addresses](../img/ovh_r7_ip.png)
![ovh_r4 IP addresses](../img/ovh_r4_ip.png)

The DNS zone (`/etc/master/ovh.com.zone`) is configured as follows:

```
$TTL 3600

; SOA Records
@        IN    SOA    resolver1.ns.ovh.com. dns.ovh.com. 2020042701 3600 10800 3600000 300

; NS Records
         IN    NS    resolver1.ns.ovh.com.
         IN    NS    resolver2.ns.ovh.com.

; A Records
www      IN    A     12.11.0.56

;EOF
```

with these lines added to `named.conf.local` (`/etc/bind/`):

```
zone "ovh.com" {
		type master;
		file "/etc/master/ovh.com.zone";
		allow-transfer {
			127.0.0.1;			# localhost
			12.11.0.54;			# DNS resolver1's IPv4 address
			12.11.0.54;			# DNS resolver2's IPv4 address
		};
		notify yes;
};
```

## Tests

- `ovh_r12` tries to reach `resolver1` and `resolver2`:

![ping DNS resolvers](../img/ping_resolvers.png)

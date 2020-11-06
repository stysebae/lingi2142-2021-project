# Security

## BGP

### Session security

- Adding message authentification : if the router doesn't provide a robust cryptographic mecanisms, TCP-MD5 must be used (it's better than nothing). The password string has to be complex enough otherwise this step became useless and **a different secret must be used on each interconnexion**. The choosen secret has to be manually configured by the peers and must match.
```
neighbor <ip-address> password <string>
```
*(This command has to be executed on each edge router)*

### Prefix filtering

- Add a filter on reserved IPv4 and IPv6 prefixes (martian addresses and illegals (127.0.0.1, 0.0.0.0, etc))  
If we annonce the route 0.0.0.0, we start to be a transit AS

```
ip prefix-list <list-name > | <list-number > [seqnumber] {deny <network>/<length> | permit <network>/<length>} [ge ge-length] [le le-length]
```

- Add a filter on prefixes considered as too specific (more than /24 for IPv4 and /48 for IPv6). This rule limit the size of the routing table.

```
ip prefix-list too-specific seq 5 permit 0.0.0.0/0 le 24
```

- Limit the number of annonced prefixes by a peer : this rule must be set to protect the router with limited memory to be overload and, more importently, to prevent the routing coherence. For exemple, a peer can send his whole routing table (containing the whole Internet) with the consequence of making some prefix unrechable.  
We known how many prefixes a peer will send, we can set the maximum prefix value for the interconnexion to this value (added with a certain amount to keep some extension freedom).

```
neighbor <ip-address> | <group-name> maximum-prefix <maximum> [threshold] [restart restart-interval] [warning-only]
```

- Don't announce private AS number : some AS number are reserved for internal purposes (like 192.168.x.x for IPv4), these number are between 64512 and 65534 (more recently, the range between 4200000000 and 4294967294 has been added to the list). Theses number can't be announced over the Internet because multiple AS can use them simultaneously ! They have to be deleted from the announce list at the edge of the AS.
```
neighbor <ip-address> | <group-name> remove-private-as [all [replace-as]]
```
*(This command has to be executed on each edge router)*

### Logging

- Enable the logging system on each router

```
bgp log-neighbor-changes
```

## References

- [ANSSI - Bonnes pratiques de configuration de BGP](https://www.ssi.gouv.fr/guide/le-guide-des-bonnes-pratiques-de-configuration-de-bgp/)  
In this document, our configuration of OVH can be classified into interconnexion 1 and relation 3
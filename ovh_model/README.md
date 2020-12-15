# OVH Network

This is a part of the "Computer Networks: Configuration and Management" course (LINGI2142, UCLouvain, academic year 2020-2021). The aim of this project is to develop a model of the OVH network (a large cloud provider based in France), configure it and manage it.

## Structure of this directory

There are some folders included in this current directory:

- `pcap`: You will find some `tcpdump` files used to test anycast DNS and to observe a reply from the server (even though the DNS requests which are sent are malformed by sending them via `netcat`);
- `docs` contains some documents that we used during the project to check how the implementation works

## How to launch the project

There are two files available in the *ovh_model*: *main.py* and *routers_cmd.py*. The first one permits to launch the OVH topology without the use of external commands from IPMininet and the second one allows us to use such commands. However, you will need *pexpect* to execute *routers_cmd.py* (you can install it with *pip install pexpect*)

Our version of IPMininet is not modified, but we recommend to install the version included in this project in order to have the same version than us when we did the project.

Lastly, if you want to test the security part of the project or if you want to see our eBGP announcements, you will need to use *routers_cmd.py*.

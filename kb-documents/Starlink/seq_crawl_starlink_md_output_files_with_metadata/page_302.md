---
title: What IP address does Starlink provide?
article_id: 1192f3ef-2a17-31d9-261a-a59d215629f4
category: Account
last_modified: '2025-04-04'
language: en
---

### What IP address does Starlink provide? 
##### On this page
  * [Starlink will allocate:](https://www.starlink.com/support/article/#starlink-will-allocate)


Starlink offers two IPv4 policies, "default" and "public". The default IPv4 configuration uses Carrier-Grade Network Address Translation (CGNAT) using private address space from the 100.64.0.0/10 prefix assigned to Starlink clients via DHCP. Network Address Translation (NAT) translates between private and Starlink public IPv4 Addresses. Starlink supports native IPv6 across all Starlink routers, kit versions, and service plans. All IPv6 compatible Starlink router clients are assigned IPv6 addresses.
The Starlink public IPv4 policy is an optional configuration available to Priority and Mobile Priority customers. A public IPv4 is reachable from any device on the Internet and is assigned to Starlink network clients using DHCP. Although truly static IPs are not available, a reservation system retains the public IPv4 address and IPv6 prefix even when the system is off or rebooted. However, relocating the Starlink or software updates may change these addresses. Public IPv4 address are not available for Standard and Mobile plans. The public IPv4 option can be enabled from the account dashboard, see instructions [here](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=13f0056c-6f6d-5a55-623c-fe94ad9947c5>). Note: Starlink WiFi routers do not support port forwarding or firewall rules for IPv4 or IPv6.
Each Starlink is allocated one IPv4 address via DHCPv4 and a delegated /56 IPv6 prefix via DHCPv6-PD. The "default" IPv4 CGNAT policy does not allow inbound traffic. Customers needing inbound traffic should consider using a third-party router, and if IPv4 inbound traffic is needed, a Starlink service plan with the public IPv4 option.
The IP address 206.214.239.194 indicates that Starlink is not connected to our Point of Presence (PoP) and therefore unable to receive its allocated IP address. The default 206.214.239.194 address is expected when Starlink is not connected to the PoP.
In addition, when the Starlink is in the process of connecting to the network, a default DNS server of 34.145.127.1 will be provided. Once the Starlink has verified connectivity with the Starlink network, then the DNS server will update to the DNS servers (usually 8.8.8.8 and 1.1.1.1).
Outbound ports TCP/25 (SMTP) and TCP/445 (SMB) are blocked for all customers per information security best practices.
As Starlink continues to expand and upgrades its global internet service, users may experience changes such as publicly routable addresses and non-CGNAT configurations.
​
Priority plan customers can view their public IP on the service line page at Starlink.com. When the public IP policy is set, the IP addresses appear at the top of the Devices section, above the graphs.
#### Starlink will allocate:
  * **One public IPv4 address for the customer’s wide area network (WAN)** , provisioned via Dynamic Host Configuration Protocol (DHCP) for routers/firewalls using IPv4.
  * **One IPv6 /64 prefix for the customer’s wide area network (WAN)** , provisioned via Stateless Address Auto Configuration (SLAAC) for routers/firewalls using IPv6.
  * **One IPv6 /56 prefix for the customer’s local area network (LAN)** , provisioned to routers capable of issuing a DHCPv6-PD request.


IP addresses are also available through the Starlink APIs. For more information, see [here](https://www.starlink.com/support/article/<https:/www.starlink.com/support/article/90109cc2-c7ec-31ff-d160-0a87f16ef759>).
The Starlink’s cell may be rehomed to a different PoP (Point of Presence) occasionally for latency improvements. As the cell is rehomed, the user terminal (UT) will have IP allocations from both PoPs and will determine when to switch over to the new PoP. During this time, IPs from both PoPs will be displayed, which will be six IP addresses overall. This will only last for about 10 minutes.
​
**Related questions:**
[How do I set my IP address to Public?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=13f0056c-6f6d-5a55-623c-fe94ad9947c5>)
[What ports does Starlink block?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=c3caacdf-1c1f-98db-b821-bbb36ca9d89b>)
---
title: What ports does Starlink block?
article_id: c3caacdf-1c1f-98db-b821-bbb36ca9d89b
category: Account
last_modified: '2025-04-04'
language: en
---

### What ports does Starlink block?
IP Version | Protocol | Port | Direction of Blocking | Common Port Use  
---|---|---|---|---  
IPv4 and IPv6 | TCP and UDP | 0 | Both Outbound and Inbound | Reserved  
IPv4 and IPv6 | UDP | 17 | Inbound | Quote of the Day (QOTD)  
IPv4 and IPv6 | UDP | 19 | Inbound | Character Generator Protocol (CHARGEN)  
IPv4 and IPv6 | TCP and UDP | 25 | Outbound | SMTP  
IPv4 | UDP | 67 | Both Outbound and Inbound | DHCP  
IPv4 and IPv6 | TCP and UDP | 135 to 139 | Both Outbound and Inbound | NetBios  
IPv4 | TCP | 445 | Outbound | SMB  
IPv4 | UDP | 520 | Inbound | RIP  
IPv6 | UDP | 546 to 547 | Both Outbound and Inbound | DHCPv6  
IPv4 and IPv6 | UDP | 1900 | Inbound | SSDP  
IPv4 and IPv6 | UDP | 11211 | Inbound | Memcached  
Note: In Indonesia, local regulations require us to block port 465 TCP. This may cause issues with Apple Mail on iOS when using the default settings. To resolve this, configure your mail client to use port 567 instead.
**Related questions:**
[What IP address does Starlink provide?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=1192f3ef-2a17-31d9-261a-a59d215629f4>)
---
title: Will enterprise site-to-site VPN or SDWAN appliances work on Starlink?
article_id: aa5aecf3-e97c-e84e-3f87-8d2ecdfde857
category: Account
last_modified: '2025-04-04'
language: en
---

### Will enterprise site-to-site VPN or SDWAN appliances work on Starlink? 
Yes. Like client VPN applications, NAT traversal support via TCP or UDP is required on the Starlink side of the VPN/SDWAN appliance. VPNs that rely on protocols 47 (GRE), 50 (ESP), 51 (AH), 115 (L2TP) are dropped by CGNAT at this time. 
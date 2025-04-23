---
title: How do I use the Starlink app with my third-party router?
article_id: 27802782-944e-10aa-bc29-23ccbc1fce73
category: Account
last_modified: '2025-04-04'
language: en
---

### How do I use the Starlink app with my third-party router?
You can utilize the Starlink app to view statistics, access terminal settings and contact support. Configuration may be required for the Starlink app to work with some third-party routers.
After you have set up your third-party router and connected to Starlink with the WAN port, open the Starlink app. If the app says "Starlink unreachable", create a static route in your router configuration settings.
Please refer to your router's documentation for instructions on setting a static route.
  * Network destination: 192.168.100.0
  * Subnet Mask: 255.255.255.0
  * Gateway: 192.168.100.1
  * Interface: WAN


**Note: These options may differ depending on your specific hardware and network configuration.**
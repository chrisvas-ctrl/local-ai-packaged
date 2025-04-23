---
title: Content Filtering
article_id: 1542bce8-8fa4-158f-5880-2dd366dec075
category: Account
last_modified: '2025-04-04'
language: en
---

### Content Filtering
Content Filtering allows you to block access to certain types of websites on your Starlink network. This feature is accessed through the Settings screen in the Router tab of the Starlink App. It offers three filtering options:
  * **No Filtering:** All websites are accessible.
  * **Malware:** Blocks websites that may contain malware.
  * **Malware and Adult Content:** Blocks both malware and adult content websites.


​ 
**How does it work?**
  * Under the hood, the Content Filtering feature works by setting a custom DNS server provided by Cloudflare (Cloudflare for Families). When Content Filtering is enabled, your router uses one of Cloudflare's DNS servers to help prevent access to specific categories of websites.


​ 
**Important considerations:**
  * **Best Effort:** This feature is a best effort solution to block certain types of websites. No filtering solution is perfect, and some sites may bypass these DNS filters.
  * **Over-blocking:** In some cases, legitimate sites may be unintentionally blocked.
  * **Limited Control:** Starlink uses Cloudflare’s DNS filtering, and as a result, we cannot control the specific websites that are blocked.


​ 
For more details on Cloudflare for Families, you can visit Cloudflare's blog.
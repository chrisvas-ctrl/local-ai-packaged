---
title: What do the different values in the data bucket represent under the data usage
  section of the API?
article_id: b4518e80-cdaf-f665-dceb-44e24ce34738
category: Account
last_modified: '2025-04-04'
language: en
---

### What do the different values in the data bucket represent under the data usage section of the API?
The "dataBucket", "restricted", and "unrestricted" fields refer to a "DataBucketType" enum with the following values:
  * 0: Unknown (e.x. data recorded before April 13th)
  * 1: Mobile Data
  * 2: Mobile Priority Data
  * 3: Standard Data
  * 4: Priority Data
  * 5: Non-billable (occasionally we will not count data as billable for various reasons)The "restricted" and "unrestricted" fields refer to the type of data that is provided when under or over the included priority data limit (if not opted in)


If "includeUnknownDataBin" parameter is not set to true then any "Unknown" buckets will not be included in the response.
For detailed information on this endpoint, refer to our[ readme.io](https://www.starlink.com/support/article/<https:/readme.com/>) documentation (<https://starlink.readme.io/docs>). Your account manager can provide a password for access to our documentation.
**Note:** API access is provided to larger business customers to manage accounts, user terminals, and service.
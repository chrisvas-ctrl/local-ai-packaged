---
title: Can an existing Starlink purchased from a retailer or end-user be transferred
  to a Reseller account?
article_id: 8b1ec404-00c2-8087-fd13-19001c2c0906
category: Account
last_modified: '2025-04-04'
language: en
---

### Can an existing Starlink purchased from a retailer or end-user be transferred to a Reseller account? 
Eligible Starlink kits and services purchased directly from Starlink can be transferred to authorized resellers. All terminals are eligible for transfer to resellers. 
  * **Note:** The Residential transfer restriction of 120 days after purchase or 90 days from service activation does **not** apply to Enterprise accounts.


Instructions to transfer your Starlink to a Reseller as an end-user:
  1. End-User needs to cancel service for the service line to be transferred
     * This can be completed via the portal from the " Manage" button under the home page
     * Select "Cancel Service" for the Starlink you wish to transfer
  2. End-User will need to click the "Transfer" button on the "Home" tab under "Manage" to unlock the kit from their account
     * This can be completed via your Starlink account from the "Manage" button under the home page
     * In the "Devices" section, locate the Starlink being transferred and select "Transfer"
     * **Note:** Selecting this button will stop service immediately regardless of time left in the current billing cycle. The "Transfer" button will only be accessible after the service is cancelled.
  3. End-user will need to communicate the Starlink ID to the Reseller
     * Your Starlink ID can be found under the "manage" button under the "Home" tab
  4. Reseller will need to add the serial number to their account 
     * Reseller will need to do this via the "Add and Unlock Starlinks" button under the Dashboard Page
     * Using the API, the Reseller will need to do this via the [POST] function under "User Terminal"
  5. Reseller will need to create a new service line to activate service for that Starlink 
     * This can be completed via the dashboard tab under "All Service Lines" (see [How do I activate my Starlink/service line using the dashboard?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=f75eb51b-323a-7d65-49d4-898a192e2400>))
     * This can be completed via the API via the [POST] function under "Service Line" and the [POST] function under "User Terminal"
     * **Note** : There may be an overlap for the first billing period when the kit is transferred; reseller is responsible for managing expectations with the end user.


Related Questions:
[What is a starlink identifier? ](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=2802431a-135f-0671-4c1b-4cedb65b291a>)
[How do I deactivate/cancel a service line using the dashboard?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=aad0c84a-cdb1-8b3c-78c8-fa794b29b36f>)
[How do I activate my Starlink/service line using the dashboard? ](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=f75eb51b-323a-7d65-49d4-898a192e2400>)
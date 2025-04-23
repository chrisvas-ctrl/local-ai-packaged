---
title: What is Starlink's proactive alerting?
article_id: 384ab23d-ff3a-5f33-5755-10c5e5a976ae
category: Account
last_modified: '2025-04-04'
language: en
---

### What is Starlink's proactive alerting?
Starlink now offers Enterprise customers the capability to create and manage alert emails. The customer has the capability to pick which metrics are important to their business and who should be emailed if that condition occurs. After creation, you can edit or delete proactive alerts on your account.
Currently, alerts will apply to all the devices under the account. In an effort to reduce spam, alerts will only trigger an email when the metric goes from a good to a bad state. This means if one of your devices is persistently in a bad state, we will only send one email when it initially gets into a bad state. An example is if you set up an alert for Software Update Reboot Required, it will only send an email when the device goes from not being in a reboot required state, to being in a reboot required state.
The proactive alert functionality is located on the dashboard tab of Starlink.com and can be accessed by users with the following roles: Admin, Technical, Technical Read-only. To access proactive alerts, click on the three horizontal lines at the top right of the service line list, then click "Proactive Alerts".
When you click the button, a window appears to create proactive alert.
  1. First select the device type to set up an alert for. If the account has routers, "Routers" and "Starlinks" will be selectable. Otherwise, it will default to Starlinks.
  2. Next, select the metric. Routers and Starlinks will have different metric options.
  3. Constraint: Depending on the metric selected, some metrics have Constraint options that you can select from. For example, if latency is the metric selected, you can pick between 5 options between 25ms and 250ms.
  4. Time: The amount of time the alert is in a bad state before sending the email. The alerts default to 10 minutes, but you can select other durations up to 60 minutes.
  5. Override Emails. If this field is left blank, all users on the account will be emailed when the condition is triggered. You can enter in multiple emails by separating the email addresses with a comma.


To view, edit, or delete existing proactive alerts, click into the "Edit/Delete Proactive Alerts" section. In this view, the "pencil" icon allows you to edit and the "trash can" icon allows you to delete.
Note: If the account only has one Starlink terminal, and it is using a 3rd party router, the only option for proactive alerts would be for the Starlink (not available for the 3rd party router). However, if the one Starlink terminal was using a Starlink router, proactive alerts would be available for both, even if the hardware is offline.
If you have a service line where service availablity is critical, you can take the following steps to ensure you have the maximum time to plan and coordinate the software update.
  1. Enable the 'Defer Software Updates' feature to increase the notification window to 3 days
  2. Configure a proactive alert for software updates to be notified of when the software update is pending.


Please check out these FAQs for additional information: 
[What is the 'Defer Software Updates' feature?](https://www.starlink.com/support/article/<https:/www.starlink.com/support/article/4331faa0-0edd-274e-6ace-7b3188afb4b4>)
[What is the "Late Adopter" configuration?](https://www.starlink.com/support/article/<https:/www.starlink.com/support/article/219ac7cc-4436-8260-36bc-af0a6765d704>)
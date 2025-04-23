---
title: What are the telemetry API alerts on my dashboard?
article_id: 413011a8-34c9-5b33-bf97-03f7ca7273ea
category: Account
last_modified: '2025-04-04'
language: en
---

### What are the telemetry API alerts on my dashboard?
Below is a list of Telemetry Alerts from your Starlink Device that may appear on your Dashboard and suggested actions on how to potentially resolve the issue. These alerts are triggered if the specific condition was met at least once in the previous 15 seconds. They will persist for as long as they are active.
**ETHERNET SLOW 10 MBPS**
  * **Definition:** The ethernet link has auto negotiated to 10 Mbps. The Starlink device should auto negotiate to 1000 Mbps. There may be a cable or connection issue.
  * **Suggested Action:** Make sure the client device port is configured to 1000 Mbps auto-negotiation.


**ETHERNET SLOW 100 MBPS**
  * **Definition:** The ethernet link has auto negotiated to 100 Mbps. The Starlink device should auto negotiate to 1000 Mbps. There may be a cable or connection issue.
  * **Suggested Action:** Make sure the client device port is configured to 1000 Mbps auto-negotiation.


**POWER SUPPLY THERMAL THROTTLING**
  * **Definition:** The power supply is exceeding it's upper safety thermal threshold. As a result, the Starlink is throttling itself to reduce its power draw and to let the power brick cool down.
  * **Suggested Action:** Physically check that the Starlink power supply is installed in a location that is properly ventilated and not exposed to external heat sources (e.g. near an exhaust vent).


**ACTUATOR MOTOR STUCK**
  * **Definition:** For actuated Starlink devices, the actuator motor is jammed and is not able to align the Starlink antenna to the desired angle. This can cause reduced performance, or the Starlink may not be able to connect to the network if the tilt too far from nominal.
  * **Suggested Action:** Physically check that there is no debris jammed in the Starlink preventing it from actuating. If there is no visible jam sources, please submit a ticket to Starlink Support for further assistance.


**MAST NOT VERTICAL**
  * **Definition:** For actuated Starlink devices, the Starlink alignment system is not able to align the Starlink antenna to the desired angle because the mast is greater than 30 degrees from vertical. This may cause poor performance, or the Starlink device may not be able to connect to the network unless corrected.
  * **Suggested Action:** Physically check that the Starlink terminal mast is vertical, and the terminal mount is securely installed. If necessary, adjust the mount so that the mast is vertical.


**UNABLE TO ALIGN**
  * **Definition:** The Starlink device is installed in a location that it's not able to align the antenna to the desired angle. This may cause poor performance, or the Starlink device may not be able to connect to the network unless corrected.
  * **Suggested Action:**
    * If the Starlink device has an actuated motor, physically inspect the Starlink install to ensure that the motor is functioning correctly by stowing and un-stowing the Starlink from the Starlink mobile app.
    * If the Starlink device is a Flat mount (un-actuated) model, check that the Starlink is securely attached to a horizontal surface.


**POWER DISCONNECT DETECTED**
  * **Definition:** The Starlink will report this alert when recovering from an unexpectedly power disconnect.
  * **Suggested Action:** If alert persists, check power source to power supply and check cable connections to power supply and terminal.


**THERMAL SHUTDOWN**
  * **Definition:** The Starlink device has reached the maximum temperature threshold and has stopped service to cool down. Service will resume when the Starlink device reaches a nominal operating temperature. Starlink devices are designed to operation nominally when the ambient temperature is below 50 degrees Celcius.
  * **Suggested Action:** (In extreme cases the Starlink will reboot in order to recover.) Physically check that the Starlink device is installed in a location that is properly ventilated and not exposed to external heat sources, e.g. near an exhaust vent.


**THERMAL THROTTLE**
  * **Definition:** The Starlink device has reached a high temperature threshold and is throttling performance to cool down. Performance will improve when the Starlink device reaches a nominal operating temperature. Starlink devices are designed to operation nominally when the ambient temperature is below 50 degrees Celcius.
  * **Suggested Action:** Physically check that the Starlink device is installed in a location that is properly ventilated and not exposed to external heat sources e.g. near an exhaust vent.


**DISABLED NO ACTIVE SERVICE LINE**
  * **Definition:** The account or service line associated with the Starlink device is not active or has been cancelled.
  * **Suggested Action:** Check that the service line is active and the account is in good standing. Ensure that payment details are setup and no outstanding unpaid invoices have caused the service to be disabled.


**DISABLED TOO FAR FROM SERVICE ADDRESS**
  * **Definition:** The Starlink device has moved too far from the service location on the account.
  * **Suggested Action:** Update the service address to resume service.


**DISABLED NO SERVICE IN OCEAN**
  * **Definition:** The Starlink device has moved into ocean coverage and does not have mobile priority data available.
  * **Suggested Action:** Update service plans to a Mobile Priority plan with additional data, or opt-in for Mobile Priority Data if you are on a mobile plan and have exceeded the Mobile Priority Data limit.


**DISABLED UNSUPPORTED COUNTRY**
  * **Definition:** The Starlink device has moved to a country where Starlink is either not enabled or the service plan is limited to a specific region.
  * **Suggested Action:** If Starlink is coverage is enabled, upgrade to a Mobile Global or Mobile Priority Service plan. Or opt-in for Mobile Priority Data.


**POP CHANGE**
  * **Definition:** The Starlink point of presence (PoP) has changed and as a result the Starlink will have a new IP address assigned for that region.
  * **Suggested Action:** You may need to reboot your Starlink or third-party equipment in order to get back online. If alert persists and performance is affected for more than 30 minutes, please contact Starlink Support for further assistance.


**DISABLED MOVING WHILE NOT MOBILE**
  * **Definition:** The Starlink device is moving at greater than 10 MPH (4.4. meters per second) and service has been disabled.
  * **Suggested Action:** Update the service plan to a Mobile Priority service plan. Or opt-in for Mobile Priority Data.


**DISABLED MOVING TOO FAST**
  * **Definition:** The Starlink device is moving faster than the configured policy allows and service has been disabled.
  * **Suggested Action:** Update the service plan to one which supports higher speeds.


**HIGH TIME OBSTRUCTION**
  * **Definition:** The Starlink device detected a high percentage of the time when the Starlink device was not able to make a connection to a satellite. The high time obstruction alert is an indicator of the time that Starlink was unable to successfully make a connection and the connection was dropped. This alert will be set if 0.27% of the time Starlink field of view is obstructed.
  * **Suggested Action:** Check that the Starlink is in an unobstructed location in all directions.


**SOFTWARE UPDATE REBOOT PENDING**
  * **Definition:** The Starlink device has downloaded a software update and is scheduled to reboot at 3 AM local time +/- 30 minutes. Local time is based on the current physical location of the Starlink hardware. After this alert is triggered, a manual reboot will also update the software if a the scheduled time is inconvenient.
  * **Suggested Action:** If you would prefer to have the software update happen at a different time, you can manually reboot via the dashboard or app to apply the update at a time of your choice.


**SANDBOX DISABLED**
  * **Definition:** A Starlink router is configured with a sandbox domain allow list, but has disabled sandboxing functionality. Sandboxed clients are no longer restricted to the sandbox domain allow list and have full internet access. See [documentation](https://www.starlink.com/support/article/<https:/starlink.readme.io/docs/client-sandboxing#failover>) for scenarios that cause this alert.
  * **Suggested Action:** The router will recover from this state on reboot. Either wait for the router to reboot, or manually trigger a reboot.


Related Topics:
  * [What is the Telemetry API and how do I get started?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=90109cc2-c7ec-31ff-d160-0a87f16ef759>)
  * [How do I check my Starlink's usage statistics on the dashboard?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=1992c87c-a3fa-cdc8-a05a-0573c1d02017>)
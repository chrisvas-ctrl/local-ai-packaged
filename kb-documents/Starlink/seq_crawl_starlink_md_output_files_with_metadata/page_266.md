---
title: How to install Starlink on boats
article_id: 6d0a3213-27e9-1698-d877-08e181928e25
category: Account
last_modified: '2025-04-04'
language: en
---

### How to install Starlink on boats
##### On this page
  * [Prepare for Install](https://www.starlink.com/support/article/#prepare-for-install)
  * [Key Considerations for a Successful Install](https://www.starlink.com/support/article/#key-considerations-for-a-successful-install)
  * [Installation Instructions](https://www.starlink.com/support/article/#installation-instructions)


#### Prepare for Install
**Starlink App:** Download the Starlink app first. The app will help you find an unobstructed install location, manage your account, test your connection, and browse the shop. (Download for [iOS](https://www.starlink.com/support/article/<https:/apps.apple.com/us/app/starlink/id1537177988>) /[Android](https://www.starlink.com/support/article/<https:/play.google.com/store/apps/details?id=com.starlink.mobile>))
The Starlink Flat High Performance Kit & the Starlink Standard Kit are both able to be installed on a Boat/Vessel. The Flat High Performance Kit is the recommended hardware as it has a wider field of view compared to the Standard Kit. Due to the Standard Kit having a smaller field of view, it is more sensitive to obstructions that may be more prevalent on boats in marinas, with short outages as a result. [**Click here**](https://www.starlink.com/support/article/<https:/www.starlink.com/support/article/24882fc1-7706-75f8-85f5-4bae73cb6020>) for more information on the differences between the Flat High Performance and Standard kit.
  * **Starlink Flat High Performance Kit:** Recommended hardware for boats. ([Flat High Performance setup guide](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=adc0df15-bcdf-909f-a0d3-40afc6c9e8a8>))
  * **Starlink Standard Kit:** Small shifts in position that are common in maritime environments may cause service interruptions as satellites move across the sky and out of the comparatively smaller field of view. ([Standard Kit setup guide](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=412a70ca-0d9a-813e-b18f-75c36b84ec06>))


Note: Customers using a Starlink that is not the Flat High Performance, Standard or Mini in-motion do so at their own risk. Damage to the Starlink while in motion may result in a void of your [Starlink warranty](https://www.starlink.com/support/article/<https:/www.starlink.com/legal/documents/DOC-1020-91087-64?regionCode=US>).
​
​
#### Key Considerations for a Successful Install
  * **Minimize Obstructions:** Each Starlink should have a clear view of the sky 20° elevation above the horizon, 360° around the azimuth. You may need to raise the antennas on a pole/pedestal to get a clear view of the sky & good service. If you have obstructions > 20° elevation in any direction, the connection may be occasionally interrupted.
  * **Orientation of the Mounts:** The mounts are tilted 8° to facilitate water runoff. Ideally, the antennas should be tilted in the direction with the fewest obstructions. Be sure to use a removable thread locker on all threaded fasteners.
    * Each Starlink has different mounts for different setup installations.
      * The Flat High Performance Kit comes with a wedge mount
      * The Standard Kit has a mobility mount available for purchase in the Starlink shop.
  * **Orientation of the Dish & Power Supply Unit:** Dish & PSU should be set up so that connectors are facing down or to the side. This is to avoid water collecting or sitting around the seal.
  * **Cables:** The maximum distance from the dish to the power supply is 25m (75'). The maximum total distance from the dish to the network equipment (passing through the power supply) is 100m (300'). The minimum bend radius of the cable is 5cm (2"). Sharp kinks in the ethernet cables can lower the throughput speed. The cables are _not reversible_. The connector on the end of the cable is specific to the device to which it connects.
  * **Power:** Starlink power supply input range 100-240V - 6.3A 50 - 60 Hz. Recommend using UPS-backed power supply to maintain internet connection through power dips and short power outages. The Starlink Power Supply supplies power to the dish and allows the data to pass through. For DC power sources, use a Pure Sine Wave inverter rated minimum 500W.
  * **Network:** Once the dish connects to the Starlink network, it allows the local device to request and be assigned an IP address. This IP will default to a CGNAT IP address unless the "Public IP" option is configured in the dashboard. More information on IP addresses can be found here
  * **Multiple Starlinks:** If installing multiple Starlinks in one location, the minimum separation distance from the mount center to mount center should be 3 meters. A third-party router can be used to connect the Starlinks together into one network and provide load balancing, traffic shaping, failover, and other advanced capabilities.
  * **Support:** It may take up to 20 minutes for Starlink to connect to the network. If you are having issues with setup, review the guidance in the Troubleshooting and Setup sections in Support. <https://support.starlink.com/>


​
​
#### Installation Instructions
  1. **Find an Unobstructed Location:**
     * Starlink must be 100% unobstructed for best performance. Even small obstructions in the field of view will have a negative impact on the quality of the connection, including intermittent outages, dropped packets or sessions, and a reduction in overall average bandwidth capacity.
     * Each dish should have clear view of the sky from around 20° elevation (above the horizon), with a full 360° azimuth (rotation). Any dish with obstructions will result in lower than the rated performance (i.e. bandwidth throughput) from that dish. It is of utmost importance to install in a location with a clear view of the sky. _(Customers have been successful installing Starlink on masts, railings, elevated posts, and roofs, since the dishes are less likely to be obstructed and are better protected from salt spray.)_
     * If your Starlink will not be the tallest object in sight at the install location, be sure to use the Starlink app to ensure no obstructions such as masts, antennas, or other structures will interrupt your service.
  2. **Mount the Starlink:**
     * Maritime & Mobility applications are best served by the **Flat High Performance Starlink** (spec sheet [here](https://www.starlink.com/support/article/<https:/www.starlink.com/specifications?spec=3>)). For most applications with the Flat High Performance Starlink, we recommend mounting using our [wedge mount](https://www.starlink.com/support/article/<https:/www.starlink.com/public-files/WedgeMountGuide_MobileHP_English.pdf>) to install the dish at a slight angle. This encourages rain water to run off the dish to prevent accumulation of droplets which would impact performance by blocking the beams to/from the satellite. However, for higher-speed vehicles a flat (horizontal) installation is acceptable to minimize drag. Be sure to use removable thread locker (for example Loctite 222) on all threaded fasteners, to prevent the faster from backing out due to vibration.
     * Other Mounting Solutions:
       * **Starlink Pole Mount Adapter for Flat High Performance (Flat HP):** for mounting on the end of a pole or mast.
       * Beam clamps or U-Bolts can be used to install the wedge mount on a railing. (This will require drilling into the mount.)
       * _Mounting options can vary by boat, and third-party mounts may suit your needs._


  1. **Connect Starlink:**
     * Connect the Starlink dish to power supply with the provided Starlink cable(s).
     * The Flat High Performance kit includes a 25 meter cable. Due to power requirements, the cable from the power supply to the dish can not be extended beyond 25m.
  2. **Connect the Power:**
     * Use the power cable to connect the power supply and the router (if in use) to a power source supplying AC voltage.
     * It is recommended to power the Starlink and any downstream router from a power source protected by an Uninterruptable Power Supply (UPS) to protect the Starlink from power spikes and surges and to provide continuous power to the Starlink through minor dips (brownouts) or short power outages.
  3. **Connect to the Network:**
     * **OPTION 1: Use the Starlink WiFi router.** (Not included in the Flat High Performance Kit, available for purchase via Starlink shop)
       * Use the Starlink Router cable to connect the power supply to the Starlink WiFi router.
       * Stand close to the router, open the Starlink app, and tap ‘Start Setup’. - This will guide you through the setup and prompt with WiFi configuration steps like setting a Network name and password. - No Starlink app? Find and connect to the STARLINK network in your device’s WiFi settings.
         * Confirm you are connected by navigating to a website, watching a video, or running a speed test from the app while connected to Starlink. You will see an ONLINE status on the main screen of the app.
         * We recommend using the Starlink router for initial setup confirmation.
     * **OPTION 2: Connect directly to a device or third-party router.**
       * Use the Starlink Ethernet cable to connect the power supply directly to ethernet port of a device or to the WAN port of a third-party router.
       * If the ethernet connection cable is not long enough, we suggest terminating or patching the cable. If the connection is outdoors, be sure to use a weatherproof connection. This cable from the power supply to your network is standard ethernet and can be extended up to 100m.
       * Connect the RJ-45 on the end of the ethernet cable to a computer or third-party router (or other network device).
       * Use the computer to navigate to a website, or use the third-party router's diagnostics to confirm a connection to the internet.


​
**Related Topics:**
  * [Flat High Performance Kit setup guide](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=adc0df15-bcdf-909f-a0d3-40afc6c9e8a8>)
  * [Standard Kit setup guide](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=412a70ca-0d9a-813e-b18f-75c36b84ec06>)
  * [Can I use Starlink in motion?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=50e933eb-54f5-1a77-cc85-c6c8325564cf>)
  * [Can I use Starlink on the ocean?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=952e770f-570e-d984-5014-35ae2add51c7>)
  * [Where can I use Starlink in motion for land mobility or maritime use?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=9eb841b3-2e43-a6fb-ecc7-ea58fb5600b5>)
  * [Is Starlink waterproof?](https://www.starlink.com/support/article/<https:/support.starlink.com/?topic=75d8de56-8906-34b5-5b94-b668d81a0cd6>)
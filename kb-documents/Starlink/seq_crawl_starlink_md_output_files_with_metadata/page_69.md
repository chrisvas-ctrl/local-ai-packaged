---
title: How does billing work for Enterprise?
article_id: f68a15d0-9ead-f4fb-c0c6-d069279a185d
category: Account
last_modified: '2025-04-04'
language: en
---

### How does billing work for Enterprise?
##### On this page
  * [Billing Day of Month Overview:](https://www.starlink.com/support/article/#billing-day-of-month-overview)
  * [Pro-ration Overview:](https://www.starlink.com/support/article/#pro-ration-overview)
  * [Data Treatment Examples:](https://www.starlink.com/support/article/#data-treatment-examples)
  * [To calculate the pro-rated charges corresponding to a given service line’s product updates using the API:](https://www.starlink.com/support/article/#to-calculate-the-pro-rated-charges-corresponding-to-a-given-service-line-s-product-updates-using-the-api)
  * [Frequently Asked Questions:](https://www.starlink.com/support/article/#frequently-asked-questions)


#### Billing Day of Month Overview:
As an Enterprise account, you will have a billing day of the month. The billing day of the month will be the day the invoice is generated. By default, payments are due 7 days after invoice generation.
The billing day of the month is linked at an account level and is based off the date you activate your first subscription. After your first subscription, all active subscriptions on the account, regardless of activation date, will be billed on the billing day of the month.
  * Example: If a subscription is activated on 2/10, the billing day of the month becomes the 10th. The first invoice will be generated on 3/10 and will bill for services activated since 2/10 and 3/10-4/10.


​
#### Pro-ration Overview:
Starting November 1, 2023, and reflected on monthly service invoices beginning December 1, 2023, monthly fees for any new service line or service plan upgrade will be subject to pro-rated billing.
  * **Change to a higher priced plan:** Access to the upgraded service plan will be immediate and you will be charged the higher price starting on the day you upgrade the plan. Your monthly invoice will reflect the difference in the pro-rated monthly price for the upgraded plan and the remaining days of your billing cycle.
  * **Change to a lower priced plan:** Your current service plan will remain the same for the remainder of the billing cycle. Access to the downgraded service plan will take effect at the start of your next billing cycle. If there are any overage charges that accrued under the previous and new service plans, you will be charged for them in the invoice for the next billing cycle. You will be charged the lower monthly service price for the downgraded service plan at the start of your next billing cycle.
  * **Change to a plan priced the same:** Access to the service plan will be immediate. Pricing reflected on the monthly invoice will remain the same.
  * **Pausing or cancelling a service plan:** A service plan that is paused or cancelled will remain active until the end of the current billing cycle. If that service plan is later reactivated, it will be pro-rated similar to a newly created service plan.
  * **Priority and Mobile Priority data consumption:** The data allocated under the service plan is not pro-rated. If you switch between Priority and Mobile Priority, data is allocated separately. If you incur overage data, you will be charged for the overage regardless of plan changes mid-billing cycle. See examples below of how data usage is treated if you change your plan mid-billing cycle.


​
#### Data Treatment Examples:
  * **Treatment of unused data after changing plans:**
    * A user is on a Priority 1TB Plan, in which 450GB of data is consumed during the billing cycle.
    * The user upgrades to the higher priced Mobile Priority 5TB Plan mid-billing cycle.
    * The user’s access to the Mobile Priority Plan is effective immediately with 5TB of data available for remainder of the billing cycle; the unused data from the original Priority 1TB Plan is not included, and 450GB of data is ignored.
  * **Treatment of unused data after changing plans with the same type of data:**
    * A user is on a Priority 1TB Plan, in which 450GB of data is consumed during the billing cycle.
    * The user upgrades to the higher priced Priority 5TB Plan mid-billing cycle.
    * The user’s access to the higher priced Priority Plan is effective immediately with 4550GB of data available for remainder of the billing cycle; the unused data from the original Priority 1TB Plan is not included.
  * **Treatment of overage data after changing plans:**
    * A user is on a Priority 1TB Plan, in which 450GB of data is consumed during the billing cycle.
    * The user upgrades to the higher priced Mobile Priority 50GB Plan mid-billing cycle.
    * The user’s access to the Mobile Priority Plan is effective immediately with 50GB of data available for the remainder of the billing cycle; the unused data from the original Priority 1TB Plan is not included, and 450GB of data is ignored. If the user has opted into additional data, the user will be charged an overaged fee once the 50GB of data is consumed. Overage fees are described [here](https://www.starlink.com/support/article/<https:/www.starlink.com/legal/documents/DOC-1469-65206-75?regionCode=>).


**IMPORTANT: If the data you have consumed for the month exceeds your plan’s data allocation, you will be charged overage fees. This overage charge will happen regardless of what plan you change to. If you want to avoid the possibility of overage fees, opt-out of overage data before overage data is incurred.**
​
#### To calculate the pro-rated charges corresponding to a given service line’s product updates using the API:
  1. GET partial periods for the target service line, which will be a list of start/end dates representing the period and the product ID held during that period.
     * Note: This endpoint will not reflect the current product held by the service line. For a complete pro-rated estimation, you will need to consider the additional partial period of your service line’s current product, which is held until your next billing day assuming no more changes are made.
  2. GET the available products, which map the product ID to the monthly service price
     * <https://starlink.readme.io/reference/get_enterprise-v1-account-accountnumber-subscriptions-available-products>


For detailed information, refer to our [readme.io documentation](https://www.starlink.com/support/article/<https:/starlink.readme.io/password?redirect=/docs>). Your account manager can provide a password for access to our documentation.
​
#### Frequently Asked Questions:
​
**A user is on a 5TB Mobile Priority Plan, then switches mid-billing cycle to a 50GB Mobile Priority Plan, how does this work?**
Since the 50GB Mobile Priority plan is a lower cost, they will remain on the 5TB plan for the rest of the billing cycle. Access to the 50GB Mobile Priority plan will take effect at the start of the next billing cycle. You will be charged for the 50GB Mobile Priority Plan on the start of your next billing cycle.
​
**A user is on a 50GB Mobile Priority Plan, then switches mid-billing cycle to a 5TB Mobile Priority Plan, how does this work?**
Access to the 5TB Mobile Priority Plan will be immediate and you will be charged the higher price starting on the day you upgrade the plan. Your monthly invoice will reflect the difference in the pro-rated monthly price for the upgraded plan and the remaining days of your billing cycle. 
For example, billing day of month is the 1st:
  1. Customer pays $250 on November 1st.
  2. Customer upgrades to a $1000 plan November 15th.
  3. December 1st, customer is charged (upgraded plan price - original plan price) * (number of days remaining in billing cycle/days in billing cycle month) = Pro-rated service plan price. 
     * ($1000 - $250) * (15/30) = $375


​
**A user is on a 40GB Priority Plan, opted-in for additional priority data, and consumes 1TB of Priority data. If the customer upgrades to the 1TB plan before the end of the month, are they charged overage fees?**
Overage data is calculated and charged based on the data limit of the plan you are on when the overage data is used. If your service plan is 40GB and you use 1TB of data, you will incur overage charges for 960GB of Priority data. If you upgrade to the 1TB plan at the end of the month, it does not cancel out your overage fees.
​
**How are pro-rated charges reflected on my invoice?**
If you change to a higher price plan or activate a service line mid-billing cycle, there will be a two invoice lines: 
  1. The previous billing cycle's pro-rated charge with the dates the service plan was active. 
  2. The current billing cycle's charge with the dates the service plan is active.


​
**How are days counted?**
For billing purposes, the pro-ration counts time using the specific timestamp of the upgrade. This means that an upgrade can take effect immediately.
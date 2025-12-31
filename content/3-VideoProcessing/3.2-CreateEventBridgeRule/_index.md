---
title : "Prepare Event Coordination Center (Amazon EventBridge)"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 3.2 </b> "
---

#### What is EventBridge Rule 
EventBridge Rule is a component that helps automatically route events from various sources to appropriate targets. It acts as a "traffic controller" for events in your system, determining which events should be sent where based on predefined patterns.

#### Objective
Create a **Rule** in **Amazon EventBridge** to:
- **Listen** to all events in the system
- **Detect** `Checkout` events from `BasketFunction`
- **Forward** those events to the **SQS `OrderingQueue`**

#### Practice
1. Access AWS Console, enter **EventBridge** and access the **Amazon EventBridge** service
![](/images/3-2/01.png?width=50pc)

2. From the interface, select **Rule** in the left slider and click **Create rule**
![](/images/3-2/02.png?width=50pc)

3. From the Create rule interface
   - Name enter: **`CheckoutToOrderingRule1`**
   - Click **Next**
![](/images/3-2/03.png?width=50pc)

4. In the Build event pattern step
   - Event source select **Other**
   - Event pattern select **Custom pattern (JSON editor)**
   - Click **Next**

```json
{
  "source": ["com.ecommerce.basket"],
  "detail-type": ["CheckoutEvent"]
}
```
![](/images/3-2/04.png?width=50pc)

5. In the Select target step
   - Target type select **AWS service**
   - Select a target choose **SQS queue**
   - Queue select **OrderingQueue1**
   - Click **Next**
![](/images/3-2/05.png?width=50pc)

6. Review and click **Create rule**
![](/images/3-2/06.png?width=50pc)

7. Successfully created EventBridge Rule by checking **Status** is **Enabled**
![](/images/3-2/07.png?width=50pc)
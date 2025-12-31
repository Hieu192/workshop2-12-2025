---
title : "Connect SQS with Lambda"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 3.3 </b> "
---

#### Objective
Configure our OrderingFunction1 to be automatically "triggered" whenever there is a new message in OrderingQueue1.

#### Practice
1. Access AWS Console, enter **Lambda** and access the **AWS Lambda** service
![](/images/2-3/01.png?width=50pc)

2. From the list of lambda functions, click **OrderingFunction1** and select **Add trigger**
![](/images/3-3/02.png?width=50pc)

3. In the add trigger interface
   - Select a source choose: **SQS**
   - SQS Queue select **OrderingQueue1**
   - Click **Add**
![](/images/3-3/03.png?width=50pc)

4. Verify the trigger was successfully added
![](/images/3-3/04.png?width=50pc)
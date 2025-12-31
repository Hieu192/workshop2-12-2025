---
title : "Create SQS and DLQ"
date :  "2024-10-27" 
weight : 1 
chapter : false
pre : " <b> 3.1 </b> "
---

#### What is SQS
SQS stands for Amazon Simple Queue Service – a fully managed message queue service by AWS. It's a service that allows you to send, store, and receive messages between software components asynchronously, without requiring components to run simultaneously or know each other's location.

#### Create SQS
1. Access AWS Console, enter **SQS** and navigate to the **Simple Queue Service**
   - In the **Amazon SQS** interface, select **Create queue**
![](/images/3-1/01.png?width=50pc)

2. In the queue creation interface:
   - Type: select **Standard**
   - Name: enter **`video-embedding-dlq`**
   - Scroll down and click **Create queue**
![](/images/3-1/02.png?width=50pc)

3. In the queue creation interface:
   - Type: select **Standard**
   - Name: enter **`video-embedding-queue`**
   - Scroll down and click **Create queue**
![](/images/3-1/03.png?width=50pc)
   - Dead-letter-queue: select **`video-embedding-dlq`**
   - Maximum receive count: enter **3**
   - Scroll down and click **Create queue**
![](/images/3-1/04.png?width=50pc)

4. The queue interface looks like below and remember to copy both URL and ARN values
![](/images/3-1/05.png?width=50pc)
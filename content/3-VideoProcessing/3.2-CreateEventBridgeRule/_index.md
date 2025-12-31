---
title : "S3 EventBridge Rule"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 3.2 </b> "
---

#### What is EventBridge Rule

#### Create Send Notification for EventBridge Rule
![](/images/3-2/01.png?width=50pc)
![](/images/3-2/02.png?width=50pc)
![](/images/3-2/03.png?width=50pc)

#### Create EventBridge Rule
1. Access AWS Console, enter **EventBridge** and navigate to the **Amazon EventBridge** service
   - From the interface, select **Rule** on the left sidebar and click **Create rule**
![](/images/3-2/04.png?width=50pc)

2. Navigate to Configure
   - Name: enter **`s3-video-upload-to-sqs`**
   - Event bus name: **Default**
   - Click **Create**
![](/images/3-2/05.png?width=50pc)

3. From the Build tab interface
   - Trigger events: select **Code**
   ![](/images/3-2/06.png?width=50pc)
   - Paste the code below
```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["sl-video-analysis-videos-hieu"]
    },
    "object": {
      "key": [{
        "prefix": "videos/"
      }]
    }
  }
}
```
   - Click **Next**

6. Click on **Target**
   - Target Location: **Target in this account**
   - Queue: **`video-embedding-queue`**
   - Click **Create**
![](/images/3-2/07.png?width=50pc)

7. Successfully created EventBridge Rule by checking **Status** is **Enabled**
![](/images/3-2/08.png?width=50pc)
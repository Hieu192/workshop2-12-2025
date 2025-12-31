---
title : "S3 Event bridge rule"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 3.2 </b> "
---

#### EventBridge Rule là gì 

#### Tạo send notification cho event bridge rule
![](/images/3-2/01.png?width=50pc)
![](/images/3-2/02.png?width=50pc)
![](/images/3-2/03.png?width=50pc)

#### Tạo EventBridge Rule
1. Truy cập AWS Console, nhập **EventBridge** và truy cập vào dịch vụ **Amazon EventBridge**
   - Từ giao diện, chọn **Rule** ở slider bên trái và click **Create rule**
![](/images/3-2/04.png?width=50pc)

2. Truy cập vào Configure 
   - Name nhập: **`s3-video-upload-to-sqs`**
   - Event bus name: **Default**
   - Click **Create**
![](/images/3-2/05.png?width=50pc)

3. Từ giao diện tab Build
   - Trigger events chọn **Code**
   ![](/images/3-2/06.png?width=50pc)
   - Dán đoạn code bên dưới vào
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

6. Click vào **Target**
   - Target Location: **Target in this account**
   - Queue: **`video-embedding-queue`**
   - Click **Create**
![](/images/3-2/07.png?width=50pc)

7. Tạo thành công EventBridge Rule bằng cách check **Status** là **Enabled**
![](/images/3-2/08.png?width=50pc)

---
title : "Tạo DynamoDB Tables"
date :  "2024-10-27" 
weight : 1
chapter : false
pre : " <b> 2.1 </b> "
---


Trong bước này, chúng ta sẽ tạo các bảng DynamoDB cần thiết cho hệ thống phân tích video.

### Tạo video-analysis

1. Truy cập AWS Console và điều hướng đến dịch vụ **DynamoDB**. Từ giao diện DynamoDB, click **Create table**.

![](/images/2-1/01.png?featherlight=false&width=50pc)

2. Tạo bảng video-analysis
   - Table name nhập: **`video-analysis`**
   - Partition key nhập: **`PK`** (String)
   - Sort key nhập: **`SK`** (String)
![](/images/2-1/02.png?featherlight=false&width=50pc)
3. Từ bảng video-analysis, tạo index 
   - Index name nhập: **`GS1`**
   - Partition key Attribute nhập: **`GS1PK`** (String)
   - Sort key Attribute nhập: **`GS1SK`** (String) 

![](/images/2-1/03.png?featherlight=false&width=50pc)

4. Giữ các cài đặt khác mặc định và click **Create index**.
![](/images/2-1/04.png?featherlight=false&width=50pc)


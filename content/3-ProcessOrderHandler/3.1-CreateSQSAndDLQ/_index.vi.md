---
title : "Tạo SQS và DLQ"
date :  "2024-10-27" 
weight : 1 
chapter : false
pre : " <b> 3.1 </b> "
---

#### SQS là gì 
SQS là viết tắt của Amazon Simple Queue Service – một dịch vụ hàng đợi tin nhắn (message queue) được quản lý hoàn toàn bởi AWS. Nó là dịch vụ cho phép bạn gửi, lưu trữ và nhận tin nhắn giữa các thành phần phần mềm một cách bất đồng bộ (asynchronous), mà không cần các thành phần phải chạy cùng lúc hoặc biết vị trí của nhau.

#### Tạo SQS
1. Truy cập AWS Console, nhập **SQS** và truy cập vào dịch vụ **Simple Queue Service**
   - Ở giao diện **Amazon SQS**, chọn **Create queue**
![](/images/3-1/01.png?width=50pc)

2. Ở giao diện tạo queue:
   - Type chọn **Standard**
   - Name nhập: **`video-embedding-dlq`**
   - Kéo xuống và nhấn **Create queue**
![](/images/3-1/02.png?width=50pc)

3. Ở giao diện tạo queue:
   - Type chọn **Standard**
   - Name nhập: **`video-embedding-queue`**
   - Kéo xuống và nhấn **Create queue**
![](/images/3-1/03.png?width=50pc)
   - Dead-letter-queue chọn **`video-embedding-dlq`**
   - Maximum receive count nhập: **3**
   - Kéo xuống và nhấn **Create queue**
![](/images/3-1/04.png?width=50pc)

4. Giao diện của queue như dưới và nhớ copy 2 giá trị URL và ARN
![](/images/3-1/05.png?width=50pc)

---
title : "Tạo API Gateway"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 2.3 </b> "
---


Trong bước này, chúng ta sẽ tạo các API Gateway để gọi lambda.

### Tạo API Gateway để gọi lambda

1. Truy cập AWS Console và điều hướng đến dịch vụ **API Gateway** trong AWS Console.
    - Từ slider bên trái chọn **APIs** và click **Create API**.
![](/images/2-3/01.png?featherlight=false&width=50pc)

2. Từ giao diện **Create API** lướt xuống phần **Rest API**, chọn **Build**.
![](/images/2-3/02.png?featherlight=false&width=50pc)

3. Cấu hình function:
   - Chọn **New API**
   - API name: **`video-analysis-api`**
   - Api endpoint type: **Regional**
   - Click **Create Api**.
![](/images/2-3/03.png?featherlight=false&width=50pc)


4. Tạo method POST cho endpoint:
    - Method type: **POST**
    - Integration type: **Lambda Function**
    - Lambda proxy integration: **checked**
    - Lambda function: **video_upload**
    - Click **Create Method**
![](/images/2-3/04.png?featherlight=false&width=50pc)

5. Enable CORS.
![](/images/2-3/05.png?featherlight=false&width=50pc)   

6. Click vào / và click **Deploy API**.
![](/images/2-3/06.png?featherlight=false&width=50pc)

7. Triển khai deploy API
    - Stage: *New stage*
    - Stage name: **`dev`**
    - Click **Deploy**
![](/images/2-3/07.png?featherlight=false&width=50pc)
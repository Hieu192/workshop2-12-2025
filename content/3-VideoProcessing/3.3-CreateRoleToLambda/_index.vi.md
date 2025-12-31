---
title : "Tạo role cho lambda"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 3.3 </b> "
---


#### Mục tiêu
.

#### Thực hành
1. Truy cập AWS Console, nhập **IAM** và truy cập vào dịch vụ **Identity and Access Management**
   - Trong giao diện **Identity and Access Management**, chọn **Roles** ở slider bên trái và click **Create role**
![](/images/3-3/01.png?width=50pc)

2. Trong giao diện **Create role**, chọn **Lambda** và click **Next: Permissions**
   - Trusted entity type chọn **AWS service**
   - Service chọn **Lambda**
   - Use case chọn **Lambda**
   - Click **Next**
![](/images/3-3/02.png?width=50pc)

3. Trong giao diện **Add permissions**, chọn **AWSLambdaBasicExecutionRole**, **AWSStepFunctionsFullAccess**, **AmazonS3FullAccess**, **AmazonSQSFullAccess**, **DynamoDBFullAccess** và click **Create Role**
![](/images/3-3/03.png?width=50pc)
![](/images/3-3/04.png?width=50pc)
![](/images/3-3/05.png?width=50pc)

4. Trong giao diện Role tiếp tục thêm quyền **permissions**
   - Chọn **AmazonBedrockFullAccess**
   - Click **Add permissions**
![](/images/3-3/06.png?width=50pc)
![](/images/3-3/07.png?width=50pc)
![](/images/3-3/08.png?width=50pc)


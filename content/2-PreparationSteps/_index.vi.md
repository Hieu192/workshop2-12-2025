---
title : "Các bước chuẩn bị"
date :  "2024-10-27" 
weight : 2 
chapter : false
pre : " <b> 2. </b> "
---

### Các bước chuẩn bị

Trong chương này, chúng ta sẽ thiết lập nền tảng cơ bản cho hệ thống, tập trung vào việc tạo cơ chế tải video lên S3 và lưu trữ metadata vào DynamoDB.

#### Luồng hoạt động cơ bản

1. **Người dùng (Admin)**: Gửi yêu cầu lấy đường dẫn tải lên (Presigned URL) thông qua API Gateway.
2. **Lambda (upload_video)**: Xử lý logic tạo Presigned URL an toàn và đồng thời tạo một bản ghi chờ trong DynamoDB để quản lý trạng thái video.
3. **Lưu trữ**: Video sẽ được tải trực tiếp lên S3 Bucket, kích hoạt các bước xử lý tự động ở chương sau.

![](/images/2/image.png?featherlight=false&width=50pc)

#### Các bước thực hiện

1. [Tạo bảng DynamoDB](2.1-CreateTableDynamo/)
2. [Tạo Lambda function tải video](2.2-CreateLambda/)
3. [Tạo API Gateway](2.3-CreateAPIGateway/)
4. [Kiểm tra API Gateway](2.4-TestAPIGateway/)

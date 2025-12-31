---
title : "Xây dựng cơ chế tải video"
date :  "2024-10-27" 
weight : 2 
chapter : false
pre : " <b> 2. </b> "
---

### Xây dựng cơ chế tải video (Video Upload Mechanism)

Trong chương này, chúng ta sẽ xây dựng những thành phần đầu tiên của hệ thống để cho phép tải video lên một cách an toàn và quản lý thông tin video.

#### Quy trình tải video lên

Hệ thống sử dụng kỹ thuật **Presigned URL** để cho phép người dùng tải file trực tiếp lên S3 mà không cần thông qua máy chủ trung gian, giúp tối ưu hiệu năng:
1. **Yêu cầu (Request)**: Admin gửi yêu cầu tải video thông qua API Gateway.
2. **Cấp quyền (Authorize)**: Hàm Lambda `upload_video` được kích hoạt để tạo ra một đường dẫn tải lên (Presigned URL) có thời hạn.
3. **Metadata**: Đồng thời, thông tin cơ bản về video sẽ được ghi nhận vào bảng **DynamoDB** với trạng thái ban đầu.
4. **Tải lên (Upload)**: Người dùng sử dụng đường dẫn đã được cấp để tải file video trực tiếp vào **S3 Bucket**.

![](/images/2/image.png?featherlight=false&width=50pc)

#### Các bước thực hành

1. [Tạo bảng DynamoDB lưu trữ](2.1-CreateTableDynamo/)
2. [Tạo Lambda function xử lý upload](2.2-CreateLambda/)
3. [Cấu hình API Gateway cho Upload](2.3-CreateAPIGateway/)
4. [Kiểm tra luồng tải lên API](2.4-TestAPIGateway/)

---
title : "Tìm kiếm video đa phương thức"
date :  "2024-10-27" 
weight : 4 
chapter : false
pre : " <b> 4. </b> "
---

### Tìm kiếm video đa phương thức (Multimodal Search)

Trong chương này, chúng ta sẽ xây dựng giao diện lập trình ứng dụng (API) để cho phép người dùng tìm kiếm các đoạn video dựa trên nội dung văn bản hoặc hình ảnh. Đây là phần quan trọng nhất giúp người dùng tương tác với dữ liệu video đã được xử lý.

#### Kiến trúc luồng tìm kiếm

Hệ thống sử dụng mô hình tìm kiếm ngữ nghĩa (Semantic Search) thay vì tìm kiếm theo từ khóa truyền thống:
1. **Yêu cầu (Request)**: Người dùng gửi truy vấn dưới dạng văn bản (ví dụ: "người đàn ông chơi đàn") hoặc tải lên một hình ảnh.
2. **Xử lý (Processing)**: Hàm Lambda tiếp nhận yêu cầu, sử dụng Amazon Bedrock để chuyển đổi truy vấn đó thành các vector embedding (tọa độ không gian).
3. **Truy vấn (Query)**: Thực hiện tìm kiếm vector (Vector Search) trên Amazon OpenSearch Serverless để tìm các đoạn video có vector gần giống nhất với truy vấn.
4. **Phản hồi (Response)**: Trả về thông tin chi tiết đoạn video bao gồm tên file, thời điểm bắt đầu/kết thúc và đường dẫn xem trực tiếp.

![](/images/4/image.png?featherlight=false&width=50pc)

#### Nội dung chính

1. [Tạo Lambda tìm kiếm](4.1-CreateLambdaSearch/)
2. [Cấu hình API Gateway](4.2-CreateLambdaApiGateway/)
3. [Kiểm thử bằng Postman](4.3-TestAPIByPostman/)

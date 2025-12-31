---
title : "Giới thiệu"
date :  "2024-10-27" 
weight : 1 
chapter : false
pre : " <b> 1. </b> "
---

### Giới thiệu kiến trúc Microservice trên AWS

Kiến trúc này được xây dựng theo mô hình **Event-Driven (Kiến trúc hướng sự kiện)** và **Serverless**. Mục tiêu chính là tự động hóa quy trình xử lý video từ lúc tải lên cho đến khi có thể tìm kiếm được bằng ngôn ngữ tự nhiên thông qua kỹ thuật Vector Search (sử dụng **Amazon Bedrock** và **OpenSearch**).

![](/images/1/image.png?featherlight=false&width=50pc)

### Luồng hoạt động chi tiết

#### 1. Tải lên và Lưu trữ (Ingestion Phase)
Admin gửi yêu cầu tải video thông qua **API Gateway**.

Lambda **upload_video** tiếp nhận yêu cầu, thực hiện:
- Tạo một presigned URL cho video
- Lưu trữ file video gốc vào **S3 (Video Storage)** thông qua presigned URL.
- Lưu thông tin metadata (tên, kích thước, ngày tạo...) vào **DynamoDB**.

#### 2. Kích hoạt quy trình xử lý (Trigger Phase)
- Khi video được lưu vào **S3**, một sự kiện được gửi đến **Amazon EventBridge**.
- **EventBridge** chuyển tiếp thông báo đến **SQS (Simple Queue Service)** để đảm bảo tính ổn định và khả năng mở rộng (buffering).
- Lambda **sfn_trigger** tiêu thụ tin nhắn từ SQS và kích hoạt quy trình **AWS Step Functions**.

#### 3. Trích xuất Embedding và Đánh chỉ mục (Processing Phase)
Đây là cốt lõi của hệ thống, nằm trong **Step Functions workflow**:
1. **embedding_start**: Lambda này gọi **Amazon Bedrock** (sử dụng các mô hình như Titan Multimodal Embeddings) bất đồng bộ để phân tích nội dung video và chuyển đổi thành các vector số học (embeddings).
2. **embedding_check**: Vì việc xử lý video có thể mất thời gian và bất đồng bộ, bước này dùng để kiểm tra trạng thái hoàn thành của tiến trình AI bằng cách sử dụng vòng lặp gọi lại lambda **embedding_start** cho đến khi có kết quả.
3. **embedding_index**: Sau khi có kết quả embedding, Lambda này sẽ đẩy dữ liệu vector vào **OpenSearch Serverless** để phục vụ tìm kiếm sau này. Đồng thời cập nhật trạng thái xử lý vào **DynamoDB**.

#### 4. Tìm kiếm (Search Phase)
User gửi câu truy vấn (ví dụ: "Tìm người hút thuốc trong phòng") qua **API Gateway**.

Lambda **search_video** thực hiện:
- Gọi **Amazon Bedrock** để chuyển câu truy vấn văn bản của người dùng thành vector.
- Thực hiện truy vấn **Vector Search** trên **OpenSearch Serverless** để tìm các video có nội dung tương đồng nhất.
- Lấy thêm thông tin chi tiết từ **DynamoDB** và trả về kết quả (bao gồm link video từ S3) cho người dùng.

### Các thành phần chính và vai trò
- **S3**: Lưu trữ dữ liệu thô (Video) và embedding video (Vector).
- **DynamoDB**: Lưu trữ dữ liệu có cấu trúc (Metadata, trạng thái xử lý).
- **Step Functions**: Điều phối (Orchestration) các bước xử lý phức tạp, đảm bảo tính nhất quán nếu có lỗi xảy ra.
- **Amazon Bedrock**: Cung cấp các mô hình học máy (Foundation Models) để xử lý AI mà không cần quản lý hạ tầng.
- **OpenSearch Serverless**: Cơ sở dữ liệu vector giúp tìm kiếm ngữ nghĩa (Semantic Search) nhanh chóng.
- **CloudWatch**: Giám sát log và hiệu năng của toàn bộ hệ thống.

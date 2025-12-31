---
title : "Dọn dẹp tài nguyên"
date :  "2024-10-27" 
weight : 7
chapter : false
pre : " <b> 7. </b> "
---

#### Dọn dẹp tài nguyên
Để tránh phát sinh chi phí không mong muốn, chúng ta sẽ tiến hành xóa các tài nguyên đã khởi tạo trong workshop theo thứ tự sau:

1. **Xóa API Gateway**:
   - Truy cập dịch vụ **API Gateway**.
   - Chọn API `video-analysis-api` và nhấn **Delete**.

2. **Xóa Step Functions**:
   - Truy cập dịch vụ **Step Functions**.
   - Chọn State Machine `StepLambdaEmbeddingvideo` và nhấn **Delete**.

3. **Xóa Lambda Functions**:
   - Truy cập dịch vụ **Lambda**.
   - Xóa các hàm: `upload-video`, `sfn-trigger`, `embedding-start`, `embedding-check`, `embedding-index`, `video-search`.

4. **Xóa SQS & EventBridge**:
   - Truy cập dịch vụ **SQS**, xóa `video-processing-queue` và `video-processing-dlq`.
   - Truy cập **EventBridge**, chọn Rule lắng nghe sự kiện S3 và xóa.

5. **Xóa OpenSearch Serverless**:
   - Truy cập **Amazon OpenSearch Service**, mục **Serverless**.
   - Xóa bộ sưu tập (Collection) `video-embeddings`.

6. **Xóa DynamoDB**:
   - Truy cập dịch vụ **DynamoDB**.
   - Chọn bảng `video-analysis` và nhấn **Delete table**.

7. **Xóa S3 Bucket**:
   - Truy cập dịch vụ **S3**.
   - Làm trống (Empty) và xóa Bucket chứa video và kết quả embedding.

8. **Xóa IAM Role & Policy**:
   - Truy cập dịch vụ **IAM**, xóa Role `lambda-video-embedding-role` và các Policy đi kèm.

![](/images/7/10.png?width=50pc)

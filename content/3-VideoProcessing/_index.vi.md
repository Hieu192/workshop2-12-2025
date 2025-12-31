---
title : "Xây dựng luồng xử lý Video"
date :  "2024-10-27" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

### Xây dựng luồng xử lý Video (Video Processing Pipeline)

Chương này tập trung vào việc xây dựng "trái tim" của hệ thống - luồng xử lý video tự động sử dụng kiến trúc Event-Driven kết hợp với AWS Step Functions.

#### Kiến trúc luồng xử lý tự động

Khi một video được tải lên S3 hoàn tất, hệ thống sẽ tự động thực hiện các bước sau:
1. **EventBridge & SQS**: Lắng nghe sự kiện từ S3 và đưa vào hàng đợi để đảm bảo tính ổn định của hệ thống.
2. **SFN Trigger**: Lambda function lấy tin nhắn từ SQS và kích hoạt luồng công việc (Workflow) trong AWS Step Functions.
3. **Step Functions Workflow**: Điều phối các bước xử lý:
    * **embedding_start**: Gọi mô hình Bedrock (Marengo) để bắt đầu quá trình trích xuất vector.
    * **embedding_check**: Kiểm tra định kỳ trạng thái xử lý job.
    * **embedding_index**: Sau khi có kết quả, lưu trữ các vector vào OpenSearch Serverless và cập nhật trạng thái cuối cùng vào DynamoDB.

![](/images/3/01.png?featherlight=false&width=50pc)

#### Các bước thực hành

1. [Tạo SQS và DLQ](3.1-CreateSQSAndDLQ/)
2. [Tạo EventBridge Rule](3.2-CreateEventBridgeRule/)
3. [Tạo Role cho Lambda](3.3-CreateRoleToLambda/)
4. [Tạo Lambda kích hoạt Step Functions](3.4-CreateLambdaSFN/)
5. [Tạo Lambda bắt đầu Embedding](3.5-CreateLambdaStart/)
6. [Tạo Lambda kiểm tra trạng thái Job](3.6-CreateLambdaCheck/)
7. [Tạo OpenSearch Serverless](3.7-CreateOpenSearch/)
8. [Tạo Lambda Index Vector](3.8-CreateLambdaIndex/)
9. [Tạo AWS Step Functions điều phối](3.9-CreateStepLambda/)

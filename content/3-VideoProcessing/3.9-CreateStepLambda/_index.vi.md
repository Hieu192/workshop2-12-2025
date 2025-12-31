---
title : "Tạo AWS Step Functions điều phối"
date :  "2024-10-27" 
weight : 9
chapter : false
pre : " <b> 3.9 </b> "
---

#### Mục tiêu
Tạo một State Machine bằng **AWS Step Functions** để điều phối quy trình xử lý video: từ việc bắt đầu tạo embedding, kiểm tra trạng thái cho đến khi đánh chỉ mục vào OpenSearch Serverless. Điều này giúp hệ thống hoạt động ổn định, tự động hóa quy trình polling và xử lý lỗi.

#### Thực hành

1. Truy cập AWS Console, tìm kiếm **Step Functions** và nhấn **Create state machine**.
   - Chọn **Create from blank**.
   - **State machine name**: `StepLambdaEmbeddingvideo`.
   - **State machine type**: Chọn **Standard**.
   - Nhấn **Continue**.
![](/images/3-9/01.png?width=50pc)

2. Trong giao diện thiết kế, chuyển sang tab **Code** và dán đoạn mã định nghĩa workflow bên dưới:

```json
{
  "Comment": "Video Embedding Pipeline",
  "StartAt": "StartEmbedding",
  "States": {
    "StartEmbedding": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:904233110564:function:embedding-start",
      "ResultPath": "$",
      "Next": "CheckIfSkipped",
      "Catch": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "ResultPath": "$.error",
          "Next": "Failed"
        }
      ]
    },
    "CheckIfSkipped": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.status",
          "StringEquals": "skipped",
          "Next": "Skipped"
        }
      ],
      "Default": "Wait30Seconds"
    },
    "Wait30Seconds": {
      "Type": "Wait",
      "Seconds": 30,
      "Next": "CheckStatus"
    },
    "CheckStatus": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:904233110564:function:embedding-check",
      "ResultPath": "$",
      "Next": "IsComplete",
      "Catch": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "ResultPath": "$.error",
          "Next": "Failed"
        }
      ]
    },
    "IsComplete": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.embedding_status",
          "StringEquals": "Completed",
          "Next": "IndexEmbeddings"
        },
        {
          "Variable": "$.embedding_status",
          "StringEquals": "Failed",
          "Next": "Failed"
        }
      ],
      "Default": "Wait30Seconds"
    },
    "IndexEmbeddings": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:904233110564:function:embedding-index",
      "ResultPath": "$",
      "Next": "Success",
      "Catch": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "ResultPath": "$.error",
          "Next": "Failed"
        }
      ]
    },
    "Success": {
      "Type": "Succeed"
    },
    "Skipped": {
      "Type": "Succeed"
    },
    "Failed": {
      "Type": "Fail",
      "Error": "EmbeddingError"
    }
  }
}
```
*Lưu ý: Thay đổi ARN của các hàm Lambda tương ứng với tài khoản của bạn.*
![](/images/3-9/02.png?width=50pc)

3. Chuyển sang tab **Config**:
   - Tại phần **Logging**, chọn Log level là **ALL** để hỗ trợ việc theo dõi và gỡ lỗi sau này.
   - Nhấn **Create** để hoàn tất việc tạo State Machine.
![](/images/3-9/03.png?width=50pc)

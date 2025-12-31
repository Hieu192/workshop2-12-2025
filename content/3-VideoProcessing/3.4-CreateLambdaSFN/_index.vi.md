---
title : "Tạo lambda sfn-trigger"
date :  "2024-10-27" 
weight : 4
chapter : false
pre : " <b> 3.4 </b> "
---

#### Mục tiêu
Tạo hàm Lambda mang tên **sfn-trigger** đóng vai trò là cầu nối giữa SQS và Step Functions. Hàm này sẽ lấy thông tin từ hàng đợi SQS khi có video mới được upload lên S3 và kích hoạt quy trình (Step Function) để xử lý video đó.

#### Thực hành

1. Truy cập dịch vụ **Lambda** trong AWS Console.
   - Chọn **Functions** từ menu bên trái.
   - Nhấn **Create function**.
![](/images/3-4/01.png?width=50pc)

2. Cấu hình các thông số cơ bản cho hàm Lambda:
   - Chọn **Author from scratch**.
   - **Function name**: `sfn-trigger`.
   - **Runtime**: `Python 3.14` (hoặc phiên bản mới nhất có sẵn).
   - **Architecture**: `x86_64`.
   - **Permissions**: Chọn **Use an existing role** và tìm role đã tạo ở bước trước (ví dụ: `lambda-video-embedding-role`).
   - Nhấn **Create function**.
![](/images/3-4/02.png?width=50pc)

3. Tại tab **Code**, thay thế mã nguồn mặc định bằng đoạn code dưới đây để xử lý sự kiện từ SQS và kích hoạt Step Function:

```python
import os
import json
import boto3
from urllib.parse import unquote_plus

STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN", "")
REGION = os.environ.get("AWS_REGION", "us-east-1")

sfn = boto3.client("stepfunctions", region_name=REGION)


def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    if not STATE_MACHINE_ARN:
        raise ValueError("STATE_MACHINE_ARN not set")
    
    results = []
    failed = []
    
    for record in event.get("Records", []):
        message_id = record.get("messageId", "unknown")
        
        try:
            body = json.loads(record.get("body", "{}"))
            
            # EventBridge format
            if "detail" in body:
                s3_bucket = body["detail"]["bucket"]["name"]
                s3_key = unquote_plus(body["detail"]["object"]["key"])
            else:
                print(f"Unknown format: {body}")
                continue
            
            # Extract video_id: videos/{video_id}/filename.mp4
            parts = s3_key.split("/")
            if len(parts) < 3 or parts[0] != "videos":
                print(f"Skip non-video: {s3_key}")
                continue
            
            video_id = parts[1]
            video_s3_uri = f"s3://{s3_bucket}/{s3_key}"
            
            print(f"Starting SFN for: {video_id}")
            
            response = sfn.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                name=f"video-{video_id}-{message_id[:8]}",
                input=json.dumps({
                    "video_id": video_id,
                    "video_s3_uri": video_s3_uri
                })
            )
            
            print(f"Started: {response['executionArn']}")
            results.append({"messageId": message_id})
            
        except Exception as e:
            print(f"Error: {e}")
            failed.append({"itemIdentifier": message_id})
    
    return {"batchItemFailures": failed}
```
   - Sau khi dán code, nhấn **Deploy** để lưu thay đổi.
![](/images/3-4/03.png?width=50pc)

4. Chuyển sang tab **Configuration** để điều chỉnh cấu hình hệ thống:
   - Chọn **General configuration** -> **Edit**.
![](/images/3-4/04.png?width=50pc)

5. Thiết lập thông số vận hành:
   - **Memory**: Tăng lên `256 MB` để đảm bảo tốc độ xử lý.
   - **Timeout**: Thiết lập là `30 sec` (30 giây).
   - Nhấn **Save**.
![](/images/3-4/05.png?width=50pc)

6. Quay lại phần **Function overview**, nhấn **Add trigger** để kết nối với SQS.
![](/images/3-4/06.png?width=50pc)

7. Cấu hình Trigger SQS:
   - Chọn **SQS** từ danh sách nguồn.
   - **SQS queue**: Chọn hàng đợi đã tạo (ví dụ: `video-embedding-queue`).
   - **Batch size**: Thiết lập là `1` (xử lý từng tin nhắn một).
   - **Report batch item failures**: Tích chọn (giúp quản lý lỗi tin nhắn tốt hơn).
   - Nhấn **Add**.
![](/images/3-4/07.png?width=50pc)

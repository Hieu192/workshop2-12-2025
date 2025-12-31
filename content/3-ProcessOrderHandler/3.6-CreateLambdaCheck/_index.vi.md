---
title : "Tạo lambda kiểm tra trạng thái embedding"
date :  "2024-10-27" 
weight : 6
chapter : false
pre : " <b> 3.6 </b> "
---

#### Mục tiêu
Tạo hàm Lambda mang tên **embedding-check** để truy vấn trạng thái xử lý của tiến trình embedding trên Amazon Bedrock. Hàm này sẽ được Step Function gọi lặp lại (loop) cho đến khi tiến trình hoàn tất.

#### Thực hành

1. Truy cập dịch vụ **Lambda** trong AWS Console.
   - Nhấn **Create function**.
   - **Function name**: `embedding-check`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Chọn **Use an existing role** và chọn `lambda-video-embedding-role`.
   - Nhấn **Create function**.
![](/images/3-6/01.png?width=50pc)

2. Tại tab **Code**, nhập mã nguồn sau:

```python
import os
import json
import boto3

REGION = os.environ.get("AWS_REGION", "us-east-1")
bedrock = boto3.client("bedrock-runtime", region_name=REGION)


def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    invocation_arn = event.get("invocation_arn")
    if not invocation_arn:
        raise ValueError("Missing invocation_arn")
    
    response = bedrock.get_async_invoke(invocationArn=invocation_arn)
    status = response["status"]
    
    print(f"Embedding status: {status}")
    
    return {**event, "embedding_status": status}
```
   - Nhấn **Deploy** để lưu mã nguồn.
![](/images/3-6/02.png?width=50pc)

3. Chuyển sang tab **Configuration** -> **General configuration**:
   - Nhấn **Edit**.
   - **Memory**: `256 MB`.
   - **Timeout**: `30 sec`.
   - Nhấn **Save**.
![](/images/3-6/03.png?width=50pc)

---
title : "Tạo lambda bắt đầu embedding video"
date :  "2024-10-27" 
weight : 5
chapter : false
pre : " <b> 3.5 </b> "
---

#### Mục tiêu
Tạo hàm Lambda mang tên **embedding-start** để gửi yêu cầu xử lý video đến mô hình TwelveLabs Marengo trên Amazon Bedrock. Đây là bước khởi đầu của quy trình trích xuất đặc trưng video (embedding) giúp việc tìm kiếm nội dung video sau này trở nên hiệu quả.

#### Thực hành

1. Truy cập dịch vụ **Lambda** trong AWS Console.
   - Nhấn **Create function**.
   - **Function name**: `embedding-start`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Chọn **Use an existing role** và chọn `lambda-video-embedding-role`.
   - Nhấn **Create function**.
![](/images/3-5/01.png?width=50pc)

2. Tại tab **Code**, nhập mã nguồn sau:

```python
import os
import json
import uuid
import time
import boto3
from datetime import datetime

TABLE_NAME = os.environ.get("TABLE_NAME", "video-analysis")
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "sl-video-analysis-videos-hieu")
REGION = os.environ.get("AWS_REGION", "us-east-1")
MODEL_ID = os.environ.get("MODEL_ID", "twelvelabs.marengo-embed-3-0-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)
sts = boto3.client("sts")


def get_account_id():
    return sts.get_caller_identity()["Account"]


def get_video_metadata(video_id):
    response = table.get_item(Key={"PK": f"vid#{video_id}", "SK": "METADATA"})
    return response.get("Item")


def update_status(video_id, status, **kwargs):
    timestamp = datetime.utcnow().isoformat() + "Z"
    update_expr = "SET embedding_status = :status, embedding_updated_at = :ts"
    expr_values = {":status": status, ":ts": timestamp}
    
    for key, value in kwargs.items():
        update_expr += f", {key} = :{key}"
        expr_values[f":{key}"] = value
    
    table.update_item(
        Key={"PK": f"vid#{video_id}", "SK": "METADATA"},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )


def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    start_time = int(time.time())
    
    video_id = event.get("video_id")
    video_s3_uri = event.get("video_s3_uri")
    
    if not video_id or not video_s3_uri:
        raise ValueError("Missing video_id or video_s3_uri")
    
    # Verify video exists
    metadata = get_video_metadata(video_id)
    if not metadata:
        return {"status": "skipped", "reason": "video_not_found", "video_id": video_id}
    
    # Update status
    update_status(video_id, "processing")
    
    # Start async embedding
    embedding_id = str(uuid.uuid4())
    s3_output_prefix = f"embeddings/videos/{video_id}/{embedding_id}"
    s3_output_uri = f"s3://{S3_BUCKET}/{s3_output_prefix}"
    
    print(f"Starting embedding: {video_s3_uri}")
    print(f"Output: {s3_output_uri}")
    
    response = bedrock.start_async_invoke(
        modelId=MODEL_ID,
        modelInput={
            "inputType": "video",
            "video": {
                "mediaSource": {
                    "s3Location": {
                        "uri": video_s3_uri,
                        "bucketOwner": get_account_id()
                    }
                }
            }
        },
        outputDataConfig={
            "s3OutputDataConfig": {"s3Uri": s3_output_uri}
        }
    )
    
    invocation_arn = response["invocationArn"]
    print(f"Invocation ARN: {invocation_arn}")
    
    update_status(video_id, "waiting",
        embedding_invocation_arn=invocation_arn,
        embedding_s3_prefix=s3_output_prefix
    )
    
    return {
        "status": "started",
        "video_id": video_id,
        "video_s3_uri": video_s3_uri,
        "invocation_arn": invocation_arn,
        "embedding_id": embedding_id,
        "s3_output_prefix": s3_output_prefix,
        "s3_output_uri": s3_output_uri,
        "start_time": start_time
    }
```
   - Nhấn **Deploy** để lưu mã nguồn.
![](/images/3-5/02.png?width=50pc)

3. Chuyển sang tab **Configuration** -> **Environment variables**:
   - Nhấn **Edit** và thêm các biến sau:
     - `MODEL_ID`: `twelvelabs.marengo-embed-3-0-v1:0`
     - `S3_BUCKET_NAME`: (Tên bucket của bạn)
     - `TABLE_NAME`: `video-analysis`
   - Nhấn **Save**.
![](/images/3-5/03.png?width=50pc)

4. Chuyển sang **General configuration**:
   - Nhấn **Edit**.
![](/images/3-5/04.png?width=50pc)

5. Cập nhật thông số:
   - **Memory**: `512 MB`.
   - **Timeout**: `1 min 0 sec` (1 phút).
   - Nhấn **Save**.
![](/images/3-5/05.png?width=50pc)

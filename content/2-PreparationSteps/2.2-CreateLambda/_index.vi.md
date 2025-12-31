---
title : "Tạo lambda upload video"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 2.2 </b> "
---


Chúng ta cần tạo Lambda function và thay đổi role lambda để truy cập DynamoDB và các dịch vụ AWS khác.

#### Tạo gàm lambda để xử lý tạo presigned URL cho video

1. Truy cập AWS Console và điều hướng đến dịch vụ **Lambda** trong AWS Console.
    - Từ slider bên trái chọn **Functions** và click **Create function**.

![](/images/2-2/01.png?featherlight=false&width=50pc)

2. Cấu hình function:
   - Chọn **Author from scratch**
   - Function name: **`video_upload`**
   - Runtime: **Python 3.14**
   - Architecture: **x86_64**
   - Click **Create function**.

![](/images/2-2/02.png?featherlight=false&width=50pc)

3. Thay thế code mặc định bằng đoạn code bên dưới và Click **Deploy**.:
![](/images/2-2/03.png?featherlight=false&width=50pc)

````python
import os
import json
import uuid
import boto3
from datetime import datetime
from typing import Dict, Any

# Environment variables
VIDEO_BUCKET = os.environ.get("VIDEO_BUCKET", "sl-video-analysis-videos-hieu")
TABLE_NAME = os.environ.get("TABLE_NAME", "video-analysis")
REGION = os.environ.get("AWS_REGION", "us-east-1")
PRESIGNED_URL_EXPIRY = int(os.environ.get("PRESIGNED_URL_EXPIRY", "3600"))

# Initialize clients
s3_client = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def create_response(status_code: int, body: Dict[str, Any]) -> Dict:
    """Create API Gateway response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }


def lambda_handler(event, context):

    print(f"Event: {json.dumps(event)}")
    
    # Handle OPTIONS for CORS
    if event.get("httpMethod") == "OPTIONS":
        return create_response(200, {"message": "OK"})
    
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))
        filename = body.get("filename")
        
        if not filename:
            return create_response(400, {
                "error": "Missing required field: filename"
            })
        
        # Validate file extension
        allowed_extensions = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in allowed_extensions:
            return create_response(400, {
                "error": f"Invalid file type. Allowed: {allowed_extensions}"
            })
        
        # Generate unique video ID
        video_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # S3 key for the video
        s3_key = f"videos/{video_id}/{filename}"
        s3_uri = f"s3://{VIDEO_BUCKET}/{s3_key}"
        
        # Determine content type
        content_type_map = {
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".mkv": "video/x-matroska",
            ".webm": "video/webm"
        }
        content_type = content_type_map.get(file_ext, "video/mp4")
        
        # Generate presigned URL for upload (PUT)
        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": VIDEO_BUCKET,
                "Key": s3_key,
                "ContentType": content_type
            },
            ExpiresIn=PRESIGNED_URL_EXPIRY
        )
        
        # Generate presigned URL for viewing (GET)
        video_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": VIDEO_BUCKET,
                "Key": s3_key
            },
            ExpiresIn=PRESIGNED_URL_EXPIRY
        )
        
        metadata_item = {
            # Primary Keys
            "PK": f"vid#{video_id}",           # Partition Key
            "SK": "METADATA",                   # Sort Key
            
            # Video attributes
            "video_id": video_id,
            "filename": filename,
            "s3_uri": s3_uri,
            "s3_bucket": VIDEO_BUCKET,
            "s3_key": s3_key,
            "content_type": content_type,
            "uploaded_at": timestamp,
            
            # Status tracking
            "status": "pending_upload",
            "embedding_status": "pending",
            "analysis_status": "pending",
            
            # GSI1 for querying by status
            "GSI1PK": "STATUS#pending_upload",
            "GSI1SK": timestamp
        }
        
        table.put_item(Item=metadata_item)
        print(f"Saved metadata for video_id: {video_id}")
        
        return create_response(200, {
            "video_id": video_id,
            "filename": filename,
            "upload_url": upload_url,
            "video_url": video_url,
            "s3_uri": s3_uri,
            "expires_in": PRESIGNED_URL_EXPIRY,
            "message": "Upload video using PUT request to upload_url"
        })
        
    except json.JSONDecodeError:
        return create_response(400, {"error": "Invalid JSON body"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, {"error": str(e)})
````

4. Từ Tab **Configuration** chuyển sang Tab **Environment variables** và nhấn **Edit** nhập các biến môi trường như ảnh bên dưới.
    - TABLE_NAME: **`video-analysis`**
    - VIDEO_BUCKET: **`sl-video-analysis-videos-hieu`**
![](/images/2-2/04.png?featherlight=false&width=50pc)

5. Tiếp theo từ Tab **Configuration** chuyển sang Tab **Permissions** và nhấn **Role name** như bên dưới ảnh
![](/images/2-2/05.png?featherlight=false&width=50pc)

6. Từ giao diện Role, nhấn **Add permissions** và chọn **Attach policies** như ảnh bên dưới.
![](/images/2-2/06.png?featherlight=false&width=50pc)

7. Chọn **AmazonS3FullAccess** và **AmazonDynamoDBFullAccess** và nhấn **Add permissions**.
![](/images/2-2/07.png?featherlight=false&width=50pc)
![](/images/2-2/08.png?featherlight=false&width=50pc)



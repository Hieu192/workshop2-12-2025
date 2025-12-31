---
title : "Create Lambda to Start Video Embedding"
date :  "2024-10-27" 
weight : 5
chapter : false
pre : " <b> 3.5 </b> "
---

#### Objective
Create a Lambda function named **embedding-start** to send video processing requests to the TwelveLabs Marengo model on Amazon Bedrock. This is the starting step of the video feature extraction (embedding) process that makes subsequent video content search more efficient.

#### Practice

1. Access the **Lambda** service in AWS Console.
   - Click **Create function**.
   - **Function name**: `embedding-start`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Select **Use an existing role** and choose `lambda-video-embedding-role`.
   - Click **Create function**.
![](/images/3-5/01.png?width=50pc)

2. In the **Code** tab, enter the following source code:

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
   - Click **Deploy** to save the source code.
![](/images/3-5/02.png?width=50pc)

3. Switch to the **Configuration** tab -> **Environment variables**:
   - Click **Edit** and add the following variables:
     - `MODEL_ID`: `twelvelabs.marengo-embed-3-0-v1:0`
     - `S3_BUCKET_NAME`: (Your bucket name)
     - `TABLE_NAME`: `video-analysis`
   - Click **Save**.
![](/images/3-5/03.png?width=50pc)

4. Switch to **General configuration**:
   - Click **Edit**.
![](/images/3-5/04.png?width=50pc)

5. Update parameters:
   - **Memory**: `512 MB`.
   - **Timeout**: `1 min 0 sec` (1 minute).
   - Click **Save**.
![](/images/3-5/05.png?width=50pc)
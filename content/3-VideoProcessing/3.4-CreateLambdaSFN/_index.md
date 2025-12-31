---
title : "Create Lambda sfn-trigger"
date :  "2024-10-27" 
weight : 4
chapter : false
pre : " <b> 3.4 </b> "
---

#### Objective
Create a Lambda function named **sfn-trigger** that serves as a bridge between SQS and Step Functions. This function will retrieve information from the SQS queue when a new video is uploaded to S3 and trigger the Step Function workflow to process that video.

#### Practice

1. Access the **Lambda** service in AWS Console.
   - Select **Functions** from the left menu.
   - Click **Create function**.
![](/images/3-4/01.png?width=50pc)

2. Configure the basic parameters for the Lambda function:
   - Select **Author from scratch**.
   - **Function name**: `sfn-trigger`.
   - **Runtime**: `Python 3.14` (or the latest available version).
   - **Architecture**: `x86_64`.
   - **Permissions**: Select **Use an existing role** and find the role created in the previous step (e.g., `lambda-video-embedding-role`).
   - Click **Create function**.
![](/images/3-4/02.png?width=50pc)

3. In the **Code** tab, replace the default source code with the code below to handle events from SQS and trigger Step Function:

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
   - After pasting the code, click **Deploy** to save changes.
![](/images/3-4/03.png?width=50pc)

4. Switch to the **Configuration** tab to adjust system configuration:
   - Select **General configuration** -> **Edit**.
![](/images/3-4/04.png?width=50pc)

5. Set operational parameters:
   - **Memory**: Increase to `256 MB` to ensure processing speed.
   - **Timeout**: Set to `30 sec` (30 seconds).
   - Click **Save**.
![](/images/3-4/05.png?width=50pc)

6. Return to **Function overview**, click **Add trigger** to connect with SQS.
![](/images/3-4/06.png?width=50pc)

7. Configure SQS Trigger:
   - Select **SQS** from the source list.
   - **SQS queue**: Select the queue created earlier (e.g., `video-embedding-queue`).
   - **Batch size**: Set to `1` (process one message at a time).
   - **Report batch item failures**: Check (helps manage message errors better).
   - Click **Add**.
![](/images/3-4/07.png?width=50pc)
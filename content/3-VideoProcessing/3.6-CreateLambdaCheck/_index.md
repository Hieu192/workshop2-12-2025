---
title : "Create Lambda to Check Embedding Status"
date :  "2024-10-27" 
weight : 6
chapter : false
pre : " <b> 3.6 </b> "
---

#### Objective
Create a Lambda function named **embedding-check** to query the processing status of the embedding process on Amazon Bedrock. This function will be called repeatedly (looped) by Step Function until the process is complete.

#### Practice

1. Access the **Lambda** service in AWS Console.
   - Click **Create function**.
   - **Function name**: `embedding-check`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Select **Use an existing role** and choose `lambda-video-embedding-role`.
   - Click **Create function**.
![](/images/3-6/01.png?width=50pc)

2. In the **Code** tab, enter the following source code:

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
   - Click **Deploy** to save the source code.
![](/images/3-6/02.png?width=50pc)

3. Switch to the **Configuration** tab -> **General configuration**:
   - Click **Edit**.
   - **Memory**: `256 MB`.
   - **Timeout**: `30 sec`.
   - Click **Save**.
![](/images/3-6/03.png?width=50pc)
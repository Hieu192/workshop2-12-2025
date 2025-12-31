---
title : "Create AWS Step Functions Orchestration"
date :  "2024-10-27" 
weight : 9
chapter : false
pre : " <b> 3.9 </b> "
---

#### Objective
Create a State Machine using **AWS Step Functions** to orchestrate the video processing workflow: from starting embedding creation, checking status until indexing into OpenSearch Serverless. This helps the system operate stably, automating the polling process and error handling.

#### Practice

1. Access AWS Console, search for **Step Functions** and click **Create state machine**.
   - Select **Create from blank**.
   - **State machine name**: `StepLambdaEmbeddingvideo`.
   - **State machine type**: Select **Standard**.
   - Click **Continue**.
![](/images/3-9/01.png?width=50pc)

2. In the design interface, switch to the **Code** tab and paste the workflow definition code below:

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
*Note: Change the ARN of Lambda functions corresponding to your account.*
![](/images/3-9/02.png?width=50pc)

3. Switch to the **Config** tab:
   - In the **Logging** section, select Log level as **ALL** to support tracking and debugging later.
   - Click **Create** to complete the State Machine creation.
![](/images/3-9/03.png?width=50pc)
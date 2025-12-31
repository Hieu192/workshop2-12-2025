---
title : "Building Video Processing Pipeline"
date :  "2024-10-27" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

### Building Video Processing Pipeline

This chapter focuses on building the "heart" of the system - the automated video processing pipeline using Event-Driven architecture combined with AWS Step Functions.

#### Automated Processing Architecture

When a video is uploaded to S3, the system automatically performs the following steps:
1. **EventBridge & SQS**: Listens for events from S3 and queues them to ensure system stability.
2. **SFN Trigger**: Lambda function retrieves messages from SQS and triggers the workflow in AWS Step Functions.
3. **Step Functions Workflow**: Orchestrates the processing steps:
    * **embedding_start**: Calls the Bedrock model (Marengo) to start the vector extraction process.
    * **embedding_check**: Periodically checks the job processing status.
    * **embedding_index**: After obtaining results, stores vectors in OpenSearch Serverless and updates the final status in DynamoDB.

![](/images/3/01.png?featherlight=false&width=50pc)

#### Practice Steps

1. [Create SQS and DLQ](3.1-CreateSQSAndDLQ/)
2. [Create EventBridge Rule](3.2-CreateEventBridgeRule/)
3. [Create Role for Lambda](3.3-CreateRoleToLambda/)
4. [Create Lambda to Trigger Step Functions](3.4-CreateLambdaSFN/)
5. [Create Lambda to Start Embedding](3.5-CreateLambdaStart/)
6. [Create Lambda to Check Job Status](3.6-CreateLambdaCheck/)
7. [Create OpenSearch Serverless](3.7-CreateOpenSearch/)
8. [Create Lambda Index Vector](3.8-CreateLambdaIndex/)
9. [Create AWS Step Functions Orchestration](3.9-CreateStepLambda/)
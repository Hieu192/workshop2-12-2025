---
title : "Introduction"
date :  "2024-10-27" 
weight : 1 
chapter : false
pre : " <b> 1. </b> "
---

### Introduction to Video Analysis Architecture on AWS

This architecture is built on the **Event-Driven** and **Serverless** model. The main goal is to automate the video processing workflow from upload to natural language searchability through Vector Search techniques (using **Amazon Bedrock** and **OpenSearch**).

![](/images/1/image.png?featherlight=false&width=50pc)

### Detailed Workflow

#### 1. Upload and Storage (Ingestion Phase)
Admin sends a video upload request through **API Gateway**.

Lambda **upload_video** receives the request and performs:
- Creates a presigned URL for the video
- Stores the original video file in **S3 (Video Storage)** via the presigned URL.
- Saves metadata information (name, size, creation date...) to **DynamoDB**.

#### 2. Processing Trigger (Trigger Phase)
- When a video is saved to **S3**, an event is sent to **Amazon EventBridge**.
- **EventBridge** forwards the notification to **SQS (Simple Queue Service)** to ensure stability and scalability (buffering).
- Lambda **sfn_trigger** consumes messages from SQS and triggers the **AWS Step Functions** workflow.

#### 3. Embedding Extraction and Indexing (Processing Phase)
This is the core of the system, within the **Step Functions workflow**:
1. **embedding_start**: This Lambda calls **Amazon Bedrock** (using models like Titan Multimodal Embeddings) asynchronously to analyze video content and convert it into numerical vectors (embeddings).
2. **embedding_check**: Since video processing can take time and is asynchronous, this step checks the completion status of the AI process by using a loop to call the **embedding_start** lambda until results are available.
3. **embedding_index**: After obtaining embedding results, this Lambda pushes vector data to **OpenSearch Serverless** for later searching. It also updates the processing status in **DynamoDB**.

#### 4. Search (Search Phase)
User sends a query (e.g., "Find someone smoking in a room") via **API Gateway**.

Lambda **search_video** performs:
- Calls **Amazon Bedrock** to convert the user's text query into a vector.
- Performs a **Vector Search** query on **OpenSearch Serverless** to find videos with the most similar content.
- Retrieves additional details from **DynamoDB** and returns results (including video link from S3) to the user.

### Main Components and Their Roles
- **S3**: Stores raw data (Video) and video embeddings (Vector).
- **DynamoDB**: Stores structured data (Metadata, processing status).
- **Step Functions**: Orchestrates complex processing steps, ensuring consistency if errors occur.
- **Amazon Bedrock**: Provides machine learning models (Foundation Models) for AI processing without managing infrastructure.
- **OpenSearch Serverless**: Vector database enabling fast Semantic Search.
- **CloudWatch**: Monitors logs and performance of the entire system.

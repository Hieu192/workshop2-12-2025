---
title : "Building Video Upload Mechanism"
date :  "2024-10-27" 
weight : 2 
chapter : false
pre : " <b> 2. </b> "
---

### Building Video Upload Mechanism

In this chapter, we will build the first components of the system to allow secure video uploads and manage video information.

#### Video Upload Process

The system uses **Presigned URL** technique to allow users to upload files directly to S3 without going through an intermediate server, optimizing performance:
1. **Request**: Admin sends a video upload request through API Gateway.
2. **Authorize**: Lambda function `upload_video` is triggered to create a time-limited upload link (Presigned URL).
3. **Metadata**: At the same time, basic video information is recorded in **DynamoDB** table with initial status.
4. **Upload**: User uses the provided link to upload the video file directly to **S3 Bucket**.

![](/images/2/image.png?featherlight=false&width=50pc)

#### Practice Steps

1. [Create DynamoDB Storage Table](2.1-CreateTableDynamo/)
2. [Create Lambda Function for Upload](2.2-CreateLambda/)
3. [Configure API Gateway for Upload](2.3-CreateAPIGateway/)
4. [Test Upload API Flow](2.4-TestAPIGateway/)
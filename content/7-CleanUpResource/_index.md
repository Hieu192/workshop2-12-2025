---
title : "Clean Up Resources"
date :  "2024-10-27" 
weight : 7
chapter : false
pre : " <b> 7. </b> "
---

#### Clean Up Resources
To avoid unexpected costs, we will delete the resources created in this workshop in the following order:

1. **Delete API Gateway**:
   - Access the **API Gateway** service.
   - Select API `video-analysis-api` and click **Delete**.

2. **Delete Step Functions**:
   - Access the **Step Functions** service.
   - Select State Machine `StepLambdaEmbeddingvideo` and click **Delete**.

3. **Delete Lambda Functions**:
   - Access the **Lambda** service.
   - Delete functions: `upload-video`, `sfn-trigger`, `embedding-start`, `embedding-check`, `embedding-index`, `video-search`.

4. **Delete SQS & EventBridge**:
   - Access the **SQS** service, delete `video-processing-queue` and `video-processing-dlq`.
   - Access **EventBridge**, select the Rule listening to S3 events and delete.

5. **Delete OpenSearch Serverless**:
   - Access **Amazon OpenSearch Service**, section **Serverless**.
   - Delete collection `video-embeddings`.

6. **Delete DynamoDB**:
   - Access the **DynamoDB** service.
   - Select table `video-analysis` and click **Delete table**.

7. **Delete S3 Bucket**:
   - Access the **S3** service.
   - Empty and delete the Bucket containing videos and embedding results.

8. **Delete IAM Role & Policy**:
   - Access the **IAM** service, delete Role `lambda-video-embedding-role` and associated Policies.

![](/images/7/10.png?width=50pc)
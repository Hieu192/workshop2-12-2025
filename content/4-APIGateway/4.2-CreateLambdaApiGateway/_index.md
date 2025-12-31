---
title : "Configure API Gateway for Video Search"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 4.2 </b> "
---

#### Objective
Set up Amazon API Gateway to provide a public endpoint, allowing frontend applications or tools like Postman to send search requests to the `video-search` Lambda function.

#### Practice

1. Access the **API Gateway** service in AWS Console.
   - Select the API you created (e.g., `video-analysis-api`).
   - In the **Resources** section, click **Create resource**.
![](/images/4-2/01.png?width=50pc)

2. Configure the new Resource:
   - **Resource path**: `/videos`.
   - **Resource name**: `video-search`.
   - Enable **CORS (Cross-Origin Resource Sharing)**.
   - Click **Create resource**.
![](/images/4-2/02.png?width=50pc)
![](/images/4-2/03.png?width=50pc)

3. Create Method for the resource:
   - Select resource `/video-search`.
   - Click **Create method**.
   - **Method type**: `POST`.
   - **Integration type**: `Lambda function`.
   - Enable **Lambda proxy integration**.
   - **Lambda function**: Select function `video-search` (us-east-1).
![](/images/4-2/05.png?width=50pc)
![](/images/4-2/06.png?width=50pc)

4. Confirm and save Method:
   - Click **Create method**. The system will automatically grant permissions for API Gateway to call your Lambda function.
![](/images/4-2/07.png?width=50pc)

5. Deploy API:
   - Click **Deploy API**.
   - **Stage**: Select `prod` (or create new if not exists).
   - Click **Deploy**.
![](/images/4-2/08.png?width=50pc)

6. After deploying, copy the **Invoke URL** of the `prod` stage. This is the API address we will use for testing in the next step.
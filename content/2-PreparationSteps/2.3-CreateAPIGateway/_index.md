---
title : "Create API Gateway"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 2.3 </b> "
---


In this step, we will create API Gateway to call the Lambda function.

### Create API Gateway to Call Lambda

1. Access AWS Console and navigate to the **API Gateway** service in AWS Console.
    - From the left sidebar, select **APIs** and click **Create API**.
![](/images/2-3/01.png?featherlight=false&width=50pc)

2. From the **Create API** interface, scroll down to the **Rest API** section, select **Build**.
![](/images/2-3/02.png?featherlight=false&width=50pc)

3. Configure the API:
   - Select **New API**
   - API name: **`video-analysis-api`**
   - API endpoint type: **Regional**
   - Click **Create API**.
![](/images/2-3/03.png?featherlight=false&width=50pc)


4. Create POST method for the endpoint:
    - Method type: **POST**
    - Integration type: **Lambda Function**
    - Lambda proxy integration: **checked**
    - Lambda function: **video_upload**
    - Click **Create Method**
![](/images/2-3/04.png?featherlight=false&width=50pc)

5. Enable CORS.
![](/images/2-3/05.png?featherlight=false&width=50pc)   

6. Click on / and click **Deploy API**.
![](/images/2-3/06.png?featherlight=false&width=50pc)

7. Deploy the API
    - Stage: *New stage*
    - Stage name: **`dev`**
    - Click **Deploy**
![](/images/2-3/07.png?featherlight=false&width=50pc)
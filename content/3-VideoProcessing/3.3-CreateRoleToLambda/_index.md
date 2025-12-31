---
title : "Create Role for Lambda"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 3.3 </b> "
---


#### Objective
.

#### Practice
1. Access AWS Console, enter **IAM** and navigate to the **Identity and Access Management** service
   - In the **Identity and Access Management** interface, select **Roles** on the left sidebar and click **Create role**
![](/images/3-3/01.png?width=50pc)

2. In the **Create role** interface, select **Lambda** and click **Next: Permissions**
   - Trusted entity type: select **AWS service**
   - Service: select **Lambda**
   - Use case: select **Lambda**
   - Click **Next**
![](/images/3-3/02.png?width=50pc)

3. In the **Add permissions** interface, select **AWSLambdaBasicExecutionRole**, **AWSStepFunctionsFullAccess**, **AmazonS3FullAccess**, **AmazonSQSFullAccess**, **DynamoDBFullAccess** and click **Create Role**
![](/images/3-3/03.png?width=50pc)
![](/images/3-3/04.png?width=50pc)
![](/images/3-3/05.png?width=50pc)

4. In the Role interface, continue to add **permissions**
   - Select **AmazonBedrockFullAccess**
   - Click **Add permissions**
![](/images/3-3/06.png?width=50pc)
![](/images/3-3/07.png?width=50pc)
![](/images/3-3/08.png?width=50pc)

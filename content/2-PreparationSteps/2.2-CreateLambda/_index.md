---
title : "Create IAM Roles"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 2.2 </b> "
---

We need to create IAM roles for Lambda functions to access DynamoDB and other AWS services.

### Step 1: Create Custom Policies

#### Create AllowReadProductTablePolicy1

1. Access AWS Console and navigate to the **IAM** service in AWS Console.

![](/images/2-2/01.png?featherlight=false&width=50pc)

2. Click **Policies** in the left sidebar, then **Create policy**.

![](/images/2-2/02.png?featherlight=false&width=50pc)

3. Select the **JSON** tab and paste the following policy:
![](/images/2-2/03.png?featherlight=false&width=50pc)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:Scan"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/ProductTable"
        }
    ]
}
```

4. Click **Next**.
![](/images/2-2/04.png?featherlight=false&width=50pc)

5. Next, we enter as below
   - Policy name: **`AllowReadProductTablePolicy1`**
   - Click **Create policy**
![](/images/2-2/05.png?featherlight=false&width=50pc)

6. Click **Create policy**.

#### Create AllowReadWriteBasketTablePolicy1

1. Similar to above, click **Policies** in the left sidebar, then **Create policy**.

2. Select the **JSON** tab and paste the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/BasketTable"
        }
    ]
}
```

3. Click **Next**.

4. Next, we enter as below
   - Policy name: **`AllowReadWriteBasketTablePolicy1`**
   - Click **Create policy**

![](/images/2-2/06.png?featherlight=false&width=50pc)

5. Click **Create policy**.

#### Create AllowWriteOrderingTablePolicy1

1. Similar to above, click **Policies** in the left sidebar, then **Create policy**.

2. Select the **JSON** tab and paste the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
               "dynamodb:PutItem",
               "dynamodb:Scan",
               "dynamodb:Query"
            ],
            "Resource": [
               "arn:aws:dynamodb:*:*:table/OrderingTable",
            	"arn:aws:dynamodb:*:*:table/OrderingTable/index/UserOrdersIndex"
            ]
        }
    ]
}
```

3. Click **Next**.

4. Next, we enter as below
   - Policy name: **`AllowWriteOrderingTablePolicy1`**
   - Click **Create policy**

![](/images/2-2/07.png?featherlight=false&width=50pc)

5. Click **Create policy**.

#### Create AllowPutEventsToDefaultBusPolicy1

1. Similar to above, click **Policies** in the left sidebar, then **Create policy**.

2. Select the **JSON** tab and paste the following policy:

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "events:PutEvents",
			"Resource": "arn:aws:events:*:*:event-bus/default"
		}
	]
}
```

3. Click **Next**.

4. Next, we enter as below
   - Policy name: **`AllowPutEventsToDefaultBusPolicy1`**
   - Click **Create policy**

![](/images/2-2/08.png?featherlight=false&width=50pc)

5. Click **Create policy**.

### Step 2: Create IAM Roles 

#### Create ProductLambdaRole

1. Click **Roles** in the left sidebar, then **Create role**.
![](/images/2-2/14.png?featherlight=false&width=50pc)

2. Select **AWS service** and choose **Lambda**. Click **Next**.
![](/images/2-2/09.png?featherlight=false&width=50pc)

4. Search and select policies: **`AllowReadProductTablePolicy1`**, **`AWSLambdaBasicExecutionRole`** and select **Next**
![](/images/2-2/10.png?featherlight=false&width=50pc)

5. Role name: **`ProductLambdaRole1`**
![](/images/2-2/11.png?featherlight=false&width=50pc)
7. Click **Create role**.

#### Create BasketLambdaRole

1. Repeat the same steps with:
   - Role name: **`BasketLambdaRole1`**
   - Attach policies: **`AllowPutEventsToDefaultBusPolicy1`**, **`AllowReadWriteBasketTablePolicy1`**, **`AWSLambdaBasicExecutionRole`**
![](/images/2-2/12.png?featherlight=false&width=50pc)

#### Create OrderingLambdaRole

1. Repeat the same steps with:
   - Role name: **`OrderingLambdaRole1`**
   - Attach policies: **`AllowWriteOrderingTablePolicy1`**, **`AWSLambdaBasicExecutionRole`**, **`AWSLambdaSQSQueueExecutionRole`**
![](/images/2-2/13.png?featherlight=false&width=50pc)

### Verification

After completion, you will have:
- 4 custom policies with minimal required permissions
- 3 corresponding IAM roles for each Lambda function
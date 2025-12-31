---
title : "Test API on Postman"
date :  "2024-10-27" 
weight : 2 
chapter : false
pre : " <b> 4.2 </b> "
---

#### What is Postman
Postman is a tool that supports sending and testing APIs visually, helping developers send requests to endpoints (like API Gateway) and view responses from the server, serving for API testing and debugging during microservice system development.

#### Practice API testing
1. Create data in productTable on DynamoDB for testing
![connect ec2](/images/4-2/01.png?width=50pc)
    - Click **Create item**
![connect ec2](/images/4-2/02.png?width=50pc)
    - Click **Json view**
![connect ec2](/images/4-2/03.png?width=50pc)
    - Click **View DynamoDB Json**
    ```json
    {
        "productId": "p-001",
        "brand": "Kim Đồng",
        "name": "Conan tập 1",
        "price": 250000
    }
    ```
![connect ec2](/images/4-2/04.png?width=50pc)
    - Similarly create 5-10 samples (Or you can also call API to do it quickly)
![connect ec2](/images/4-2/05.png?width=50pc)

2. Get the API Gateway URL to test on Postman
![connect ec2](/images/4-2/06.png?width=50pc)

3. Open Postman and test /products
![connect ec2](/images/4-2/07.png?width=50pc)

4. Continue testing /basket
```json
{
  "userId": "user-test-01",
  "items": [
    {
        "quantity": 2,
        "price": 260000,
        "productId": "p-002"
    },
    {
        "quantity": 4,
        "price": 250000,
        "productId": "p-001"
    }
  ]
}
```
![connect ec2](/images/4-2/08.png?width=50pc)

4. Test /basket/checkout
![connect ec2](/images/4-2/08.png?width=50pc)
    - After it responds like this **Checkout processing started** -> it has sent an asynchronous event
    ![connect ec2](/images/4-2/09.png?width=50pc)
5. Check CloudWatch
    - Go to AWS Console, enter **CloudWatch** and click.
    - Click **Log group** from the left slider, click to check the log of **BasketFunction1**
    ![connect ec2](/images/4-2/10.png?width=50pc)
    - Check the latest log and we see **Checkout event sent to EventBridge** -> the event has been sent
    ![connect ec2](/images/4-2/11.png?width=50pc)
    - Click to continue checking the log of **OrderingFunction1**
    ![connect ec2](/images/4-2/12.png?width=50pc)
    - We can see the lambda log detected SQS and successfully saved to DynamoDB.
    ![connect ec2](/images/4-2/13.png?width=50pc)
6. Check the OrderingTable 
    - We can see that OrderingTable has been successfully created by triggering Lambda function OrderingFunction1 from SQS.
![connect ec2](/images/4-2/14.png?width=50pc)
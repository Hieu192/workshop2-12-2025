---
title : "Create Rest API"
date :  "2024-10-27" 
weight : 1 
chapter : false
pre : " <b> 4.1 </b> "
---

#### What is REST API
REST API (Representational State Transfer API) is an interface that allows systems to communicate via HTTP by exchanging data (usually in JSON format). It helps microservices (like Order, Payment, Inventory...) communicate uniformly, separate processing logic, easily scale and integrate with asynchronous mechanisms like SQS or EventBridge in the order system.

#### Objective
The objective of this practice section is to create and configure REST API on Amazon API Gateway, enabling microservices (like Product, Basket, Order) to communicate through HTTP endpoints, serving the asynchronous processing flow in the Order Microservice.

#### Practice

1. Access AWS Console, enter **API Gateway** and access the **API Gateway** service
![Git Bash](/images/4-1/01.png?width=50pc)
2. Select **APIs** in the left sidebar, then click **Create API**
![Git Bash](/images/4-1/02.png?width=50pc)
3. Scroll down to find **REST API** and click **Build**
![Git Bash](/images/4-1/03.png?width=50pc)
4. In the Create REST API interface
   - Select **New API** 
   - API name enter: **`EcommerceAPI1`**
   - API endpoint type: **Regional**
   - Click **Create API**
![Git Bash](/images/4-1/04.png?width=50pc)
5. After creation, click on **/** and then click **Create resource**
![Git Bash](/images/4-1/05.png?width=50pc)
6. In the Resource name section, enter **`products`** and click **Create resource**
![Git Bash](/images/4-1/06.png?width=50pc)
7. Click on the newly created **/products**, click **Create method**
![Git Bash](/images/4-1/07.png?width=50pc)
8. In the Method details interface
   - Method type select **GET**
   - Integration type select **Lambda function**
   - Click **Lambda proxy integration**
   - Lambda function select **ProductFunction1**

![Git Bash](/images/4-1/08.png?width=40pc)
9. Complete creating an API /products
![Git Bash](/images/4-1/09.png?width=50pc)

10. Create /basket
![Git Bash](/images/4-1/10.png?width=50pc)

![Git Bash](/images/4-1/11.png?width=50pc)
11. Create /basket/checkout
![Git Bash](/images/4-1/12.png?width=50pc)

![Git Bash](/images/4-1/13.png?width=50pc)
12. Create /orders
![Git Bash](/images/4-1/14.png?width=50pc)

![Git Bash](/images/4-1/15.png?width=50pc)

13. Result
![Git Bash](/images/4-1/16.png?width=50pc)

14. Deploy API
   - Click **Deploy API**
![Git Bash](/images/4-1/17.png?width=50pc)

   - Stage select **New stage**
   - Stage name enter: **`prod`**
   - Click **Deploy**
![Git Bash](/images/4-1/18.png?width=50pc)
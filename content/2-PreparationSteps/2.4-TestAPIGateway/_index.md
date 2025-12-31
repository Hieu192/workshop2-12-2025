---
title : "Create Lambda Functions"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 2.3 </b> "
---

In this step, we will create Lambda functions for the microservices.

### Create ProductFunction1

1. Access AWS Console and navigate to the **Lambda** service in AWS Console.
![](/images/2-3/01.png?featherlight=false&width=50pc)

2. From the left sidebar, select **Functions** and click **Create function**.
![](/images/2-3/02.png?featherlight=false&width=50pc)

3. Configure the function:
   - Select **Author from scratch**
   - Function name: **`ProductFunction1`**
   - Runtime: **Node.js 22.x**
   - Architecture: **arm64**
   - Execution role: **Use an existing role** → **ProductLambdaRole1**
   - Click **Create function**.
![](/images/2-3/03.png?featherlight=false&width=50pc)

4. Replace the default code with:

```js
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, ScanCommand, GetCommand } from "@aws-sdk/lib-dynamodb";

// Initialize DynamoDB client
const client = new DynamoDBClient({});
const ddbDocClient = DynamoDBDocumentClient.from(client);

const tableName = "ProductTable"; // Your table name

export const handler = async (event) => {
    console.log("Event received:", JSON.stringify(event));

    let responseBody;
    let statusCode = 200;

    const httpMethod = event.httpMethod;
    const pathParams = event.pathParameters;

    try {
        if (httpMethod === "GET") {
            if (pathParams && pathParams.productId) {
                // Get a specific product: GET /products/{productId}
                const params = {
                    TableName: tableName,
                    Key: {
                        productId: pathParams.productId,
                    },
                };
                const { Item } = await ddbDocClient.send(new GetCommand(params));
                responseBody = Item ? Item : { message: "Product not found." };
                if (!Item) statusCode = 404;

            } else {
                // Get all products: GET /products
                const params = {
                    TableName: tableName,
                };
                const { Items } = await ddbDocClient.send(new ScanCommand(params));
                responseBody = Items;
            }
        } else {
            statusCode = 400;
            responseBody = { message: "Unsupported method" };
        }
    } catch (err) {
        console.error(err);
        statusCode = 500;
        responseBody = { message: "Internal server error", error: err.message };
    }

    // Return result for API Gateway (Lambda Proxy format)
    return {
        statusCode: statusCode,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(responseBody),
    };
};
```

5. Click **Deploy**.
![](/images/2-3/04.png?featherlight=false&width=50pc)

### Create BasketFunction1

1. Create another function similar to above with:
   - Function name: **`BasketFunction1`**
   - Runtime: **Node.js 22.x**
   - Architecture: **arm64**
   - Execution role: **BasketLambdaRole1**
![](/images/2-3/05.png?featherlight=false&width=50pc)

2. Replace the code with:

```javascript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand, GetCommand } from "@aws-sdk/lib-dynamodb";
import { EventBridgeClient, PutEventsCommand } from "@aws-sdk/client-eventbridge";

// Initialize clients
const ddbClient = new DynamoDBClient({});
const ddbDocClient = DynamoDBDocumentClient.from(ddbClient);
const ebClient = new EventBridgeClient({}); // Client for EventBridge

const basketTable = "BasketTable";

export const handler = async (event) => {
    console.log("Event received:", JSON.stringify(event));

    const { httpMethod, path, body } = event;
    let responseBody;
    let statusCode = 200;

    try {
        if (httpMethod === "POST" && path.includes("/checkout")) {
            // ---- PROCESS CHECKOUT AND SEND EVENT ----
            console.log("Processing checkout...");

            const checkoutData = JSON.parse(body || '{}');

            // Basic validation
            if (!checkoutData.userId) {
                return { statusCode: 400, body: JSON.stringify({ message: "userId is required for checkout." }) };
            }

            // 1. Create event to send
            const eventParams = {
                Entries: [
                    {
                        Source: "com.ecommerce.basket",     // Source name (remember for Rule creation)
                        DetailType: "CheckoutEvent",        // Event name (remember for Rule creation)
                        Detail: JSON.stringify(checkoutData), // Event content (entire cart)
                        EventBusName: "default"             // Use default event bus
                    },
                ],
            };

            // 2. Send event to EventBridge
            await ebClient.send(new PutEventsCommand(eventParams));

            console.log("Checkout event sent to EventBridge.");
            responseBody = { message: "Checkout processing started", eventData: checkoutData };

        } else if (httpMethod === "POST" && path.includes("/basket")) {
            // ---- PROCESS CART UPDATE ----
            const basketData = JSON.parse(body || '{}');

            if (!basketData.userId) {
                 return { statusCode: 400, body: JSON.stringify({ message: "userId is required." }) };
            }

            const params = {
                TableName: basketTable,
                Item: basketData // Save entire cart
            };
            await ddbDocClient.send(new PutCommand(params));
            responseBody = { message: "Basket updated", basket: basketData };

        } else {
            statusCode = 400;
            responseBody = { message: "Unsupported method or path" };
        }

    } catch (err) {
        console.error(err);
        statusCode = 500;
        responseBody = { message: "Internal server error", error: err.message };
    }

    return {
        statusCode: statusCode,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(responseBody),
    };
};
```

3. Click **Deploy**.
![](/images/2-3/06.png?featherlight=false&width=50pc)

### Create OrderingFunction1

1. Create another function with:
   - Function name: **OrderingFunction1**
   - Runtime: **Node.js 22.x**
   - Architecture: **arm64**
   - Execution role: **OrderingLambdaRole**
![](/images/2-3/07.png?featherlight=false&width=50pc)

2. Replace the code with:

```javascript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand, ScanCommand } from "@aws-sdk/lib-dynamodb";
import { randomUUID } from "crypto";

const ddbClient = new DynamoDBClient({});
const ddbDocClient = DynamoDBDocumentClient.from(ddbClient);

const orderTable = "OrderingTable";

export const handler = async (event) => {
    console.log("Event received:", JSON.stringify(event));

    // ----- PROCESS WHEN TRIGGERED BY SQS -----
    // event.Records is an array, SQS can send multiple messages at once
    if (event.Records) {
        console.log("Processing SQS message...");

        try {
            for (const record of event.Records) {
                const sqsBody = JSON.parse(record.body);

                // Event from EventBridge will be in the 'detail' field of SQS body
                const checkoutEventData = sqsBody.detail; 
                console.log("Checkout data from SQS:", checkoutEventData);

                // 1. Create a new orderId
                const orderId = randomUUID();

                // 2. Create order object to save
                const orderParams = {
                    TableName: orderTable,
                    Item: {
                        orderId: orderId,
                        userId: checkoutEventData.userId,
                        items: checkoutEventData.items,
                        status: "PENDING", // Initial status
                        createdAt: new Date().toISOString()
                    }
                };

                // 3. Save order to DynamoDB
                await ddbDocClient.send(new PutCommand(orderParams));
                console.log(`Order ${orderId} saved successfully.`);
            }
            // Lambda function triggered by SQS doesn't need to return anything
            return { message: "SQS messages processed successfully." };

        } catch (err) {
            console.error("Error processing SQS message:", err);
            // Important: If error is thrown, SQS will retry sending the message
            throw err; 
        }

    } 
    // ----- PROCESS WHEN TRIGGERED BY API GATEWAY -----
    else if (event.httpMethod) {
        console.log("Processing API Gateway request...");

        // Logic for API GET /orders (get all orders)
        if (event.httpMethod === "GET") {
             try {
                const params = {
                    TableName: orderTable,
                };
                const { Items } = await ddbDocClient.send(new ScanCommand(params));
                return {
                    statusCode: 200,
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(Items)
                };
            } catch (err) {
                 console.error(err);
                 return {
                    statusCode: 500,
                    body: JSON.stringify({ message: "Internal server error" })
                 };
            }
        }
    }

    // Unknown case
    console.warn("Unknown event type");
    return {
        statusCode: 400,
        body: JSON.stringify({ message: "Unsupported event source" })
    };
};
```

3. Click **Deploy**.
![](/images/2-3/08.png?featherlight=false&width=50pc)

All Lambda functions have been created successfully!

![](/images/2-3/09.png?featherlight=false&width=50pc)
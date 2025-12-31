---
title : "Create Asynchronous Processing Flow"
date :  "2024-10-27" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

#### What is Asynchronous Processing Flow?
A processing flow where the sender (producer) does not need to wait for the receiver (consumer) to finish processing immediately, but continues operating, while the work is processed in the background through intermediate mechanisms (queue, event bus, callback...).

![](/images/3/01.png?featherlight=false&width=50pc)

#### Content

1. [Create SQS](3.1-CreateSQS/)
2. [Create EventBridge](3.2-CreateEventBridgeRule/)
3. [Trigger Lambda with SQS](3.3-TriggerLambdaToSQS/)
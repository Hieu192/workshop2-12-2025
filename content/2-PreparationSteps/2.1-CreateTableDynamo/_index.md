---
title : "Create DynamoDB Tables"
date :  "2024-10-27" 
weight : 1
chapter : false
pre : " <b> 2.1 </b> "
---


In this step, we will create the DynamoDB tables needed for the video analysis system.

### Create video-analysis Table

1. Access AWS Console and navigate to the **DynamoDB** service. From the DynamoDB interface, click **Create table**.

![](/images/2-1/01.png?featherlight=false&width=50pc)

2. Create the video-analysis table
   - Table name: **`video-analysis`**
   - Partition key: **`PK`** (String)
   - Sort key: **`SK`** (String)
![](/images/2-1/02.png?featherlight=false&width=50pc)

3. From the video-analysis table, create an index
   - Index name: **`GS1`**
   - Partition key Attribute: **`GS1PK`** (String)
   - Sort key Attribute: **`GS1SK`** (String) 

![](/images/2-1/03.png?featherlight=false&width=50pc)

4. Keep other settings as default and click **Create index**.
![](/images/2-1/04.png?featherlight=false&width=50pc)

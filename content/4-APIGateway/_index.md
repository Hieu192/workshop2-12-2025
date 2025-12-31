---
title : "Multimodal Video Search"
date :  "2024-10-27" 
weight : 4 
chapter : false
pre : " <b> 4. </b> "
---

### Multimodal Video Search

In this chapter, we will build an Application Programming Interface (API) to allow users to search for video segments based on text or image content. This is the most important part that helps users interact with processed video data.

#### Search Flow Architecture

The system uses Semantic Search model instead of traditional keyword search:
1. **Request**: User sends a query in text form (e.g., "man playing guitar") or uploads an image.
2. **Processing**: Lambda function receives the request, uses Amazon Bedrock to convert the query into vector embeddings (spatial coordinates).
3. **Query**: Performs Vector Search on Amazon OpenSearch Serverless to find video segments with vectors most similar to the query.
4. **Response**: Returns detailed video segment information including filename, start/end time and direct viewing link.

![](/images/4/image.png?featherlight=false&width=50pc)

#### Main Content

1. [Create Search Lambda](4.1-CreateLambdaSearch/)
2. [Configure API Gateway](4.2-CreateLambdaApiGateway/)
3. [Test with Postman](4.3-TestAPIByPostman/)
4. [Test with CLI](4.4-TestAPIByCLI/)
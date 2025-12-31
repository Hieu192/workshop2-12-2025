---
title : "Create OpenSearch Serverless Collection"
date :  "2024-10-27" 
weight : 7
chapter : false
pre : " <b> 3.7 </b> "
---

#### Objective
Set up Amazon OpenSearch Serverless to store vector embeddings and support vector-based video content search (Vector Search). This is the main database that helps the system intelligently search videos by content meaning.

#### Practice

1. Access the **Amazon OpenSearch Service** in AWS Console.
   - In the left menu, select **Serverless** -> **Collections**.
   - Click **Create collection**.
![](/images/3-7/01.png?width=50pc)

2. Configure basic information:
   - **Collection name**: `video-embeddings`.
   - **Collection type**: Select **Vector search**.
![](/images/3-7/02.png?width=50pc)

3. Configure security and access:
   - **Security**: Select **Standard create**.
   - **Encryption**: Select **Use AWS owned key**.
   - **Network access settings**: Select **Public** (for simplicity in this practice).
![](/images/3-7/03.png?width=50pc)

4. Configure data access permissions:
   - Select **JSON** format.
   - Enter the JSON policy below to grant permissions to manage collection and index:

```json
[
  {
    "Rules": [
      {
        "Resource": ["collection/video-embeddings"],
        "Permission": [
          "aoss:CreateCollectionItems",
          "aoss:DeleteCollectionItems",
          "aoss:UpdateCollectionItems",
          "aoss:DescribeCollectionItems"
        ],
        "ResourceType": "collection"
      },
      {
        "Resource": ["index/video-embeddings/*"],
        "Permission": [
          "aoss:CreateIndex",
          "aoss:DeleteIndex",
          "aoss:UpdateIndex",
          "aoss:DescribeIndex",
          "aoss:ReadDocument",
          "aoss:WriteDocument"
        ],
        "ResourceType": "index"
      }
    ],
    "Principals": [
      "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/lambda-video-embedding-role",
      "arn:aws:iam::<YOUR_ACCOUNT_ID>:root"
    ]
  }
]
```
![](/images/3-7/04.png?width=50pc)

5. Name the access policy:
   - **Access policy name**: `video-embeddings-access-policy`.
   - Click **Next**.
![](/images/3-7/05.png?width=50pc)

6. Review the information and click **Submit**.
![](/images/3-7/06.png?width=50pc)

7. The system will initialize the collection. This process may take a few minutes.
![](/images/3-7/07.png?width=50pc)

8. When the status changes to **Active**, copy the **OpenSearch endpoint** value. We will need it for the next steps.
![](/images/3-7/08.png?width=50pc)

9. **Important**: You need to grant additional IAM permissions to the Lambda Role to call OpenSearch Serverless API.
   - Go to IAM -> Roles -> `lambda-video-embedding-role`.
   - Click **Add permissions** -> **Create inline policy**.
   - Select JSON and paste:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "OpenSearchServerlessAccess",
            "Effect": "Allow",
            "Action": [
                "aoss:APIAccessAll"
            ],
            "Resource": "arn:aws:aoss:us-east-1:<YOUR_ACCOUNT_ID>:collection/*"
        }
    ]
}
```
![](/images/3-7/09.png?width=50pc)

10. Name the policy `opensearch-serverless-access` and click **Create policy**.
![](/images/3-7/10.png?width=50pc)
---
title : "Tạo OpenSearch Serverless collection"
date :  "2024-10-27" 
weight : 7
chapter : false
pre : " <b> 3.7 </b> "
---

#### Mục tiêu
Thiết lập Amazon OpenSearch Serverless để lưu trữ các vector embedding và hỗ trợ tìm kiếm nội dung video bằng vector (Vector Search). Đây là cơ sở dữ liệu chính giúp hệ thống có thể tìm kiếm video theo ý nghĩa nội dung một cách thông minh.

#### Thực hành

1. Truy cập dịch vụ **Amazon OpenSearch Service** trong AWS Console.
   - Tại menu bên trái, chọn **Serverless** -> **Collections**.
   - Nhấn **Create collection**.
![](/images/3-7/01.png?width=50pc)

2. Cấu hình thông tin cơ bản:
   - **Collection name**: `video-embeddings`.
   - **Collection type**: Chọn **Vector search**.
![](/images/3-7/02.png?width=50pc)

3. Cấu hình bảo mật và truy cập:
   - **Security**: Chọn **Standard create**.
   - **Encryption**: Chọn **Use AWS owned key**.
   - **Network access settings**: Chọn **Public** (để đơn giản cho bài thực hành).
![](/images/3-7/03.png?width=50pc)

4. Cấu hình quyền truy cập dữ liệu (Data access):
   - Chọn định dạng **JSON**.
   - Nhập đoạn policy JSON dưới đây để cấp quyền quản lý collection và index:

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

5. Đặt tên cho access policy:
   - **Access policy name**: `video-embeddings-access-policy`.
   - Nhấn **Next**.
![](/images/3-7/05.png?width=50pc)

6. Kiểm tra lại thông tin (Review) và nhấn **Submit**.
![](/images/3-7/06.png?width=50pc)

7. Hệ thống sẽ tiến hành khởi tạo collection. Quá trình này có thể mất vài phút.
![](/images/3-7/07.png?width=50pc)

8. Khi trạng thái chuyển sang **Active**, hãy copy lại giá trị **OpenSearch endpoint**. Chúng ta sẽ cần nó cho các bước tiếp theo.
![](/images/3-7/08.png?width=50pc)

9. **Quan trọng**: Cần cấp thêm quyền IAM cho Lambda Role để có thể gọi API của OpenSearch Serverless.
   - Truy cập IAM -> Roles -> `lambda-video-embedding-role`.
   - Nhấn **Add permissions** -> **Create inline policy**.
   - Chọn JSON và dán:

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

10. Đặt tên policy là `opensearch-serverless-access` và nhấn **Create policy**.
![](/images/3-7/10.png?width=50pc)

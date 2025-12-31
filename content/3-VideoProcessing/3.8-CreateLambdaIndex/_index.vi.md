---
title : "Tạo lambda index video embedding"
date :  "2024-10-27" 
weight : 8
chapter : false
pre : " <b> 3.8 </b> "
---

#### Mục tiêu
Tạo hàm Lambda mang tên **embedding-index** để hoàn tất quy trình bằng cách lấy các vector embedding đã xử lý từ S3 (do Bedrock tạo ra) và lưu vào Amazon OpenSearch Serverless. Hàm này giúp video chính thức có thể tìm kiếm được.

#### Thực hành

1. Tạo hàm Lambda:
   - **Function name**: `embedding-index`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Sử dụng role `lambda-video-embedding-role`.
![](/images/3-8/01.png?width=50pc)
![](/images/3-8/02.png?width=50pc)

2. Cấu hình cơ bản cho hàm (vì việc index vector có thể tốn tài nguyên):
   - **Memory**: `1024 MB`.
   - **Timeout**: `5 min 0 sec`.
![](/images/3-8/03.png?width=50pc)

3. Cấu hình biến môi trường:
   - **OPENSEARCH_HOST**: (Endpoint bạn đã copy ở bước 3.7, bỏ phần https://).
   - **OPENSEARCH_INDEX**: `video-segments-index`.
   - **S3_BUCKET_NAME**: (Tên bucket chứa video).
   - **TABLE_NAME**: `video-analysis`.
![](/images/3-8/04.png?width=50pc)

4. **Tạo Lambda Layer** (do Lambda mặc định không có thư viện OpenSearch):
   - Vào menu **Layers** ở bên trái Console.
   - Nhấn **Create layer**.
   - Tên: `opensearch-py-layer`.
   - Tải lên file `.zip` chứa thư viện `opensearch-py` và `requests-aws4auth`.
   - Architecture: `x86_64`.
   - Runtimes: `Python 3.12`.
![](/images/3-8/06.png?width=50pc)

5. Gán Layer vào hàm `embedding-index`:
   - Tại giao diện hàm Lambda, kéo xuống phần **Layers**.
   - Nhấn **Add a layer**.
   - Chọn **Custom layers** và chọn layer bạn vừa tạo.
![](/images/3-8/07.png?width=50pc)
![](/images/3-8/08.png?width=50pc)

6. Tại tab **Code**, dán đoạn mã nguồn xử lý index:

```python
import os
import json
import time
import boto3
from datetime import datetime

TABLE_NAME = os.environ.get("TABLE_NAME", "video-analysis")
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "sl-video-analysis-videos-hieu")
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "")
OPENSEARCH_INDEX = os.environ.get("OPENSEARCH_INDEX", "video-segments-index")
REGION = os.environ.get("AWS_REGION", "us-east-1")

s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def get_embedding_output(s3_output_prefix):
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=s3_output_prefix)
    
    for obj in response.get("Contents", []):
        if obj["Key"].endswith("output.json"):
            obj_response = s3.get_object(Bucket=S3_BUCKET, Key=obj["Key"])
            content = obj_response["Body"].read().decode("utf-8")
            return json.loads(content).get("data", [])
    
    raise Exception(f"No output.json found in {s3_output_prefix}")


def get_opensearch_client():
    if not OPENSEARCH_HOST:
        return None
    
    from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
    
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, REGION, "aoss")
    
    return OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=60
    )


def index_embeddings(embedding_data, video_id):
    client = get_opensearch_client()
    if not client:
        print("OpenSearch not configured")
        return 0
    
    indexed = 0
    for i, segment in enumerate(embedding_data):
        start_time = segment.get("startSec", 0)
        end_time = segment.get("endSec", 0)
        embedding = segment.get("embedding")
        option = segment.get("embeddingOption", "visual")
        
        if not embedding:
            continue
        
        doc = {
            "embedding": embedding,
            "video_id": video_id,
            "segment_id": i,
            "start_time": start_time,
            "end_time": end_time,
            "embedding_option": option
        }
        
        doc_id = f"{video_id}_{i}_{option}"
        client.index(index=OPENSEARCH_INDEX, body=doc)
        indexed += 1
    
    return indexed


def update_status(video_id, status, **kwargs):
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    update_expr = "SET embedding_status = :status, embedding_updated_at = :ts"
    expr_values = {":status": status, ":ts": timestamp}
    expr_names = {}
    
    if status == "completed":
        update_expr += ", #st = :video_status, GSI1PK = :gsi1pk"
        expr_values[":video_status"] = "ready"
        expr_values[":gsi1pk"] = "STATUS#ready"
        expr_names["#st"] = "status"
    
    for key, value in kwargs.items():
        update_expr += f", {key} = :{key}"
        expr_values[f":{key}"] = value
    
    update_kwargs = {
        "Key": {"PK": f"vid#{video_id}", "SK": "METADATA"},
        "UpdateExpression": update_expr,
        "ExpressionAttributeValues": expr_values
    }
    if expr_names:
        update_kwargs["ExpressionAttributeNames"] = expr_names
    
    table.update_item(**update_kwargs)


def save_embedding_record(video_id, embedding_id, embedding_s3_uri,
                          segments_count, modalities, indexed_count, processing_seconds):
    timestamp = datetime.utcnow().isoformat() + "Z"
    table.put_item(Item={
        "PK": f"vid#{video_id}",
        "SK": f"EMBEDDING#{timestamp}",
        "video_id": video_id,
        "embedding_id": embedding_id,
        "embedding_s3_uri": embedding_s3_uri,
        "segments_count": segments_count,
        "modalities": modalities,
        "indexed_count": indexed_count,
        "processing_seconds": processing_seconds
    })


def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    video_id = event.get("video_id")
    embedding_id = event.get("embedding_id")
    s3_output_prefix = event.get("s3_output_prefix")
    s3_output_uri = event.get("s3_output_uri")
    start_time = event.get("start_time", int(time.time()))
    
    try:
        update_status(video_id, "indexing")
        
        # Get embeddings from S3
        print(f"Getting embeddings from: {s3_output_prefix}")
        embedding_data = get_embedding_output(s3_output_prefix)
        segments_count = len(embedding_data)
        print(f"Got {segments_count} segments")
        
        # Extract modalities
        modalities = list(set(seg.get("embeddingOption", "visual") for seg in embedding_data))
        
        # Index to OpenSearch
        indexed_count = index_embeddings(embedding_data, video_id)
        print(f"Indexed {indexed_count} documents")
        
        processing_seconds = int(time.time()) - start_time
        
        # Save embedding record
        save_embedding_record(
            video_id, embedding_id, s3_output_uri,
            segments_count, modalities, indexed_count, processing_seconds
        )
        
        # Update status
        update_status(video_id, "completed",
            embedding_s3_uri=s3_output_uri,
            segments_count=segments_count,
            modalities=modalities,
            indexed_count=indexed_count,
            embedding_processing_seconds=processing_seconds
        )
        
        return {
            "status": "success",
            "video_id": video_id,
            "segments_count": segments_count,
            "indexed_count": indexed_count,
            "modalities": modalities,
            "processing_seconds": processing_seconds
        }
        
    except Exception as e:
        print(f"Error: {e}")
        update_status(video_id, "failed", embedding_error=str(e))
        raise
```
   - Nhấn **Deploy**.
![](/images/3-8/02.png?width=50pc)

---
title : "Create Lambda Video Search Function"
date :  "2024-10-27" 
weight : 1
chapter : false
pre : " <b> 4.1 </b> "
---

#### Objective
Create a Lambda function named **video-search** that receives requests from users (text or image), converts them into vector embeddings through Bedrock, then queries OpenSearch to find the most suitable video segments.

#### Practice

1. Create Lambda function:
   - **Function name**: `video-search`.
   - **Runtime**: `Python 3.12`.
   - **Architecture**: `x86_64`.
   - **Permissions**: Use role `lambda-video-embedding-role`.
![](/images/4-1/02.png?width=50pc)

2. Configure basic settings for the function:
   - **Memory**: `512 MB`.
   - **Timeout**: `30 sec`.
![](/images/4-1/08.png?width=50pc)

3. Configure environment variables:
   - **OPENSEARCH_HOST**: (Your OpenSearch Endpoint).
   - **OPENSEARCH_INDEX**: `video-segments-index`.
   - **TABLE_NAME**: `video-analysis`.
   - **VIDEO_BUCKET**: (Bucket containing videos for preview links).
![](/images/4-1/03.png?width=50pc)

4. Attach Lambda Layer:
   - Similar to step 3.8, we need to attach the `opensearch-py-layer` layer so the function can use the OpenSearch library.
![](/images/4-1/05.png?width=50pc)
![](/images/4-1/07.png?width=50pc)

5. In the **Code** tab, paste the multimodal search source code:

```python
import os
import json
import boto3
import base64
import uuid
from typing import Dict, Any, List, Optional
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from urllib.parse import urlparse
from boto3.dynamodb.conditions import Key

# Environment variables
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "thzwv0rsospdk9d1ewp8.us-east-1.aoss.amazonaws.com")
OPENSEARCH_INDEX = os.environ.get("OPENSEARCH_INDEX", "video-segments-index")
TABLE_NAME = os.environ.get("TABLE_NAME", "video-analysis")
VIDEO_BUCKET = os.environ.get("VIDEO_BUCKET", "sl-video-analysis-videos-hieu")
REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID", "904233110564")
MARENGO_MODEL_ID = os.environ.get("MARENGO_MODEL_ID", "us.twelvelabs.marengo-embed-3-0-v1:0")
DEFAULT_TOP_K = int(os.environ.get("DEFAULT_TOP_K", "5"))
PRESIGNED_URL_EXPIRY = int(os.environ.get("PRESIGNED_URL_EXPIRY", "3600"))

# S3 prefix for temporary image uploads
S3_TEMP_IMAGES_PREFIX = "temp-search-images"

# Initialize clients
bedrock_client = boto3.client("bedrock-runtime", region_name=REGION)
s3_client = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

# OpenSearch client (lazy initialization)
opensearch_client = None


def get_opensearch_client():
    """Initialize OpenSearch client with IAM auth."""
    global opensearch_client
    
    if opensearch_client is not None:
        return opensearch_client
    
    if not OPENSEARCH_HOST:
        raise ValueError("OPENSEARCH_HOST environment variable not set")
    
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, REGION, "aoss")
    
    opensearch_client = OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
        timeout=30
    )
    
    return opensearch_client


def create_response(status_code: int, body: Dict[str, Any]) -> Dict:
    """Create API Gateway response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }


def create_text_embedding(text: str) -> List[float]:
    response = bedrock_client.invoke_model(
        modelId=MARENGO_MODEL_ID,
        body=json.dumps({
            "inputType": "text",
            "text": {
                "inputText": text
            }
        })
    )
    
    result = json.loads(response["body"].read())
    return result["data"][0]["embedding"]


def create_image_embedding(image_base64: str) -> List[float]:
    # Generate unique filename
    image_id = str(uuid.uuid4())
    s3_key = f"{S3_TEMP_IMAGES_PREFIX}/{image_id}.jpg"
    
    # Decode and upload to S3
    image_bytes = base64.b64decode(image_base64)
    s3_client.put_object(
        Bucket=VIDEO_BUCKET,
        Key=s3_key,
        Body=image_bytes,
        ContentType="image/jpeg"
    )
    
    s3_image_uri = f"s3://{VIDEO_BUCKET}/{s3_key}"
    print(f"Uploaded temp image to: {s3_image_uri}")
    
    try:
        # Call Bedrock for image embedding
        response = bedrock_client.invoke_model(
            modelId=MARENGO_MODEL_ID,
            body=json.dumps({
                "inputType": "image",
                "image": {
                    "mediaSource": {
                        "s3Location": {
                            "uri": s3_image_uri,
                            "bucketOwner": AWS_ACCOUNT_ID
                        }
                    }
                }
            })
        )
        
        result = json.loads(response["body"].read())
        return result["data"][0]["embedding"]
        
    finally:
        # Clean up: delete temp image from S3
        try:
            s3_client.delete_object(Bucket=VIDEO_BUCKET, Key=s3_key)
            print(f"Cleaned up temp image: {s3_key}")
        except Exception as e:
            print(f"Warning: Failed to delete temp image: {e}")


def search_opensearch(
    query_embedding: List[float],
    video_id: Optional[str] = None,
    modalities: Optional[List[str]] = None,
    top_k: int = 5
) -> List[Dict]:
    """Search OpenSearch for similar video segments."""
    client = get_opensearch_client()
    
    # Build filter conditions
    filter_conditions = []
    
    if video_id:
        filter_conditions.append({"term": {"video_id": video_id}})
    
    if modalities and "all" not in modalities:
        filter_conditions.append({"terms": {"embedding_option": modalities}})
    
    # Build query
    if filter_conditions:
        inner_query = {"bool": {"filter": filter_conditions}}
    else:
        inner_query = {"match_all": {}}
    
    search_body = {
        "query": {
            "script_score": {
                "query": inner_query,
                "script": {
                    "source": "knn_score",
                    "lang": "knn",
                    "params": {
                        "field": "embedding",
                        "query_value": query_embedding,
                        "space_type": "cosinesimil"
                    }
                }
            }
        },
        "size": top_k,
        "_source": ["video_id", "segment_id", "start_time", "end_time", "embedding_option"]
    }
    
    response = client.search(index=OPENSEARCH_INDEX, body=search_body)
    
    # Parse results
    results = []
    for hit in response["hits"]["hits"]:
        results.append({
            "score": round(hit["_score"], 4),
            "video_id": hit["_source"]["video_id"],
            "segment_id": hit["_source"]["segment_id"],
            "start_time": hit["_source"]["start_time"],
            "end_time": hit["_source"]["end_time"],
            "embedding_option": hit["_source"].get("embedding_option", "visual")
        })
    
    return results


def get_video_metadata(video_id: str) -> Optional[Dict]:
    """
    response = table.get_item(
        Key={
            "PK": f"vid#{video_id}",
            "SK": "METADATA"
        }
    )
    return response.get("Item")
    """

def generate_presigned_url(s3_uri: str) -> str:
    """Generate presigned URL from S3 URI."""
    parsed = urlparse(s3_uri)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=PRESIGNED_URL_EXPIRY
    )


def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    # Handle OPTIONS for CORS
    if event.get("httpMethod") == "OPTIONS":
        return create_response(200, {"message": "OK"})
    
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))
        
        # Determine search type (default to "text" for backward compatibility)
        search_type = body.get("search_type", "text").lower()
        
        # Common parameters
        video_id = body.get("video_id")
        modalities = body.get("modalities")
        top_k = body.get("top_k", DEFAULT_TOP_K)
        
        # Validate search_type
        if search_type not in ["text", "image"]:
            return create_response(400, {
                "error": f"Invalid search_type: {search_type}. Must be 'text' or 'image'"
            })
        
        # Validate video_id if provided
        if video_id:
            metadata = get_video_metadata(video_id)
            if not metadata:
                return create_response(404, {"error": f"Video not found: {video_id}"})
        
        # Create embedding based on search type
        query_text = None
        
        if search_type == "text":
            # TEXT SEARCH
            query_text = body.get("query")
            if not query_text:
                return create_response(400, {"error": "Missing required field: query (for text search)"})
            
            print(f"Creating TEXT embedding for: {query_text}")
            query_embedding = create_text_embedding(query_text)
            print(f"Text embedding created, dimension: {len(query_embedding)}")
            
        else:
            # IMAGE SEARCH
            image_base64 = body.get("image_base64")
            if not image_base64:
                return create_response(400, {"error": "Missing required field: image_base64 (for image search)"})
            
            # Validate base64 format
            try:
                # Check if it's valid base64
                base64.b64decode(image_base64)
            except Exception:
                return create_response(400, {"error": "Invalid image_base64 format"})
            
            print(f"Creating IMAGE embedding (base64 length: {len(image_base64)})")
            query_embedding = create_image_embedding(image_base64)
            print(f"Image embedding created, dimension: {len(query_embedding)}")
        
        # Search OpenSearch
        print(f"Searching (search_type={search_type}, video_id={video_id}, modalities={modalities}, top_k={top_k})")
        search_results = search_opensearch(
            query_embedding=query_embedding,
            video_id=video_id,
            modalities=modalities,
            top_k=top_k
        )
        print(f"Found {len(search_results)} results")
        
        # Enrich results with video URLs
        metadata_cache = {}
        enriched_results = []
        
        for i, result in enumerate(search_results, 1):
            vid = result["video_id"]
            
            # Get metadata from cache or DynamoDB
            if vid not in metadata_cache:
                metadata = get_video_metadata(vid)
                if metadata:
                    metadata_cache[vid] = metadata
            
            metadata = metadata_cache.get(vid)
            
            # Generate presigned URL
            video_url = None
            if metadata and metadata.get("s3_uri"):
                video_url = generate_presigned_url(metadata["s3_uri"])
            
            enriched_results.append({
                "rank": i,
                "score": result["score"],
                "video_id": vid,
                "video_url": video_url,
                "filename": metadata.get("filename") if metadata else None,
                "start_time": result["start_time"],
                "end_time": result["end_time"],
                "segment_id": result["segment_id"],
                "embedding_option": result["embedding_option"]
            })
        
        # Build response
        response_body = {
            "search_type": search_type,
            "query": query_text,  # None if image search
            "total_results": len(enriched_results),
            "results": enriched_results
        }
        
        if video_id:
            response_body["filtered_by_video_id"] = video_id
        
        return create_response(200, response_body)
        
    except json.JSONDecodeError:
        return create_response(400, {"error": "Invalid JSON body"})
    except ValueError as e:
        return create_response(500, {"error": str(e)})
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return create_response(500, {"error": str(e)})

```
   - Click **Deploy**.
![](/images/4-1/04.png?width=50pc)
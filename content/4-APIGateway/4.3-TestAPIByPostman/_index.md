---
title : "Test Search API with Postman"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 4.3 </b> "
---

#### Objective
Use Postman tool to verify the accuracy of the video search system. We will test both forms: Text Search and Image Search.

#### Practice

1. Configure Postman:
   - Open Postman, select method **POST**.
   - Paste the API URL you copied in step 4.2 (with suffix `/videos/video-search`).

2. **Text Search**:
   - In the **Body** tab, select **raw** and format **JSON**.
   - Enter search content (e.g., find footage of a man playing guitar):
   ```json
   {
       "text": "Person using sign language"
   }
   ```
   - Returns status `200 OK` and list of related video segments with `score` (similarity) and preview link.

![](/images/4-3/01.png?width=50pc)

3. **Text Search for Specific Video**:
   - Change the Body content:
   ```json
   {
       "text": "Man smoking"
   }
   ```
   - The system will extract vector from the image and find video segments with similar image content.
![](/images/4-3/03.png?width=50pc)
**Result Explanation**:
   - **video_id**: Video identifier in the system.
   - **start_time / end_time**: Time range where matching content appears in the video.
   - **score**: Relevance level of the result (higher is more accurate).
   - **presigned_url**: Temporary link for you to directly view that video segment.

4. **Verify Returned Video Segments**
   - Open the video in S3 directly or open the link returned in Postman.
   - Seek to the video segment returned in Postman and verify.

![](/images/4-3/04.png?width=50pc)

5. **Image Search**:
   - In case you want to search for video segments based on an existing image.
   - First, download the sample image below to your computer:
   - [**Download sample image here (Right click -> Save Image As)**](/images/4-3/test-image.jpg)
   
![](/images/4-3/test-image.jpg?width=30pc)

   - Convert this image to **Base64** format (Use online tools or scripts).
   - Send POST request with the following configuration:
   - **search_type**: `image`
   - **image_base64**: (Base64 string of the image you just downloaded)

```json
{
    "search_type": "image",
    "image_base64": "your base64 string",
    "video_id": "8df657ff-88bd-4b2d-84e9-f825feb13810",
    "modalities": ["visual"],
    "top_k": 5
}
```

![](/images/4-3/05.png?width=50pc)

6. **Verify Image Search Results**:
   - The system will return video segments containing images similar to the sample image.
   - Copy the `video_url` returned and open in browser to verify. You will see results exactly as in the original video.

![](/images/4-3/06.png?width=50pc)
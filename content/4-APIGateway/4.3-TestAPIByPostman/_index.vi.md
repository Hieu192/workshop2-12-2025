---
title : "Kiểm thử API tìm kiếm bằng Postman"
date :  "2024-10-27" 
weight : 3
chapter : false
pre : " <b> 4.3 </b> "
---

#### Mục tiêu
Sử dụng công cụ Postman để kiểm tra độ chính xác của hệ thống tìm kiếm video. Chúng ta sẽ thử nghiệm cả hai hình thức: tìm kiếm bằng văn bản (Text Search) và tìm kiếm bằng hình ảnh (Image Search).

#### Thực hành

1. Cấu hình Postman:
   - Mở Postman, chọn method **POST**.
   - Dán URL API bạn đã copy ở bước 4.2 (có đuôi `/videos/video-search`).

2. **Tìm kiếm bằng văn bản (Text Search)**:
   - Tại tab **Body**, chọn **raw** và định dạng **JSON**.
   - Nhập nội dung tìm kiếm (ví dụ: tìm cảnh quay người đàn ông chơi guitar):
   ```json
   {
       "text": "Người dùng ngôn ngữ kí hiệu"
   }
   ```
   - Trạng thái trả về `200 OK` và danh sách các đoạn video liên quan kèm theo `score` (độ tương đồng) và link xem thử.

![](/images/4-3/01.png?width=50pc)

3. **Tìm kiếm bằng văn bản cho video cụ thể (Text Search)**:
   - Thay đổi nội dung Body:
   ```json
   {
       "text": "Người đàn ông hút thuốc"
   }
   ```
   - Hệ thống sẽ trích xuất vector từ hình ảnh và tìm các phân đoạn video có nội dung hình ảnh tương tự.
![](/images/4-3/03.png?width=50pc)
**Giải thích kết quả**:
   - **video_id**: Định danh của video trong hệ thống.
   - **start_time / end_time**: Khoảng thời gian xuất hiện đoạn nội dung phù hợp trong video.
   - **score**: Mức độ phù hợp của kết quả (càng cao càng chính xác).
   - **presigned_url**: Đường dẫn tạm thời để bạn có thể xem trực tiếp đoạn video đó.

4. **Kiểm tra đoạn video trả về**
   - Mở video trong s3 mở trực tiếp và truy cập video hoặc mở link trong postman trả về.
   - Tua đến đoạn video trả về trong postman và xác nhận kiểm tra.

![](/images/4-3/04.png?width=50pc)

5. **Tìm kiếm bằng hình ảnh (Image Search)**:
   - Trong trường hợp bạn muốn tìm kiếm các đoạn video dựa trên một hình ảnh có sẵn.
   - Đầu tiên, hãy tải hình ảnh mẫu bên dưới về máy tính của bạn:
   - [**Tải ảnh mẫu tại đây (Chuột phải -> Save Image As)**](/images/4-3/test-image.jpg)
   
![](/images/4-3/test-image.jpg?width=30pc)

   - Chuyển đổi hình ảnh này sang định dạng **Base64** (Sử dụng các công cụ online hoặc script).
   - Gửi yêu cầu POST với cấu hình như sau:
   - **search_type**: `image`
   - **image_base64**: (Chuỗi Base64 của ảnh bạn vừa tải)

```json
{
    "search_type": "image",
    "image_base64": "chuỗi base của bạn",
    "video_id": "8df657ff-88bd-4b2d-84e9-f825feb13810",
    "modalities": ["visual"],
    "top_k": 5
}
```

![](/images/4-3/05.png?width=50pc)

6. **Xác nhận kết quả Image Search**:
   - Hệ thống sẽ trả về các đoạn video chứa hình ảnh tương đồng với ảnh mẫu.
   - Copy đường dẫn `video_url` trả về và mở trên trình duyệt để kiểm tra. Bạn sẽ thấy kết quả chính xác như trong video gốc.

![](/images/4-3/06.png?width=50pc)

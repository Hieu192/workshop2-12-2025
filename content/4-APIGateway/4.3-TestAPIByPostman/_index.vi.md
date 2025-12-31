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

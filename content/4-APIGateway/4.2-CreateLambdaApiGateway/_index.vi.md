---
title : "Cấu hình API Gateway cho tìm kiếm video"
date :  "2024-10-27" 
weight : 2
chapter : false
pre : " <b> 4.2 </b> "
---

#### Mục tiêu
Thiết lập Amazon API Gateway để cung cấp một public endpoint, cho phép các ứng dụng giao diện (Frontend) hoặc công cụ như Postman có thể gửi yêu cầu tìm kiếm đến hàm Lambda `video-search`.

#### Thực hành

1. Truy cập dịch vụ **API Gateway** trong AWS Console.
   - Chọn API đã khởi tạo (ví dụ: `video-analysis-api`).
   - Tại phần **Resources**, nhấn **Create resource**.
![](/images/4-2/01.png?width=50pc)

2. Cấu hình Resource mới:
   - **Resource path**: `/videos`.
   - **Resource name**: `video-search`.
   - Bật **CORS (Cross-Origin Resource Sharing)**.
   - Nhấn **Create resource**.
![](/images/4-2/02.png?width=50pc)
![](/images/4-2/03.png?width=50pc)

3. Tạo Method cho resource vừa tạo:
   - Chọn resource `/video-search`.
   - Nhấn **Create method**.
   - **Method type**: `POST`.
   - **Integration type**: `Lambda function`.
   - Bật **Lambda proxy integration**.
   - **Lambda function**: Chọn hàm `video-search` (us-east-1).
![](/images/4-2/05.png?width=50pc)
![](/images/4-2/06.png?width=50pc)

4. Xác nhận và lưu Method:
   - Nhấn **Create method**. Hệ thống sẽ tự động gán quyền để API Gateway có thể gọi hàm Lambda của bạn.
![](/images/4-2/07.png?width=50pc)

5. Triển khai API (Deploy):
   - Nhấn **Deploy API**.
   - **Stage**: Chọn `prod` (hoặc tạo mới nếu chưa có).
   - Nhấn **Deploy**.
![](/images/4-2/08.png?width=50pc)

6. Sau khi deploy, hãy copy lại **Invoke URL** của stage `prod`. Đây chính là địa chỉ API mà chúng ta sẽ dùng để test ở bước tiếp theo.

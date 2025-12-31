---
title : "Test API bằng curl"
date :  "2024-10-27" 
weight : 4 
chapter : false
pre : " <b> 4.4 </b> "
---

#### Postman là gì
Postman là công cụ hỗ trợ gửi và kiểm thử API một cách trực quan, giúp nhà phát triển gửi yêu cầu (request) đến các endpoint (như API Gateway) và xem phản hồi (response) từ server, phục vụ cho việc kiểm thử và gỡ lỗi API trong quá trình phát triển hệ thống microservice.

#### Thực hành test api
1. Tạo dữ liệu productTable trên dynamoDB để test
![connect ec2](/images/4-2/01.png?width=50pc)
    - Click **Create item**
![connect ec2](/images/4-2/02.png?width=50pc)
    - Click **Json view**
![connect ec2](/images/4-2/03.png?width=50pc)
    - Click **View DynamoDB Json**
    ```json
    {
        "productId": "p-001",
        "brand": "Kim Đồng",
        "name": "Conan tập 1",
        "price": 250000
    }
    ```
![connect ec2](/images/4-2/04.png?width=50pc)
    - Tương tự tạo 5-10 mẫu (Hoặc bạn cũng có thể gọi API để làm nhanh)
![connect ec2](/images/4-2/05.png?width=50pc)

2. Lấy URL của API Gateway để test trên Postman
![connect ec2](/images/4-2/06.png?width=50pc)

3. Mở Postman và test /products
![connect ec2](/images/4-2/07.png?width=50pc)

4. Tiếp tục test /basket
```json
{
  "userId": "user-test-01",
  "items": [
    {
        "quantity": 2,
        "price": 260000,
        "productId": "p-002"
    },
    {
        "quantity": 4,
        "price": 250000,
        "productId": "p-001"
    }
  ]
}
```
![connect ec2](/images/4-2/08.png?width=50pc)

5. Test /basket/checkout
![connect ec2](/images/4-2/08.png?width=50pc)
    - Sau khi nó phản hồi như thế này **Checkout processing started** -> nó đã gửi sự kiện bất đồng bộ
    ![connect ec2](/images/4-2/09.png?width=50pc)
5. Kiểm tra CloudWatch
    - Vào AWS Console, nhập **CloudWatch** và click.
    - Click **Log group** từ slider bên trái, click kiểm tra log của **BasketFunction1**
    ![connect ec2](/images/4-2/10.png?width=50pc)
    - Kiểm tra log mới nhất và ta thấy **Checkout event sent to EventBridge** -> sự kiện đã được gửi đi
    ![connect ec2](/images/4-2/11.png?width=50pc)
    - Click kiểm tra tiếp log của **OrderingFunction1**
    ![connect ec2](/images/4-2/12.png?width=50pc)
    - Ta thấy được log lambda thấy được SQS và lưu vào dynamoDB thành công.
    ![connect ec2](/images/4-2/13.png?width=50pc)
6. Kiểm tra bảng OrderingTable 
    - Ta thấy được OrderingTable đã được tạo thành công bằng cách kích hoạt Lambda function OrderingFunction1 từ SQS.
![connect ec2](/images/4-2/14.png?width=50pc)


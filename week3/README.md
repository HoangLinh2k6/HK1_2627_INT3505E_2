Bài 1

1.1.Xác định resources:

    posts: bài viết
    comments: bình luận
    tags: thẻ bài viết
    users: người dùng
    profiles: hồ sơ người dùng
    follows: theo dõi

1.2.Phân loại collection / item / sub-resource:

    Collection:
        /posts
        /users
        /tags
    Item:
        /posts/{id}
        /users/{id}
        /tags/{id}
    Sub-resource:
        /posts/{id}/tags
        /users/{id}/follows

1.3.Sơ đồ
![1.3](kq/bt1_3.drawio.png)

1.4 kết quả chạy code
![1.4](kq/bt1.png)

Bài 2
![2](kq/bt2.png)

Bài 3
Test: curl 'localhost:5000/orders?status=paid'
![3.1](kq/bt3_1.png)

Test: curl 'localhost:5000/orders?limit=5'
![3.2](kq/bt3_2.png)

Test: curl 'localhost:5000/orders?fields=id,total'
![3.3](kq/bt3_3.png)

Test: lỗi 400 Bad Request
![3.3](kq/bt3_4.png)
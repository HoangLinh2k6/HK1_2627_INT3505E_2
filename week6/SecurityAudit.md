Lỗ hổng BOLA:   
Mô tả: Tại endpoint GET /posts/{id}, ứng dụng chỉ xác thực JWT của người dùng nhưng quên kiểm tra bài viết có thuộc về chính người dùng đó hay bài viết riêng tư của người khác.
Khắc phục: Áp dụng decorator kiểm tra quyền sở hữu đối tượng dựa trên owner_id trong cơ sở dữ liệu.

Chấp nhận thuật toán alg:
Mô tả: Lớp xác thực JWT không giới hạn allowlist các thuật toán mã hóa, dẫn đến kẻ tấn công có thể chỉnh sửa header JWT thành alg: none để vượt qua kiểm tra chữ ký hoặc giả mạo chữ ký mã hóa.
Khắc phục: Cấu hình cứng danh sách thuật toán hợp lệ (JWT_ALGORITHM="HS256" hoặc mã khóa bất đối xứng) khi giải mã token.

Thời gian sống của Access Token quá lâu / Không thu hồi Refresh Token khi Logout:
Mô tả: Access Token có thời hạn sử dụng dài và không hỗ trợ cơ chế thu hồi. Nếu bị rò rỉ token, kẻ tấn công có thể giả mạo phiên lâu dài.
Khắc phục: Đặt hạn ngạch ngắn cho Access Token (ví dụ: 15 phút), duy trì Refresh Token dài hạn (30 ngày).

Lưu giữ Token ở localStorage dễ bị tấn công XSS:
Mô tả: Phía Client lưu trữ Access Token hoặc Refresh Token trong window.localStorage, khiến bất kỳ đoạn mã độc Cross-Site Scripting (XSS) nào chạy trên trang đều có thể đọc và lấy trộm token.
Khắc phục: Lưu trữ Refresh Token trong HttpOnly Cookie với cờ Secure và SameSite phù hợp.

Thiếu Rate-Limiting tại endpoint POST /auth/login (Credential Stuffing):   
Mô tả: Endpoint đăng nhập không giới hạn số lần gửi yêu cầu, cho phép kẻ tấn công thực hiện vét cạn mật khẩu.
Khắc phục: Thêm lớp Middleware Rate-Limit dựa trên địa chỉ IP.
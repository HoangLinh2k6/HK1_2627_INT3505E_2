Review API "https://pokeapi.co/api/v2/" theo 9 tiêu chí:
1. Resources là danh từ, method diễn đạt hành động.

    Đạt yêu cầu

    Vd:

    ![vd1](<Screenshot 2026-10-06 193335.png>)
2. Naming lowercase, kebab-case path, snake_case query.

    Đạt yêu cầu

    Vd:

    ![vd2](<Screenshot 2026-10-06 193715.png>)

3. Endpoint depth ≤ 3; flatten với filter khi sâu hơn.

    Đạt yêu cầu

4. Treat POST as không-idempotent; PUT, DELETE idempotent.

    Chưa đạt yêu cầu

    Lý do: API công khai này chỉ hỗ trợ phương thức GET (Read-Only API)

5. Status code đúng nghĩa · không bao giờ trả 200 + error.

    Đạt yêu cầu

    Vd:

    ![vd5](<Screenshot 2026-10-06 194522.png>)

6. Error response theo RFC 7807 problem+json nhất quán.

    Chưa đạt yêu cầu

    Lý do: Eror response trả về không theo chuẩn RFC 7807 problem+json

7. Pagination: chọn offset, cursor hoặc keyset theo use case.

    Đạt yêu cầu

    Vd:

    ![vd7](<Screenshot 2026-10-06 195204.png>)

8. Hỗ trợ filter, sort, sparse fieldsets cho mọi collection.

    Chưa đạt yêu cầu

    Lý do: Chưa hỗ trợ sort, sparse fieldsets

9. Versioning từ ngày đầu; tài liệu deprecation rõ ràng.

    Đạt yêu cầu

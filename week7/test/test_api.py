from sqlalchemy import event
from product_api.extensions import db
from product_api.models.product import Product

# Test 1: POST /api/v1/products[cite: 209, 227]
def test_create_product(client):
    res = client.post("/api/v1/products", json={
        "sku": "SKU-TEST-01",
        "name": "Chuột máy tính",
        "price_cents": 150000,
        "qty_in_stock": 5
    })
    assert res.status_code == 201
    assert res.json["sku"] == "SKU-TEST-01"

# Test 2: GET /api/v1/orders có Eager Loading (Kiểm tra lỗi N+1)[cite: 205, 206, 227]
def test_list_orders_eager_loading(client, app):
    # Tạo dữ liệu mẫu
    with app.app_context():
        p1 = Product(sku="P1", name="SP 1", price_cents=100, qty_in_stock=10)
        db.session.add(p1)
        db.session.commit()

        # Tạo đơn hàng
        client.post("/api/v1/orders", json={
            "customer_email": "khach1@gmail.com",
            "items": [{"product_id": p1.id, "quantity": 1}]
        })

    # Đếm số lượng SQL Query phát ra khi gọi GET /orders[cite: 205, 206]
    query_count = 0
    def count_queries(conn, cursor, statement, parameters, context, executemany):
        nonlocal query_count
        query_count += 1

    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", count_queries)
        res = client.get("/api/v1/orders")
        event.remove(db.engine, "before_cursor_execute", count_queries)

    assert res.status_code == 200
    # Đảm bảo số truy vấn <= 2 (1 query lấy Order, 1 query selectinload lấy OrderItem)[cite: 205, 206]
    assert query_count <= 2
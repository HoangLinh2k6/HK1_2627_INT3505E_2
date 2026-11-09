from flask import Blueprint, jsonify, request
from sqlalchemy.orm import selectinload
from product_api.extensions import db
from product_api.models.order import Order, OrderItem
from product_api.models.product import Product
from product_api.errors import NotFound, OutOfStock
from product_api.api.schemas import OrderIn, OrderOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

# POST /api/v1/orders - Tạo đơn hàng mới
@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.json or {})
    order = Order(customer_email=body["customer_email"])

    for item_data in body["items"]:
        product = db.session.get(Product, item_data["product_id"])
        if not product or product.archived:
            raise NotFound(message=f"Product {item_data['product_id']} not found")
        
        if product.qty_in_stock < item_data["quantity"]:
            raise OutOfStock(message=f"Product {product.sku} out of stock")

        # Giảm số lượng kho và tính giá tại thời điểm mua
        product.qty_in_stock -= item_data["quantity"]
        order_item = OrderItem(
            product_id=product.id,
            quantity=item_data["quantity"],
            price_cents=product.price_cents
        )
        order.items.append(order_item)

    db.session.add(order)
    db.session.commit()
    return OrderOut().dump(order), 201

# GET /api/v1/orders - Lấy danh sách đơn hàng (Eager loading tránh N+1 Query)[cite: 205, 206, 227]
@orders_bp.get("")
def list_orders():
    # Sử dụng selectinload chuẩn SQLAlchemy 2.x để chống bẫy N+1[cite: 205, 206]
    stmt = db.select(Order).options(selectinload(Order.items))
    orders = db.session.execute(stmt).scalars().all()
    return jsonify([OrderOut().dump(o) for o in orders]), 200
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from product_api.extensions import db
from product_api.models.product import Product
from product_api.errors import Conflict, NotFound, OutOfStock
from product_api.api.schemas import ProductOut, ProductIn, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

# 1. GET /api/v1/products - Danh sách có phân trang (loại trừ archived=True)
@products_bp.get("")
def list_products():
    page = max(1, request.args.get("page", 1, type=int))
    size = min(100, max(1, request.args.get("size", 20, type=int)))

    base_query = db.select(Product).where(Product.archived.is_(False))
    
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Product).where(Product.archived.is_(False))
    )
    
    rows = db.session.execute(
        base_query.order_by(Product.id).offset((page - 1) * size).limit(size)
    ).scalars().all()

    return jsonify({
        "items": [ProductOut().dump(p) for p in rows],
        "page": page,
        "size": size,
        "total": total
    }), 200

# 2. GET /api/v1/products/<int:id> - Lấy 1 sản phẩm
@products_bp.get("/<int:id>")
def get_product(id):
    p = db.session.get(Product, id)
    if not p or p.archived:
        raise NotFound(message=f"Product with id {id} not found")
    return jsonify(ProductOut().dump(p)), 200

# 3. POST /api/v1/products - Tạo sản phẩm (409 nếu trùng SKU)
@products_bp.post("")
def create_product():
    data = request.get_json(silent=True) or {}
    body = ProductIn().load(data)
    p = Product(**body)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="SKU already exists")
    return jsonify(ProductOut().dump(p)), 201

# 4. POST /api/v1/products/<int:id>/reserve - Đặt trước sản phẩm
@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    data = request.get_json(silent=True) or {}
    body = ReserveIn().load(data)
    
    p = db.session.get(Product, id)
    if not p or p.archived:
        raise NotFound(message=f"Product with id {id} not found")

    qty = body["qty"]
    if p.qty_in_stock < qty:
        raise OutOfStock(message=f"Only {p.qty_in_stock} items left in stock")

    p.qty_in_stock -= qty
    db.session.commit()
    return jsonify(ProductOut().dump(p)), 200

# 5. PATCH /api/v1/products/<int:id> - Cập nhật một phần
@products_bp.patch("/<int:id>")
def patch_product(id):
    p = db.session.get(Product, id)
    if not p or p.archived:
        raise NotFound(message=f"Product with id {id} not found")

    data = request.get_json(silent=True) or {}
    body = ProductPatch().load(data, partial=True)
    
    for k, v in body.items():
        setattr(p, k, v)

    db.session.commit()
    return jsonify(ProductOut().dump(p)), 200

# 6. DELETE /api/v1/products/<int:id> - Soft delete (đánh dấu archived=True)
@products_bp.delete("/<int:id>")
def delete_product(id):
    p = db.session.get(Product, id)
    if not p or p.archived:
        raise NotFound(message=f"Product with id {id} not found")
    p.archived = True
    db.session.commit()
    return "", 204
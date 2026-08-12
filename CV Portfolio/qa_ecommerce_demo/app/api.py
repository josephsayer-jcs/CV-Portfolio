from flask import Blueprint, request, jsonify, session
from . import db
from .models import User, Product, Order, OrderItem

api = Blueprint("api", __name__)

def product_json(p):
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "category": p.category,
    }

@api.get("/products")
def products():
    q = request.args.get("q", "").strip()
    query = Product.query
    if q:
        query = query.filter(
            db.or_(Product.name.ilike(f"%{q}%"), Product.category.ilike(f"%{q}%"))
        )
    return jsonify([product_json(p) for p in query.order_by(Product.id).all()])

@api.get("/products/<int:product_id>")
def product(product_id):
    p = db.session.get(Product, product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product_json(p))

@api.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 409
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201

@api.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(username=data.get("username", "")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401
    session["user_id"] = user.id
    return jsonify({"message": "Logged in", "user_id": user.id})

@api.get("/orders")
def get_orders():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required"}), 401
    orders = Order.query.filter_by(user_id=uid).order_by(Order.id.desc()).all()
    return jsonify([
        {
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "items": [
                {
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                } for i in o.items
            ]
        } for o in orders
    ])

@api.post("/orders")
def create_order():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "At least one item is required"}), 400

    order_total = 0
    resolved = []
    for item in items:
        product = db.session.get(Product, item.get("product_id"))
        quantity = item.get("quantity")
        if not product:
            return jsonify({"error": "Product not found"}), 404
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": "Quantity must be a positive integer"}), 400
        if quantity > product.stock:
            return jsonify({"error": f"Insufficient stock for {product.name}"}), 409
        resolved.append((product, quantity))
        order_total += product.price * quantity

    order = Order(user_id=uid, total=round(order_total, 2))
    db.session.add(order)
    db.session.flush()

    for product, quantity in resolved:
        product.stock -= quantity
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price
        ))

    db.session.commit()
    return jsonify({"id": order.id, "total": order.total, "status": order.status}), 201

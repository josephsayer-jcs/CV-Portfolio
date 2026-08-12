from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import db
from .models import User, Product, Order, OrderItem

web = Blueprint("web", __name__)

def current_user():
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None

def cart_items():
    cart = session.get("cart", {})
    result = []
    total = 0
    for product_id, quantity in cart.items():
        product = db.session.get(Product, int(product_id))
        if product:
            subtotal = product.price * quantity
            result.append((product, quantity, subtotal))
            total += subtotal
    return result, total

@web.route("/")
def index():
    query = request.args.get("q", "").strip()
    products = Product.query
    if query:
        products = products.filter(
            db.or_(Product.name.ilike(f"%{query}%"), Product.category.ilike(f"%{query}%"))
        )
    products = products.order_by(Product.id).all()
    return render_template("products.html", products=products, query=query, user=current_user())

@web.route("/product/<int:product_id>")
def product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return "Product not found", 404
    return render_template("product.html", product=product, user=current_user())

@web.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not username or not email or not password:
            flash("All fields are required.")
            return render_template("register.html")
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.")
            return render_template("register.html")
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("web.index"))
    return render_template("register.html")

@web.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Invalid username or password.")
            return render_template("login.html")
        session["user_id"] = user.id
        return redirect(url_for("web.index"))
    return render_template("login.html")

@web.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("web.index"))

@web.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return "Product not found", 404
    quantity = max(1, int(request.form.get("quantity", 1)))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    session["cart"] = cart
    return redirect(url_for("web.cart"))

@web.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total, user=current_user())

@web.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("web.cart"))

@web.route("/checkout", methods=["GET", "POST"])
def checkout():
    user = current_user()
    if not user:
        return redirect(url_for("web.login"))
    items, total = cart_items()
    if not items:
        flash("Your basket is empty.")
        return redirect(url_for("web.cart"))
    if request.method == "POST":
        for product, quantity, _ in items:
            if quantity > product.stock:
                flash(f"Not enough stock for {product.name}.")
                return redirect(url_for("web.cart"))
        order = Order(user_id=user.id, total=round(total, 2))
        db.session.add(order)
        db.session.flush()
        for product, quantity, _ in items:
            product.stock -= quantity
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price
            ))
        db.session.commit()
        session["cart"] = {}
        return redirect(url_for("web.orders"))
    return render_template("checkout.html", items=items, total=total, user=user)

@web.route("/orders")
def orders():
    user = current_user()
    if not user:
        return redirect(url_for("web.login"))
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()
    return render_template("orders.html", orders=orders, user=user)

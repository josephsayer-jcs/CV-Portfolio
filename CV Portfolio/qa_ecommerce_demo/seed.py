from app import create_app, db
from app.models import User, Product

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(username="alice", email="alice@example.com"),
        User(username="bob", email="bob@example.com"),
    ]
    for user in users:
        user.set_password("Password123!")

    products = [
        Product(name="Mechanical Keyboard", description="Compact mechanical keyboard with hot-swappable switches.", price=89.99, stock=25, category="Accessories"),
        Product(name="Wireless Mouse", description="Ergonomic wireless mouse with programmable buttons.", price=39.99, stock=40, category="Accessories"),
        Product(name="27-inch Monitor", description="1440p IPS monitor suitable for development and gaming.", price=249.99, stock=12, category="Displays"),
        Product(name="USB-C Dock", description="Multi-port USB-C dock with HDMI and Ethernet.", price=119.00, stock=18, category="Accessories"),
        Product(name="Developer Laptop", description="14-inch developer laptop with 32GB RAM and 1TB SSD.", price=1299.00, stock=7, category="Computers"),
        Product(name="Noise Cancelling Headphones", description="Over-ear headphones with active noise cancellation.", price=199.50, stock=15, category="Audio"),
        Product(name="4K Webcam", description="4K webcam with automatic exposure and dual microphones.", price=129.95, stock=9, category="Accessories"),
        Product(name="Standing Desk", description="Electric standing desk with programmable height presets.", price=449.00, stock=5, category="Furniture"),
    ]
    db.session.add_all(users + products)
    db.session.commit()
    print("Database seeded.")


import datetime
from flask import Flask, jsonify, request, session, render_template_string, redirect, url_for
import uuid

app = Flask(__name__)
app.secret_key = 'secure_key_123'

# Backend Service with more features
class BackendService:
    def __init__(self):
        self.orders = []
        self.products = {
            "men": [
                {"id": 101, "name": "Naruto Hoodie", "price": 49.99, "image": "hoodie.jpg"},
                {"id": 102, "name": "One Piece T-Shirt", "price": 29.99, "image": "tshirt.jpg"},
                {"id": 103, "name": "DBZ Jacket", "price": 59.99, "image": "jacket.jpg"}
            ],
            "women": [
                {"id": 201, "name": "Sailor Moon Brooch", "price": 89.99, "image": "brooch.jpg"},
                {"id": 202, "name": "MHA Jacket", "price": 54.99, "image": "mha_jacket.jpg"}
            ]
        }
        self.featured = [101, 201]
        self.users = [
            {"username": "admin", "password": "admin123", "role": "admin", "status": "active"},
            {"username": "user", "password": "user123", "role": "customer", "status": "active"}
        ]

    def create_order(self, cart):
        order = {
            "order_id": f"ORD-{uuid.uuid4().hex[:6]}",
            "items": cart,
            "status": "Processing",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "total": sum(item['price'] * item['quantity'] for item in cart)
        }
        self.orders.append(order)
        return order

    def get_sales_report(self):
        if not self.orders: 
            return {"message": "No orders yet"}
        
        product_counts = {}
        for order in self.orders:
            for item in order['items']:
                product_counts[item['id']] = product_counts.get(item['id'], 0) + item['quantity']
        
        top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:2]
        return {
            "total_orders": len(self.orders),
            "total_revenue": sum(order['total'] for order in self.orders),
            "top_products": top_products
        }
    
    def authenticate(self, username, password):
        return next(
            (user for user in self.users 
             if user['username'] == username and user['password'] == password),
            None
        )

backend = BackendService()

# Template for consistent layout
def base_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Anime Store</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; }}
            .navbar {{ background-color: #4B0082; }}
            .card {{ transition: transform 0.2s; margin-bottom: 20px; }}
            .card:hover {{ transform: scale(1.03); }}
            .product-img {{ height: 200px; object-fit: cover; }}
            .banner {{ 
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                url('https://via.placeholder.com/1200x400');
                background-size: cover;
                color: white;
                padding: 100px 20px;
                text-align: center;
                margin-bottom: 30px;
            }}
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/">Anime Merch</a>
                <div class="collapse navbar-collapse">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="/products">Products</a></li>
                        <li class="nav-item"><a class="nav-link" href="/orders">Orders</a></li>
                        <li class="nav-item"><a class="nav-link" href="/admin">Admin</a></li>
                    </ul>
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/cart">
                                Cart ({len(session.get('cart', []))})
                            </a>
                        </li>
                        {session.get('user', '') and 
                         f'<li class="nav-item"><a class="nav-link" href="/logout">Logout</a></li>' or 
                         '<li class="nav-item"><a class="nav-link" href="/login">Login</a></li>'}
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Banner -->
        <div class="banner">
            <h1>Anime Merchandise Store</h1>
            <p>Your one-stop shop for exclusive anime products</p>
        </div>

        <!-- Main Content -->
        <div class="container">
            {content}
        </div>

        <!-- Footer -->
        <footer class="bg-dark text-white py-4 mt-5">
            <div class="container text-center">
                <p>&copy; 2023 Anime Merch. All rights reserved.</p>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

# Frontend Routes
@app.route('/')
def home():
    featured = [p for cat in backend.products.values() for p in cat if p['id'] in backend.featured]
    products_html = ''.join(
        f"""<div class="col-md-4">
            <div class="card">
                <img src="https://via.placeholder.com/300x200?text={p['name']}" class="card-img-top product-img">
                <div class="card-body">
                    <h5 class="card-title">{p['name']}</h5>
                    <p class="card-text">${p['price']}</p>
                    <a href="/add-to-cart/{p['id']}" class="btn btn-primary">Add to Cart</a>
                </div>
            </div>
        </div>""" 
        for p in featured
    )
    
    content = f"""
    <div class="row">
        <div class="col-md-8">
            <h2>Featured Products</h2>
            <div class="row">
                {products_html}
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h3>Categories</h3>
                    <div class="list-group">
                        {"".join(f'<a href="/products?category={cat}" class="list-group-item list-group-item-action">{cat.capitalize()}</a>' 
                         for cat in backend.products.keys())}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return base_template("Home", content)

@app.route('/products')
def products():
    category = request.args.get('category', 'all')
    products_html = ''
    
    for cat, items in backend.products.items():
        if category == 'all' or category == cat:
            products_html += f'<h3>{cat.capitalize()}</h3><div class="row">'
            for product in items:
                products_html += f"""
                <div class="col-md-4">
                    <div class="card">
                        <img src="https://via.placeholder.com/300x200?text={product['name']}" class="card-img-top product-img">
                        <div class="card-body">
                            <h5 class="card-title">{product['name']}</h5>
                            <p class="card-text">${product['price']}</p>
                            <a href="/add-to-cart/{product['id']}" class="btn btn-primary">Add to Cart</a>
                        </div>
                    </div>
                </div>
                """
            products_html += '</div>'
    
    content = f"""
    <h1>Products</h1>
    <div class="mb-4">
        <a href="/products?category=all" class="btn {'btn-primary' if category == 'all' else 'btn-outline-primary'} me-2">All</a>
        {"".join(f'<a href="/products?category={cat}" class="btn {'btn-primary' if category == cat else 'btn-outline-primary'} me-2">{cat.capitalize()}</a>' 
         for cat in backend.products.keys())}
    </div>
    {products_html}
    """
    return base_template("Products", content)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for cat in backend.products.values() for p in cat if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        item = next((item for item in cart if item['id'] == product_id), None)
        if item:
            item['quantity'] += 1
        else:
            cart.append({**product, "quantity": 1})
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    items_html = ''.join(
        f"""<tr>
            <td>{item['name']}</td>
            <td>${item['price']}</td>
            <td>{item['quantity']}</td>
            <td>${item['price'] * item['quantity']:.2f}</td>
            <td><a href="/remove-from-cart/{item['id']}" class="btn btn-sm btn-danger">Remove</a></td>
        </tr>""" 
        for item in cart
    ) or "<tr><td colspan='5'>Your cart is empty</td></tr>"
    
    content = f"""
    <h1>Your Shopping Cart</h1>
    <table class="table table-striped">
        <thead>
            <tr><th>Product</th><th>Price</th><th>Qty</th><th>Total</th><th>Action</th></tr>
        </thead>
        <tbody>
            {items_html}
        </tbody>
        <tfoot>
            <tr class="table-primary">
                <th colspan="3">Total</th>
                <th colspan="2">${total:.2f}</th>
            </tr>
        </tfoot>
    </table>
    <div class="text-end">
        <a href="/" class="btn btn-secondary">Continue Shopping</a>
        {"<a href='/checkout' class='btn btn-success ms-2'>Checkout</a>" if cart else ""}
    </div>
    """
    return base_template("Cart", content)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != product_id]
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('cart'))
    
    order = backend.create_order(cart)
    session['cart'] = []
    
    items_html = ''.join(
        f"<li>{item['name']} x {item['quantity']} - ${item['price'] * item['quantity']:.2f}</li>" 
        for item in order['items']
    )
    
    content = f"""
    <div class="text-center py-4">
        <div class="display-1 text-success">✓</div>
        <h1>Order Confirmed!</h1>
        <p class="lead">Thank you for your purchase</p>
        
        <div class="card mx-auto mt-4" style="max-width: 500px;">
            <div class="card-body">
                <h5>Order Details</h5>
                <p><strong>Order ID:</strong> {order['order_id']}</p>
                <p><strong>Date:</strong> {order['timestamp'][:10]}</p>
                <p><strong>Status:</strong> {order['status']}</p>
                <h6>Items:</h6>
                <ul>{items_html}</ul>
                <p class="h5">Total: ${order['total']:.2f}</p>
            </div>
        </div>
        
        <div class="mt-4">
            <a href="/" class="btn btn-primary">Continue Shopping</a>
            <a href="/orders" class="btn btn-outline-primary ms-2">View Orders</a>
        </div>
    </div>
    """
    return base_template("Order Confirmed", content)

@app.route('/orders')
def orders():
    orders_html = ''.join(
        f"""<div class="card mb-3">
            <div class="card-header">
                Order #{order['order_id']} - {order['timestamp'][:10]}
                <span class="badge bg-primary float-end">{order['status']}</span>
            </div>
            <div class="card-body">
                <ul>
                    {"".join(f"<li>{item['name']} x {item['quantity']}</li>" for item in order['items'])}
                </ul>
                <p class="h5">Total: ${order['total']:.2f}</p>
            </div>
        </div>""" 
        for order in backend.orders
    ) or "<div class='alert alert-info'>No orders yet</div>"
    
    content = f"""
    <h1>Your Orders</h1>
    {orders_html}
    """
    return base_template("Your Orders", content)

@app.route('/admin')
def admin():
    if not session.get('user') or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    
    report = backend.get_sales_report()
    report_html = ""
    
    if 'message' in report:
        report_html = f"<p>{report['message']}</p>"
    else:
        report_html = f"""
        <p><strong>Total Orders:</strong> {report['total_orders']}</p>
        <p><strong>Total Revenue:</strong> ${report['total_revenue']:.2f}</p>
        <h5>Top Products:</h5>
        <ul>
            {"".join(f"<li>Product {pid}: {qty} sold</li>" for pid, qty in report['top_products'])}
        </ul>
        """
    
    content = f"""
    <h1>Admin Dashboard</h1>
    <div class="card">
        <div class="card-body">
            <h3>Sales Report</h3>
            {report_html}
        </div>
    </div>
    """
    return base_template("Admin", content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = backend.authenticate(username, password)
        if user:
            session['user'] = {"username": user['username'], "role": user['role']}
            return redirect(url_for('admin'))
        error = "Invalid credentials"
    
    content = f"""
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="text-center">Admin Login</h2>
                    {error and f'<div class="alert alert-danger">{error}</div>'}
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """
    return base_template("Login", content)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

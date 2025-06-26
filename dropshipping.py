import datetime
from flask import Flask, jsonify, request, session
import uuid
import random
import datetime
app = Flask(__name__)
app.secret_key = 'ksss'


# ===== BACKEND SERVICE =====
class BackendService:
    def __init__(self):
        self.orders = []
        self.products = {
            "men": [
                {"id": 101, "name": "Naruto Hoodie", "price": 49.99},
                {"id": 102, "name": "One Piece T-Shirt", "price": 29.99},
                {"id": 103, "name": "DBZ Jacket", "price": 59.99},
                {"id": 104, "name": "AOT Jacket", "price": 69.99}
            ],
            "women": [
                {"id": 201, "name": "Sailor Moon Brooch", "price": 89.99},
                {"id": 202, "name": "MHA Jacket", "price": 54.99},
                {"id": 203, "name": "Nezuko Kimono", "price": 74.99},
                {"id": 204, "name": "JJK Fingercaps", "price": 39.99}
            ]
        }
        self.featured_products = [101, 201]
        self.users = [
            {"username": "admin", "role": "admin", "status": "active"},
            {"username": "manager", "role": "marketing", "status": "active"}
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
            "top_products": [{"id": pid, "quantity": qty} for pid, qty in top_products]
        }

backend = BackendService()

# ===== REQUIREMENTS DOCUMENTATION =====
REQUIREMENTS = {
    "stakeholders": [
        {
            "name": "Customer",
            "functional": [
                "Browse products by category",
                "Add products to shopping cart",
                "View shopping cart contents",
                "Remove items from cart",
                "Complete checkout process"
            ],
            "non_functional": [
                "Product images load within 2 seconds",
                "Checkout process completes within 10 seconds"
            ]
        },
        {
            "name": "Marketing Manager",
            "functional": [
                "View sales reports",
                "Update featured products",
                "Track product popularity",
                "Manage promotional campaigns",
                "Analyze customer demographics"
            ],
            "non_functional": [
                "Sales report generation under 5 seconds",
                "System available 99.9% of business hours"
            ]
        }
    ],
    "use_cases": [
        "View product catalog",
        "Add item to shopping cart",
        "Remove item from shopping cart",
        "Checkout and create order",
        "Generate sales report",
        "Update featured products",
        "View system requirements",
        "Toggle user status"
    ]
}

# ===== API ENDPOINTS =====

# ----- Core Functionality -----
@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category and category in backend.products:
        return jsonify(backend.products[category])
    return jsonify(backend.products)



@app.route('/api/cart', methods=['GET', 'POST'])
def manage_cart():
    if request.method == 'GET':
        return jsonify(session.get('cart', []))
    
    # POST - Add to cart
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Find product
    product = next(
        (p for cat in backend.products.values() for p in cat if p['id'] == product_id),
        None
    )
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Get or create cart
    cart = session.get('cart', [])
    
    # Update if exists
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            session['cart'] = cart
            return jsonify({"message": "Item quantity updated", "cart": cart})
    
    # Add new item
    cart.append({**product, "quantity": quantity})
    session['cart'] = cart
    return jsonify({"message": "Item added to cart", "cart": cart}), 201

@app.route('/')
def index():
    return "Welcome to the Dropshipping API!"

@app.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_item(product_id):
    cart = session.get('cart', [])
    new_cart = [item for item in cart if item['id'] != product_id]
    
    if len(new_cart) == len(cart):
        return jsonify({"error": "Item not in cart"}), 404
    
    session['cart'] = new_cart
    return jsonify({"message": "Item removed", "cart": new_cart})

@app.route('/api/orders', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'GET':
        return jsonify(backend.orders)
    
    # POST - Create order
    cart = session.get('cart', [])
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    
    order = backend.create_order(cart)
    session['cart'] = []  # Clear cart
    return jsonify({"message": "Order created", "order": order}), 201

# ----- Admin & Reports -----
@app.route('/api/reports/sales', methods=['GET'])
def sales_report():
    return jsonify(backend.get_sales_report())

@app.route('/api/admin/users', methods=['GET', 'PUT'])
def manage_users():
    if request.method == 'GET':
        return jsonify(backend.users)
    
    # PUT - Toggle user status
    data = request.json
    username = data.get('username')
    user = next((u for u in backend.users if u['username'] == username), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user['status'] = 'inactive' if user['status'] == 'active' else 'active'
    return jsonify({"message": "User status updated", "user": user})

# ----- Requirements Documentation -----
@app.route('/api/requirements', methods=['GET'])
def get_requirements():
    return jsonify(REQUIREMENTS)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
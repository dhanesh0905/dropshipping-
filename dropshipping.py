import tkinter as tk
import ttkbootstrap as ttk
import uuid, random, time, requests, webbrowser
from PIL import Image
from io import BytesIO
import threading

# ===== BACKEND SERVICE =====
class BackendService:
    def __init__(self):
        self.orders = []
        self.users = [
            {"username": "admin", "role": "admin", "status": "active"},
            {"username": "manager", "role": "marketing", "status": "active"},
            {"username": "customer1", "role": "customer", "status": "active"},
        ]
        self.products = {
            "men": self._create_products([
                (101, "Naruto Hoodie", 49.99, 
                 "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw1f373bf1/Apparel/KWM257PNAR%20-%20Naruto%20Shippuden%20-%20Akatsuki%20Cloud%20Cardigan/bioworld-hoodies-outerwear-naruto-shippuden-akatsuki-cloud-cardigan-31788842123308%20(1).jpg",
                 "https://store.crunchyroll.com/products/naruto-shippuden-akatsuki-cloud-cardigan-KWM257PNAR.html"),
                (102, "One Piece T-Shirt", 29.99,
                 "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dwad8fb8d2/Apparel/OPNS2737/ripple-junction-unisex-t-shirts-one-piece-straw-hat-crew-laughs-crunchyroll-exclusive-31651028336684.jpg",
                 "https://store.crunchyroll.com/products/one-piece-straw-hat-crew-laughs-t-shirt-crunchyroll-exclusive-OPNS2737.html"),
                (103, "DBZ Jacket", 59.99,
                 "https://store.crunchyroll.com/dw/image/v2/BDGC_PRD/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw9d87bce5/images/HDA2GUHDBZ_dragon-ball-z-goku-full-zip-hoodie_5.jpg?sw=300&sh=300&sm=fit",
                 "https://store.crunchyroll.com/products/dragon-ball-z-goku-full-zip-hoodie-HDA2GUHDBZ.html"),
                (104, "AOT Jacket", 69.99,
                 "https://store.crunchyroll.com/dw/image/v2/BDGC_PRD/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dwd6f334b8/Apparel/CBXAOTSG05/CBXAOT-SG-05.jpg?sw=300&sh=300&sm=fit",
                 "https://store.crunchyroll.com/products/attack-on-titan-x-color-bars-loaded-logo-hoodie-CBXAOTSG05.html")
            ]),
            "women": self._create_products([
                (201, "Sailor Moon Brooch", 89.99,
                 "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw36e3c868/rightstuf/782009243960_anime-sailor-moon-crystal-1-limited-edition-gwp-primary.jpg",
                 "https://store.crunchyroll.com/products/sailor-moon-crystal-set-1-limited-edition-blu-raydvd-782009243960.html"),
                (202, "MHA Jacket", 54.99,
                 "https://cdn.animebape.com/wp-content/uploads/2023/04/school-uniform-my-hero-academia-casual-bomber-jacket-96cvn.jpg",
                 "https://animebape.com/products/anime-school-uniform-my-hero-academia-casual-bomber-jacket-2/"),
                (203, "Nezuko Kimono", 74.99,
                 "https://img.fruugo.com/product/5/97/1692850975_0340_0340.jpg",
                 "https://www.fruugo.de/erwachsene-kind-damon-slayer-cosplay-kimono-haori-anime-kimetsu-no-yaiba-kamado-nezuko-kochou-shinobu-cosplay-kostum-sommer-mantel/p-237632505-509301387"),
                (204, "JJK Fingercaps", 39.99,
                 "https://cdn.animebape.com/wp-content/uploads/2024/09/sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight-27bx3.jpg",
                 "https://animebape.com/products/anime-sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight/")
            ])
        }
    
    def _create_products(self, items):
        return [{"id": i[0], "name": i[1], "price": i[2], "image": i[3], "source": i[4]} for i in items]
    
    def get_products(self): return self.products
    
    def create_order(self, cart):
        order = {
            "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
            "items": cart,
            "status": "Processing",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": sum(item['price'] * item['quantity'] for item in cart)
        }
        self.orders.append(order)
        return order

    def get_sales_report(self):
        if not self.orders: return "No orders yet"
        
        product_counts = {}
        for order in self.orders:
            for item in order['items']:
                product_counts[item['id']] = product_counts.get(item['id'], 0) + item['quantity']
        
        top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        report = [
            "===== SALES REPORT =====",
            f"Total Orders: {len(self.orders)}",
            f"Total Revenue: ${sum(order['total'] for order in self.orders):.2f}",
            "\nTop Selling Products:"
        ]
        
        for pid, qty in top_products:
            name = next((p['name'] for cat in self.products.values() for p in cat if p['id'] == pid), "Unknown")
            report.append(f" - {name}: {qty} sold")
        
        return "\n".join(report)

    def get_system_health(self):
        return {
            "cpu": random.randint(10, 80),
            "memory": random.randint(30, 95),
            "disk": random.randint(40, 90),
            "status": "OK" if random.random() > 0.1 else "WARNING"
        }

    def get_users(self): return self.users

    def toggle_user_status(self, username):
        for user in self.users:
            if user["username"] == username:
                user["status"] = "inactive" if user["status"] == "active" else "active"
                return True
        return False

# ===== FRONTEND APPLICATION =====
class AnimeStyleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 AnimeStyle Dropship")
        self.root.geometry("1000x700")
        self.cart = []
        self.backend = BackendService()
        self.product_images = {}
        
        self.notebook = ttk.Notebook(root, style="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_tabs()
        threading.Thread(target=self.load_images, daemon=True).start()

    def create_tabs(self):
        # Home tab
        home = ttk.Frame(self.notebook)
        self.notebook.add(home, text="🏠 Home")
        ttk.Label(home, text="🌸 AnimeStyle Dropship", font=("Arial", 20, "bold"), 
                 bootstyle="inverse-primary", padding=10).pack(fill="x")
        
        cat_frame = ttk.Frame(home)
        cat_frame.pack(fill="x", pady=10)
        ttk.Label(cat_frame, text="Browse:").pack(side="left", padx=10)
        
        self.cat_var = tk.StringVar(value="all")
        for text, val in [("All", "all"), ("Men", "men"), ("Women", "women")]:
            ttk.Radiobutton(cat_frame, text=text, variable=self.cat_var, 
                           value=val, command=self.show_products).pack(side="left", padx=5)
        
        self.product_container = ttk.Frame(home)
        self.product_container.pack(fill="both", expand=True)
        ttk.Label(self.product_container, text="Loading products...", 
                 font=("Arial", 14)).pack(pady=50)

        # Cart tab
        self.cart_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cart_frame, text="🛒 Cart (0)")
        self.cart_content = ttk.Frame(self.cart_frame)
        self.cart_content.pack(fill="both", expand=True)
        self.show_cart()

        # Requirements tab
        req = ttk.Frame(self.notebook)
        self.notebook.add(req, text="📋 Requirements")
        content = """STAKEHOLDERS & REQUIREMENTS
        
👨‍💼 Store Manager:
- Inventory management
- Order processing
- Sales analytics

👩 Customer:
- Product browsing
- Shopping cart
- Checkout process

👨‍💼 Marketing Manager:
Functional:
1. Update featured products
2. Track product popularity
3. Manage promotional campaigns
4. Analyze customer demographics
5. Generate sales reports

Non-Functional:
1. Report generation < 5 seconds
2. Campaign updates without downtime

👨‍💻 System Administrator:
Functional:
1. Monitor system health
2. Manage user accounts
3. Configure system settings
4. Perform backups
5. View audit logs

Non-Functional:
1. 99.9% uptime SLA
2. Real-time health monitoring"""
        ttk.Label(req, text=content, font=("Arial", 11), 
                 padding=20).pack(fill="both", expand=True)

        # Marketing tab
        market = ttk.Frame(self.notebook)
        self.notebook.add(market, text="📊 Marketing")
        ttk.Label(market, text="Marketing Dashboard", font=("Arial", 16, "bold"), 
                 bootstyle="inverse-primary", padding=5).pack(fill="x")
        
        ttk.Labelframe(market, text="Sales Analytics", padding=10).pack(fill="x", pady=10, padx=10)
        ttk.Button(market, text="Generate Sales Report", 
                  command=lambda: ttk.dialogs.Messagebox.show_info(
                      self.backend.get_sales_report(), "Sales Report", parent=market)
                  ).pack(pady=10)
        
        manage_frame = ttk.Labelframe(market, text="Product Management", padding=10)
        manage_frame.pack(fill="x", pady=10, padx=10)
        ttk.Label(manage_frame, text="Featured Products:").pack(anchor="w", padx=10, pady=5)
        
        self.featured_var = tk.StringVar(value="101")
        for cat in self.backend.get_products().values():
            for p in cat:
                ttk.Radiobutton(manage_frame, text=p["name"], variable=self.featured_var,
                               value=str(p["id"])).pack(anchor="w", padx=20)
        
        ttk.Button(manage_frame, text="Update Featured Products", bootstyle="danger",
                  command=lambda: ttk.dialogs.Messagebox.show_info("Featured products updated!", "Success")
                  ).pack(pady=10)

        # Admin tab
        admin = ttk.Frame(self.notebook)
        self.notebook.add(admin, text="⚙️ Admin")
        ttk.Label(admin, text="System Administration", font=("Arial", 16, "bold"), 
                 bootstyle="inverse-primary", padding=5).pack(fill="x")
        
        health_frame = ttk.Labelframe(admin, text="System Health", padding=10)
        health_frame.pack(fill="x", pady=10, padx=10)
        
        self.health_labels = {
            k: ttk.Label(health_frame, text=f"{k.upper()}: --") for k in ["cpu", "memory", "disk"]
        }
        self.health_labels["status"] = ttk.Label(health_frame, text="Status: --", font=("Arial", 10, "bold"))
        for label in self.health_labels.values():
            label.pack(anchor="w", padx=10, pady=2)
        
        ttk.Button(health_frame, text="Refresh Health", bootstyle="primary",
                  command=self.update_system_health).pack(pady=10)
        
        user_frame = ttk.Labelframe(admin, text="User Management", padding=10)
        user_frame.pack(fill="x", pady=10, padx=10)
        ttk.Label(user_frame, text="User Accounts:").pack(anchor="w", padx=10, pady=5)
        
        self.user_list_frame = ttk.Frame(user_frame)
        self.user_list_frame.pack(fill="x", padx=10, pady=5)
        self.update_user_list()
        
        ttk.Button(user_frame, text="Perform System Backup", bootstyle="danger",
                  command=lambda: ttk.dialogs.Messagebox.show_info("System backup completed!", "Backup")
                  ).pack(pady=10)

    def load_images(self):
        for cat in self.backend.get_products().values():
            for p in cat:
                try:
                    img = Image.open(BytesIO(requests.get(p["image"]).content))
                    img = img.resize((150, 150), Image.LANCZOS)
                    self.product_images[p["id"]] = tk.PhotoImage(img)
                except:
                    placeholder = Image.new('RGB', (150, 150), '#e0e0e0')
                    self.product_images[p["id"]] = tk.PhotoImage(placeholder)
        self.show_products()

    def update_user_list(self):
        for w in self.user_list_frame.winfo_children(): w.destroy()
        for user in self.backend.get_users():
            frame = ttk.Frame(self.user_list_frame)
            frame.pack(fill="x", pady=2)
            status = "active" if user["status"] == "active" else "inactive"
            ttk.Label(frame, text=f"{user['username']} ({user['role']})", width=20).pack(side="left", padx=5)
            ttk.Label(frame, text=status, bootstyle="success" if status == "active" else "danger", width=10).pack(side="left", padx=5)
            ttk.Button(frame, text="Toggle Status", command=lambda u=user['username']: self.toggle_user(u)).pack(side="right", padx=5)

    def toggle_user(self, username):
        if self.backend.toggle_user_status(username):
            self.update_user_list()
            ttk.dialogs.Messagebox.show_info(f"User {username} status updated", "Success")
        else:
            ttk.dialogs.Messagebox.show_error("User not found", "Error")

    def update_system_health(self):
        health = self.backend.get_system_health()
        for k in ["cpu", "memory", "disk"]:
            self.health_labels[k].config(text=f"{k.upper()}: {health[k]}%")
        self.health_labels["status"].config(
            text=f"Status: {health['status']}", 
            bootstyle="success" if health["status"] == "OK" else "warning"
        )

    def show_products(self):
        for w in self.product_container.winfo_children(): w.destroy()
        products = self.backend.get_products()
        cat = self.cat_var.get()
        plist = products["men"] + products["women"] if cat == "all" else products[cat]
        
        for i, p in enumerate(plist):
            row, col = divmod(i, 2)
            frame = ttk.Frame(self.product_container, padding=10, relief="groove")
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            img = self.product_images.get(p["id"])
            (ttk.Label(frame, image=img).pack() if img else 
             ttk.Label(frame, text="Image Loading...", width=20, height=8).pack())
            
            ttk.Label(frame, text=p["name"], font=("Arial", 11, "bold")).pack()
            ttk.Label(frame, text=f"${p['price']:.2f}", bootstyle="danger").pack()
            
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill="x", pady=5)
            ttk.Button(btn_frame, text="Add to Cart", bootstyle="primary",
                      command=lambda p=p: self.add_to_cart(p)).pack(side="left")
            ttk.Button(btn_frame, text="Details", bootstyle="secondary",
                      command=lambda url=p["source"]: webbrowser.open(url)).pack(side="left", padx=5)
        
        self.product_container.columnconfigure(0, weight=1)
        self.product_container.columnconfigure(1, weight=1)

    def add_to_cart(self, product):
        for item in self.cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                ttk.dialogs.Messagebox.show_info(f"Added another {product['name']}!", "Cart Updated")
                self.update_cart()
                return
        self.cart.append({**product, "quantity": 1})
        ttk.dialogs.Messagebox.show_info(f"Added {product['name']} to cart!", "Added")
        self.update_cart()

    def remove_from_cart(self, pid):
        self.cart = [item for item in self.cart if item['id'] != pid]
        self.update_cart()
        self.show_cart()

    def update_cart(self):
        total = sum(item['quantity'] for item in self.cart)
        self.notebook.tab(1, text=f"🛒 Cart ({total})")
        self.show_cart()

    def show_cart(self):
        for w in self.cart_content.winfo_children(): w.destroy()
        
        if not self.cart:
            ttk.Label(self.cart_content, text="🛒 Your Cart", font=("Arial", 18, "bold")).pack(pady=10)
            ttk.Label(self.cart_content, text="Your cart is empty", font=("Arial", 14)).pack(pady=50)
            ttk.Button(self.cart_content, text="Browse Products", command=lambda: self.notebook.select(0)).pack()
            return
        
        ttk.Label(self.cart_content, text="🛒 Your Cart", font=("Arial", 18, "bold")).pack(pady=10)
        for item in self.cart:
            frame = ttk.Frame(self.cart_content, padding=10, relief="groove")
            frame.pack(fill="x", padx=20, pady=5)
            
            ttk.Label(frame, text=item["name"], font=("Arial", 12, "bold")).pack(fill="x", anchor="w")
            ttk.Label(frame, text=f"${item['price']:.2f} × {item['quantity']}").pack(fill="x", anchor="w")
            ttk.Label(frame, text=f"Total: ${item['price'] * item['quantity']:.2f}").pack(fill="x", anchor="w")
            ttk.Button(frame, text="Remove", bootstyle="danger", 
                      command=lambda id=item["id"]: self.remove_from_cart(id)).pack(anchor="e")
        
        ttk.Button(self.cart_content, text="Checkout", font=("Arial", 14), 
                  bootstyle="primary", command=self.process_checkout).pack(pady=20)

    def process_checkout(self):
        order = self.backend.create_order(self.cart)
        ttk.dialogs.Messagebox.show_info(f"Thank you!\nOrder ID: {order['order_id']}", "Order Placed")
        self.cart = []
        self.update_cart()

if __name__ == "__main__":
    root = ttk.Window(themename="morph")
    AnimeStyleApp(root)
    root.mainloop()
    
    
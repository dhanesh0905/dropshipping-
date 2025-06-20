import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import uuid
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

# ===== BACKEND SERVICE =====
class BackendService:
    def __init__(self):
     products = {
    "men": [
        {
            "id": 101,
            "name": "Naruto Akatsuki Cloud Hoodie",
            "price": 49.99,
            "description": "Officially licensed black hoodie with red cloud pattern",
            "tags": ["Naruto", "Hoodie", "Popular"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw1f373bf1/Apparel/KWM257PNAR%20-%20Naruto%20Shippuden%20-%20Akatsuki%20Cloud%20Cardigan/bioworld-hoodies-outerwear-naruto-shippuden-akatsuki-cloud-cardigan-31788842123308%20(1).jpg",
            "source": "https://store.crunchyroll.com/products/naruto-shippuden-akatsuki-cloud-cardigan-KWM257PNAR.html"
        },
        {
            "id": 102,
            "name": "One Piece Straw Hat Pirates T-Shirt",
            "price": 29.99,
            "description": "Premium cotton t-shirt with Jolly Roger emblem",
            "tags": ["One Piece", "T-Shirt", "Cotton"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dwad8fb8d2/Apparel/OPNS2737/ripple-junction-unisex-t-shirts-one-piece-straw-hat-crew-laughs-crunchyroll-exclusive-31651028336684.jpg",
            "source": "https://store.crunchyroll.com/products/one-piece-straw-hat-crew-laughs-t-shirt-crunchyroll-exclusive-OPNS2737.html"
        },
        {
            "id": 103,
            "name": "Dragon Ball Z Goku Gi Jacket",
            "price": 59.99,
            "description": "Orange windbreaker with Turtle School insignia",
            "tags": ["DBZ", "Jacket", "Goku"],
            "image": "https://store.crunchyroll.com/dw/image/v2/BDGC_PRD/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw9d87bce5/images/HDA2GUHDBZ_dragon-ball-z-goku-full-zip-hoodie_5.jpg?sw=300&sh=300&sm=fit",
            "source": "https://store.crunchyroll.com/products/dragon-ball-z-goku-full-zip-hoodie-HDA2GUHDBZ.html"
        },
        {
            "id": 104,
            "name": "Attack on Titan Survey Corps Jacket",
            "price": 69.99,
            "description": "Military-style jacket with Wings of Freedom emblem",
            "tags": ["AOT", "Jacket", "Scout"],
            "image": "https://store.crunchyroll.com/dw/image/v2/BDGC_PRD/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dwd6f334b8/Apparel/CBXAOTSG05/CBXAOT-SG-05.jpg?sw=300&sh=300&sm=fit",
            "source": "https://store.crunchyroll.com/products/attack-on-titan-x-color-bars-loaded-logo-hoodie-CBXAOTSG05.html"
        }
    ],
    "women": [
        {
            "id": 201,
            "name": "Sailor Moon Transformation Brooch Set",
            "price": 89.99,
            "description": "Authentic replica brooches with display case",
            "tags": ["Sailor Moon", "Jewelry", "Collectible"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw36e3c868/rightstuf/782009243960_anime-sailor-moon-crystal-1-limited-edition-gwp-primary.jpg",
            "source": "https://store.crunchyroll.com/products/sailor-moon-crystal-set-1-limited-edition-blu-raydvd-782009243960.html"
        },
        {
            "id": 202,
            "name": "My Hero Academia UA Track Jacket",
            "price": 54.99,
            "description": "Athletic jacket with UA High School logo",
            "tags": ["MHA", "Jacket", "Sportswear"],
            "image": "https://cdn.animebape.com/wp-content/uploads/2023/04/school-uniform-my-hero-academia-casual-bomber-jacket-96cvn.jpg",
            "source": "https://animebape.com/products/anime-school-uniform-my-hero-academia-casual-bomber-jacket-2/"
        },
        {
            "id": 203,
            "name": "Demon Slayer Nezuko Kimono Robe",
            "price": 74.99,
            "description": "Silk blend kimono with floral pattern",
            "tags": ["Kimetsu", "Robe", "Loungewear"],
            "image": "https://img.fruugo.com/product/5/97/1692850975_0340_0340.jpg",
            "source": "https://www.fruugo.de/erwachsene-kind-damon-slayer-cosplay-kimono-haori-anime-kimetsu-no-yaiba-kamado-nezuko-kochou-shinobu-cosplay-kostum-sommer-mantel/p-237632505-509301387"
        },
        {
            "id": 204,
            "name": "Jujutsu Kaisen Sukuna Fingercaps",
            "price": 39.99,
            "description": "Resin fingercaps with intricate details",
            "tags": ["JJK", "Accessory", "Cosplay"],
            "image": "https://cdn.animebape.com/wp-content/uploads/2024/09/sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight-27bx3.jpg",
            "source": "https://animebape.com/products/anime-sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight/"
        }
    ]
}
    
    def get_products(self):
        """Get all products"""
        return self.products
    
    def create_order(self, cart):
        """Create new order"""
        return {
            "order_id": f"ORD-{str(uuid.uuid4())[:8].upper()}",
            "items": cart,
            "status": "Processing"
        }

# ===== FRONTEND APPLICATION =====
THEME_COLOR = "#6a0dad"
ACCENT_COLOR = "#ff6b6b"
BG_COLOR = "#f8f0ff"

class AnimeStyleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 AnimeStyle Dropship")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)
        self.cart = []
        self.backend = BackendService()
        self.product_images = {}
        
        self.setup_ui()
        self.load_images_async()

    def setup_ui(self):
        """Setup main UI components"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_home_tab()
        self.create_cart_tab()
        self.create_requirements_tab()

    def load_images_async(self):
        """Load product images in background thread"""
        def load_task():
            for cat in self.backend.products.values():
                for product in cat:
                    try:
                        response = requests.get(product["image"], timeout=5)
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((150, 150), Image.LANCZOS)
                        self.product_images[product["id"]] = ImageTk.PhotoImage(img)
                    except Exception:
                        pass
            self.show_products()
        
        threading.Thread(target=load_task, daemon=True).start()

    def create_home_tab(self):
        """Create product browsing tab"""
        self.home_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.home_frame, text="🏠 Home")
        
        header = tk.Frame(self.home_frame, bg=THEME_COLOR)
        header.pack(fill="x", pady=10)
        tk.Label(header, text="🌸 AnimeStyle Dropship", 
                 font=("Arial", 20, "bold"), fg="white", bg=THEME_COLOR).pack(pady=10)
        
        cat_frame = tk.Frame(self.home_frame, bg=BG_COLOR)
        cat_frame.pack(fill="x", pady=10)
        tk.Label(cat_frame, text="Browse:", bg=BG_COLOR).pack(side="left", padx=10)
        
        self.cat_var = tk.StringVar(value="all")
        for text, val in [("All", "all"), ("Men", "men"), ("Women", "women")]:
            tk.Radiobutton(cat_frame, text=text, variable=self.cat_var, 
                          value=val, command=self.show_products, 
                          bg=BG_COLOR).pack(side="left", padx=5)
        
        self.product_container = tk.Frame(self.home_frame, bg=BG_COLOR)
        self.product_container.pack(fill="both", expand=True)
        
        # Show loading message
        tk.Label(self.product_container, text="Loading products...", 
                 font=("Arial", 14), bg=BG_COLOR).pack(pady=50)

    def create_cart_tab(self):
        """Create shopping cart tab"""
        self.cart_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cart_frame, text="🛒 Cart (0)")
        self.cart_content = tk.Frame(self.cart_frame, bg=BG_COLOR)
        self.cart_content.pack(fill="both", expand=True)
        self.show_cart()

    def create_requirements_tab(self):
        """Create requirements documentation tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Requirements")
        
        content = """
        STAKEHOLDERS & REQUIREMENTS
        
        👨‍💼 Store Manager:
        - Inventory management
        - Order processing
        - Sales analytics
        
        👩 Customer:
        - Product browsing
        - Shopping cart
        - Checkout process
        
        SYSTEM FEATURES:
        1. Product catalog
        2. Shopping cart
        3. Order management
        4. Responsive design
        5. RESTful backend
        """
        
        tk.Label(frame, text=content, font=("Arial", 11), 
                justify="left", padx=20, pady=20).pack(fill="both", expand=True)

    def show_products(self):
        """Display products based on selected category"""
        for widget in self.product_container.winfo_children():
            widget.destroy()
        
        # Get products from backend
        products = self.backend.get_products()
        category = self.cat_var.get()
        product_list = (products["men"] + products["women"] if category == "all" 
                        else products[category])
        
        # Display products in grid
        for i, product in enumerate(product_list):
            row, col = divmod(i, 2)
            frame = tk.Frame(self.product_container, bg="white", 
                            relief="groove", padx=10, pady=10)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Product image
            img = self.product_images.get(product["id"])
            if img:
                tk.Label(frame, image=img, bg="white").pack()
            
            # Product info
            tk.Label(frame, text=product["name"], 
                    font=("Arial", 11, "bold"), bg="white").pack()
            tk.Label(frame, text=f"${product['price']:.2f}", 
                    font=("Arial", 10), fg=ACCENT_COLOR, bg="white").pack()
            
            # Action buttons
            btn_frame = tk.Frame(frame, bg="white")
            btn_frame.pack(fill="x", pady=5)
            
            tk.Button(btn_frame, text="Add to Cart", bg=THEME_COLOR, fg="white",
                     command=lambda p=product: self.add_to_cart(p)).pack(side="left")
            tk.Button(btn_frame, text="Details", bg=ACCENT_COLOR, fg="white",
                     command=lambda url=product["source"]: webbrowser.open(url)).pack(side="left", padx=5)
        
        # Configure grid columns
        self.product_container.columnconfigure(0, weight=1)
        self.product_container.columnconfigure(1, weight=1)

    def add_to_cart(self, product):
        """Add product to cart"""
        for item in self.cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                messagebox.showinfo("Cart Updated", f"Added another {product['name']}!")
                self.update_cart_tab()
                return
        
        self.cart.append({**product, "quantity": 1})
        messagebox.showinfo("Added", f"Added {product['name']} to cart!")
        self.update_cart_tab()

    def remove_from_cart(self, product_id):
        """Remove product from cart"""
        self.cart = [item for item in self.cart if item['id'] != product_id]
        self.update_cart_tab()
        self.show_cart()

    def update_cart_tab(self):
        """Update cart tab label"""
        total_items = sum(item['quantity'] for item in self.cart)
        self.notebook.tab(1, text=f"🛒 Cart ({total_items})")

    def show_cart(self):
        """Display cart contents"""
        for widget in self.cart_content.winfo_children():
            widget.destroy()
        
        tk.Label(self.cart_content, text="🛒 Your Cart", 
                font=("Arial", 18, "bold"), bg=BG_COLOR).pack(pady=10)
        
        if not self.cart:
            tk.Label(self.cart_content, text="Your cart is empty", 
                    font=("Arial", 14), bg=BG_COLOR).pack(pady=50)
            tk.Button(self.cart_content, text="Browse Products", 
                     command=lambda: self.notebook.select(0)).pack()
            return
        
        # Display cart items
        for item in self.cart:
            frame = tk.Frame(self.cart_content, bg="white", 
                            relief="groove", padx=10, pady=10)
            frame.pack(fill="x", padx=20, pady=5)
            
            tk.Label(frame, text=item["name"], 
                    font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x")
            tk.Label(frame, text=f"${item['price']:.2f} × {item['quantity']}", 
                    font=("Arial", 11), bg="white", anchor="w").pack(fill="x")
            tk.Label(frame, text=f"Total: ${item['price'] * item['quantity']:.2f}", 
                    font=("Arial", 11), bg="white", anchor="w").pack(fill="x")
            
            tk.Button(frame, text="Remove", bg=ACCENT_COLOR, fg="white",
                     command=lambda id=item["id"]: self.remove_from_cart(id)).pack(anchor="e")
        
        # Checkout button
        tk.Button(self.cart_content, text="Checkout", 
                 font=("Arial", 14), bg=THEME_COLOR, fg="white",
                 command=self.process_checkout).pack(pady=20)

    def process_checkout(self):
        """Process order checkout"""
        order = self.backend.create_order(self.cart)
        messagebox.showinfo("Order Placed", 
                          f"Thank you for your order!\n\nOrder ID: {order['order_id']}")
        self.cart = []
        self.update_cart_tab()
        self.show_cart()

# ===== RUN APPLICATION =====
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeStyleApp(root)
    root.mainloop()
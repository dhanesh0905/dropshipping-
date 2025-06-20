import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# ======================================
#  APP CONFIGURATION
# ======================================
st.set_page_config(
    page_title="AnimeStyle Dropship",
    page_icon="🌸",
    layout="wide"
)
ITEMS_PER_PAGE = 8
SHIPPING_THRESHOLD = 100
TAX_RATE = 0.08

# ======================================
#  PRODUCT DATA
# ======================================
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

# ======================================
#  UTILITY FUNCTIONS
# ======================================
@st.cache_data(show_spinner=False)
def load_image(url):
    """Load and cache product images"""
    try:
        response = requests.get(url, timeout=5)
        return Image.open(BytesIO(response.content))
    except Exception:
        return None

def init_session():
    """Initialize session state variables"""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    if 'product_page' not in st.session_state:
        st.session_state.product_page = 0
    if 'checkout_step' not in st.session_state:
        st.session_state.checkout_step = 0

def add_to_cart(product):
    """Add product to shopping cart"""
    for item in st.session_state.cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            st.success(f"Added another {product['name']} to cart!")
            return
            
    st.session_state.cart.append({**product, "quantity": 1})
    st.success(f"Added {product['name']} to cart!")

def remove_from_cart(product_id):
    """Remove product from shopping cart"""
    st.session_state.cart = [item for item in st.session_state.cart if item['id'] != product_id]

def calculate_order():
    """Calculate order totals"""
    cart = st.session_state.cart
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    shipping = 0 if subtotal >= SHIPPING_THRESHOLD else 9.99
    tax = subtotal * TAX_RATE
    grand_total = subtotal + shipping + tax
    return subtotal, shipping, tax, grand_total

# ======================================
#  UI COMPONENTS
# ======================================
def product_card(product):
    """Display product card"""
    col1, col2 = st.columns([1, 3])
    with col1:
        if image := load_image(product["image"]):
            st.image(image, use_container_width=True)
    
    with col2:
        st.subheader(product["name"])
        st.markdown(f"**${product['price']:.2f}**")
        st.caption(product["description"])
        st.caption(" ".join(f"`{tag}`" for tag in product["tags"]))
        st.markdown(f"[Product Details]({product['source']})")
        
        if st.button("🛒 Add to Cart", key=f"add_{product['id']}", use_container_width=True):
            add_to_cart(product)

def render_products(product_list, title):
    """Render product grid with pagination"""
    st.header(title)
    page = st.session_state.product_page
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, len(product_list))
    
    for i in range(start_idx, end_idx, 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < end_idx:
                with cols[j]:
                    product_card(product_list[i + j])
    
    # Pagination controls
    if len(product_list) > ITEMS_PER_PAGE:
        prev, _, next_ = st.columns([1, 8, 1])
        if page > 0 and prev.button("← Previous", use_container_width=True):
            st.session_state.product_page -= 1
            st.rerun()
        if end_idx < len(product_list) and next_.button("Next →", use_container_width=True):
            st.session_state.product_page += 1
            st.rerun()

def cart_item(item):
    """Display cart item"""
    col1, col2 = st.columns([1, 4])
    with col1:
        if image := load_image(item["image"]):
            st.image(image, width=100)
    
    with col2:
        st.subheader(item["name"])
        st.markdown(f"**Price:** ${item['price']:.2f} | **Qty:** {item['quantity']}")
        st.markdown(f"**Subtotal:** ${item['price'] * item['quantity']:.2f}")
        if st.button("🗑️ Remove", key=f"remove_{item['id']}"):
            remove_from_cart(item['id'])
            st.rerun()
    st.divider()

def checkout_form():
    """Multi-step checkout form"""
    step = st.session_state.checkout_step
    
    if step == 0:  # Shipping info
        with st.form("shipping_form"):
            st.header("📦 Shipping Information")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            address = st.text_area("Shipping Address")
            city, state = st.columns(2)
            city = city.text_input("City")
            state = state.text_input("State")
            zip_code, country = st.columns(2)
            zip_code = zip_code.text_input("ZIP Code")
            country = country.selectbox("Country", ["USA", "Japan", "UK", "Canada"])
            
            if st.form_submit_button("Continue to Payment"):
                st.session_state.shipping_info = {
                    "name": name, "email": email, "address": address,
                    "city": city, "state": state, "zip": zip_code, "country": country
                }
                st.session_state.checkout_step = 1
                st.rerun()
    
    elif step == 1:  # Payment info
        with st.form("payment_form"):
            st.header("💳 Payment Details")
            st.write(f"**Shipping to:** {st.session_state.shipping_info['address']}")
            payment = st.radio("Payment Method", ["Credit Card", "PayPal"])
            
            if payment == "Credit Card":
                card, exp, cvc = st.columns(3)
                card.text_input("Card Number", placeholder="1234 5678 9012 3456")
                exp.text_input("Expiry", placeholder="MM/YY")
                cvc.text_input("CVC", placeholder="123", type="password")
            
            if st.form_submit_button("Review Order"):
                st.session_state.checkout_step = 2
                st.rerun()
    
    elif step == 2:  # Order review
        with st.form("order_form"):
            st.header("✅ Order Confirmation")
            ship = st.session_state.shipping_info
            st.write(f"**Name:** {ship['name']} | **Email:** {ship['email']}")
            st.write(f"**Address:** {ship['address']}, {ship['city']}, {ship['state']} {ship['zip']}")
            
            subtotal, shipping, tax, total = calculate_order()
            st.subheader("Order Summary")
            st.write(f"Subtotal: ${subtotal:.2f}")
            st.write(f"Shipping: {'FREE' if shipping == 0 else f'${shipping:.2f}'}")
            st.write(f"Tax: ${tax:.2f}")
            st.write(f"**Total: ${total:.2f}**")
            
            if st.checkbox("I agree to terms"):
                if st.form_submit_button("Place Order 🚀", type="primary"):
                    st.session_state.order_id = f"ORD-{abs(hash(str(st.session_state.cart))):010x}"[:10].upper()
                    st.session_state.checkout_step = 3
                    st.rerun()
    
    if step > 0 and st.button("← Go Back"):
        st.session_state.checkout_step -= 1
        st.rerun()

# ======================================
#  PAGE RENDERING
# ======================================
def home_page():
    """Home page with products"""
    st.title("🎌 AnimeStyle Dropship")
    st.subheader("Authentic Japanese Anime Merchandise")
    
    # Category selection
    category = st.radio("Category", ["All", "Men's", "Women's"], horizontal=True)
    st.divider()
    
    # Show products
    if category == "All":
        all_products = products["men"] + products["women"]
        render_products(all_products, "🔥 All Products")
    elif category == "Men's":
        render_products(products["men"], "👕 Men's Collection")
    else:
        render_products(products["women"], "👚 Women's Collection")
    
    # Benefits
    st.divider()
    st.write("""
    **✨ Why Shop With Us?**  
    • 🚚 Fast shipping from Japan  
    • ✅ Officially licensed merchandise  
    • 🔄 30-day hassle-free returns  
    • 🔒 Secure payments  
    """)

def cart_page():
    """Shopping cart page"""
    st.title("🛒 Your Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty")
        st.button("Continue Shopping", on_click=lambda: st.session_state.update({"current_page": "🏠 Home"}))
    else:
        for item in st.session_state.cart:
            cart_item(item)
        
        # Order summary
        subtotal, shipping, tax, total = calculate_order()
        st.subheader("Order Summary")
        st.write(f"Subtotal: ${subtotal:.2f}")
        st.write(f"Shipping: {'FREE 🎉' if shipping == 0 else f'${shipping:.2f}'}")
        st.write(f"Tax: ${tax:.2f}")
        st.write(f"**Total: ${total:.2f}**")
        
        # Action buttons
        col1, col2 = st.columns(2)
        col1.button("Continue Shopping", on_click=lambda: st.session_state.update({"current_page": "🏠 Home"}))
        if col2.button("Checkout", type="primary"):
            st.session_state.checkout_step = 0
        
        # Checkout form
        if st.session_state.checkout_step >= 0:
            checkout_form()
            
            # Confirmation
            if st.session_state.checkout_step == 3:
                st.success(f"## Order Placed! 🎉 ID: {st.session_state.order_id}")
                st.balloons()
                if st.button("Continue Shopping"):
                    st.session_state.cart = []
                    st.session_state.checkout_step = 0
                    st.session_state.current_page = "🏠 Home"
                    st.rerun()

# ======================================
#  MAIN APP
# ======================================
def main():
    init_session()
    
    # Sidebar
    with st.sidebar:
        st.title("🌸 AnimeStyle")
        page = st.radio("Menu", ["🏠 Home", "🛒 Cart"])
        st.session_state.current_page = page
        
        if st.session_state.cart:
            st.divider()
            total_items = sum(item['quantity'] for item in st.session_state.cart)
            st.write(f"**Cart:** {total_items} item{'s' if total_items > 1 else ''}")
            _, _, _, total = calculate_order()
            st.write(f"**Total:** ${total:.2f}")
    
    # Page routing
    if page == "🏠 Home":
        home_page()
    else:
        cart_page()

if __name__ == "__main__":
    main()
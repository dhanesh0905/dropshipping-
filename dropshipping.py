import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# App Configuration
st.set_page_config(page_title="AnimeStyle Dropship", page_icon="🌸", layout="wide")
ITEMS_PER_PAGE, SHIPPING_THRESHOLD, TAX_RATE = 8, 100, 0.08

products = {
    "men": [
        {
            "id": 101,
            "name": "Naruto Akatsuki Cloud Hoodie",
            "price": 49.99,
            "description": "Officially licensed black hoodie with iconic Akatsuki red cloud pattern",
            "tags": ["Naruto", "Hoodie", "Popular"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw1f373bf1/Apparel/KWM257PNAR%20-%20Naruto%20Shippuden%20-%20Akatsuki%20Cloud%20Cardigan/bioworld-hoodies-outerwear-naruto-shippuden-akatsuki-cloud-cardigan-31788842123308%20(1).jpg",
            "source": "https://store.crunchyroll.com/products/naruto-shippuden-akatsuki-cloud-cardigan-KWM257PNAR.html"
        },
        {
            "id": 102,
            "name": "One Piece Straw Hat Pirates T-Shirt",
            "price": 29.99,
            "description": "Premium cotton t-shirt with official Straw Hat Jolly Roger design",
            "tags": ["One Piece", "T-Shirt", "Cotton"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dwad8fb8d2/Apparel/OPNS2737/ripple-junction-unisex-t-shirts-one-piece-straw-hat-crew-laughs-crunchyroll-exclusive-31651028336684.jpg",
            "source": "https://store.crunchyroll.com/products/one-piece-straw-hat-crew-laughs-t-shirt-crunchyroll-exclusive-OPNS2737.html"
        },
        {
            "id": 103,
            "name": "Dragon Ball Z Goku Gi Jacket",
            "price": 59.99,
            "description": "Official orange and blue windbreaker with Turtle School insignia",
            "tags": ["DBZ", "Jacket", "Goku"],
            "image": "https://store.crunchyroll.com/dw/image/v2/BDGC_PRD/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw9d87bce5/images/HDA2GUHDBZ_dragon-ball-z-goku-full-zip-hoodie_5.jpg?sw=300&sh=300&sm=fit",
            "source": "https://store.crunchyroll.com/products/dragon-ball-z-goku-full-zip-hoodie-HDA2GUHDBZ.html"
        },
        {
            "id": 104,
            "name": "Attack on Titan Survey Corps Jacket",
            "price": 69.99,
            "description": "Authentic military-style jacket with Wings of Freedom emblem",
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
            "description": "Official replica brooches with velvet display case",
            "tags": ["Sailor Moon", "Jewelry", "Collectible"],
            "image": "https://store.crunchyroll.com/on/demandware.static/-/Sites-crunchyroll-master-catalog/default/dw36e3c868/rightstuf/782009243960_anime-sailor-moon-crystal-1-limited-edition-gwp-primary.jpg",
            "source": "https://store.crunchyroll.com/products/sailor-moon-crystal-set-1-limited-edition-blu-raydvd-782009243960.html"
        },
        {
            "id": 202,
            "name": "My Hero Academia UA Track Jacket",
            "price": 54.99,
            "description": "Authentic red and blue athletic jacket with UA High School logo",
            "tags": ["MHA", "Jacket", "Sportswear"],
            "image": "https://cdn.animebape.com/wp-content/uploads/2023/04/school-uniform-my-hero-academia-casual-bomber-jacket-96cvn.jpg",
            "source": "https://animebape.com/products/anime-school-uniform-my-hero-academia-casual-bomber-jacket-2/?utm_source=google&utm_medium=paid&utm_campaign=21759809028&utm_content=&utm_term=&gadid=&gad_source=1&gad_campaignid=21766255661&gclid=Cj0KCQjwjdTCBhCLARIsAEu8bpIJSLDpI1T2QC96YbvtwRP8s89IjDvIbaHr9VfaYn7d9brc-52ulvcaAvKgEALw_wcB"
        },
        {
            "id": 203,
            "name": "Demon Slayer Nezuko Kimono Robe",
            "price": 74.99,
            "description": "Official silk blend kimono robe with bamboo pattern",
            "tags": ["Kimetsu", "Robe", "Loungewear"],
            "image": "https://img.fruugo.com/product/5/97/1692850975_0340_0340.jpg",
            "source": "https://www.fruugo.de/erwachsene-kind-damon-slayer-cosplay-kimono-haori-anime-kimetsu-no-yaiba-kamado-nezuko-kochou-shinobu-cosplay-kostum-sommer-mantel/p-237632505-509301387?language=de&ac=ProductCasterAPI&asc=pmax&gad_source=1&gad_campaignid=20424378884&gclid=Cj0KCQjwjdTCBhCLARIsAEu8bpLF1YsO5UKAC28vOVV-q53UE90ywNyVLCBXrrpwGKuucqBuc5xPiO4aAtZoEALw_wcB"
        },
        {
            "id": 204,
            "name": "Jujutsu Kaisen Sukuna Fingercaps",
            "price": 39.99,
            "description": "Officially licensed resin fingercaps with cursed seal details",
            "tags": ["JJK", "Accessory", "Cosplay"],
            "image": "https://cdn.animebape.com/wp-content/uploads/2024/09/sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight-27bx3.jpg",
            "source": "https://animebape.com/products/anime-sukuna-jujutsu-kaisen-custom-unisex-leggings-spats-training-tight/?utm_source=google&utm_medium=paid&utm_campaign=21759809028&utm_content=&utm_term=&gadid=&gad_source=1&gad_campaignid=21766255661&gclid=Cj0KCQjwjdTCBhCLARIsAEu8bpI0Gsm9VEB_fQyXG7xtOiQiUr9Yy4dtXYDI1zZ6nqaFvkcyeDpkGB0aAq8bEALw_wcB"
        }
    ]
}

# Utilities
@st.cache_data(show_spinner=False)
def load_image(url):
    try: return Image.open(BytesIO(requests.get(url, timeout=5).content))
    except: return None

def init_session():
    defaults = {'cart': [], 'current_page': "🏠 Home", 'product_page': 0, 'checkout_step': 0}
    for k, v in defaults.items(): st.session_state.setdefault(k, v)

def cart_action(product, action="add"):
    if action == "add":
        if existing := next((i for i in st.session_state.cart if i["id"] == product["id"]), None):
            existing["quantity"] += 1
        else:
            st.session_state.cart.append({**product, "quantity": 1})
        st.success(f"Added {product['name']} to cart!")
    else: 
        st.session_state.cart = [i for i in st.session_state.cart if i['id'] != product]

def calculate_order():
    cart = st.session_state.cart
    total = sum(i['price'] * i['quantity'] for i in cart)
    shipping = 0 if total >= SHIPPING_THRESHOLD else 9.99
    tax = total * TAX_RATE
    return total, shipping, tax, total + shipping + tax

# Components
def product_card(product):
    with st.container():
        if img := load_image(product["image"]): st.image(img, use_container_width=True)
        st.subheader(product["name"])
        st.markdown(f"**${product['price']}**")
        st.caption(product["description"])
        st.caption(" ".join(f"`{tag}`" for tag in product["tags"]))
        st.markdown(f"[🔍 Product Details]({product['source']})")
        if st.button("🛒 Add to Cart", key=f"add_{product['id']}", use_container_width=True):
            cart_action(product)

def render_products(products, title):
    st.header(title)
    page, num_pages = st.session_state.product_page, max(1, (len(products) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    
    cols = st.columns(4)
    for i, p in enumerate(products[page*ITEMS_PER_PAGE: (page+1)*ITEMS_PER_PAGE]):
        with cols[i % 4]: product_card(p)
    
    if num_pages > 1:
        col1, col2, _ = st.columns([1, 1, 6])
        if page > 0 and col1.button("← Previous", use_container_width=True):
            st.session_state.product_page -= 1
            st.rerun()
        if page < num_pages-1 and col2.button("Next →", use_container_width=True):
            st.session_state.product_page += 1
            st.rerun()

def cart_item(item):
    col1, col2 = st.columns([1, 3])
    with col1:
        if img := load_image(item["image"]): st.image(img, width=100)
    with col2:
        st.subheader(item["name"])
        st.markdown(f"**Price:** ${item['price']} | **Qty:** {item['quantity']}")
        st.markdown(f"**Subtotal:** ${item['price'] * item['quantity']:.2f}")
        if st.button("🗑️ Remove", key=f"remove_{item['id']}"):
            cart_action(item['id'], "remove")
            st.rerun()
    st.divider()

def checkout_form():
    step = st.session_state.checkout_step
    with st.form(f"checkout_step_{step}"):
        if step == 0:  # Shipping
            st.header("📦 Shipping Information")
            name = st.text_input("Full Name", key="name")
            email = st.text_input("Email", key="email")
            address = st.text_area("Shipping Address", key="address")
            city, state = st.columns(2)
            city, state = city.text_input("City", key="city"), state.text_input("State/Province", key="state")
            zip_code, country = st.columns(2)
            zip_code, country = zip_code.text_input("ZIP/Postal Code", key="zip"), country.selectbox("Country", ["USA", "Japan", "Canada", "UK", "Australia"])
            
            if st.form_submit_button("Continue to Payment", use_container_width=True):
                st.session_state.shipping_info = locals()
                st.session_state.checkout_step = 1
                st.rerun()
                
        elif step == 1:  # Payment
            st.header("💳 Payment Details")
            ship = st.session_state.shipping_info
            st.subheader("Shipping to:")
            st.markdown(f"{ship['address']}, {ship['city']}, {ship['state']} {ship['zip']}, {ship['country']}")
            payment = st.radio("Payment Method", ["Credit Card", "PayPal", "Google Pay"])
            
            if payment == "Credit Card":
                cols = st.columns(3)
                cols[0].text_input("Card Number", placeholder="1234 5678 9012 3456")
                cols[1].text_input("Expiration", placeholder="MM/YY")
                cols[2].text_input("CVC", placeholder="123", type="password")
            
            if st.form_submit_button("Review Order", use_container_width=True):
                st.session_state.checkout_step = 2
                st.rerun()
                
        elif step == 2:  # Review
            st.header("✅ Order Confirmation")
            st.success("Almost done! Review your order:")
            ship = st.session_state.shipping_info
            st.subheader("Shipping Information:")
            st.markdown(f"**Name:** {ship['name']} | **Email:** {ship['email']}")  
            st.markdown(f"**Address:** {ship['address']}")  
            st.markdown(f"**City:** {ship['city']} | **State:** {ship['state']} | **ZIP:** {ship['zip']} | **Country:** {ship['country']}")  
            
            total, shipping, tax, grand_total = calculate_order()
            st.subheader("Order Summary")
            st.markdown(f"**Subtotal:** ${total:.2f}")
            st.markdown(f"**Shipping:** {'FREE 🎉' if shipping == 0 else f'${shipping:.2f}'}")
            st.markdown(f"**Tax:** ${tax:.2f}")
            st.markdown(f"## Grand Total: ${grand_total:.2f}")
            
            if st.checkbox("I agree to terms and conditions", key="terms"):
                if st.form_submit_button("Place Order 🚀", type="primary", use_container_width=True):
                    st.session_state.order_id = f"ORD-{hash(str(st.session_state.cart)):x}"[:10].upper()
                    st.session_state.checkout_step = 3
                    st.rerun()
    
    if step > 0 and st.button("← Go Back", use_container_width=True):
        st.session_state.checkout_step = max(0, step - 1)
        st.rerun()

# Pages
def home_page():
    st.title("🎌 AnimeStyle Dropship")
    st.subheader("Authentic Japanese Anime Merchandise Shipped Worldwide")
    st.image("https://images.unsplash.com/photo-1633327941347-6cea0bdce44d?auto=format&fit=crop&w=1200&h=400", 
             use_container_width=True, caption="Shop exclusive anime merchandise")
    
    category = st.radio("Shop By Category", ["All", "Men's", "Women's"], horizontal=True, label_visibility="collapsed")
    st.divider()
    
    if category == "All": render_products(products["men"] + products["women"], "🔥 All Collections")
    elif category == "Men's": render_products(products["men"], "👕 Men's Collection")
    else: render_products(products["women"], "👚 Women's Collection")
    
    st.divider()
    st.header("✨ Premium Benefits")
    for col, (icon, title, desc) in zip(st.columns(4), [
        ("🚚", "Fast Shipping", "From Tokyo in 24h"),
        ("✅", "Authentic", "Official merchandise"),
        ("🔄", "Easy Returns", "30-day policy"),
        ("🔒", "Secure", "Encrypted payments")
    ]):
        col.subheader(f"{icon} {title}")
        col.caption(desc)
    
    st.divider()
    st.markdown("""
    **🏢 About AnimeStyle**  
    Authentic merchandise direct from Japan  
    **📞 Contact:** support@animestyledropship.com | +81 3-1234-5678  
    **🌐 Connect:**  
    [Instagram](https://instagram.com/animestyle_dropship) | 
    [Twitter](https://twitter.com/animestyle_ds) | 
    [Facebook](https://facebook.com/animestyledropship)
    """)

def requirements_page():
    st.title("📋 System Requirements")
    for title, content in [
        ("Customer Experience", """
        - **Product Discovery**: Browse by category, search, filters
        - **Shopping Cart**: Add/remove items, real-time calculations
        - **Checkout**: Multi-step with multiple payment options
        - **Order Management**: Confirmation, tracking, returns"""),
        
        ("Store Management", """
        - **Inventory**: Real-time tracking, low stock alerts
        - **Order Processing**: Dashboard, status workflow
        - **Product Management**: Add/edit/archive products
        - **Analytics**: Sales performance, customer metrics"""),
        
        ("Technical Specs", """
        - **Frontend**: Streamlit-based responsive UI
        - **Backend**: Python microservices, PostgreSQL
        - **Integrations**: Payment gateways, shipping carriers
        - **Security**: PCI-DSS compliance, GDPR handling""")
    ]:
        with st.expander(title, expanded=True): st.markdown(content)

def cart_page():
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Browse our collections!")
        st.image("https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=600&h=300", 
                 use_container_width=True)
        st.button("Continue Shopping", use_container_width=True,
                 on_click=lambda: st.session_state.update({"current_page": "🏠 Home"}))
    else:
        for item in st.session_state.cart: cart_item(item)
        
        total, shipping, tax, grand_total = calculate_order()
        st.subheader("Order Summary")
        st.markdown(f"**Subtotal:** ${total:.2f}")
        st.markdown(f"**Shipping:** {'FREE 🎉' if shipping == 0 else f'${shipping:.2f}'}")
        st.markdown(f"**Tax:** ${tax:.2f}")
        st.markdown(f"## Grand Total: ${grand_total:.2f}")
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.button("Continue Shopping", use_container_width=True,
                   on_click=lambda: st.session_state.update({"current_page": "🏠 Home"}))
        if col2.button("Proceed to Checkout", type="primary", use_container_width=True):
            st.session_state.checkout_step = 0
        
        if st.session_state.checkout_step >= 0:
            checkout_form()
            
            if st.session_state.checkout_step == 3:
                st.success(f"## Order Placed! 🎉")
                st.balloons()
                st.markdown(f"**Your order ID:** {st.session_state.order_id}")
                st.image("https://images.unsplash.com/photo-1594179047519-f347310d3322?auto=format&fit=crop&w=600&h=300", 
                         use_container_width=True)
                st.button("Continue Shopping", use_container_width=True,
                         on_click=lambda: [st.session_state.update({'cart': [], 'checkout_step': -1}), 
                                          st.session_state.update({"current_page": "🏠 Home"})])

# Main App
def main():
    init_session()
    with st.sidebar:
        st.title("🌸 AnimeStyle")
        st.session_state.current_page = st.radio("Navigation", ["🏠 Home", "📋 Requirements", "🛒 Cart"], 
                        index=["🏠 Home", "📋 Requirements", "🛒 Cart"].index(st.session_state.current_page))
        
        if st.session_state.cart:
            st.divider()
            st.subheader("Cart Summary")
            total_items = sum(i['quantity'] for i in st.session_state.cart)
            st.caption(f"{total_items} item{'s' if total_items > 1 else ''}")
            _, _, _, grand_total = calculate_order()
            st.markdown(f"**Total:** ${grand_total:.2f}")
            st.button("View Cart", on_click=lambda: st.session_state.update({"current_page": "🛒 Cart"}))
    
    if st.session_state.current_page == "🏠 Home": home_page()
    elif st.session_state.current_page == "📋 Requirements": requirements_page()
    else: cart_page()

if __name__ == "__main__":
    main()
import streamlit as st

# Configure page
st.set_page_config(
    page_title="AnimeStyle Dropship",
    page_icon="🌸",
    layout="wide"
)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Store the current page in session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Actual anime merchandise database
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

# Create page selection in sidebar
page = st.sidebar.selectbox("Navigation", ["🏠 Home", "📋 Requirements", "🛒 Cart"], 
                           key='page_selector',
                           index=["🏠 Home", "📋 Requirements", "🛒 Cart"].index(st.session_state.current_page))

# Update session state with current page
st.session_state.current_page = page

# Home Page
if page == "🏠 Home":
    st.title("🎌 AnimeStyle Dropship")
    st.subheader("Authentic Japanese Anime Merchandise Shipped Worldwide")

    # Category selection
    gender_category = st.radio("Shop By Category", ["All", "Men's Collection", "Women's Collection"], horizontal=True)
    st.markdown("---")
    
    # Product display function
    def display_products(product_list):
        cols = st.columns(4)
        for idx, product in enumerate(product_list):
            with cols[idx % 4]:
                with st.container():
                    # Display product image
                    try:
                        st.image(
                            product["image"],
                            width=300,
                            use_container_width=True,
                            caption=product["name"]
                        )
                    except:
                        st.error("Image not available")
                    
                    # Product info
                    st.subheader(product["name"])
                    st.write(f"**${product['price']}**")
                    st.caption(product["description"])
                    
                    # Tags
                    tag_str = " ".join([f"`{tag}`" for tag in product["tags"]])
                    st.caption(tag_str)
                    
                    # Source link
                    st.markdown(f"[🔍 Product Details →]({product['source']})")
                    
                    # Add to cart button
                    if st.button("🛒 Add to Cart", key=product["id"]):
                        existing = next((item for item in st.session_state.cart if item["id"] == product["id"]), None)
                        if existing:
                            existing["quantity"] += 1
                        else:
                            st.session_state.cart.append({
                                "id": product["id"],
                                "name": product["name"],
                                "price": product["price"],
                                "quantity": 1,
                                "image": product["image"]
                            })
                        st.success(f"Added {product['name']} to cart!")

    # Show products based on selection
    if gender_category == "All":
        st.subheader("🔥 All Anime Collections")
        display_products(products["men"] + products["women"])
    elif gender_category == "Men's Collection":
        st.subheader("👕 Men's Anime Collection")
        display_products(products["men"])
    elif gender_category == "Women's Collection":
        st.subheader("👚 Women's Anime Collection")
        display_products(products["women"])

    # Promotional banner
    st.markdown("---")
    st.subheader("✨ Premium Shipping & Guarantee")
    st.markdown("""
    - **Fast Worldwide Shipping**: All orders ship from our Tokyo warehouse within 24 hours
    - **Authenticity Guaranteed**: Official licensed merchandise with hologram seals
    - **Easy Returns**: 30-day no-questions-asked return policy
    - **Secure Payments**: SSL encrypted transactions with multiple payment options
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **🏢 About AnimeStyle Dropship**  
    We partner directly with Japanese manufacturers and licensors to bring you authentic anime merchandise. 
    All products are officially licensed and ship directly from our distribution center in Tokyo, Japan.

    **📞 Customer Support**  
    Email: support@animestyledropship.com  
    Phone: +81 3-1234-5678  
    Business Hours: Mon-Fri 9AM-6PM JST

    **🌐 Connect With Us**  
    [Instagram](https://instagram.com/animestyle_dropship) | [Twitter](https://twitter.com/animestyle_ds) | [Facebook](https://facebook.com/animestyledropship)

    *Prices in USD. Naruto, One Piece, Dragon Ball Z, Attack on Titan, Sailor Moon, My Hero Academia, Demon Slayer, and Jujutsu Kaisen are registered trademarks of their respective owners. All rights reserved.*
    """)

# Requirements Page
elif page == "📋 Requirements":
    st.title("📋 System Requirements Documentation")
    st.markdown("---")
    
    with st.expander("Customer Experience Requirements", expanded=True):
        st.markdown("""
        ### Persona: Anime Fan (Customer)
        
        **Functional Requirements:**
        1. **Product Discovery**  
           - Browse anime merchandise by gender categories  
           - Filter by price range and popularity  
           - *Implementation: Category filters and sorting options*
           
        2. **Product Inspection**  
           - View high-resolution product images with zoom capability  
           - Detailed specifications and materials information  
           - *Implementation: Image gallery and technical specifications section*
           
        3. **Shopping Cart**  
           - Add/remove items with quantity adjustments  
           - Save cart for later access  
           - *Implementation: Session-based cart with persistent storage*
           
        4. **Checkout Process**  
           - Multi-step checkout with shipping options  
           - Multiple payment gateway integration  
           - *Implementation: Checkout workflow with payment API integration*
           
        5. **Order Tracking**  
           - Real-time shipment tracking with carrier integration  
           - Order history with download invoices  
           - *Implementation: Shipping API integration and order management*
        
        **Performance Metrics:**
        - Page load time under 1.5 seconds
        - Mobile-responsive design (90+ Lighthouse score)
        - Payment processing under 10 seconds
        """)
    
    with st.expander("Store Management Requirements", expanded=True):
        st.markdown("""
        ### Persona: Store Owner (Admin)
        
        **Operational Requirements:**
        1. **Inventory Management**  
           - Real-time stock level monitoring  
           - Low stock alerts and automatic reordering  
           - *Implementation: Inventory dashboard with alert system*
           
        2. **Order Fulfillment**  
           - Batch processing of orders  
           - Shipping label generation  
           - *Implementation: Order management system with shipping integration*
           
        3. **Product Management**  
           - Bulk import/export of product data  
           - Automated product categorization  
           - *Implementation: CSV import/export with AI categorization*
           
        4. **Supplier Integration**  
           - API connections to manufacturer systems  
           - Automated purchase order generation  
           - *Implementation: Supplier API integration with PO system*
           
        5. **Analytics Dashboard**  
           - Sales performance metrics  
           - Customer behavior insights  
           - *Implementation: Data visualization dashboard with analytics*
        
        **Business Metrics:**
        - Order fulfillment time: <24 hours
        - Inventory accuracy: 99.5%
        - Customer satisfaction: 95% positive ratings
        """)
    
    with st.expander("Technical Specifications", expanded=True):
        st.markdown("""
        ### System Architecture
        
        **Frontend:**
        - Streamlit web application
        - Responsive design for mobile/desktop
        - Progressive Web App (PWA) capabilities
        
        **Backend:**
        - Python/FastAPI microservices
        - PostgreSQL database with Redis caching
        - Cloud deployment (AWS/GCP)
        
        **Integrations:**
        - Payment gateways: Stripe, PayPal
        - Shipping carriers: DHL, FedEx, Japan Post
        - Supplier APIs: Crunchyroll, Goodsmile
        
        **Security:**
        - PCI-DSS compliant payment processing
        - GDPR-compliant data handling
        - Regular security audits and penetration testing
        
        **Scalability:**
        - Designed to handle 10,000+ concurrent users
        - Auto-scaling cloud infrastructure
        - Content Delivery Network (CDN) for global assets
        """)
    
    st.markdown("---")
    st.caption("Document Version: 2.1 | Last Updated: June 20, 2025")

# Cart Page
elif page == "🛒 Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Browse our collections to add items!")
        # Using a placeholder image from a URL
        st.image("https://cdn.dribbble.com/users/5107895/screenshots/14532312/media/a7e6c2e9333d0989e3a54c95dd8321d7.jpg", 
                 caption="Find amazing anime merchandise!", 
                 use_container_width=True)
        if st.button("Continue Shopping"):
            st.session_state.current_page = "🏠 Home"
            st.experimental_rerun()
    else:
        total = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
        shipping = 9.99 if total < 100 else 0
        tax = total * 0.08
        grand_total = total + shipping + tax
        
        # Display cart items
        for item in st.session_state.cart:
            col1, col2 = st.columns([1, 3])
            with col1:
                try:
                    st.image(item["image"], width=100)
                except:
                    st.error("Image not available")
            with col2:
                st.subheader(item["name"])
                st.write(f"Price: ${item['price']} | Qty: {item['quantity']}")
                st.write(f"Subtotal: ${item['price'] * item['quantity']:.2f}")
                if st.button("Remove", key=f"remove_{item['id']}"):
                    st.session_state.cart = [i for i in st.session_state.cart if i['id'] != item['id']]
                    st.experimental_rerun()
            st.markdown("---")
        
        # Order summary
        st.subheader("Order Summary")
        st.write(f"Subtotal: ${total:.2f}")
        st.write(f"Shipping: ${shipping:.2f}")
        st.write(f"Tax: ${tax:.2f}")
        st.write(f"**Grand Total: ${grand_total:.2f}**")
        
        # Checkout options
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue Shopping"):
                st.session_state.current_page = "🏠 Home"
                st.experimental_rerun()
        with col2:
            if st.button("Proceed to Checkout", type="primary"):
                st.session_state.cart = []
                st.success("Order placed successfully! Your anime gear will ship from Tokyo within 3-5 business days!")
                st.balloons()
        
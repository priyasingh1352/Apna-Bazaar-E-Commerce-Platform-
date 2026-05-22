import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime
import database
import admin
import styles

# Initialize database
database.init_db()

# Apply custom CSS
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'user' not in st.session_state:
    st.session_state.user = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'All'
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = 'Featured'

# Navigation
def render_navigation():
    st.markdown("""
    <div class="app-header">
        <h1>Apna <span>Bazaar</span></h1>
        <div style="display: flex; gap: 1rem; align-items: center;">
    """, unsafe_allow_html=True)
    
    # Search bar
    search_query = st.text_input(
        "Search products...",
        placeholder="Search for products, brands and more",
        value=st.session_state.search_query,
        key="nav_search",
        label_visibility="collapsed"
    )
    
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    with col2:
        if st.button("🛒 Cart", use_container_width=True):
            st.session_state.page = 'cart'
            st.rerun()
    
    with col3:
        if st.session_state.user:
            if st.button("👤 My Orders", use_container_width=True):
                st.session_state.page = 'orders'
                st.rerun()
        else:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
    
    with col4:
        if st.session_state.user and st.session_state.user['role'] == 'admin':
            if st.button("⚙️ Admin", use_container_width=True):
                st.session_state.page = 'admin'
                st.rerun()
        elif st.session_state.user:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = {}
                st.session_state.page = 'home'
                st.rerun()

    # Cart indicator
    if st.session_state.cart:
        cart_count = sum(item['quantity'] for item in st.session_state.cart.values())
        st.markdown(f"""
        <div style="position: fixed; top: 80px; right: 20px; background: #FF5722; color: white; 
                    padding: 5px 15px; border-radius: 20px; font-weight: bold; z-index: 1000;">
            🛒 {cart_count} items
        </div>
        """, unsafe_allow_html=True)

# Login page
def render_login():
    st.markdown("<h2 style='color:#2874F0; text-align: center; margin: 2rem 0;'>Login to Apna Bazaar</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        login_tab, register_tab = st.tabs(["Login", "Register"])
        
        with login_tab:
            with st.form("login_form"):
                username = st.text_input("Username*", placeholder="Enter your username")
                password = st.text_input("Password*", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if username and password:
                        user = database.authenticate_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.success(f"Welcome back, {username}!")
                            st.session_state.page = 'home'
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please fill in all fields")
        
        with register_tab:
            with st.form("register_form"):
                new_username = st.text_input("Username*", placeholder="Choose a username")
                new_email = st.text_input("Email*", placeholder="Enter your email")
                new_password = st.text_input("Password*", type="password", placeholder="Choose a password")
                confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
                submitted = st.form_submit_button("Register", use_container_width=True)
                
                if submitted:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters")
                        else:
                            success = database.add_user(new_username, new_password, new_email, "customer")
                            if success:
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Username already exists")
                    else:
                        st.error("Please fill in all fields")

# Home page with product listing
def render_home():
    st.markdown("""
    <div class="banner-carousel">
        <h2 style="margin: 0; font-size: 2rem;">🎉 Big Sale! Up to 50% Off</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.1rem;">Shop the best deals on electronics, fashion, and more!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        categories = ["All"] + database.get_categories()
        selected_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0
        )
        if selected_category != st.session_state.selected_category:
            st.session_state.selected_category = selected_category
            st.rerun()
    
    with col2:
        sort_options = ["Featured", "Price: Low to High", "Price: High to Low", "Customer Rating"]
        sort_by = st.selectbox(
            "Sort by",
            sort_options,
            index=sort_options.index(st.session_state.sort_by) if st.session_state.sort_by in sort_options else 0
        )
        if sort_by != st.session_state.sort_by:
            st.session_state.sort_by = sort_by
            st.rerun()
    
    with col3:
        min_price = st.number_input("Min Price (₹)", min_value=0, value=0, step=100)
        max_price = st.number_input("Max Price (₹)", min_value=0, value=200000, step=1000)
    
    # Get products
    products = database.get_all_products(
        category=st.session_state.selected_category,
        search_query=st.session_state.search_query,
        sort_by=st.session_state.sort_by,
        min_price=min_price,
        max_price=max_price
    )
    
    if not products:
        st.info("No products found. Try adjusting your filters or search query.")
    else:
        st.markdown(f"### {len(products)} Products Found")
        st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
        
        # Display products in grid
        for i in range(0, len(products), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(products):
                    product = products[idx]
                    with col:
                        render_product_card(product)
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_product_card(product):
    # Handle image
    img_src = product['image_path']
    if img_src and not img_src.startswith("http"):
        local_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_src)
        if os.path.exists(local_img_path):
            try:
                img_src = Image.open(local_img_path)
            except:
                img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
        else:
            img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
    
    st.markdown(f"""
    <div class="product-card">
        <div class="product-img-container">
    """, unsafe_allow_html=True)
    
    if img_src:
        st.image(img_src, use_container_width=True)
    
    st.markdown("""
        </div>
        <div class="product-info">
            <div class="product-category">{}</div>
            <div class="product-title">{}</div>
            <div class="rating-badge">★ {}</div>
            <div class="price-row">
                <span class="price-current">₹{:.2f}</span>
            </div>
        </div>
    </div>
    """.format(
        product['category'],
        product['title'],
        product['rating'],
        product['price']
    ), unsafe_allow_html=True)
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True):
            add_to_cart(product['id'], product['title'], product['price'], product['image_path'])
    
    with col2:
        if st.button("View Details", key=f"view_{product['id']}", use_container_width=True):
            st.session_state.view_product_id = product['id']
            st.session_state.page = 'product_details'
            st.rerun()

def add_to_cart(product_id, title, price, image_path):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id]['quantity'] += 1
    else:
        st.session_state.cart[product_id] = {
            'title': title,
            'price': price,
            'image_path': image_path,
            'quantity': 1
        }
    st.success(f"Added {title} to cart!")
    st.rerun()

# Product details page
def render_product_details():
    if 'view_product_id' not in st.session_state:
        st.session_state.page = 'home'
        st.rerun()
        return
    
    product_id = st.session_state.view_product_id
    product = database.get_product_by_id(product_id)
    
    if not product:
        st.error("Product not found")
        st.session_state.page = 'home'
        st.rerun()
        return
    
    # Handle image
    img_src = product['image_path']
    if img_src and not img_src.startswith("http"):
        local_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_src)
        if os.path.exists(local_img_path):
            try:
                img_src = Image.open(local_img_path)
            except:
                img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
        else:
            img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if img_src:
            st.image(img_src, use_container_width=True)
    
    with col2:
        st.markdown(f"<h1 style='color:#212121;'>{product['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"**Category:** {product['category']}")
        st.markdown(f"**Rating:** ⭐ {product['rating']}/5")
        st.markdown(f"**Stock:** {product['stock']} units available")
        st.markdown(f"**Price:** ₹{product['price']:,.2f}")
        
        st.markdown("---")
        st.markdown("### Description")
        st.markdown(product['description'])
        
        st.markdown("---")
        
        # Quantity selector
        quantity = st.number_input("Quantity", min_value=1, max_value=product['stock'], value=1)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("Add to Cart", use_container_width=True, key="detail_add_cart"):
                for _ in range(quantity):
                    add_to_cart(product['id'], product['title'], product['price'], product['image_path'])
        
        with col_btn2:
            if st.button("Buy Now", use_container_width=True, key="detail_buy_now"):
                for _ in range(quantity):
                    add_to_cart(product['id'], product['title'], product['price'], product['image_path'])
                st.session_state.page = 'cart'
                st.rerun()
    
    # Reviews section
    st.markdown("---")
    st.markdown("### Customer Reviews")
    
    reviews = database.get_reviews_for_product(product_id)
    
    if not reviews:
        st.info("No reviews yet. Be the first to review!")
    else:
        for review in reviews:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #e0e0e0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{review['username']}</strong>
                    <span style="background: #388E3C; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">★ {review['rating']}</span>
                </div>
                <p style="margin: 0.5rem 0 0 0; color: #555;">{review['comment']}</p>
                <small style="color: #888;">{review['created_at']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Add review form
    if st.session_state.user:
        st.markdown("### Write a Review")
        with st.form("add_review_form"):
            rating = st.slider("Rating", min_value=1, max_value=5, value=5)
            comment = st.text_area("Your Review", placeholder="Share your experience with this product...")
            submitted = st.form_submit_button("Submit Review")
            
            if submitted:
                if comment:
                    database.add_review(product_id, st.session_state.user['username'], rating, comment)
                    st.success("Review submitted successfully!")
                    st.rerun()
                else:
                    st.error("Please write a review")
    else:
        st.info("Please login to write a review")
    
    if st.button("← Back to Products"):
        st.session_state.page = 'home'
        st.rerun()

# Cart page
def render_cart():
    st.markdown("<h2 style='color:#2874F0;'>Shopping Cart</h2>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is empty")
        if st.button("Continue Shopping", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    total_price = 0
    
    for product_id, item in list(st.session_state.cart.items()):
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
        
        # Handle image
        img_src = item['image_path']
        if img_src and not img_src.startswith("http"):
            local_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_src)
            if os.path.exists(local_img_path):
                try:
                    img_src = Image.open(local_img_path)
                except:
                    img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
            else:
                img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
        
        with col1:
            if img_src:
                st.image(img_src, width=80)
        
        with col2:
            st.markdown(f"**{item['title']}**")
            st.markdown(f"₹{item['price']:,.2f}")
        
        with col3:
            new_quantity = st.number_input(
                "Qty",
                min_value=1,
                max_value=10,
                value=item['quantity'],
                key=f"qty_{product_id}"
            )
            if new_quantity != item['quantity']:
                st.session_state.cart[product_id]['quantity'] = new_quantity
                st.rerun()
        
        with col4:
            item_total = item['price'] * item['quantity']
            st.markdown(f"**₹{item_total:,.2f}**")
            total_price += item_total
        
        with col5:
            if st.button("🗑️", key=f"remove_{product_id}"):
                del st.session_state.cart[product_id]
                st.rerun()
        
        st.markdown("---")
    
    # Cart summary
    st.markdown(f"""
    <div class="checkout-box">
        <div class="checkout-header">Order Summary</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Subtotal ({len(st.session_state.cart)} items)</span>
            <span>₹{total_price:,.2f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Delivery</span>
            <span>FREE</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.2rem; margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #e0e0e0;">
            <span>Total</span>
            <span>₹{total_price:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user:
        st.warning("Please login to proceed with checkout")
        if st.button("Login to Checkout", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    else:
        if st.button("Proceed to Checkout", use_container_width=True, type="primary"):
            st.session_state.checkout_total = total_price
            st.session_state.page = 'checkout'
            st.rerun()

# Checkout page
def render_checkout():
    if not st.session_state.user:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    if not st.session_state.cart:
        st.session_state.page = 'home'
        st.rerun()
        return
    
    st.markdown("<h2 style='color:#2874F0;'>Checkout</h2>", unsafe_allow_html=True)
    
    total_price = st.session_state.get('checkout_total', sum(item['price'] * item['quantity'] for item in st.session_state.cart.values()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Shipping Details")
        with st.form("checkout_form"):
            address = st.text_area("Delivery Address*", placeholder="Enter your complete delivery address", height=100)
            phone = st.text_input("Phone Number*", placeholder="Enter your 10-digit phone number")
            payment_method = st.selectbox(
                "Payment Method*",
                ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
            )
            
            submitted = st.form_submit_button("Place Order", use_container_width=True, type="primary")
            
            if submitted:
                if address and phone:
                    if len(phone) != 10 or not phone.isdigit():
                        st.error("Please enter a valid 10-digit phone number")
                    else:
                        try:
                            order_id = database.create_order(
                                st.session_state.user['id'],
                                total_price,
                                address,
                                phone,
                                payment_method,
                                st.session_state.cart
                            )
                            st.session_state.cart = {}
                            st.session_state.order_success = order_id
                            st.session_state.page = 'order_success'
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to place order: {e}")
                else:
                    st.error("Please fill in all required fields")
    
    with col2:
        st.markdown("### Order Summary")
        st.markdown(f"""
        <div class="checkout-box">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Items ({len(st.session_state.cart)})</span>
                <span>₹{total_price:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Delivery</span>
                <span>FREE</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.2rem; margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #e0e0e0;">
                <span>Total</span>
                <span>₹{total_price:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Order success page
def render_order_success():
    if 'order_success' not in st.session_state:
        st.session_state.page = 'home'
        st.rerun()
        return
    
    order_id = st.session_state.order_success
    
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🎉</div>
        <h2 style="color: #388E3C;">Order Placed Successfully!</h2>
        <p style="font-size: 1.2rem; color: #555;">Your order ID is: <strong>#{order_id}</strong></p>
        <p style="color: #888;">You will receive a confirmation email shortly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("Continue Shopping", use_container_width=True):
            del st.session_state.order_success
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("View My Orders", use_container_width=True):
            del st.session_state.order_success
            st.session_state.page = 'orders'
            st.rerun()

# Orders page
def render_orders():
    if not st.session_state.user:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown("<h2 style='color:#2874F0;'>My Orders</h2>", unsafe_allow_html=True)
    
    orders = database.get_orders_by_user(st.session_state.user['id'])
    
    if not orders:
        st.info("You haven't placed any orders yet.")
        if st.button("Start Shopping", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    for order in orders:
        status_colors = {
            'Pending': '#FFF9C4',
            'Shipped': '#E3F2FD',
            'Delivered': '#E8F5E9',
            'Cancelled': '#FFEBEE'
        }
        status_text_colors = {
            'Pending': '#F57F17',
            'Shipped': '#0D47A1',
            'Delivered': '#1B5E20',
            'Cancelled': '#B71C1C'
        }
        
        bg_color = status_colors.get(order['status'], '#FFF9C4')
        text_color = status_text_colors.get(order['status'], '#F57F17')
        
        st.markdown(f"""
        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <strong>Order #{order['id']}</strong>
                    <small style="color: #888; margin-left: 1rem;">{order['created_at']}</small>
                </div>
                <span style="background: {bg_color}; color: {text_color}; padding: 4px 12px; border-radius: 4px; font-weight: 600; font-size: 0.9rem;">
                    {order['status']}
                </span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <strong>Total:</strong> ₹{order['total_price']:,.2f}
            </div>
            <div style="color: #666; font-size: 0.9rem;">
                <div>Payment: {order['payment_method']}</div>
                <div>Address: {order['address']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show order items
        items = database.get_order_items(order['id'])
        if st.button(f"View Items (Order #{order['id']})", key=f"items_{order['id']}"):
            with st.expander("Order Items", expanded=True):
                for item in items:
                    col_img, col_info = st.columns([1, 5])
                    
                    img_src = item['image_path']
                    if img_src and not img_src.startswith("http"):
                        local_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_src)
                        if os.path.exists(local_img_path):
                            try:
                                img_src = Image.open(local_img_path)
                            except:
                                img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
                        else:
                            img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
                    
                    with col_img:
                        if img_src:
                            st.image(img_src, width=60)
                    
                    with col_info:
                        st.markdown(f"**{item['title']}**")
                        st.markdown(f"Qty: {item['quantity']} | Price: ₹{item['price']:,.2f}")
        
        st.markdown("---")

# Main app logic
def main():
    render_navigation()
    
    # Route to appropriate page
    if st.session_state.page == 'login':
        render_login()
    elif st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'product_details':
        render_product_details()
    elif st.session_state.page == 'cart':
        render_cart()
    elif st.session_state.page == 'checkout':
        render_checkout()
    elif st.session_state.page == 'order_success':
        render_order_success()
    elif st.session_state.page == 'orders':
        render_orders()
    elif st.session_state.page == 'admin':
        if st.session_state.user and st.session_state.user['role'] == 'admin':
            admin.show_admin_dashboard()
        else:
            st.error("Access denied. Admin only.")
            st.session_state.page = 'home'
            st.rerun()

if __name__ == "__main__":
    main()

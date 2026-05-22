import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime
from PIL import Image
import database

def show_admin_dashboard():
    st.markdown("<h2 style='color:#2874F0; margin-bottom:1.5rem;'>Merchant Administration Portal</h2>", unsafe_allow_html=True)
    
    # Tabs for different admin sections
    tab_analytics, tab_products, tab_orders = st.tabs([
        "📈 Sales & Analytics", 
        "📦 Inventory & Products", 
        "🛍️ Order Fulfilment"
    ])
    
    # ------------------ ANALYTICS TAB ------------------
    with tab_analytics:
        st.subheader("Business Metrics Dashboard")
        
        # Load Analytics Summary
        summary = database.get_analytics_summary()
        
        # Render KPI Cards in HTML/CSS
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">₹{summary['revenue']:,.2f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">{summary['orders']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Products</div>
                <div class="kpi-value">{summary['products']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Customers</div>
                <div class="kpi-value">{summary['customers']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Revenue by Category")
            cat_data = database.get_revenue_by_category()
            if cat_data:
                df_cat = pd.DataFrame(cat_data)
                fig_cat = px.bar(
                    df_cat, 
                    x='category', 
                    y='revenue', 
                    labels={'category': 'Product Category', 'revenue': 'Revenue (₹)'},
                    color='category',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_cat.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=300)
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.info("No revenue records available yet.")
                
        with col2:
            st.markdown("### Order Status Breakdown")
            status_data = database.get_order_status_distribution()
            if status_data:
                df_status = pd.DataFrame(status_data)
                fig_status = px.pie(
                    df_status, 
                    names='status', 
                    values='count',
                    color='status',
                    color_discrete_map={
                        'Pending': '#FFCA28',
                        'Shipped': '#42A5F5',
                        'Delivered': '#66BB6A',
                        'Cancelled': '#EF5350'
                    }
                )
                fig_status.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
                st.plotly_chart(fig_status, use_container_width=True)
            else:
                st.info("No order data available yet.")
                
        st.markdown("### Revenue Trend Over Time")
        trend_data = database.get_revenue_trend()
        if trend_data:
            df_trend = pd.DataFrame(trend_data)
            fig_trend = px.line(
                df_trend, 
                x='date', 
                y='revenue', 
                labels={'date': 'Date', 'revenue': 'Daily Revenue (₹)'},
                markers=True,
                line_shape='spline'
            )
            fig_trend.update_traces(line_color='#2874F0', line_width=3)
            fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No transactional history available to plot trend.")

    # ------------------ PRODUCTS TAB ------------------
    with tab_products:
        st.subheader("Inventory Management")
        
        prod_action = st.radio("Choose Action", ["View & Manage Products", "Add New Product"], horizontal=True)
        
        if prod_action == "Add New Product":
            st.markdown("#### Create New Listing")
            
            with st.form("add_product_form", clear_on_submit=True):
                col_title, col_cat = st.columns(2)
                with col_title:
                    title = st.text_input("Product Title*", placeholder="e.g. Apple iPad Air (5th Gen)")
                with col_cat:
                    category = st.selectbox("Category*", ["Mobiles", "Electronics", "Fashion", "Home & Kitchen", "Books", "Other"])
                    custom_category = ""
                    if category == "Other":
                        custom_category = st.text_input("Specify Custom Category*", placeholder="e.g. Beauty")
                
                col_price, col_stock = st.columns(2)
                with col_price:
                    price = st.number_input("Selling Price (₹)*", min_value=1.0, value=999.0, step=10.0)
                with col_stock:
                    stock = st.number_input("Initial Inventory Count*", min_value=0, value=10, step=1)
                
                description = st.text_area("Product Description*", placeholder="Provide detailed specs, model info, and key selling points...")
                
                st.markdown("##### Product Image")
                image_source = st.radio("Select Image Source", ["Upload Local File", "Provide Image URL"], horizontal=True)
                
                uploaded_file = None
                img_url = ""
                
                if image_source == "Upload Local File":
                    uploaded_file = st.file_uploader("Upload Product Photo (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])
                else:
                    img_url = st.text_input("Image URL", placeholder="https://images.unsplash.com/...")
                
                submitted = st.form_submit_button("List Product on Apna Bazaar", use_container_width=True)
                
                if submitted:
                    final_category = custom_category if category == "Other" else category
                    
                    if not title or not description or not final_category:
                        st.error("Please fill in all required (*) fields.")
                    else:
                        image_path = ""
                        
                        # Handle image save
                        if image_source == "Upload Local File" and uploaded_file is not None:
                            try:
                                # Save file locally
                                file_extension = os.path.splitext(uploaded_file.name)[1]
                                timestamp = int(time.time())
                                safe_title = "".join(x for x in title if x.isalnum())[:15]
                                filename = f"{safe_title}_{timestamp}{file_extension}"
                                
                                images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
                                full_path = os.path.join(images_dir, filename)
                                
                                # Use PIL to save uploaded image
                                img = Image.open(uploaded_file)
                                img.save(full_path)
                                
                                # Store relative path or absolute file path
                                image_path = f"images/{filename}"
                            except Exception as e:
                                st.error(f"Failed to save uploaded image: {e}")
                        else:
                            image_path = img_url if img_url else "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop" # fallback placeholder
                        
                        # Add to database
                        new_id = database.add_product(title, description, price, final_category, image_path, stock)
                        st.success(f"Successfully added product: **{title}** with ID: {new_id}!")
                        time.sleep(1)
                        st.rerun()
                        
        else:
            # View and Manage Products
            st.markdown("#### Active Catalog Listings")
            products = database.get_all_products()
            
            if not products:
                st.info("The catalog is currently empty. Add a product to get started.")
            else:
                # Convert to DataFrame for readable viewing
                df_prods = pd.DataFrame(products)
                
                # Show key fields
                display_cols = ['id', 'title', 'category', 'price', 'stock', 'rating']
                st.dataframe(
                    df_prods[display_cols],
                    column_config={
                        "id": "ID",
                        "title": "Product Title",
                        "category": "Category",
                        "price": st.column_config.NumberColumn("Price (₹)", format="₹%.2f"),
                        "stock": "Stock Quantity",
                        "rating": "Avg Rating"
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Edit or Delete selector
                st.markdown("---")
                st.markdown("#### Edit / Delete Listing")
                
                prod_choices = {f"ID {p['id']} - {p['title'][:40]}...": p['id'] for p in products}
                selected_prod_label = st.selectbox("Select Product to Modify", list(prod_choices.keys()))
                
                if selected_prod_label:
                    selected_id = prod_choices[selected_prod_label]
                    prod_data = database.get_product_by_id(selected_id)
                    
                    if prod_data:
                        col_edit, col_del = st.columns([3, 1])
                        
                        with col_edit:
                            st.markdown(f"##### Update Details for ID: {selected_id}")
                            with st.form(f"edit_form_{selected_id}"):
                                edit_title = st.text_input("Product Title", value=prod_data['title'])
                                edit_category = st.text_input("Category", value=prod_data['category'])
                                edit_price = st.number_input("Price (₹)", min_value=1.0, value=float(prod_data['price']), step=10.0)
                                edit_stock = st.number_input("Stock", min_value=0, value=int(prod_data['stock']), step=1)
                                edit_desc = st.text_area("Description", value=prod_data['description'])
                                edit_img = st.text_input("Image Path / URL", value=prod_data['image_path'] or "")
                                
                                save_btn = st.form_submit_button("Save Changes", use_container_width=True)
                                if save_btn:
                                    database.update_product(
                                        selected_id, 
                                        edit_title, 
                                        edit_desc, 
                                        edit_price, 
                                        edit_category, 
                                        edit_img, 
                                        edit_stock
                                    )
                                    st.success("Product details updated successfully!")
                                    time.sleep(1)
                                    st.rerun()
                                    
                        with col_del:
                            st.markdown("##### Remove Listing")
                            st.warning("Deleting this item is permanent and will remove it from search.")
                            confirm_del = st.button("Delete Permanently", type="primary", use_container_width=True, key=f"del_btn_{selected_id}")
                            if confirm_del:
                                database.delete_product(selected_id)
                                st.success("Product deleted successfully!")
                                time.sleep(1)
                                st.rerun()

    # ------------------ ORDERS TAB ------------------
    with tab_orders:
        st.subheader("Order Fulfilment Center")
        
        orders = database.get_all_orders()
        
        if not orders:
            st.info("No orders placed yet.")
        else:
            # Order summary dataframe
            df_orders = pd.DataFrame(orders)
            
            # Format display
            df_display = df_orders[['id', 'username', 'email', 'total_price', 'status', 'created_at']].copy()
            df_display['total_price'] = df_display['total_price'].map(lambda x: f"₹{x:,.2f}")
            
            st.dataframe(
                df_display,
                column_config={
                    "id": "Order ID",
                    "username": "Customer",
                    "email": "Email",
                    "total_price": "Order Total",
                    "status": "Current Status",
                    "created_at": "Order Date"
                },
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            st.markdown("#### Process Order")
            
            order_choices = {f"Order #{o['id']} - {o['username']} (₹{o['total_price']:,.2f})": o['id'] for o in orders}
            selected_order_label = st.selectbox("Select Order to Manage", list(order_choices.keys()))
            
            if selected_order_label:
                order_id = order_choices[selected_order_label]
                order_info = [o for o in orders if o['id'] == order_id][0]
                
                # Fetch order items
                items = database.get_order_items(order_id)
                
                # Display order details
                col_det1, col_det2 = st.columns(2)
                
                with col_det1:
                    st.markdown(f"**Customer:** {order_info['username']} ({order_info['email']})")
                    st.markdown(f"**Phone:** {order_info['phone']}")
                    st.markdown(f"**Shipping Address:** {order_info['address']}")
                    st.markdown(f"**Date:** {order_info['created_at']}")
                    st.markdown(f"**Payment Method:** {order_info['payment_method']}")
                    
                with col_det2:
                    st.markdown(f"#### Current Status: :{order_info['status']}")
                    
                    new_status = st.selectbox(
                        "Update Status", 
                        ["Pending", "Shipped", "Delivered", "Cancelled"], 
                        index=["Pending", "Shipped", "Delivered", "Cancelled"].index(order_info['status'])
                    )
                    
                    update_status_btn = st.button("Apply Status Change", use_container_width=True)
                    if update_status_btn:
                        database.update_order_status(order_id, new_status)
                        st.success(f"Order #{order_id} status updated to {new_status}!")
                        time.sleep(1)
                        st.rerun()
                
                st.markdown("##### Order Items Breakdown")
                for item in items:
                    # Handle image path
                    img_src = item['image_path']
                    if img_src and not img_src.startswith("http"):
                        # Local path
                        local_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_src)
                        if os.path.exists(local_img_path):
                            try:
                                img_src = Image.open(local_img_path)
                            except:
                                img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
                        else:
                            img_src = "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop"
                            
                    col_img, col_info = st.columns([1, 5])
                    with col_img:
                        if img_src:
                            st.image(img_src, width=60)
                    with col_info:
                        st.markdown(f"**{item['title']}**")
                        st.markdown(f"Qty: {item['quantity']} | Price: ₹{item['price']:,.2f} | Total: ₹{(item['price'] * item['quantity']):,.2f}")
                    st.markdown("<hr style='margin: 0.5rem 0; border: 0.5px solid #eaeaea;'>", unsafe_allow_html=True)

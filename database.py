import sqlite3
import os
import hashlib
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apna_bazaar.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Simple SHA-256 password hashing."""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initializes all tables and seeds the database with initial records."""
    # Ensure images directory exists
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    conn = get_connection()
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'customer')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image_path TEXT,
        stock INTEGER NOT NULL DEFAULT 0,
        rating REAL DEFAULT 4.0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Reviews Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
    )
    """)

    # Create Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Create Order Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    """)

    # Check if we need to seed the tables
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Seed users
        admin_pass = hash_password("admin123")
        customer_pass = hash_password("customer123")
        
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                       ("admin", admin_pass, "admin@apnabazaar.com", "admin"))
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                       ("priya", customer_pass, "priya@gmail.com", "customer"))

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Seed initial high-quality products with Unsplash image links
        initial_products = [
            # Mobiles
            ("Apple iPhone 15 Pro (128 GB) - Natural Titanium", 
             "Experience the ultimate iPhone experience. Features a strong and light aerospace-grade titanium design, a massive camera upgrade with a 48MP main sensor, and the groundbreaking A17 Pro chip.", 
             129900.0, "Mobiles", 
             "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500&auto=format&fit=crop", 
             15, 4.8),
            ("Samsung Galaxy S24 Ultra (512 GB) - Titanium Gray", 
             "Welcome to the era of mobile AI. With Galaxy S24 Ultra in your hands, you can unleash whole new levels of creativity, productivity and possibility. 200MP camera, built-in S Pen, and Snapdragon 8 Gen 3.", 
             139999.0, "Mobiles", 
             "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&auto=format&fit=crop", 
             20, 4.7),
            
            # Electronics
            ("Sony WH-1000XM5 Wireless Headphones", 
             "Industry leading noise cancellation with two processors controlling 8 microphones. Exceptional sound quality with High-Resolution Audio, up to 30-hour battery life, and ultra-comfortable design.", 
             29990.0, "Electronics", 
             "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop", 
             25, 4.6),
            ("Apple MacBook Air M3 (13.6-inch, 8GB RAM, 256GB SSD)", 
             "The M3 chip brings even greater capabilities to the super-portable MacBook Air. With up to 18 hours of battery life, a stunning Liquid Retina display, and an incredibly thin design, it's perfect for work and play.", 
             114900.0, "Electronics", 
             "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop", 
             10, 4.7),
            
            # Fashion
            ("Levis Men's Premium Denim Jacket", 
             "A classic denim jacket that stands the test of time. Crafted from high-quality 100% cotton denim, featuring a standard fit, button-up front, and button-flap chest pockets. Perfect for layering.", 
             3499.0, "Fashion", 
             "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500&auto=format&fit=crop", 
             50, 4.3),
            ("Daniel Wellington Minimalist Quartz Watch", 
             "Sleek and sophisticated. This minimalist timepiece features an ultra-thin 36mm rose gold case, an eggshell white dial, and a genuine brown leather strap. Water-resistant up to 3 ATM.", 
             12499.0, "Fashion", 
             "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop", 
             30, 4.5),
            
            # Home & Kitchen
            ("Philips Fully Automatic Smart Espresso Machine", 
             "Enjoy 5 delicious coffees from fresh beans, including Cappuccino, at your fingertips. The LatteGo system tops milk varieties with silky smooth froth, is easy to set up and can be cleaned in as little as 15 seconds.", 
             45999.0, "Home & Kitchen", 
             "https://images.unsplash.com/photo-1517256064527-09c53b2d0bc6?w=500&auto=format&fit=crop", 
             8, 4.4),
            ("Ergonomic Mesh High-Back Office Chair", 
             "Designed for comfort. Features a highly breathable double mesh back, adjustable lumbar support, adjustable 3D armrests, and a tilt lock mechanism. Supports up to 136 kg.", 
             8999.0, "Home & Kitchen", 
             "https://images.unsplash.com/photo-1505797149-43b0069ec26b?w=500&auto=format&fit=crop", 
             40, 4.2),
            
            # Books
            ("Atomic Habits by James Clear", 
             "No matter your goals, Atomic Habits offers a proven framework for improving—every day. James Clear, one of the world's leading experts on habit formation, reveals practical strategies to form good habits.", 
             499.0, "Books", 
             "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&auto=format&fit=crop", 
             100, 4.9)
        ]

        cursor.executemany("""
        INSERT INTO products (title, description, price, category, image_path, stock, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, initial_products)

        # Seed some dummy reviews
        cursor.execute("SELECT id FROM products")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        dummy_reviews = [
            (product_ids[0], "Rahul Sharma", 5, "Absolutely gorgeous! The Titanium feel is premium and battery life is way better."),
            (product_ids[0], "Ananya Iyer", 4, "Amazing camera, but very expensive. Charging speed could be faster."),
            (product_ids[1], "Amit Verma", 5, "The AI features are actually useful. Circle to Search is a game changer! Screen is incredible."),
            (product_ids[2], "Neha Gupta", 4, "Top-tier noise cancellation. Extremely comfortable for long flights. Audio is crisp."),
            (product_ids[8], "Vikram Malhotra", 5, "Life changing book! Everyone should read this to build good systems in life.")
        ]
        
        cursor.executemany("""
        INSERT INTO reviews (product_id, username, rating, comment)
        VALUES (?, ?, ?, ?)
        """, dummy_reviews)

        # Seed some dummy orders for analytics representation
        # Order 1 (Priya's order - Delivered)
        cursor.execute("""
        INSERT INTO orders (user_id, total_price, status, address, phone, payment_method, created_at)
        VALUES (2, 29990.0, 'Delivered', 'Sector 62, Noida, UP, 201301', '9876543210', 'UPI', '2026-05-10 14:30:00')
        """)
        order_id = cursor.lastrowid
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, 1, 29990.0)", (order_id, product_ids[2]))

        # Order 2 (Priya's order - Shipped)
        cursor.execute("""
        INSERT INTO orders (user_id, total_price, status, address, phone, payment_method, created_at)
        VALUES (2, 3998.0, 'Shipped', 'Sector 62, Noida, UP, 201301', '9876543210', 'Credit Card', '2026-05-20 10:15:00')
        """)
        order_id2 = cursor.lastrowid
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, 1, 3499.0)", (order_id2, product_ids[4]))
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, 1, 499.0)", (order_id2, product_ids[8]))

        # Order 3 (Priya's order - Pending)
        cursor.execute("""
        INSERT INTO orders (user_id, total_price, status, address, phone, payment_method, created_at)
        VALUES (2, 114900.0, 'Pending', 'Sector 62, Noida, UP, 201301', '9876543210', 'Net Banking', '2026-05-22 18:45:00')
        """)
        order_id3 = cursor.lastrowid
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, 1, 114900.0)", (order_id3, product_ids[3]))

    conn.commit()
    conn.close()

# Users DB methods
def add_user(username, password, email, role="customer"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                       (username, hash_password(password), email, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

# Products DB methods
def get_all_products(category=None, search_query=None, sort_by=None, min_price=0, max_price=1000000):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE price >= ? AND price <= ?"
    params = [min_price, max_price]

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if search_query:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")

    if sort_by == "Price: Low to High":
        query += " ORDER BY price ASC"
    elif sort_by == "Price: High to Low":
        query += " ORDER BY price DESC"
    elif sort_by == "Customer Rating":
        query += " ORDER BY rating DESC"
    else:
        query += " ORDER BY id DESC"

    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return dict(product) if product else None

def add_product(title, description, price, category, image_path, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO products (title, description, price, category, image_path, stock, rating)
    VALUES (?, ?, ?, ?, ?, ?, 4.0)
    """, (title, description, price, category, image_path, stock))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_product(product_id, title, description, price, category, image_path, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE products 
    SET title = ?, description = ?, price = ?, category = ?, image_path = ?, stock = ?
    WHERE id = ?
    """, (title, description, price, category, image_path, stock, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# Reviews DB methods
def get_reviews_for_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC", (product_id,))
    reviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return reviews

def add_review(product_id, username, rating, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO reviews (product_id, username, rating, comment)
    VALUES (?, ?, ?, ?)
    """, (product_id, username, rating, comment))
    
    # Recalculate average rating for product
    cursor.execute("SELECT AVG(rating) FROM reviews WHERE product_id = ?", (product_id,))
    avg_rating = cursor.fetchone()[0]
    if avg_rating:
        cursor.execute("UPDATE products SET rating = ? WHERE id = ?", (round(avg_rating, 1), product_id))
        
    conn.commit()
    conn.close()

# Orders DB methods
def create_order(user_id, total_price, address, phone, payment_method, cart_items):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create order entry
        cursor.execute("""
        INSERT INTO orders (user_id, total_price, address, phone, payment_method, status)
        VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (user_id, total_price, address, phone, payment_method))
        order_id = cursor.lastrowid
        
        # Add order items & update stock
        for product_id, item in cart_items.items():
            quantity = item['quantity']
            price = item['price']
            
            # Record order item
            cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
            """, (order_id, product_id, quantity, price))
            
            # Deduct stock
            cursor.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?", (quantity, product_id))
            
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_orders_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return orders

def get_order_items(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT oi.*, p.title, p.image_path 
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = ?
    """, (order_id,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

# Admin specific methods
def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT o.*, u.username, u.email 
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.created_at DESC
    """)
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return orders

def update_order_status(order_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

# Analytics methods
def get_analytics_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total Revenue
    cursor.execute("SELECT SUM(total_price) FROM orders WHERE status != 'Cancelled'")
    total_revenue = cursor.fetchone()[0] or 0.0
    
    # Total Orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0] or 0
    
    # Total Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0] or 0
    
    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'customer'")
    total_customers = cursor.fetchone()[0] or 0
    
    conn.close()
    return {
        "revenue": total_revenue,
        "orders": total_orders,
        "products": total_products,
        "customers": total_customers
    }

def get_revenue_by_category():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.category, SUM(oi.price * oi.quantity) as revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN orders o ON oi.order_id = o.id
    WHERE o.status != 'Cancelled'
    GROUP BY p.category
    """)
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def get_revenue_trend():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DATE(created_at) as date, SUM(total_price) as revenue
    FROM orders
    WHERE status != 'Cancelled'
    GROUP BY DATE(created_at)
    ORDER BY date ASC
    """)
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def get_order_status_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM orders GROUP BY status")
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

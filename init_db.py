#!/usr/bin/env python3
"""
Initialize database with admin user
"""
import sqlite3
import hashlib
import os

def create_simple_admin():
    """Create admin user with simple password hashing"""
    
    # Remove existing database
    if os.path.exists("ecommerce.db"):
        os.remove("ecommerce.db")
        print("🗑️ Removed existing database")
    
    # Create new database
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR UNIQUE NOT NULL,
            username VARCHAR UNIQUE NOT NULL,
            hashed_password VARCHAR NOT NULL,
            full_name VARCHAR,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """)
    
    # Create categories table
    cursor.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR UNIQUE NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL,
            description TEXT,
            price FLOAT NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            sku VARCHAR UNIQUE,
            is_active BOOLEAN DEFAULT 1,
            image_url VARCHAR,
            category_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number VARCHAR UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            total_amount FLOAT NOT NULL,
            status VARCHAR DEFAULT 'pending',
            shipping_address VARCHAR NOT NULL,
            shipping_city VARCHAR NOT NULL,
            shipping_postal_code VARCHAR NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price FLOAT NOT NULL,
            total_price FLOAT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)
    
    # Simple password hash (for demo purposes)
    password = "admin"
    simple_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert admin user
    cursor.execute("""
        INSERT INTO users (username, email, full_name, hashed_password, is_admin, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("admin", "admin@ecommerce.com", "System Administrator", simple_hash, 1, 1))
    
    # Insert fashion categories
    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, ("Women's Clothing", "Dresses, tops, pants, and women's fashion"))
    
    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, ("Men's Clothing", "Shirts, pants, jackets, and men's fashion"))
    
    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, ("Women's Shoes", "Heels, sneakers, boots, and women's footwear"))
    
    cursor.execute("""
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """, ("Men's Shoes", "Sneakers, dress shoes, boots, and men's footwear"))
    
    # Insert sample fashion products with Ethiopian Birr prices and images
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Elegant Black Dress", "Beautiful black evening dress\nSize: S, M, L, XL\nColor: Black", 2699.99, 25, "DRESS-001", 1, "https://images.unsplash.com/photo-1566479179817-c0ae8e5b4e8e?w=400&h=600&fit=crop"))
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Classic White Sneakers", "Comfortable white sneakers for everyday wear\nSize: 36, 37, 38, 39, 40, 41, 42\nColor: White", 2399.99, 50, "SNEAK-001", 3, "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop"))
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Men's Casual Shirt", "Cotton casual shirt, perfect for everyday wear\nSize: S, M, L, XL, XXL\nColor: Blue", 1399.99, 30, "SHIRT-001", 2, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=600&fit=crop"))
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Leather Boots", "Premium leather boots for men\nSize: 40, 41, 42, 43, 44, 45\nColor: Brown", 3899.99, 20, "BOOT-001", 4, "https://images.unsplash.com/photo-1608256246200-53e8b47b2dc1?w=400&h=600&fit=crop"))
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Traditional Ethiopian Dress", "Beautiful traditional Ethiopian habesha kemis\nSize: S, M, L, XL\nColor: White with colorful borders", 4599.99, 15, "TRAD-001", 1, "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?w=400&h=600&fit=crop"))
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, sku, category_id, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Women's High Heels", "Elegant high heel shoes for special occasions\nSize: 36, 37, 38, 39, 40\nColor: Black", 1899.99, 35, "HEEL-001", 3, "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=400&fit=crop"))
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print("✅ Admin user created:")
    print("   Username: admin")
    print("   Password: admin")
    print("✅ Ethiopian Fashion Store ready:")
    print("   - Women's Clothing, Men's Clothing")
    print("   - Women's Shoes, Men's Shoes")
    print("   - Prices in Ethiopian Birr (ETB)")
    print("   - Sample fashion items with images included")
    print("   - Traditional Ethiopian dress added!")

if __name__ == "__main__":
    create_simple_admin()
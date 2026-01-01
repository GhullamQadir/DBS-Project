#!/usr/bin/env python3
"""
Database Initialization Script
Creates the SQLite database and tables for the inventory management system
"""

import sqlite3
from datetime import datetime

def init_database():
    """Initialize the SQLite database with schema and sample data"""

    # Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect('inventory_new.db')
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            unit_price REAL NOT NULL,
            reorder_level INTEGER DEFAULT 10,
            image_url TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create suppliers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            outstanding_balance REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE NOT NULL,
            supplier_id INTEGER,
            purchase_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_amount REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    ''')

    # Create purchase_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE NOT NULL,
            customer_name TEXT,
            sale_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount_amount REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            payment_status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create sale_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Create stock_movements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            movement_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            reference_type TEXT,
            reference_id INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Insert sample data for products
    products_data = [
        ('Wireless Mouse', 'WM-001', 'Electronics', 150, 29.99, 20, 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400'),
        ('Mechanical Keyboard', 'KB-002', 'Electronics', 75, 89.99, 15, 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400'),
        ('USB-C Hub', 'UH-003', 'Accessories', 200, 45.99, 30, 'https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?w=400'),
        ('Monitor Stand', 'MS-004', 'Furniture', 50, 34.99, 10, 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400'),
        ('Webcam HD', 'WC-005', 'Electronics', 120, 79.99, 25, 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO products (name, sku, category, quantity, unit_price, reorder_level, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products_data)

    # Insert sample data for suppliers
    suppliers_data = [
        ('Tech Distributors Ltd', 'John Smith', 'john@techdist.com', '+1-555-0101', 15000.00),
        ('Global Electronics', 'Sarah Johnson', 'sarah@globalelec.com', '+1-555-0102', 8500.00),
        ('Office Supplies Co', 'Mike Brown', 'mike@officesupplies.com', '+1-555-0103', 3200.00)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO suppliers (name, contact_person, email, phone, outstanding_balance)
        VALUES (?, ?, ?, ?, ?)
    ''', suppliers_data)

    # Commit changes
    conn.commit()
    conn.close()

    print("Database initialized successfully!")
    print("Created tables: products, suppliers, purchases, purchase_items, sales, sale_items, stock_movements")
    print("Inserted sample data for products and suppliers")
    print("Database file: inventory_new.db")

if __name__ == '__main__':
    init_database()

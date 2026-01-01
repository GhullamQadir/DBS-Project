"""
Inventory Management System - Python Flask Backend
===================================================
Students: This is a complete Flask backend example

Setup:
1. pip install flask flask-cors psycopg2-binary python-dotenv
2. Create .env file with DATABASE_URL
3. python backend_flask.py

For MySQL: pip install flask-mysqlconnector
For SQLite: No additional install needed
"""

from flask import Flask, request, jsonify
import sqlite3
from datetime import date, datetime
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ============================================
# DATABASE CONNECTION
# ============================================
def get_db_connection():
    """Create database connection - using SQLite for new database"""
    # SQLite connection for new database
    conn = sqlite3.connect('inventory_new.db')
    conn.row_factory = sqlite3.Row
    return conn

    # For PostgreSQL (existing setup - commented out):
    # import psycopg2
    # from psycopg2.extras import RealDictCursor
    # conn = psycopg2.connect(
    #     host=os.getenv('DB_HOST', 'localhost'),
    #     database=os.getenv('DB_NAME', 'inventory_management'),
    #     user=os.getenv('DB_USER', 'postgres'),
    #     password=os.getenv('DB_PASSWORD', ''),
    #     cursor_factory=RealDictCursor
    # )
    # return conn

    # For MySQL, use:
    # import mysql.connector
    # conn = mysql.connector.connect(
    #     host='localhost',
    #     database='inventory_management',
    #     user='root',
    #     password=''
    # )
    # return conn


# Helper to serialize dates
def serialize_row(row):
    if row is None:
        return None
    result = dict(row)
    for key, value in result.items():
        if isinstance(value, (date, datetime)):
            result[key] = value.isoformat()
    return result


# ============================================
# PRODUCTS API
# ============================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products - SQL: SELECT * FROM products ORDER BY created_at DESC"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products ORDER BY created_at DESC')
        products = [serialize_row(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    """Get single product - SQL: SELECT * FROM products WHERE id = ?"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE id = ?', (id,))
        product = serialize_row(cur.fetchone())
        cur.close()
        conn.close()
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    """Create product - SQL: INSERT INTO products (...) VALUES (...) RETURNING *"""
    try:
        data = request.get_json()
        
        # Input validation
        if not data.get('name') or not data.get('sku'):
            return jsonify({'error': 'Name and SKU are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO products (name, sku, category, quantity, unit_price, reorder_level, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['sku'],
            data.get('category', ''),
            data.get('quantity', 0),
            data.get('unit_price', 0),
            data.get('reorder_level', 10),
            data.get('image_url', '')
        ))
        product_id = cur.lastrowid
        cur.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = serialize_row(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    """Update product - SQL: UPDATE products SET ... WHERE id = $1"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE products
            SET name = ?, sku = ?, category = ?, quantity = ?,
                unit_price = ?, reorder_level = ?, image_url = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['name'],
            data['sku'],
            data.get('category', ''),
            data.get('quantity', 0),
            data.get('unit_price', 0),
            data.get('reorder_level', 10),
            data.get('image_url', ''),
            id
        ))
        cur.execute('SELECT * FROM products WHERE id = ?', (id,))
        product = serialize_row(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Delete product - SQL: DELETE FROM products WHERE id = ?"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# SUPPLIERS API
# ============================================

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM suppliers ORDER BY name')
        suppliers = [serialize_row(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(suppliers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM suppliers WHERE id = ?', (id,))
        supplier = serialize_row(cur.fetchone())
        cur.close()
        conn.close()
        if supplier is None:
            return jsonify({'error': 'Supplier not found'}), 404
        return jsonify(supplier)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO suppliers (name, contact_person, email, phone, address, outstanding_balance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('contact_person', ''),
            data['email'],
            data.get('phone', ''),
            data.get('address', ''),
            data.get('outstanding_balance', 0)
        ))
        supplier_id = cur.lastrowid
        cur.execute('SELECT * FROM suppliers WHERE id = ?', (supplier_id,))
        supplier = serialize_row(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(supplier), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suppliers/<int:id>', methods=['PUT'])
def update_supplier(id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE suppliers
            SET name = ?, contact_person = ?, email = ?, phone = ?,
                address = ?, outstanding_balance = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['name'],
            data.get('contact_person', ''),
            data['email'],
            data.get('phone', ''),
            data.get('address', ''),
            data.get('outstanding_balance', 0),
            id
        ))
        cur.execute('SELECT * FROM suppliers WHERE id = ?', (id,))
        supplier = serialize_row(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
        if supplier is None:
            return jsonify({'error': 'Supplier not found'}), 404
        return jsonify(supplier)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM suppliers WHERE id = ?', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Supplier deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# PURCHASES API
# ============================================

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    """Get all purchases with supplier info"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT p.*, s.name as supplier_name
            FROM purchases p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            ORDER BY p.purchase_date DESC
        ''')
        purchases = [serialize_row(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(purchases)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchases/<int:id>', methods=['GET'])
def get_purchase(id):
    """Get purchase with items"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get purchase header
        cur.execute('''
            SELECT p.*, s.name as supplier_name
            FROM purchases p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.id = ?
        ''', (id,))
        purchase = serialize_row(cur.fetchone())

        if purchase is None:
            return jsonify({'error': 'Purchase not found'}), 404

        # Get purchase items
        cur.execute('''
            SELECT pi.*, pr.name as product_name
            FROM purchase_items pi
            JOIN products pr ON pi.product_id = pr.id
            WHERE pi.purchase_id = ?
        ''', (id,))
        purchase['items'] = [serialize_row(row) for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        return jsonify(purchase)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchases', methods=['POST'])
def create_purchase():
    """Create purchase with items (transaction)"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Calculate totals
        subtotal = sum(item['quantity'] * item['unit_price'] for item in data['items'])
        tax_amount = subtotal * (data.get('tax_percent', 0) / 100)
        discount_amount = subtotal * (data.get('discount_percent', 0) / 100)
        total_amount = subtotal + tax_amount - discount_amount
        
        # Insert purchase header
        cur.execute('''
            INSERT INTO purchases (invoice_no, supplier_id, purchase_date, subtotal, tax_amount, discount_amount, total_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['invoice_no'],
            data['supplier_id'],
            data['purchase_date'],
            subtotal,
            tax_amount,
            discount_amount,
            total_amount
        ))
        purchase_id = cur.lastrowid
        
        # Insert items and update stock
        for item in data['items']:
            item_total = item['quantity'] * item['unit_price']
            
            # Insert purchase item
            cur.execute('''
                INSERT INTO purchase_items (purchase_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (purchase_id, item['product_id'], item['quantity'], item['unit_price'], item_total))

            # Update product quantity
            cur.execute('UPDATE products SET quantity = quantity + ? WHERE id = ?',
                       (item['quantity'], item['product_id']))

            # Record stock movement
            cur.execute('''
                INSERT INTO stock_movements (product_id, movement_type, quantity, reference_type, reference_id)
                VALUES (?, 'purchase', ?, 'purchase', ?)
            ''', (item['product_id'], item['quantity'], purchase_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': purchase_id, 'message': 'Purchase created'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# SALES API
# ============================================

@app.route('/api/sales', methods=['GET'])
def get_sales():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sales ORDER BY sale_date DESC')
        sales = [serialize_row(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(sales)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sales/<int:id>', methods=['GET'])
def get_sale(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM sales WHERE id = ?', (id,))
        sale = serialize_row(cur.fetchone())

        if sale is None:
            return jsonify({'error': 'Sale not found'}), 404

        cur.execute('''
            SELECT si.*, p.name as product_name
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        ''', (id,))
        sale['items'] = [serialize_row(row) for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        return jsonify(sale)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sales', methods=['POST'])
def create_sale():
    """Create sale with items (transaction)"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        
        subtotal = sum(item['quantity'] * item['selling_price'] for item in data['items'])
        discount_amount = subtotal * (data.get('discount_percent', 0) / 100)
        total_amount = subtotal - discount_amount
        
        cur.execute('''
            INSERT INTO sales (invoice_no, customer_name, sale_date, subtotal, discount_amount, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['invoice_no'],
            data['customer_name'],
            data['sale_date'],
            subtotal,
            discount_amount,
            total_amount
        ))
        sale_id = cur.lastrowid
        
        for item in data['items']:
            item_total = item['quantity'] * item['selling_price']
            
            cur.execute('''
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, selling_price, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (sale_id, item['product_id'], item['quantity'],
                  item.get('unit_price', item['selling_price']), item['selling_price'], item_total))

            cur.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?',
                       (item['quantity'], item['product_id']))

            cur.execute('''
                INSERT INTO stock_movements (product_id, movement_type, quantity, reference_type, reference_id)
                VALUES (?, 'sale', ?, 'sale', ?)
            ''', (item['product_id'], -item['quantity'], sale_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': sale_id, 'message': 'Sale created'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# DASHBOARD API
# ============================================

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT
                (SELECT COUNT(*) FROM products) as total_products,
                (SELECT COUNT(*) FROM products WHERE quantity <= reorder_level) as low_stock_count,
                (SELECT COALESCE(SUM(total_amount), 0) FROM sales WHERE sale_date = date('now')) as today_sales,
                (SELECT COALESCE(SUM(total_amount), 0) FROM purchases WHERE purchase_date = date('now')) as today_purchases
        ''')
        stats = serialize_row(cur.fetchone())
        cur.close()
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/chart-data', methods=['GET'])
def get_chart_data():
    """Get chart data for dashboard"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Monthly sales
        cur.execute('''
            SELECT
                strftime('%m', sale_date) as month_num,
                CASE strftime('%m', sale_date)
                    WHEN '01' THEN 'Jan'
                    WHEN '02' THEN 'Feb'
                    WHEN '03' THEN 'Mar'
                    WHEN '04' THEN 'Apr'
                    WHEN '05' THEN 'May'
                    WHEN '06' THEN 'Jun'
                    WHEN '07' THEN 'Jul'
                    WHEN '08' THEN 'Aug'
                    WHEN '09' THEN 'Sep'
                    WHEN '10' THEN 'Oct'
                    WHEN '11' THEN 'Nov'
                    WHEN '12' THEN 'Dec'
                END as month,
                COALESCE(SUM(total_amount), 0) as revenue
            FROM sales
            WHERE sale_date >= date('now', '-6 months')
            GROUP BY strftime('%m', sale_date)
            ORDER BY strftime('%m', sale_date)
        ''')
        monthly_sales = [serialize_row(row) for row in cur.fetchall()]
        
        # Category stock
        cur.execute('''
            SELECT category, SUM(quantity * unit_price) as value
            FROM products
            WHERE category IS NOT NULL AND category != ''
            GROUP BY category
        ''')
        category_stock = [serialize_row(row) for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        return jsonify({
            'monthly_sales': monthly_sales,
            'category_stock': category_stock
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# RUN SERVER
# ============================================
if __name__ == '__main__':
    print("Starting Inventory Management API Server...")
    print("API running at: http://localhost:3001")
    app.run(host='0.0.0.0', port=3001, debug=True)

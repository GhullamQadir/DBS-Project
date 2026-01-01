# Backend Setup Guide for Students

This document provides instructions for setting up the backend for the Inventory Management System.

## 📁 Project Structure

```
sql/
├── schema.sql    # Database tables and sample data
├── queries.sql   # CRUD operations reference
```

## 🗄️ Database Setup

### Option 1: PostgreSQL (Recommended)
```bash
# Install PostgreSQL
# Create database
createdb inventory_management

# Run schema
psql -d inventory_management -f sql/schema.sql
```

### Option 2: MySQL
```bash
# Create database
mysql -u root -p -e "CREATE DATABASE inventory_management"

# Run schema (modify SERIAL to AUTO_INCREMENT)
mysql -u root -p inventory_management < sql/schema.sql
```

### Option 3: SQLite
```bash
sqlite3 inventory.db < sql/schema.sql
```

## 🔧 Backend API Structure

Create a REST API with these endpoints:

### Products API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| GET | `/api/products/:id` | Get single product |
| POST | `/api/products` | Create product |
| PUT | `/api/products/:id` | Update product |
| DELETE | `/api/products/:id` | Delete product |

### Suppliers API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/suppliers` | Get all suppliers |
| GET | `/api/suppliers/:id` | Get single supplier |
| POST | `/api/suppliers` | Create supplier |
| PUT | `/api/suppliers/:id` | Update supplier |
| DELETE | `/api/suppliers/:id` | Delete supplier |

### Purchases API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/purchases` | Get all purchases |
| GET | `/api/purchases/:id` | Get purchase with items |
| POST | `/api/purchases` | Create purchase |

### Sales API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sales` | Get all sales |
| GET | `/api/sales/:id` | Get sale with items |
| POST | `/api/sales` | Create sale |

### Dashboard API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Get dashboard statistics |
| GET | `/api/dashboard/chart-data` | Get chart data |

## 📝 Backend Implementation Examples

### Option A: Python Flask (Recommended for beginners)

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python backend_flask.py
```

The complete Flask backend is in `backend_flask.py` with all CRUD endpoints.

### Option B: Node.js/Express

```bash
# Setup
npm init -y
npm install express cors pg dotenv
```

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({
  user: 'your_username',
  host: 'localhost',
  database: 'inventory_management',
  password: 'your_password',
  port: 5432,
});

// GET all products
app.get('/api/products', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM products ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST create product
app.post('/api/products', async (req, res) => {
  const { name, sku, category, quantity, unit_price, reorder_level, image_url } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO products (name, sku, category, quantity, unit_price, reorder_level, image_url) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *',
      [name, sku, category, quantity, unit_price, reorder_level, image_url]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ... Add more endpoints

app.listen(3001, () => console.log('Server running on port 3001'));
```

## 🔗 Connecting Frontend to Backend

In the React frontend, update the API calls. Example:

```typescript
// src/services/api.ts
const API_BASE = 'http://localhost:3001/api';

export const productService = {
  getAll: async () => {
    const res = await fetch(`${API_BASE}/products`);
    return res.json();
  },
  
  create: async (product: Product) => {
    const res = await fetch(`${API_BASE}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    });
    return res.json();
  },
  
  update: async (id: number, product: Product) => {
    const res = await fetch(`${API_BASE}/products/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    });
    return res.json();
  },
  
  delete: async (id: number) => {
    await fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' });
  },
};
```

## ✅ Tasks for Students

1. [ ] Set up your preferred database (PostgreSQL/MySQL/SQLite)
2. [ ] Run the schema.sql to create tables
3. [ ] Create a backend server (Node.js, Python Flask, Java Spring, etc.)
4. [ ] Implement all CRUD endpoints using queries from queries.sql
5. [ ] Connect the frontend to your backend API
6. [ ] Test all functionality

## 🎯 Learning Objectives

- Database design and normalization
- SQL CRUD operations
- REST API development
- Frontend-backend integration
- Transaction management (purchases/sales)

## 📚 Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [React Query for API calls](https://tanstack.com/query/latest)

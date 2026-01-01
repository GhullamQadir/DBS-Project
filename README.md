# Inventory Management System

A complete inventory management system built with React (frontend) and Flask (backend) with SQLite database.

## Quick Start 🚀

Get the application running locally in 3 simple steps:

```bash
# 1. Clone and setup backend
git clone <YOUR_GIT_URL>
cd <YOUR_PROJECT_NAME>
pip install -r requirements.txt
python init_db.py

# 2. Setup frontend (in another terminal)
npm install

# 3. Start both servers
python backend_flask.py    # Terminal 1: Backend on http://localhost:3001
npm run dev               # Terminal 2: Frontend on http://localhost:5173
```

**Open http://localhost:5173 in your browser** - That's it! 🎉

## Features

- **Product Management**: Add, view, update, and delete products with inventory tracking
- **Supplier Management**: Manage suppliers and track outstanding balances
- **Purchase Orders**: Create purchase orders with automatic inventory updates
- **Sales Management**: Process sales transactions and track revenue
- **Dashboard**: Real-time statistics and charts for business insights
- **Stock Monitoring**: Automatic low stock alerts and reorder level management
- **Reports**: Comprehensive reporting for inventory and sales data

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- shadcn/ui for UI components
- React Query for data fetching
- React Router for navigation

### Backend
- Flask with Python
- SQLite database
- Flask-CORS for cross-origin requests
- RESTful API design

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database:**
   ```bash
   python init_db.py
   ```

3. **Start the Flask backend server:**
   ```bash
   python backend_flask.py
   ```
   The backend will run on `http://localhost:3001`

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

### Accessing the Application

1. Open your browser and navigate to `http://localhost:5173`
2. The frontend will automatically connect to the backend API at `http://localhost:3001`

### Sample Data

The application comes with pre-loaded sample data including:
- 5 sample products (electronics, furniture, etc.)
- 3 sample suppliers
- Ready-to-use inventory data

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Create new product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Suppliers
- `GET /api/suppliers` - Get all suppliers
- `GET /api/suppliers/:id` - Get single supplier
- `POST /api/suppliers` - Create new supplier
- `PUT /api/suppliers/:id` - Update supplier
- `DELETE /api/suppliers/:id` - Delete supplier

### Purchases
- `GET /api/purchases` - Get all purchases
- `GET /api/purchases/:id` - Get purchase with items
- `POST /api/purchases` - Create new purchase

### Sales
- `GET /api/sales` - Get all sales
- `GET /api/sales/:id` - Get sale with items
- `POST /api/sales` - Create new sale

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/chart-data` - Get chart data

## Database Schema

The application uses SQLite with the following main tables:
- `products` - Product catalog with inventory levels
- `suppliers` - Supplier information and balances
- `purchases` - Purchase orders and items
- `sales` - Sales transactions and items
- `stock_movements` - Inventory movement audit trail

## Development

### Running Tests
```bash
# Backend tests
python test_flask.py

# API tests
python test_api.py
```

### Building for Production
```bash
# Frontend build
npm run build

# Backend (Flask handles this automatically in production mode)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.




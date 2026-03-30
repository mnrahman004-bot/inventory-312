# Inventory Management System with AI Demand Prediction

A complete AI-enabled inventory management system for small retail shops featuring real-time inventory tracking, sales management, and machine learning-based demand prediction.

## Features

### 1. **Authentication & Security**
- Secure admin login with JWT token-based authentication
- Password hashing using Werkzeug
- Session management and token expiration

### 2. **Dashboard**
- Real-time statistics dashboard
- Low stock alerts
- Daily sales summary
- Sales trend charts (7-day view)

### 3. **Product Management**
- Add, edit, and delete products
- Categorize products
- Track supplier information
- Set reorder levels
- View product inventory

### 4. **Inventory Control**
- Update stock quantities
- Track stock changes with inventory logs
- Low stock warning alerts
- Automatic stock deduction on sales

### 5. **Sales Management**
- Record product sales
- Generate invoices
- Track customer information
- Support multiple payment methods
- Automatic stock reduction

### 6. **Supplier Management**
- Add and manage suppliers
- Link suppliers to products
- Store supplier contact details
- View products by supplier

### 7. **Reports**
- Daily sales reports
- Monthly sales analysis
- Product sales reports
- Export reports to CSV
- Date range filtering

### 8. **AI/ML Features**
- **Demand Prediction**: Uses scikit-learn linear regression to predict next week's demand
- **Reorder Recommendations**: Automatically suggests reorder quantities based on:
  - Historical sales data
  - Average daily sales
  - Safety stock calculations
  - Lead time considerations
- **Confidence Scores**: R² values indicate prediction accuracy

### 9. **Database**
- SQLite for data persistence
- Comprehensive data models for all entities
- Automatic audit logging with inventory_logs table

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5
- **Backend**: Python Flask
- **Database**: SQLite
- **Machine Learning**: Scikit-learn with NumPy
- **Authentication**: Flask-JWT-Extended
- **API**: RESTful JSON API with CORS support

## Project Structure

```
inventory_management_system/
├── backend/
│   ├── app.py                 # Flask application factory
│   ├── models.py              # SQLAlchemy database models
│   ├── routes.py              # All API endpoints
│   └── demand_prediction.py   # ML module for demand prediction
├── frontend/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── products.html          # Product management
│   ├── sales.html             # Sales transactions
│   ├── suppliers.html         # Supplier management
│   ├── reports.html           # Reports and analytics
│   └── static/
│       └── css/
│           └── style.css      # Global styling
├── database/
│   └── inventory.db           # SQLite database (auto-created)
├── init_db.py                 # Database initialization with sample data
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Clone/Download the Project
```bash
cd inventory_management_system
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database with Sample Data
```bash
python init_db.py
```

This will:
- Create the SQLite database
- Initialize all tables
- Create an admin user (username: `admin`, password: `admin123`)
- Add 4 sample suppliers
- Add 10 sample products
- Generate 30 days of sales history

### Step 5: Run the Application
```bash
cd backend
python app.py
```

The application will start at `http://localhost:5000`

## Usage

### 1. Login
- Navigate to `http://localhost:5000`
- Login with credentials:
  - **Username**: admin
  - **Password**: admin123

### 2. Dashboard
- View key metrics (total products, low stock count, today's sales)
- Monitor sales trends with interactive charts
- Check low stock alerts

### 3. Product Management
- Click "Products" in sidebar
- Add new products with supplier assignment
- Edit product details and prices
- Update stock quantities
- Delete products (without sales history)

### 4. Record Sales
- Click "Sales" in sidebar
- Click "+ New Sale" button
- Select product and quantity
- Enter customer information
- Choose payment method
- System automatically updates inventory

### 5. Manage Suppliers
- Click "Suppliers" in sidebar
- Add new suppliers with contact details
- Edit supplier information
- Link suppliers to products

### 6. Generate Reports
- Click "Reports" in sidebar
- Select report type:
  - **Daily Sales**: View sales for a specific date
  - **Monthly Sales**: Monthly breakdown by day
  - **Product Sales**: Sales performance by product
- Export reports to CSV

### 7. AI Demand Prediction
- Access via API: `/api/predictions/demand/<product_id>`
- Get predictions for all products: `/api/predictions/all`

The system analyzes the last 90 days of sales data to predict:
- Next week's demand
- Reorder quantity recommendations
- Prediction confidence (R² score)

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Create admin account
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Add product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product
- `GET /api/products/categories` - Get all categories
- `POST /api/products/<id>/update-stock` - Update stock
- `GET /api/products/low-stock` - Get low stock items

### Sales
- `GET /api/sales` - List all sales
- `POST /api/sales` - Record new sale
- `GET /api/sales/<id>` - Get sale details
- `GET /api/sales/<id>/invoice` - Get invoice

### Suppliers
- `GET /api/suppliers` - List all suppliers
- `GET /api/suppliers/<id>` - Get supplier details
- `POST /api/suppliers` - Add supplier
- `PUT /api/suppliers/<id>` - Update supplier
- `DELETE /api/suppliers/<id>` - Delete supplier

### Reports
- `GET /api/reports/daily-sales` - Daily sales report
- `GET /api/reports/monthly-sales` - Monthly sales report
- `GET /api/reports/product-sales` - Product sales report
- `GET /api/reports/export-csv` - Export to CSV

### Predictions
- `GET /api/predictions/demand/<product_id>` - Get demand prediction
- `GET /api/predictions/all` - Get all predictions

### Dashboard
- `GET /api/dashboard/summary` - Dashboard summary
- `GET /api/dashboard/sales-chart` - Sales chart data

## Database Models

### User
- Secure admin authentication
- Email and username fields
- Password hashing

### Product
- Product details (name, category, price, quantity)
- Reorder level setting
- Supplier relationship
- Timestamps for audit trail

### Supplier
- Contact information
- Address details
- Product relationship

### Sale
- Transaction recording
- Invoice generation
- Customer and payment tracking
- Automatic stock reduction

### InventoryLog
- Track all inventory changes
- Reason and reference tracking
- Audit trail for all modifications

### DemandPrediction
- Store ML predictions
- Confidence scores
- Reorder recommendations

## Machine Learning Module

The demand prediction system uses:

1. **Data Collection**: Last 90 days of sales history
2. **Feature Engineering**: Daily sales aggregation
3. **Model**: Linear regression with scikit-learn
4. **Prediction**: 7-day demand forecast
5. **Reorder Logic**:
   - Base Demand = Average Daily Sales
   - Lead Time = 3 days (configurable)
   - Safety Stock = 2 days of inventory
   - Reorder Point = (Daily Sales × Lead Time) + Safety Stock

### Example Usage
```python
from demand_prediction import predict_product_demand

# Get prediction for product ID 1
prediction = predict_product_demand(1)
print(f"Predicted demand: {prediction['predicted_demand']} units")
print(f"Reorder quantity: {prediction['reorder_quantity']} units")
print(f"Confidence: {prediction['confidence']:.2%}")
```

## Configuration

### Modify settings in `backend/app.py`:

```python
# JWT expiration (days)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/inventory.db'

# Secret key (change in production!)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
```

### ML Prediction Settings in `backend/demand_prediction.py`:

```python
# Lead time days (for reorder calculation)
lead_time_days = 3

# Safety stock (days of inventory)
safety_stock = avg_daily_sales * 2
```

## Deployment

### Using Render Cloud Hosting

1. **Set up GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Environment**: Python 3.11
     - **Build command**: `pip install -r requirements.txt && python init_db.py`
     - **Start command**: `cd backend && python app.py`

4. **Set Environment Variables**
   ```
   JWT_SECRET_KEY=<your-secret-key>
   FLASK_ENV=production
   ```

5. **Deploy**
   - Click "Deploy"
   - Render will automatically build and deploy

### Local Development Server

```bash
# Run backend
cd backend
python app.py

# Application available at http://localhost:5000
```

## Troubleshooting

### Issue: "Cannot resolve 'socket' library"
**Solution**: Install required dependencies:
```bash
pip install --upgrade flask-cors
```

### Issue: Database locked
**Solution**: Delete `database/inventory.db` and reinitialize:
```bash
python init_db.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: CORS errors
**Solution**: Check that backend is running and accessible

## Security Considerations

⚠️ **Important for Production**:

1. **Change JWT Secret Key**
   - Modify `JWT_SECRET_KEY` in `backend/app.py`
   - Use a strong, random string

2. **Update Database Password** (if using PostgreSQL later)
   - Use environment variables
   - Never commit credentials

3. **Enable HTTPS**
   - Use SSL certificates
   - Set secure cookies

4. **Input Validation**
   - Implement rate limiting
   - Validate all inputs

5. **Database Backups**
   - Regular automated backups
   - Test restore procedures

## Performance Tips

1. **Indexing**: Database queries are optimized with proper indexes
2. **Pagination**: Product and sales lists are paginated (20 items per page)
3. **Caching**: Dashboard refreshes every 30 seconds
4. **Lazy Loading**: Frontend loads data on demand

## Testing

### Sample Data for Testing

The `init_db.py` script creates:
- 10 products across 3 categories
- 4 suppliers
- 30 days of sales history (~180 transactions)
- Real-world pricing and stock levels

### Test Scenarios

1. **Test Low Stock Alert**
   - Manually reduce product quantity below reorder level
   - Check dashboard alert

2. **Test Demand Prediction**
   - Create sales for a product
   - Generate prediction from `/api/predictions/demand/1`

3. **Test Reports**
   - Generate reports for different date ranges
   - Verify calculations

## Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics with Tableau
- [ ] Barcode scanning
- [ ] Multi-user roles (cashier, manager, etc.)
- [ ] Inventory expiration tracking
- [ ] Automated reorder purchase orders
- [ ] Real-time inventory sync
- [ ] Email notifications for low stock
- [ ] Advanced ML models (ARIMA, Prophet)
- [ ] Seasonal demand adjustment

## Support & License

For issues or questions, please check the API documentation or review the code comments.

This project is provided as-is for educational and commercial use.

## Author

Created as a complete inventory management solution for small retail businesses.

---

**Happy Inventory Managing! 📦**

# Quick Start Guide - Inventory Management System

## 5-Minute Setup

### Step 1: Install Python Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database with Sample Data (1 min)
```bash
python init_db.py
```
This creates:
- SQLite database
- Admin account: `admin` / `admin123`
- 10 sample products
- 4 suppliers
- 30 days of sales history

### Step 3: Start Backend Server (30 sec)
```bash
cd backend
python app.py
```

### Step 4: Open in Browser (30 sec)
Navigate to: **http://localhost:5000**

### Step 5: Login (30 sec)
- Username: `admin`
- Password: `admin123`

✅ **Done! System is ready to use**

---

## Quick Navigation

| Feature | Path | Description |
|---------|------|-------------|
| Dashboard | `/dashboard` | View key metrics and charts |
| Products | `/products` | Manage inventory items |
| Sales | `/sales` | Record and track sales |
| Suppliers | `/suppliers` | Manage supplier information |
| Reports | `/reports` | Generate sales reports |

---

## Common Tasks

### Add a New Product
1. Go to **Products** page
2. Click **+ Add Product**
3. Fill in details:
   - Product Name
   - Category
   - Price
   - Quantity
   - Reorder Level
   - Supplier
4. Click **Save**

### Record a Sale
1. Go to **Sales** page
2. Click **+ New Sale**
3. Select product and quantity
4. Enter customer details
5. Choose payment method
6. Click **Record Sale**
✅ Inventory automatically updated!

### View Sales Report
1. Go to **Reports** page
2. Choose report type:
   - Daily Sales
   - Monthly Sales
   - Product Sales
3. Select date/period
4. Click **Generate Report**
5. Optional: Click **Export to CSV**

### Track Low Stock Items
1. Go to **Dashboard**
2. Check "Low Stock Items" card
3. Or view full list in **Products** page
4. Items with "Low Stock" badge need reordering

---

## API Quick Reference

All APIs require Bearer token authentication:
```
Authorization: Bearer <token>
```

Get token via login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Example Curl Commands

**List Products**
```bash
curl http://localhost:5000/api/products \
  -H "Authorization: Bearer <token>"
```

**Record Sale**
```bash
curl -X POST http://localhost:5000/api/sales \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2,
    "customer_name": "John Doe",
    "payment_method": "Cash"
  }'
```

**Get Demand Prediction**
```bash
curl http://localhost:5000/api/predictions/demand/1 \
  -H "Authorization: Bearer <token>"
```

---

## Sample Data Overview

### Products (10 total)
- Laptop ($799.99) - Stock: 45
- Mouse ($29.99) - Stock: 150
- Keyboard ($79.99) - Stock: 85
- Monitor ($299.99) - Stock: 32
- USB Cable ($9.99) - Stock: 500
- Headphones ($149.99) - Stock: 60
- Desk Chair ($249.99) - Stock: 25
- Standing Desk ($499.99) - Stock: 18
- Webcam ($89.99) - Stock: 40
- Power Bank ($49.99) - Stock: 120

### Suppliers (4 total)
- Global Electronics Supply (USA)
- FastTrack Supplies (USA)
- Premium Distribution (USA)
- Quality Imports Ltd (UK)

### Sales History
- 30 days of transaction data
- ~180 sample sales
- Random daily variations
- Real customer scenarios

---

## Understanding the Dashboard

**Stats Cards:**
- **Total Products**: Count of all inventory items
- **Low Stock Items**: Products below reorder level
- **Today's Sales**: Total revenue for current day
- **Total Suppliers**: Number of active suppliers

**Sales Chart:**
- Shows 7-day sales trend
- Updates every 30 seconds
- Helps track sales patterns

**Low Stock Alert:**
- Appears if any items are below reorder level
- Click product to adjust stock
- Reorder recommendations available

---

## Demand Prediction Guide

The system uses machine learning to predict demand:

**How It Works:**
1. Analyzes last 90 days of sales data
2. Calculates average daily sales
3. Predicts next 7 days demand
4. Recommends reorder quantity

**Using Predictions:**
1. Go to **Products** page
2. Check product's predicted demand
3. Use recommendation for reordering

**API Access:**
```bash
# Get prediction for product ID 1
curl http://localhost:5000/api/predictions/demand/1 \
  -H "Authorization: Bearer <token>"

# Get all predictions
curl http://localhost:5000/api/predictions/all \
  -H "Authorization: Bearer <token>"
```

---

## Troubleshooting

**Q: Port 5000 already in use**
- Change port in `backend/app.py` line: `app.run(..., port=5001)`

**Q: Module not found error**
- Run: `pip install -r requirements.txt`

**Q: Database locked**
- Delete `database/inventory.db` and run `python init_db.py`

**Q: Login not working**
- Verify you're running `init_db.py` first
- Check credentials: admin / admin123

**Q: Can't access frontend pages**
- Ensure backend server is running (`python app.py`)
- Check http://localhost:5000 is accessible

---

## Next Steps

### 1. Customize Sample Data
Edit `init_db.py` to add your own:
- Products
- Suppliers
- Initial sales data

### 2. Configure System Settings
Edit `backend/config.py`:
- JWT expiration
- Lead time for predictions
- Safety stock levels

### 3. Deploy to Cloud
See README.md for deployment instructions

### 4. Explore Advanced Features
- Export reports to CSV
- Generate invoices
- Manage multiple suppliers
- Track inventory changes

---

## Key Features Summary

✅ **Authentication** - Secure admin login
✅ **Inventory Tracking** - Real-time stock levels
✅ **Sales Management** - Invoice generation
✅ **Supplier Management** - Track suppliers
✅ **Reports** - Sales analytics
✅ **AI/ML** - Demand prediction
✅ **Responsive UI** - Mobile-friendly
✅ **REST APIs** - Programmatic access

---

## Support

For detailed documentation, see:
- `README.md` - Full documentation
- `backend/routes.py` - API endpoint details
- `backend/models.py` - Database schema

---

**That's it! Enjoy managing your inventory! 📦**

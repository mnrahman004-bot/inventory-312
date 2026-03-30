# API Documentation - Inventory Management System

## Base URL
```
http://localhost:5000/api
```

## Authentication

All API endpoints require JWT Bearer token authentication.

### Get Access Token

**Endpoint**: `POST /auth/login`

**Request**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response** (200):
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@inventory.com",
    "is_admin": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Headers for Authenticated Requests**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Authentication Endpoints

### 1. Register Admin User

**Endpoint**: `POST /auth/register`

**Request**:
```json
{
  "username": "newadmin",
  "email": "admin@example.com",
  "password": "securepassword"
}
```

**Response** (201):
```json
{
  "message": "User created successfully",
  "user": {
    "id": 2,
    "username": "newadmin",
    "email": "admin@example.com",
    "is_admin": true,
    "created_at": "2024-01-15T10:35:00"
  }
}
```

### 2. Get Current User

**Endpoint**: `GET /auth/me`

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@inventory.com",
  "is_admin": true,
  "created_at": "2024-01-15T10:30:00"
}
```

---

## Product Endpoints

### 1. Get All Products

**Endpoint**: `GET /products?page=1&category=Electronics`

**Query Parameters**:
- `page` (int): Page number, default 1
- `category` (string): Filter by category (optional)

**Response** (200):
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "category": "Electronics",
      "description": "High-performance laptop",
      "price": 799.99,
      "quantity": 45,
      "reorder_level": 10,
      "supplier_id": 1,
      "supplier_name": "Global Electronics Supply",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-15T10:00:00"
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

### 2. Get Single Product

**Endpoint**: `GET /products/{id}`

**Path Parameters**:
- `id` (int): Product ID

**Response** (200):
```json
{
  "id": 1,
  "name": "Laptop",
  "category": "Electronics",
  "description": "High-performance laptop",
  "price": 799.99,
  "quantity": 45,
  "reorder_level": 10,
  "supplier_id": 1,
  "supplier_name": "Global Electronics Supply",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

### 3. Create Product

**Endpoint**: `POST /products`

**Request**:
```json
{
  "name": "Monitor",
  "category": "Electronics",
  "description": "4K display monitor",
  "price": 349.99,
  "quantity": 20,
  "reorder_level": 5,
  "supplier_id": 1
}
```

**Response** (201):
```json
{
  "message": "Product created successfully",
  "product": {
    "id": 11,
    "name": "Monitor",
    "category": "Electronics",
    "description": "4K display monitor",
    "price": 349.99,
    "quantity": 20,
    "reorder_level": 5,
    "supplier_id": 1,
    "supplier_name": "Global Electronics Supply",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  }
}
```

### 4. Update Product

**Endpoint**: `PUT /products/{id}`

**Request**:
```json
{
  "price": 379.99,
  "quantity": 25,
  "reorder_level": 8
}
```

**Response** (200):
```json
{
  "message": "Product updated successfully",
  "product": { /* updated product */ }
}
```

### 5. Delete Product

**Endpoint**: `DELETE /products/{id}`

**Response** (200):
```json
{
  "message": "Product deleted successfully"
}
```

### 6. Get Product Categories

**Endpoint**: `GET /products/categories`

**Response** (200):
```json
{
  "categories": [
    "Electronics",
    "Accessories",
    "Furniture"
  ]
}
```

### 7. Get Low Stock Products

**Endpoint**: `GET /products/low-stock`

**Response** (200):
```json
{
  "count": 3,
  "products": [
    {
      "id": 2,
      "name": "Desk Chair",
      "quantity": 4,
      "reorder_level": 10,
      /* ... more fields ... */
    }
  ]
}
```

### 8. Update Stock

**Endpoint**: `POST /products/{id}/update-stock`

**Request**:
```json
{
  "quantity": 50,
  "reason": "Restock from supplier"
}
```

**Response** (200):
```json
{
  "message": "Stock updated successfully",
  "product": { /* updated product */ }
}
```

---

## Sales Endpoints

### 1. Get All Sales

**Endpoint**: `GET /sales?page=1&start_date=2024-01-01&end_date=2024-01-31`

**Query Parameters**:
- `page` (int): Page number
- `start_date` (date): Filter from date (ISO format)
- `end_date` (date): Filter to date (ISO format)

**Response** (200):
```json
{
  "sales": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Laptop",
      "quantity": 2,
      "unit_price": 799.99,
      "total_amount": 1599.98,
      "customer_name": "John Doe",
      "payment_method": "Card",
      "invoice_number": "INV-20240115-0001",
      "notes": "Bulk order",
      "created_at": "2024-01-15T14:30:00"
    }
  ],
  "total": 15,
  "pages": 1
}
```

### 2. Get Single Sale

**Endpoint**: `GET /sales/{id}`

**Response** (200):
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "Laptop",
  /* ... full sale details ... */
}
```

### 3. Record Sale

**Endpoint**: `POST /sales`

**Request**:
```json
{
  "product_id": 1,
  "quantity": 2,
  "customer_name": "John Doe",
  "payment_method": "Card",
  "notes": "Bulk order"
}
```

**Response** (201):
```json
{
  "message": "Sale recorded successfully",
  "sale": { /* sale object */ },
  "invoice_number": "INV-20240115-0001"
}
```

### 4. Get Invoice

**Endpoint**: `GET /sales/{id}/invoice`

**Response** (200):
```json
{
  "invoice_number": "INV-20240115-0001",
  "date": "2024-01-15",
  "customer": "John Doe",
  "product": "Laptop",
  "quantity": 2,
  "unit_price": 799.99,
  "total": 1599.98,
  "payment_method": "Card"
}
```

---

## Supplier Endpoints

### 1. Get All Suppliers

**Endpoint**: `GET /suppliers?page=1`

**Response** (200):
```json
{
  "suppliers": [
    {
      "id": 1,
      "name": "Global Electronics Supply",
      "contact_person": "John Smith",
      "phone": "+1-555-0101",
      "email": "contact@globaltics.com",
      "address": "123 Industrial Ave",
      "city": "Los Angeles",
      "country": "USA",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 4,
  "pages": 1
}
```

### 2. Get Single Supplier

**Endpoint**: `GET /suppliers/{id}`

**Response** (200):
```json
{
  "id": 1,
  "name": "Global Electronics Supply",
  /* ... supplier details ... */
  "products": [
    /* linked products */
  ]
}
```

### 3. Create Supplier

**Endpoint**: `POST /suppliers`

**Request**:
```json
{
  "name": "New Supplier Co",
  "contact_person": "Jane Doe",
  "phone": "+1-555-9999",
  "email": "contact@newsupplier.com",
  "address": "999 Commerce Lane",
  "city": "New York",
  "country": "USA"
}
```

**Response** (201):
```json
{
  "message": "Supplier created successfully",
  "supplier": { /* supplier object */ }
}
```

### 4. Update Supplier

**Endpoint**: `PUT /suppliers/{id}`

**Request**:
```json
{
  "phone": "+1-555-8888",
  "email": "newemail@supplier.com"
}
```

**Response** (200):
```json
{
  "message": "Supplier updated successfully",
  "supplier": { /* updated supplier */ }
}
```

### 5. Delete Supplier

**Endpoint**: `DELETE /suppliers/{id}`

**Response** (200):
```json
{
  "message": "Supplier deleted successfully"
}
```

---

## Reports Endpoints

### 1. Daily Sales Report

**Endpoint**: `GET /reports/daily-sales?date=2024-01-15`

**Query Parameters**:
- `date` (date): Report date (YYYY-MM-DD)

**Response** (200):
```json
{
  "date": "2024-01-15",
  "total_sales": 5499.95,
  "total_quantity": 12,
  "number_of_transactions": 5,
  "sales": [
    /* sales for the day */
  ]
}
```

### 2. Monthly Sales Report

**Endpoint**: `GET /reports/monthly-sales?year=2024&month=1`

**Query Parameters**:
- `year` (int): Year
- `month` (int): Month (1-12)

**Response** (200):
```json
{
  "period": "2024-01",
  "total_sales": 125000.50,
  "total_quantity": 250,
  "number_of_transactions": 100,
  "daily_breakdown": {
    "2024-01-01": {
      "sales": 1200.00,
      "quantity": 5,
      "transactions": 2
    }
    /* more days ... */
  }
}
```

### 3. Product Sales Report

**Endpoint**: `GET /reports/product-sales?product_id=1`

**Query Parameters**:
- `product_id` (int): Product ID (optional, leave empty for all)

**Response** (200):
```json
{
  "product_name": "Laptop",
  "product_sales": {
    "1": {
      "name": "Laptop",
      "total_amount": 4799.94,
      "total_quantity": 6,
      "transactions": 3
    }
  },
  "total_sales": 4799.94
}
```

### 4. Export to CSV

**Endpoint**: `GET /reports/export-csv?start_date=2024-01-01&end_date=2024-01-31`

**Query Parameters**:
- `start_date` (date): Filter from date
- `end_date` (date): Filter to date

**Response** (200):
```json
{
  "csv_data": "Invoice,Date,Product,Quantity,Unit Price,Total,Customer,Payment\nINV-20240115...",
  "filename": "sales_report_20240115.csv"
}
```

---

## Prediction Endpoints

### 1. Get Product Demand Prediction

**Endpoint**: `GET /predictions/demand/{product_id}`

**Path Parameters**:
- `product_id` (int): Product ID

**Response** (200):
```json
{
  "product_id": 1,
  "product_name": "Laptop",
  "current_stock": 45,
  "status": "success",
  "predicted_demand": 8.5,
  "predicted_demand_per_day": 1.25,
  "next_7_days_forecast": [1, 2, 1, 1, 2, 1, 2],
  "reorder_quantity": 15,
  "confidence": 0.856,
  "historical_avg_daily_sales": 1.25
}
```

### 2. Get All Predictions

**Endpoint**: `GET /predictions/all`

**Response** (200):
```json
{
  "predictions": [
    {
      "product_id": 1,
      "product_name": "Laptop",
      "current_stock": 45,
      "status": "success",
      "predicted_demand": 8.5,
      "reorder_quantity": 15,
      "confidence": 0.856
    }
    /* more predictions ... */
  ]
}
```

---

## Dashboard Endpoints

### 1. Get Dashboard Summary

**Endpoint**: `GET /dashboard/summary`

**Response** (200):
```json
{
  "total_products": 50,
  "total_suppliers": 4,
  "low_stock_count": 3,
  "today_sales": 2450.75,
  "today_transactions": 5
}
```

### 2. Get Sales Chart Data

**Endpoint**: `GET /dashboard/sales-chart?days=7`

**Query Parameters**:
- `days` (int): Number of days (default: 7)

**Response** (200):
```json
[
  {
    "date": "2024-01-09",
    "sales": 1200.50
  },
  {
    "date": "2024-01-10",
    "sales": 1805.25
  }
  /* more days ... */
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "message": "Bad request",
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "message": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "message": "Resource not found",
  "error": "Product with ID 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "message": "Internal server error",
  "error": "Database connection failed"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. For production, add:

```python
from flask_limiter import Limiter

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## Pagination

Endpoints returning lists support pagination:

**Parameters**:
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)

**Response includes**:
```json
{
  "items": [...],
  "total": 100,
  "pages": 5,
  "current_page": 1
}
```

---

## Filtering & Searching

**Supported Filters**:
- Products by category
- Sales by date range
- Suppliers by name

**Example**:
```
GET /products?category=Electronics
GET /sales?start_date=2024-01-01&end_date=2024-01-31
```

---

## Example Client Code

### JavaScript/Fetch

```javascript
// Login
const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});
const { access_token } = await loginResponse.json();

// Use token for authenticated requests
const productsResponse = await fetch('http://localhost:5000/api/products', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const products = await productsResponse.json();
```

### Python/Requests

```python
import requests

# Login
login_response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={'username': 'admin', 'password': 'admin123'}
)
access_token = login_response.json()['access_token']

# Get products
products_response = requests.get(
    'http://localhost:5000/api/products',
    headers={'Authorization': f'Bearer {access_token}'}
)
products = products_response.json()
```

### cURL

```bash
# Login
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# Get products
curl http://localhost:5000/api/products \
  -H "Authorization: Bearer $TOKEN"
```

---

## Webhooks (Future Feature)

Not currently implemented. Would allow real-time notifications for:
- Low stock alerts
- Sales completed
- Inventory changes
- Demand predictions

---

## Versioning

Current API Version: **v1**

Future versions will be accessible at `/api/v2/`, etc.

---

## Support

For API issues:
1. Check response status codes
2. Review error messages
3. Verify authentication token
4. Check request format
5. See backend/routes.py for implementation details

---

**Last Updated**: 2024-01-15

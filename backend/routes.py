"""
API Routes for Inventory Management System
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import db, User, Product, Sale, Supplier, InventoryLog, DemandPrediction
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import csv
import io

# Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
product_bp = Blueprint('product', __name__, url_prefix='/api/products')
sale_bp = Blueprint('sale', __name__, url_prefix='/api/sales')
supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/suppliers')
report_bp = Blueprint('report', __name__, url_prefix='/api/reports')
prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predictions')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


# ============ AUTHENTICATION ROUTES ============

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Admin registration"""
    data = request.get_json()
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        is_admin=True
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# ============ PRODUCT ROUTES ============

@product_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    products = query.paginate(page=page, per_page=20)
    
    return jsonify({
        'products': [p.to_dict() for p in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': page
    }), 200


@product_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get single product"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    return jsonify(product.to_dict()), 200


@product_bp.route('', methods=['POST'])
@jwt_required()
def add_product():
    """Add new product"""
    data = request.get_json()
    
    if not data.get('name') or not data.get('price'):
        return jsonify({'message': 'Name and price required'}), 400
    
    product = Product(
        name=data.get('name'),
        category=data.get('category', 'Uncategorized'),
        description=data.get('description'),
        price=float(data.get('price')),
        quantity=int(data.get('quantity', 0)),
        reorder_level=int(data.get('reorder_level', 10)),
        supplier_id=data.get('supplier_id')
    )
    
    db.session.add(product)
    db.session.commit()
    
    # Create initial inventory log
    log = InventoryLog(
        product_id=product.id,
        previous_quantity=0,
        new_quantity=product.quantity,
        change_type='initial',
        reason='Product created'
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': product.to_dict()
    }), 201


@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'category' in data:
        product.category = data['category']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'reorder_level' in data:
        product.reorder_level = int(data['reorder_level'])
    if 'supplier_id' in data:
        product.supplier_id = data['supplier_id']
    
    product.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product.to_dict()
    }), 200


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete product"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Don't delete if there are sales records
    if Sale.query.filter_by(product_id=product_id).first():
        return jsonify({'message': 'Cannot delete product with sales history'}), 400
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200


@product_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all product categories"""
    categories = db.session.query(Product.category).distinct().all()
    return jsonify({
        'categories': [c[0] for c in categories if c[0]]
    }), 200


# ============ INVENTORY ROUTES ============

@product_bp.route('/<int:product_id>/update-stock', methods=['POST'])
@jwt_required()
def update_stock(product_id):
    """Update product stock"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    data = request.get_json()
    new_quantity = int(data.get('quantity', 0))
    reason = data.get('reason', 'Manual adjustment')
    
    # Create inventory log
    log = InventoryLog(
        product_id=product_id,
        previous_quantity=product.quantity,
        new_quantity=new_quantity,
        change_type='adjustment',
        reason=reason
    )
    
    product.quantity = new_quantity
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': 'Stock updated successfully',
        'product': product.to_dict()
    }), 200


@product_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get products with low stock"""
    products = Product.query.filter(Product.quantity <= Product.reorder_level).all()
    
    return jsonify({
        'count': len(products),
        'products': [p.to_dict() for p in products]
    }), 200


# ============ SALES ROUTES ============

@sale_bp.route('', methods=['GET'])
@jwt_required()
def get_sales():
    """Get all sales"""
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Sale.query
    
    if start_date:
        query = query.filter(Sale.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Sale.created_at <= datetime.fromisoformat(end_date))
    
    sales = query.order_by(desc(Sale.created_at)).paginate(page=page, per_page=20)
    
    return jsonify({
        'sales': [s.to_dict() for s in sales.items],
        'total': sales.total,
        'pages': sales.pages
    }), 200


@sale_bp.route('', methods=['POST'])
@jwt_required()
def record_sale():
    """Record a sale"""
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    if product.quantity < quantity:
        return jsonify({'message': 'Insufficient stock'}), 400
    
    # Create sale record
    invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    sale = Sale(
        product_id=product_id,
        quantity=quantity,
        unit_price=product.price,
        total_amount=product.price * quantity,
        customer_name=data.get('customer_name', 'Walk-in Customer'),
        payment_method=data.get('payment_method', 'Cash'),
        invoice_number=invoice_number,
        notes=data.get('notes')
    )
    
    # Update inventory
    product.quantity -= quantity
    
    # Create inventory log
    log = InventoryLog(
        product_id=product_id,
        previous_quantity=product.quantity + quantity,
        new_quantity=product.quantity,
        change_type='sale',
        reason=f'Sale {invoice_number}',
        reference_id=sale.id
    )
    
    db.session.add(sale)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': 'Sale recorded successfully',
        'sale': sale.to_dict(),
        'invoice_number': invoice_number
    }), 201


@sale_bp.route('/<int:sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    """Get sale details"""
    sale = Sale.query.get(sale_id)
    
    if not sale:
        return jsonify({'message': 'Sale not found'}), 404
    
    return jsonify(sale.to_dict()), 200


@sale_bp.route('/<int:sale_id>/invoice', methods=['GET'])
@jwt_required()
def get_invoice(sale_id):
    """Generate invoice"""
    sale = Sale.query.get(sale_id)
    
    if not sale:
        return jsonify({'message': 'Sale not found'}), 404
    
    invoice_data = {
        'invoice_number': sale.invoice_number,
        'date': sale.created_at.strftime('%Y-%m-%d'),
        'customer': sale.customer_name,
        'product': sale.product.name,
        'quantity': sale.quantity,
        'unit_price': sale.unit_price,
        'total': sale.total_amount,
        'payment_method': sale.payment_method
    }
    
    return jsonify(invoice_data), 200


# ============ SUPPLIER ROUTES ============

@supplier_bp.route('', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all suppliers"""
    page = request.args.get('page', 1, type=int)
    suppliers = Supplier.query.paginate(page=page, per_page=20)
    
    return jsonify({
        'suppliers': [s.to_dict() for s in suppliers.items],
        'total': suppliers.total,
        'pages': suppliers.pages
    }), 200


@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    """Get supplier details"""
    supplier = Supplier.query.get(supplier_id)
    
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    
    supplier_data = supplier.to_dict()
    supplier_data['products'] = [p.to_dict() for p in supplier.products]
    
    return jsonify(supplier_data), 200


@supplier_bp.route('', methods=['POST'])
@jwt_required()
def add_supplier():
    """Add new supplier"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Supplier name required'}), 400
    
    supplier = Supplier(
        name=data.get('name'),
        contact_person=data.get('contact_person'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        city=data.get('city'),
        country=data.get('country')
    )
    
    db.session.add(supplier)
    db.session.commit()
    
    return jsonify({
        'message': 'Supplier created successfully',
        'supplier': supplier.to_dict()
    }), 201


@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
@jwt_required()
def update_supplier(supplier_id):
    """Update supplier"""
    supplier = Supplier.query.get(supplier_id)
    
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        supplier.name = data['name']
    if 'contact_person' in data:
        supplier.contact_person = data['contact_person']
    if 'phone' in data:
        supplier.phone = data['phone']
    if 'email' in data:
        supplier.email = data['email']
    if 'address' in data:
        supplier.address = data['address']
    if 'city' in data:
        supplier.city = data['city']
    if 'country' in data:
        supplier.country = data['country']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Supplier updated successfully',
        'supplier': supplier.to_dict()
    }), 200


@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(supplier_id):
    """Delete supplier"""
    supplier = Supplier.query.get(supplier_id)
    
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    
    if supplier.products:
        return jsonify({'message': 'Cannot delete supplier with linked products'}), 400
    
    db.session.delete(supplier)
    db.session.commit()
    
    return jsonify({'message': 'Supplier deleted successfully'}), 200


# ============ REPORTS ROUTES ============

@report_bp.route('/daily-sales', methods=['GET'])
@jwt_required()
def daily_sales_report():
    """Daily sales report"""
    date_str = request.args.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    next_day = date_obj + timedelta(days=1)
    
    sales = Sale.query.filter(
        Sale.created_at >= date_obj,
        Sale.created_at < next_day
    ).all()
    
    total_sales = sum(s.total_amount for s in sales)
    total_quantity = sum(s.quantity for s in sales)
    
    return jsonify({
        'date': date_str,
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'number_of_transactions': len(sales),
        'sales': [s.to_dict() for s in sales]
    }), 200


@report_bp.route('/monthly-sales', methods=['GET'])
@jwt_required()
def monthly_sales_report():
    """Monthly sales report"""
    year = request.args.get('year', datetime.utcnow().year, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    sales = Sale.query.filter(
        Sale.created_at >= start_date,
        Sale.created_at < end_date
    ).all()
    
    total_sales = sum(s.total_amount for s in sales)
    total_quantity = sum(s.quantity for s in sales)
    
    # Group by day
    daily_data = {}
    for sale in sales:
        day = sale.created_at.strftime('%Y-%m-%d')
        if day not in daily_data:
            daily_data[day] = {'sales': 0, 'quantity': 0, 'transactions': 0}
        daily_data[day]['sales'] += sale.total_amount
        daily_data[day]['quantity'] += sale.quantity
        daily_data[day]['transactions'] += 1
    
    return jsonify({
        'period': f'{year}-{month:02d}',
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'number_of_transactions': len(sales),
        'daily_breakdown': daily_data
    }), 200


@report_bp.route('/product-sales', methods=['GET'])
@jwt_required()
def product_sales_report():
    """Product sales report"""
    product_id = request.args.get('product_id', type=int)
    
    if product_id:
        sales = Sale.query.filter_by(product_id=product_id).all()
        product = Product.query.get(product_id)
        product_name = product.name if product else 'Unknown'
    else:
        sales = Sale.query.all()
        product_name = 'All Products'
    
    # Group by product
    products_sales = {}
    for sale in sales:
        pid = sale.product_id
        if pid not in products_sales:
            products_sales[pid] = {
                'name': sale.product.name,
                'total_amount': 0,
                'total_quantity': 0,
                'transactions': 0
            }
        products_sales[pid]['total_amount'] += sale.total_amount
        products_sales[pid]['total_quantity'] += sale.quantity
        products_sales[pid]['transactions'] += 1
    
    return jsonify({
        'product_name': product_name,
        'product_sales': products_sales,
        'total_sales': sum(p['total_amount'] for p in products_sales.values())
    }), 200


@report_bp.route('/export-csv', methods=['GET'])
@jwt_required()
def export_csv():
    """Export sales to CSV"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Sale.query
    
    if start_date:
        query = query.filter(Sale.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Sale.created_at <= datetime.fromisoformat(end_date))
    
    sales = query.all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Invoice', 'Date', 'Product', 'Quantity', 'Unit Price', 'Total', 'Customer', 'Payment'])
    
    for sale in sales:
        writer.writerow([
            sale.invoice_number,
            sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            sale.product.name,
            sale.quantity,
            sale.unit_price,
            sale.total_amount,
            sale.customer_name,
            sale.payment_method
        ])
    
    return jsonify({
        'csv_data': output.getvalue(),
        'filename': f"sales_report_{datetime.utcnow().strftime('%Y%m%d')}.csv"
    }), 200


# ============ PREDICTION ROUTES ============

@prediction_bp.route('/demand/<int:product_id>', methods=['GET'])
@jwt_required()
def predict_demand(product_id):
    """Get demand prediction for product"""
    from demand_prediction import predict_product_demand
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    prediction_result = predict_product_demand(product_id)
    
    return jsonify(prediction_result), 200


@prediction_bp.route('/all', methods=['GET'])
@jwt_required()
def predict_all():
    """Get predictions for all products"""
    from demand_prediction import predict_all_products
    
    predictions = predict_all_products()
    
    return jsonify({
        'predictions': predictions
    }), 200


# ============ DASHBOARD ROUTES ============

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def dashboard_summary():
    """Dashboard summary"""
    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    low_stock_count = Product.query.filter(Product.quantity <= Product.reorder_level).count()
    
    # Today's sales
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    today_sales = Sale.query.filter(
        Sale.created_at >= today_start,
        Sale.created_at <= today_end
    ).all()
    
    today_amount = sum(s.total_amount for s in today_sales)
    today_transactions = len(today_sales)
    
    return jsonify({
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'low_stock_count': low_stock_count,
        'today_sales': today_amount,
        'today_transactions': today_transactions
    }), 200


@dashboard_bp.route('/sales-chart', methods=['GET'])
@jwt_required()
def sales_chart():
    """Sales chart data (last 7 days)"""
    days = int(request.args.get('days', 7))
    
    chart_data = []
    for i in range(days, 0, -1):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date, datetime.max.time())
        
        daily_sales = db.session.query(func.sum(Sale.total_amount)).filter(
            Sale.created_at >= date_start,
            Sale.created_at <= date_end
        ).scalar() or 0
        
        chart_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'sales': float(daily_sales)
        })
    
    return jsonify(chart_data), 200

"""
Database Initialization Script with Sample Data
Run this script to populate the database with example data
"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, User, Supplier, Product, Sale, InventoryLog
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("✓ Database tables created")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@inventory.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Admin user created (username: admin, password: admin123)")
        
        # Create suppliers
        suppliers_data = [
            {
                'name': 'Global Electronics Supply',
                'contact_person': 'John Smith',
                'phone': '+1-555-0101',
                'email': 'contact@globaltics.com',
                'address': '123 Industrial Ave',
                'city': 'Los Angeles',
                'country': 'USA'
            },
            {
                'name': 'FastTrack Supplies',
                'contact_person': 'Sarah Johnson',
                'phone': '+1-555-0102',
                'email': 'sales@fasttrack.com',
                'address': '456 Commerce Blvd',
                'city': 'Houston',
                'country': 'USA'
            },
            {
                'name': 'Premium Distribution',
                'contact_person': 'Mike Chen',
                'phone': '+1-555-0103',
                'email': 'info@premium-dist.com',
                'address': '789 Market St',
                'city': 'Chicago',
                'country': 'USA'
            },
            {
                'name': 'Quality Imports Ltd',
                'contact_person': 'Emma Wilson',
                'phone': '+44-208-0104',
                'email': 'contact@quality-imports.uk',
                'address': '321 Trade Avenue',
                'city': 'London',
                'country': 'UK'
            }
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
            suppliers.append(supplier)
        
        db.session.commit()
        print(f"✓ {len(suppliers)} suppliers created")
        
        # Create products
        products_data = [
            {'name': 'Laptop', 'category': 'Electronics', 'price': 799.99, 'quantity': 45, 'reorder_level': 10},
            {'name': 'Mouse', 'category': 'Accessories', 'price': 29.99, 'quantity': 150, 'reorder_level': 50},
            {'name': 'Keyboard', 'category': 'Accessories', 'price': 79.99, 'quantity': 85, 'reorder_level': 30},
            {'name': 'Monitor', 'category': 'Electronics', 'price': 299.99, 'quantity': 32, 'reorder_level': 10},
            {'name': 'USB Cable', 'category': 'Accessories', 'price': 9.99, 'quantity': 500, 'reorder_level': 100},
            {'name': 'Headphones', 'category': 'Accessories', 'price': 149.99, 'quantity': 60, 'reorder_level': 15},
            {'name': 'Desk Chair', 'category': 'Furniture', 'price': 249.99, 'quantity': 25, 'reorder_level': 5},
            {'name': 'Standing Desk', 'category': 'Furniture', 'price': 499.99, 'quantity': 18, 'reorder_level': 5},
            {'name': 'Webcam', 'category': 'Electronics', 'price': 89.99, 'quantity': 40, 'reorder_level': 10},
            {'name': 'Power Bank', 'category': 'Accessories', 'price': 49.99, 'quantity': 120, 'reorder_level': 30},
        ]
        
        products = []
        for idx, product_data in enumerate(products_data):
            product_data['supplier_id'] = suppliers[idx % len(suppliers)].id
            product = Product(**product_data)
            db.session.add(product)
            products.append(product)
        
        db.session.commit()
        print(f"✓ {len(products)} products created")
        
        # Create inventory logs for initial stock
        for product in products:
            log = InventoryLog(
                product_id=product.id,
                previous_quantity=0,
                new_quantity=product.quantity,
                change_type='initial',
                reason='Initial stock'
            )
            db.session.add(log)
        
        db.session.commit()
        print("✓ Initial inventory logs created")
        
        # Create sales history (last 30 days)
        sales_count = 0
        for days_ago in range(30):
            date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Random 2-8 sales per day
            daily_sales = random.randint(2, 8)
            
            for _ in range(daily_sales):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                
                # Only create sale if stock available
                if product.quantity >= quantity:
                    customer_names = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Walk-in Customer', 'David Lee', 'Emma Davis']
                    payment_methods = ['Cash', 'Card', 'Check', 'Mobile Money']
                    
                    sale = Sale(
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=product.price,
                        total_amount=product.price * quantity,
                        customer_name=random.choice(customer_names),
                        payment_method=random.choice(payment_methods),
                        invoice_number=f"INV-{date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                        created_at=date + timedelta(hours=random.randint(8, 18), minutes=random.randint(0, 59))
                    )
                    
                    # Update product stock
                    product.quantity -= quantity
                    
                    # Create inventory log
                    log = InventoryLog(
                        product_id=product.id,
                        previous_quantity=product.quantity + quantity,
                        new_quantity=product.quantity,
                        change_type='sale',
                        reason=f'Sale {sale.invoice_number}',
                        reference_id=sale.id
                    )
                    
                    db.session.add(sale)
                    db.session.add(log)
                    sales_count += 1
        
        db.session.commit()
        print(f"✓ {sales_count} sales transactions created")
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE!")
        print("="*50)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nAll sample data has been loaded successfully!")


if __name__ == '__main__':
    init_database()

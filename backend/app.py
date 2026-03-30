"""
Flask Application - Inventory Management System
"""
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db
import os

def create_app():
    """Application factory"""
    app = Flask(__name__, 
                template_folder='../frontend',
                static_folder='../frontend/static')
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes import auth_bp, product_bp, sale_bp, supplier_bp, report_bp, prediction_bp, dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(sale_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(dashboard_bp)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad request', 'error': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found', 'error': str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'message': 'Internal server error', 'error': str(error)}), 500
    
    # Serve frontend pages
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/products')
    def products():
        return render_template('products.html')
    
    @app.route('/sales')
    def sales():
        return render_template('sales.html')
    
    @app.route('/suppliers')
    def suppliers():
        return render_template('suppliers.html')
    
    @app.route('/reports')
    def reports():
        return render_template('reports.html')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

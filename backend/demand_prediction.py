"""
Machine Learning Module - Demand Prediction
Uses scikit-learn to predict future product demand based on historical sales data
"""
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from models import db, Sale, Product, DemandPrediction
import warnings

warnings.filterwarnings('ignore')


def get_product_sales_data(product_id, days=90):
    """
    Get historical sales data for a product
    
    Args:
        product_id: Product ID
        days: Number of days to look back
        
    Returns:
        list of tuples: (day_number, quantity, amount)
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    sales = Sale.query.filter(
        Sale.product_id == product_id,
        Sale.created_at >= start_date
    ).all()
    
    # Group sales by day
    daily_sales = {}
    for sale in sales:
        day = sale.created_at.date()
        if day not in daily_sales:
            daily_sales[day] = {'quantity': 0, 'amount': 0}
        daily_sales[day]['quantity'] += sale.quantity
        daily_sales[day]['amount'] += sale.total_amount
    
    return daily_sales


def prepare_training_data(daily_sales_dict):
    """
    Prepare data for ML model
    
    Args:
        daily_sales_dict: Dictionary of daily sales data
        
    Returns:
        tuple: (X features, y target)
    """
    if not daily_sales_dict:
        return None, None
    
    sorted_dates = sorted(daily_sales_dict.keys())
    
    # Create X (day index) and y (quantity sold)
    X = np.array([i for i in range(len(sorted_dates))]).reshape(-1, 1)
    y = np.array([daily_sales_dict[date]['quantity'] for date in sorted_dates])
    
    return X, y


def train_demand_model(product_id):
    """
    Train linear regression model for demand prediction
    
    Args:
        product_id: Product ID
        
    Returns:
        dict: Model metrics and predictions
    """
    daily_sales = get_product_sales_data(product_id)
    
    if not daily_sales:
        return {
            'status': 'no_data',
            'message': 'Not enough sales data for prediction',
            'predicted_demand': 0,
            'reorder_quantity': 0,
            'confidence': 0
        }
    
    X, y = prepare_training_data(daily_sales)
    
    if X is None or len(X) < 3:
        return {
            'status': 'insufficient_data',
            'message': 'Need at least 3 days of sales data',
            'predicted_demand': 0,
            'reorder_quantity': 0,
            'confidence': 0
        }
    
    try:
        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate R-squared (confidence)
        score = model.score(X, y)
        
        # Predict next 7 days
        future_days = np.array([len(X) + i for i in range(7)]).reshape(-1, 1)
        future_predictions = model.predict(future_days)
        
        # Ensure no negative predictions
        future_predictions = np.maximum(future_predictions, 0)
        
        # Calculate average demand for next week
        predicted_demand = np.mean(future_predictions)
        
        # Calculate reorder quantity (safety stock + predicted demand)
        product = Product.query.get(product_id)
        current_stock = product.quantity if product else 0
        avg_daily_sales = np.mean(y)
        
        # Reorder point: (avg daily sales × lead time) + safety stock
        lead_time_days = 3  # Assumed lead time
        safety_stock = avg_daily_sales * 2  # 2 days of stock as buffer
        reorder_point = (avg_daily_sales * lead_time_days) + safety_stock
        
        reorder_quantity = max(0, int(reorder_point - current_stock))
        
        return {
            'status': 'success',
            'predicted_demand': float(np.round(predicted_demand, 2)),
            'predicted_demand_per_day': float(np.round(avg_daily_sales, 2)),
            'next_7_days_forecast': [int(p) for p in future_predictions],
            'reorder_quantity': reorder_quantity,
            'confidence': float(np.round(score, 3)),
            'current_stock': current_stock,
            'historical_avg_daily_sales': float(np.round(avg_daily_sales, 2))
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'predicted_demand': 0,
            'reorder_quantity': 0,
            'confidence': 0
        }


def predict_product_demand(product_id):
    """
    Get demand prediction for single product
    
    Args:
        product_id: Product ID
        
    Returns:
        dict: Prediction results
    """
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}
    
    prediction = train_demand_model(product_id)
    
    # Store prediction in database
    existing_pred = DemandPrediction.query.filter_by(product_id=product_id).first()
    
    pred_record = existing_pred if existing_pred else DemandPrediction(product_id=product_id)
    pred_record.predicted_demand = prediction.get('predicted_demand', 0)
    pred_record.reorder_quantity = prediction.get('reorder_quantity', 0)
    pred_record.confidence = prediction.get('confidence', 0)
    pred_record.predicted_date = datetime.utcnow() + timedelta(days=7)
    
    db.session.add(pred_record)
    db.session.commit()
    
    return {
        'product_id': product_id,
        'product_name': product.name,
        'current_stock': product.quantity,
        **prediction
    }


def predict_all_products():
    """
    Generate predictions for all products
    
    Returns:
        list: Predictions for all products
    """
    products = Product.query.all()
    predictions = []
    
    for product in products:
        pred = predict_product_demand(product.id)
        if pred.get('status') == 'success':
            predictions.append(pred)
    
    # Sort by reorder quantity (highest priority first)
    predictions.sort(key=lambda x: x.get('reorder_quantity', 0), reverse=True)
    
    return predictions


def get_demand_forecast_chart(product_id, days=30):
    """
    Generate forecast chart data for next N days
    
    Args:
        product_id: Product ID
        days: Number of days to forecast
        
    Returns:
        list: Forecast data with dates
    """
    daily_sales = get_product_sales_data(product_id)
    X, y = prepare_training_data(daily_sales)
    
    if X is None:
        return []
    
    model = LinearRegression()
    model.fit(X, y)
    
    forecast = []
    today = datetime.utcnow()
    
    for i in range(days):
        date = today + timedelta(days=i)
        day_index = np.array([[len(X) + i]])
        predicted_qty = max(0, model.predict(day_index)[0])
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'predicted_demand': int(predicted_qty),
            'day': i + 1
        })
    
    return forecast


# Example usage for batch prediction
def generate_batch_predictions():
    """
    Generate and store predictions for all products at once
    Useful for scheduled jobs
    """
    products = Product.query.all()
    
    results = {
        'total_products': len(products),
        'predictions': [],
        'reorder_recommendations': []
    }
    
    for product in products:
        pred = predict_product_demand(product.id)
        
        if pred.get('status') == 'success':
            results['predictions'].append(pred)
            
            if pred.get('reorder_quantity', 0) > 0:
                results['reorder_recommendations'].append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'reorder_quantity': pred['reorder_quantity'],
                    'supplier_id': product.supplier_id,
                    'predicted_demand': pred['predicted_demand'],
                    'confidence': pred['confidence']
                })
    
    return results

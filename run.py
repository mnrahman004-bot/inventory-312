#!/usr/bin/env python3
"""
StockSense IMS — convenience launcher.
Run from the project root:  python run.py
"""
import sys
import os

# Make backend importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app
from models import init_db, seed_data

if __name__ == '__main__':
    os.makedirs('database', exist_ok=True)
    init_db()
    seed_data()
    print("\n" + "="*50)
    print("  📦  StockSense IMS — Starting server")
    print("="*50)
    print("  🌐  URL      : http://localhost:5000")
    print("  🔐  Username : admin")
    print("  🔑  Password : admin123")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)

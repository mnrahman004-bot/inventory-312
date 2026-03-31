import os
import glob
import re

frontend_dir = r"d:\inventory_management_system\frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update routing links
    content = content.replace('href="/dashboard"', 'href="dashboard.html"')
    content = content.replace('href="/products"', 'href="products.html"')
    content = content.replace('href="/sales"', 'href="sales.html"')
    content = content.replace('href="/suppliers"', 'href="suppliers.html"')
    content = content.replace('href="/reports"', 'href="reports.html"')
    content = content.replace('href="/login"', 'href="login.html"')
    content = content.replace("window.location.href = '/login'", "window.location.href = 'login.html'")
    content = content.replace("window.location.href = '/dashboard'", "window.location.href = 'dashboard.html'")

    # 2. Add config.js script before the custom script block
    if '<script src="static/js/config.js"></script>' not in content:
        # Some files have <script> block, some have script src
        # Let's insert it before the last script tag or before const API_BASE
        content = content.replace("const API_BASE = 'http://localhost:5000/api';", "")
        content = re.sub(r'(<script>\s*let salesChart)', r'<script src="static/js/config.js"></script>\n    \1', content)
        content = re.sub(r'(<script>\s*// Check)', r'<script src="static/js/config.js"></script>\n    \1', content)
        content = re.sub(r'(<script>\s*function login)', r'<script src="static/js/config.js"></script>\n    \1', content)
        content = re.sub(r'(<script>\s*let editing)', r'<script src="static/js/config.js"></script>\n    \1', content)
        content = re.sub(r'(<script>\s*let current)', r'<script src="static/js/config.js"></script>\n    \1', content)
        content = re.sub(r'(<script>\s*const API_BASE)', r'<script src="static/js/config.js"></script>\n    <script>', content) # if we missed API_BASE

    # 3. Remove local checkAuth and logout functions to let config.js handle them
    # But wait! config.js defines them globally. Let's just remove the duplicate declarations.
    content = re.sub(r'// Check authentication.*?}\n+', '', content, flags=re.DOTALL)
    # the above might be risky if we match too much. Let's do it carefully:
    auth_func = """function checkAuth() {
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = 'login.html';
            }
            const user = JSON.parse(localStorage.getItem('user'));
            if (user) {
                document.getElementById('userName').textContent = user.username;
            }
        }"""
    auth_func_orig = auth_func.replace("'login.html'", "'/login'")
    
    # Let's use simpler regex
    content = re.sub(r'function checkAuth\(\) \{.*?\n        \}\n', '', content, flags=re.DOTALL)
    content = re.sub(r'function logout\(\) \{.*?\n        \}\n', '', content, flags=re.DOTALL)

    # In index.html
    if 'index.html' in file_path:
        content = content.replace("window.location.href = '/login';", "window.location.href = 'login.html';")
        content = content.replace("window.location.href = '/dashboard';", "window.location.href = 'dashboard.html';")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Processed {len(html_files)} files.")

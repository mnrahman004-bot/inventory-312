# Deployment Guide - Inventory Management System

## Deployment Options

- [Option 1: Render Cloud](#option-1-render-cloud-recommended)
- [Option 2: Heroku](#option-2-heroku)
- [Option 3: AWS](#option-3-aws)
- [Option 4: Local VPS](#option-4-local-vps-linux)

---

## Option 1: Render Cloud (RECOMMENDED)

### Easiest & Fastest Cloud Deployment

**Requirements:**
- GitHub account
- Render account (free tier available)

### Step 1: Prepare GitHub Repository

```bash
# Initialize git repository
git init

# Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create .gitignore
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "database/*.db" >> .gitignore

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Inventory Management System"

# Create repository on GitHub and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/inventory-management-system.git
git push -u origin main
```

### Step 2: Create Render Web Service

1. **Sign up at https://render.com**
   - Connect GitHub account
   - Authorize Render access

2. **Create New Web Service**
   - Dashboard → New → Web Service
   - Select your repository
   - Branch: `main`

3. **Configure Build Settings**
   - **Environment**: Python 3.11
   - **Region**: Select closest to you
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python init_db.py
     ```
   - **Start Command**: 
     ```
     cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
     ```

4. **Environment Variables**
   - Click "Environment"
   - Add variables:
     ```
     FLASK_ENV=production
     JWT_SECRET_KEY=<generate-random-key>
     FLASK_DEBUG=False
     ```

5. **Deploy**
   - Click "Deploy"
   - Monitor deployment (takes 2-3 min)
   - Get public URL

### Step 3: Install Production Dependencies

Before deploying, add Gunicorn to requirements.txt:

```bash
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn for production"
git push
```

### Post-Deployment

1. **Create Admin Account** (if not auto-created)
   - SSH into Render
   - Or create via `/api/auth/register` endpoint

2. **Test Application**
   - Visit your Render URL
   - Login with admin credentials
   - Verify all features work

---

## Option 2: Heroku

### Traditional Heroku Deployment

**Requirements:**
- Heroku account
- Heroku CLI installed

### Step 1: Heroku Setup

```bash
# Login to Heroku
heroku login

# Create app
heroku create inventory-management-app

# Add Python buildpack
heroku buildpacks:add heroku/python
```

### Step 2: Add Procfile

Create `Procfile` in project root:

```
web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
release: python init_db.py
```

### Step 3: Add Requirements

Update `requirements.txt`:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

### Step 4: Deploy

```bash
# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=<your-secret-key>

# Deploy
git push heroku main

# Monitor logs
heroku logs --tail
```

### Step 5: Verify

```bash
# Open app
heroku open

# Check database
heroku run python init_db.py --exit-code
```

---

## Option 3: AWS

### Deploy to AWS EC2

**Requirements:**
- AWS account
- EC2 instance (t2.micro eligible for free tier)

### Step 1: Launch EC2 Instance

1. **Create Instance**
   - AMI: Ubuntu 22.04 LTS
   - Type: t2.micro (free tier)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect to Instance**

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Dependencies

```bash
# Install Python and tools
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/inventory-management-system.git
cd inventory-management-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 3: Initialize Database

```bash
# Create database
python init_db.py

# Set permissions
sudo chown ubuntu:ubuntu database/inventory.db
```

### Step 4: Configure Gunicorn

Create `/etc/systemd/system/inventory-app.service`:

```ini
[Unit]
Description=Inventory Management System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/inventory-management-system
ExecStart=/home/ubuntu/inventory-management-system/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 'backend.app:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable inventory-app
sudo systemctl start inventory-app
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/inventory`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/inventory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup HTTPS (Optional)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Option 4: Local VPS (Linux)

### Deploy on Your Own Server

**Requirements:**
- Linux VPS (Ubuntu 22.04 recommended)
- SSH access
- Domain name (optional)

### Quick Setup

```bash
# SSH into server
ssh root@your-server-ip

# Install dependencies
apt update && apt install -y python3 python3-pip python3-venv git

# Clone and setup
git clone https://github.com/YOUR_USERNAME/inventory-management-system.git
cd inventory-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Initialize
python init_db.py

# Start in background
nohup gunicorn -w 4 -b 0.0.0.0:5000 'backend.app:create_app()' &

# Access at http://your-server-ip:5000
```

---

## Production Checklist

Before going live, ensure:

### Security
- [ ] Change JWT_SECRET_KEY to strong random value
- [ ] Set FLASK_DEBUG=False
- [ ] Use HTTPS (SSL certificate)
- [ ] Update default admin password
- [ ] Enable CORS only for trusted origins

### Performance
- [ ] Use Gunicorn with 4+ workers
- [ ] Enable database indexing
- [ ] Configure caching headers
- [ ] Monitor error logs

### Monitoring
- [ ] Setup log aggregation (ELK, Splunk)
- [ ] Configure alerts
- [ ] Monitor CPU/Memory usage
- [ ] Setup automated backups

### Maintenance
- [ ] Regular security updates
- [ ] Database optimization
- [ ] Backup schedule
- [ ] Disaster recovery plan

---

## Environment Variables for Production

```
# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Security
JWT_SECRET_KEY=<generate-with-secrets.token_hex(32)>
SECRET_KEY=<another-random-key>

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/inventory_db

# ML Settings
LEAD_TIME_DAYS=3
SAFETY_STOCK_DAYS=2

# CORS
ALLOWED_ORIGINS=https://yourdomain.com

# Email (optional notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## Database Migration (SQLite → PostgreSQL)

For production, consider PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost:5432/inventory"

# Run migrations
python init_db.py
```

---

## Scaling Considerations

### Phase 1: Single Server (Current)
- Suitable for: Small shops (100-1000 daily transactions)

### Phase 2: Separate Database
- Move SQLite to PostgreSQL on separate server
- Cost: ~$5-10/month

### Phase 3: Load Balancing
- Multiple app servers behind load balancer
- Shared database
- Cost: ~$30-50/month

### Phase 4: Microservices
- Separate services for sales, inventory, predictions
- Message queues for async tasks
- Cost: $100+/month

---

## Troubleshooting Deployment

**Issue: Module not found**
```bash
# Verify requirements
pip install -r requirements.txt
```

**Issue: Database errors**
```bash
# Reinitialize database
python init_db.py
```

**Issue: 502 Bad Gateway (Nginx)**
```bash
# Check Gunicorn logs
sudo journalctl -u inventory-app -n 50

# Restart service
sudo systemctl restart inventory-app
```

**Issue: Cannot write to database**
```bash
# Fix permissions
sudo chown www-data:www-data database/inventory.db
chmod 666 database/inventory.db
```

---

## Monitoring Tools

Recommended for production:

- **Uptime Monitoring**: UptimeRobot (free)
- **Error Tracking**: Sentry (free tier)
- **Performance**: New Relic (free tier)
- **Logs**: ELK Stack or Papertrail
- **Database Backups**: AWS S3 / Google Cloud Storage

---

## Cost Estimates (Monthly)

| Platform | Cost | Best For |
|----------|------|----------|
| Render | $7-20 | Best ease of use |
| Heroku | $7-50 | Traditional apps |
| AWS | $5-15 | Scalability |
| DigitalOcean | $5-20 | Cost-effective |
| Contabo | $4-30 | Budget-friendly |

---

## Rollback Procedure

If deployment fails:

### Render
```bash
# Revert to previous version
# Dashboard → Deploys → Previous version → Activate
```

### Git-based
```bash
# Revert last commit
git revert HEAD --no-edit
git push

# System auto-redeploys
```

---

## Support

For deployment issues:
- Check logs: `heroku logs --tail` or Render dashboard
- Verify environment variables
- Test locally first with production settings
- Review backend/app.py error handlers

---

**Happy Deploying! 🚀**

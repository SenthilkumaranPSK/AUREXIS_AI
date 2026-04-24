# AUREXIS AI - Deployment Guide

**Version**: 1.0.0  
**Last Updated**: April 23, 2026

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [SSL Configuration](#ssl-configuration)
7. [Monitoring](#monitoring)
8. [Backup Strategy](#backup-strategy)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 20 GB SSD
- **OS**: Ubuntu 20.04 LTS or later

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 50 GB SSD
- **OS**: Ubuntu 22.04 LTS

### Software Requirements
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (or SQLite for development)
- Nginx
- Redis (optional, for caching)

---

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/aurexis-ai.git
cd aurexis-ai
```

### 2. Create Environment File
```bash
cp .env.example .env
```

### 3. Configure Environment Variables
Edit `.env`:
```env
# Application
APP_NAME=AUREXIS AI
APP_ENV=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aurexis
# Or for SQLite:
# DATABASE_URL=sqlite:///./aurexis.db

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com

# Ollama (LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-v3.1:671b-cloud

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS (Optional - Twilio)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=+1234567890

# Push Notifications (Optional - Firebase)
FIREBASE_SERVER_KEY=your-firebase-server-key

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0
```

---

## Database Setup

### PostgreSQL (Recommended for Production)

#### 1. Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### 2. Create Database
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE aurexis;
CREATE USER aurexis_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE aurexis TO aurexis_user;
\q
```

#### 3. Initialize Database
```bash
cd backend
python init_db.py
```

### SQLite (Development Only)
```bash
cd backend
python init_db.py
```

---

## Backend Deployment

### 1. Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python migrate.py
```

### 3. Test Backend
```bash
python start.py
```

### 4. Production Server (Gunicorn)

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Create Systemd Service
Create `/etc/systemd/system/aurexis-backend.service`:
```ini
[Unit]
Description=AUREXIS AI Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/aurexis-ai/backend
Environment="PATH=/var/www/aurexis-ai/backend/venv/bin"
ExecStart=/var/www/aurexis-ai/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

#### Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl start aurexis-backend
sudo systemctl enable aurexis-backend
sudo systemctl status aurexis-backend
```

---

## Frontend Deployment

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Build for Production
```bash
npm run build
```

### 3. Serve with Nginx

#### Install Nginx
```bash
sudo apt install nginx
```

#### Configure Nginx
Create `/etc/nginx/sites-available/aurexis`:
```nginx
server {
    listen 80;
    server_name yourapp.com www.yourapp.com;

    # Frontend
    location / {
        root /var/www/aurexis-ai/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

#### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/aurexis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL Configuration

### Using Let's Encrypt (Certbot)

#### 1. Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

#### 2. Obtain Certificate
```bash
sudo certbot --nginx -d yourapp.com -d www.yourapp.com
```

#### 3. Auto-Renewal
```bash
sudo certbot renew --dry-run
```

Certbot will automatically renew certificates before expiry.

---

## Monitoring

### 1. Health Check Endpoint
```bash
curl http://localhost:8000/
```

### 2. System Monitoring

#### Install Monitoring Tools
```bash
sudo apt install htop iotop nethogs
```

#### Monitor Logs
```bash
# Backend logs
sudo journalctl -u aurexis-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Application Monitoring

#### Backend Logs
```bash
tail -f backend/logs/aurexis.log
tail -f backend/logs/errors.log
```

### 4. Database Monitoring
```bash
# PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Check database size
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('aurexis'));"
```

---

## Backup Strategy

### 1. Database Backup

#### PostgreSQL Backup Script
Create `/usr/local/bin/backup-aurexis-db.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/aurexis"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U aurexis_user aurexis > $BACKUP_DIR/aurexis_$DATE.sql

# Compress
gzip $BACKUP_DIR/aurexis_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "aurexis_*.sql.gz" -mtime +7 -delete

echo "Backup completed: aurexis_$DATE.sql.gz"
```

#### Make Executable
```bash
sudo chmod +x /usr/local/bin/backup-aurexis-db.sh
```

#### Schedule with Cron
```bash
sudo crontab -e
```

Add:
```
0 2 * * * /usr/local/bin/backup-aurexis-db.sh
```

### 2. File Backup
```bash
# Backup application files
tar -czf /var/backups/aurexis/aurexis_files_$(date +%Y%m%d).tar.gz /var/www/aurexis-ai
```

### 3. Restore from Backup
```bash
# Restore database
gunzip < /var/backups/aurexis/aurexis_20260423.sql.gz | psql -U aurexis_user aurexis
```

---

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u aurexis-backend -n 50

# Check if port is in use
sudo lsof -i :8000

# Test manually
cd /var/www/aurexis-ai/backend
source venv/bin/activate
python start.py
```

### Database Connection Issues
```bash
# Test connection
psql -U aurexis_user -d aurexis -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

### WebSocket Connection Issues
```bash
# Check if WebSocket endpoint is accessible
wscat -c ws://localhost:8000/ws?token=<jwt_token>

# Check Nginx WebSocket configuration
sudo nginx -T | grep -A 10 "location /ws"
```

### High Memory Usage
```bash
# Check memory usage
free -h

# Check process memory
ps aux --sort=-%mem | head -10

# Restart backend
sudo systemctl restart aurexis-backend
```

---

## Performance Optimization

### 1. Enable Gzip Compression
Add to Nginx configuration:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### 2. Enable Caching
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (UFW)
- [ ] Configure SSL/TLS
- [ ] Set up fail2ban
- [ ] Enable CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor logs
- [ ] Rate limiting enabled

---

## Support

For deployment support:
- Email: devops@aurexis.ai
- Documentation: https://docs.aurexis.ai/deployment
- Status: https://status.aurexis.ai

---

**Last Updated**: April 23, 2026  
**Version**: 1.0.0

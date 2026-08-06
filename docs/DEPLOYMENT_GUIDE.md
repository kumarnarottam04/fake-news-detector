# Step-by-Step Server Deployment Guide

This guide provides exact step-by-step instructions for deploying the **Fake News Detection System** to a live production server.

---

## OPTION 1: Deploy to Render Cloud (Easiest & Free - Recommended)

Render provides zero-cost cloud hosting with automatic SSL (HTTPS) and auto-deploy on git push.

### Step 1: Push Code to GitHub
Ensure all code and configuration files (`render.yaml`, `gunicorn.conf.py`, `Procfile`, `requirements.txt`, `app.py`) are pushed to your GitHub repository:
```bash
git add .
git commit -m "feat: prepare production deployment"
git push origin main
```

### Step 2: Sign Up / Log In to Render
1. Go to [render.com](https://render.com/).
2. Create a free account or sign in with GitHub.

### Step 3: Connect Repository
1. In your Render Dashboard, click **New +** $\rightarrow$ select **Web Service**.
2. Connect your GitHub account and select your repository (`fake-news-detection`).

### Step 4: Configure Web Service
Render will automatically detect your `render.yaml` blueprint. If configuring manually:

- **Name:** `fake-news-detector`
- **Region:** Choose nearest region (e.g., Oregon or Frankfurt)
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
  ```
- **Start Command:**
  ```bash
  gunicorn -c gunicorn.conf.py app:app
  ```
- **Instance Type:** Select **Free** (512 MB RAM)

### Step 5: Add Environment Variables
Under the **Environment** tab, add the following variables:

| Key | Value |
| :--- | :--- |
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.12.0` |
| `LOG_LEVEL` | `INFO` |
| `SECRET_KEY` | `generate-a-secure-random-string-here` |

### Step 6: Deploy & Verify
1. Click **Create Web Service**.
2. Render will build the environment, download NLTK data, and start Gunicorn.
3. Once the build finishes, your live URL will be active (e.g. `https://fake-news-detector.onrender.com`).
4. Test the health endpoint: `https://fake-news-detector.onrender.com/health` (should return `{"status": "healthy"}`).

---

## OPTION 2: Deploy to Ubuntu VPS (AWS EC2 / DigitalOcean / Linode)

For self-managed deployment on an Ubuntu 22.04 LTS server using Nginx and Gunicorn.

### Step 1: Connect to your VPS
```bash
ssh root@YOUR_SERVER_IP
```

### Step 2: Update Server & Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git curl -y
```

### Step 3: Clone Repository & Set Up Virtual Environment
```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/fake-news-detection.git
cd fake-news-detection

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK datasets
python3 -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 4: Train Initial Model (If artifacts not tracked)
```bash
python3 -m src.training.train
```

### Step 5: Test Gunicorn WSGI Server
```bash
gunicorn -c gunicorn.conf.py app:app
```
*(Press `Ctrl+C` once verified)*

### Step 6: Create Systemd Service for Gunicorn
Create `/etc/systemd/system/fakenews.service`:
```bash
sudo nano /etc/systemd/system/fakenews.service
```

Paste the following configuration:
```ini
[Unit]
Description=Gunicorn instance for Fake News Detection App
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/fake-news-detection
Environment="PATH=/var/www/fake-news-detection/venv/bin"
Environment="FLASK_ENV=production"
Environment="PORT=5000"
ExecStart=/var/www/fake-news-detection/venv/bin/gunicorn -c gunicorn.conf.py app:app

[Install]
WantedBy=multi-user.target
```

Start and enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl start fakenews
sudo systemctl enable fakenews
sudo systemctl status fakenews
```

### Step 7: Configure Nginx Reverse Proxy
Edit Nginx site configuration `/etc/nginx/sites-available/fakenews`:
```bash
sudo nano /etc/nginx/sites-available/fakenews
```

Paste the following:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_SERVER_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site & restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/fakenews /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Enable SSL (HTTPS) with Certbot (Optional)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d YOUR_DOMAIN
```

---

## OPTION 3: Deploy with Docker

### Step 1: Build Docker Image
```bash
docker build -t fake-news-detector:1.0 .
```

### Step 2: Run Container
```bash
docker run -d \
  --name fake_news_app \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PORT=5000 \
  fake-news-detector:1.0
```

### Step 3: Verify Container Uptime
```bash
curl http://localhost:5000/health
```

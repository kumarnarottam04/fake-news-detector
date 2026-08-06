"""
Production Gunicorn WSGI Server Configuration
"""
import os

# Server Socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Concurrency & Worker Model
workers = int(os.getenv('WEB_CONCURRENCY', '2'))
threads = 2
worker_class = 'gthread'

# Timeouts
timeout = 60
keepalive = 5

# Process Naming
proc_name = 'fake_news_detector_gunicorn'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()

# Server Mechanics
preload_app = True

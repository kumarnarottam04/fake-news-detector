"""
Flask Application Factory Entry Point
"""
import json
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import get_config
from src.prediction.predict import predict_article
from src.prediction.model_loader import ModelLoader
from src.training.train import train_pipeline
from src.utils.logger import logger

START_TIME = time.time()

def create_app(config_object=None):
    """Application Factory Pattern for initializing Flask WSGI server."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    if config_object is None:
        config_object = get_config()
        
    app.config.from_object(config_object)

    # 1. CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 2. Rate Limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    # 3. Security Response Headers Middleware
    @app.after_request
    def apply_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    # 4. Initialize Model Singleton
    with app.app_context():
        loader = ModelLoader()
        if not loader.is_loaded:
            if not config_object.MODEL_PATH.exists() or not config_object.VECTORIZER_PATH.exists():
                logger.info("Model artifacts missing. Bootstrapping training pipeline...")
                try:
                    train_pipeline()
                except Exception as e:
                    logger.error(f"Error bootstrapping training pipeline: {e}")
            loader.load_artifacts()

    # ==================== REST ROUTES ====================

    @app.route('/')
    def home():
        """Renders single-page presentation interface."""
        return render_template('index.html')

    @app.route('/health', methods=['GET'])
    def health_check():
        """System Uptime, Memory Footprint & Health Check REST endpoint."""
        loader = ModelLoader()
        uptime = round(time.time() - START_TIME, 2)
        return jsonify({
            "status": "healthy",
            "model_loaded": loader.is_loaded,
            "vectorizer_loaded": loader.is_loaded,
            "uptime_seconds": uptime,
            "version": "1.0.0"
        }), 200

    @app.route('/api/samples', methods=['GET'])
    def get_sample_articles():
        """Returns sample news articles for demonstration."""
        sample_file = config_object.SAMPLES_DIR / 'sample_articles.json'
        if sample_file.exists():
            with open(sample_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({"success": True, "samples": data}), 200
        else:
            return jsonify({"success": False, "error": "Sample file missing"}), 404

    @app.route('/api/predict', methods=['POST'])
    @limiter.limit("30 per minute")
    def predict():
        """Real-time article authenticity prediction REST endpoint."""
        try:
            data = request.get_json(silent=True)
            if not data or 'text' not in data:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "MISSING_PAYLOAD",
                        "message": "JSON body must contain a non-empty 'text' string parameter."
                    }
                }), 400

            raw_text = data['text']
            result = predict_article(raw_text)
            return jsonify(result), 200

        except ValueError as ve:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": str(ve)
                }
            }), 400

        except RuntimeError as re:
            return jsonify({
                "success": False,
                "error": {
                    "code": "MODEL_UNAVAILABLE",
                    "message": str(re)
                }
            }), 503

        except Exception as e:
            logger.error(f"Unhandled prediction error: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "An unexpected error occurred while processing the request."
                }
            }), 500

    # ==================== ERROR HANDLERS ====================

    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({"success": False, "error": {"code": "BAD_REQUEST", "message": "Bad request format."}}), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "Resource not found."}}), 404

    @app.errorhandler(429)
    def rate_limit_error(e):
        return jsonify({"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Rate limit exceeded. Try again in 60s."}}), 429

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"success": False, "error": {"code": "INTERNAL_SERVER_ERROR", "message": "Internal server error."}}), 500

    return app

# WSGI Application Instance for Gunicorn / Development Server
app = create_app()

if __name__ == '__main__':
    config_obj = get_config()
    port = int(config_obj.PORT) if hasattr(config_obj, 'PORT') else 5000
    logger.info(f"Starting Fake News Detector Flask App on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=config_obj.DEBUG)

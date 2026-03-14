from flask import Flask
import os
import logging
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    from config_new import Config
    app.config.from_object(Config)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    from models.user import db
    db.init_app(app)
    
    # Load ML models
    load_ml_models(app)
    
    # Register blueprints
    from routes import register_all_routes
    register_all_routes(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

def load_ml_models(app):
    """Load ML models with error handling"""
    try:
        app.model = joblib.load("model.pkl")
        logger.info("Crop recommendation model loaded")
    except Exception as e:
        logger.error(f"Failed to load crop model: {e}")
        app.model = None
    
    try:
        app.yield_model = joblib.load("yield_model.pkl")
        logger.info("Yield prediction model loaded")
    except Exception as e:
        logger.error(f"Failed to load yield model: {e}")
        app.yield_model = None
    
    try:
        app.disease_model = joblib.load("disease_model.pkl")
        logger.info("Disease detection model loaded")
    except Exception as e:
        logger.warning(f"Disease model not found: {e}")
        app.disease_model = None

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

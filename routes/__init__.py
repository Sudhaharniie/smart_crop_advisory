from .auth_routes import auth_bp
from .dashboard_routes import dashboard_bp
from .api_routes import api_bp
from .waste_routes import waste_bp

def register_all_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(waste_bp, url_prefix='/api/waste')

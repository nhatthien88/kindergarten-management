
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.extensions import db, migrate, jwt
from flask_session import Session 


def create_app(config_name='development'):

    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    Session(app) 

    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    

    with app.app_context():
        from app import models
    

    from app.blueprints.auth import auth_bp
    from app.blueprints.parent import parent_bp
    from app.blueprints.teacher import teacher_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(parent_bp, url_prefix='/api/parent')
    app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')


    
    
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login_page'))
    

    @app.route('/api')
    def api_health():
        return {
            'message': 'Kindergarten Management API',
            'status': 'running',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'parent': '/api/parent',
                'teacher': '/api/teacher',
                'admin': '/api/admin'
            }
        }
    
    return app
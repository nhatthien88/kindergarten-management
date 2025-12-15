
from flask import Flask
from app.config import config
from app.extensions import db, migrate

def create_app(config_name='development'):
   
    app = Flask(__name__)
    
    """doc het config"""
    app.config.from_object(config[config_name])

    
   
    db.init_app(app)
    migrate.init_app(app, db)
    """flask db migrate, flask db upgrade"""

    with app.app_context():
        from app import models
    
 
    from app.blueprints.parent import parent_bp
    from app.blueprints.teacher import teacher_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(parent_bp, url_prefix='/api/parent')
    app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
   
    @app.route('/')
    def index():
        return {'message': 'Kindergarten Management API', 'status': 'running'}
    
    return app
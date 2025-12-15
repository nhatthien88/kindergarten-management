from flask import jsonify
from app.blueprints.admin import admin_bp

@admin_bp.route('/dashboard')

def dashboard():
        return jsonify({
        'message': 'Admin Dashboard',
        'user':  'Admin'
    })
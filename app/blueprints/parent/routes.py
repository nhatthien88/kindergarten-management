
from flask import jsonify
from app.blueprints.parent import parent_bp

@parent_bp.route('/dashboard')

def dashboard():
        return jsonify({
        'message': 'Parent Dashboard',
        'user':  'Parent'
    })

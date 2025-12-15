from flask import jsonify
from app.blueprints.teacher import teacher_bp


@teacher_bp.route('/dashboard')

def dashboard():
        return jsonify({
        'message': 'teacher Dashboard',
        'user':  'teacher'
    })


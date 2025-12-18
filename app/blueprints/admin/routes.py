# app/blueprints/admin/routes.py
from flask import render_template, redirect, url_for, flash, session
from . import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.models import User, UserRole
from app.extensions import db


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Trang dashboard chính của admin"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        

        stats = {
            'total_users': User.query.filter_by(is_active=True).count(),
            'total_students': 0,
            'total_teachers': User.query.filter_by(role=UserRole. TEACHER, is_active=True).count(),
            'total_parents': User.query.filter_by(role=UserRole.PARENT, is_active=True).count(),
        }
        

        return render_template('admin/dashboard.html', user=user, stats=stats)
        
    except Exception as e: 
        flash(f'Lỗi tải dashboard: {str(e)}', 'error')
        return redirect(url_for('auth.login_page'))
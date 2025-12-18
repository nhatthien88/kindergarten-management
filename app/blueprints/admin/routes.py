# app/blueprints/admin/routes.py
from flask import render_template, redirect, url_for, flash, session
from . import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import report_service, fee_service
from app.models import User
from app.extensions import db


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Trang dashboard chính của admin"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get stats from report service
        stats = report_service.get_dashboard_stats()
        
        # Get recent overdue fees
        recent_fees = fee_service.get_overdue_fees()[:5]
        
        return render_template('admin/dashboard.html', 
                             user=user, 
                             stats=stats,
                             recent_fees=recent_fees)
        
    except Exception as e: 
        flash(f'Lỗi tải dashboard: {str(e)}', 'error')
        return redirect(url_for('auth.login_page'))
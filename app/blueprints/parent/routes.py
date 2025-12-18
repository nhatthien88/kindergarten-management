# app/blueprints/parent/routes.py
from flask import render_template, redirect, url_for, flash, session
from . import parent_bp
from app.models import User
from app.extensions import db


@parent_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    
    if not user_id: 
        flash('Vui lòng đăng nhập', 'warning')
        return redirect(url_for('auth.login_page'))
    
    user = db.session.get(User, user_id)
    
    if not user:
        session. clear()
        flash('Tài khoản không tồn tại', 'error')
        return redirect(url_for('auth.login_page'))
    
    stats = {
        'total_children': 0,
        'unpaid_fees': 0,
        'notifications': 0,
    }
    
    return render_template('parent/dashboard.html', user=user, stats=stats)
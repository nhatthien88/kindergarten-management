# app/blueprints/teacher/routes.py
from flask import render_template, redirect, url_for, flash, session
from app.blueprints.teacher import teacher_bp
from app.models import User
from app.extensions import db


@teacher_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    
    if not user_id:  
        flash('Vui lòng đăng nhập', 'warning')
        return redirect(url_for('auth.login_page'))
    
    user = db.session.get(User, user_id)
    
    if not user:
        session.clear()
        flash('Tài khoản không tồn tại', 'error')
        return redirect(url_for('auth.login_page'))
    
    stats = {
        'total_students': 0,
        'total_classes': 0,
        'pending_tasks': 0,
    }
    
    return render_template('teacher/dashboard.html', user=user, stats=stats)
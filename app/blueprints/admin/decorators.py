# app/blueprints/admin/decorators.py
"""Admin-specific decorators"""
from functools import wraps
from flask import redirect, url_for, flash, session
from app.models import User, UserRole
from app.extensions import db

def admin_required(fn):
    """Decorator yêu cầu quyền admin - dùng session"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        
        if not user_id: 
            flash('Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('auth.login_page'))
        
        user = db. session.get(User, user_id)
        
        if not user:
            session.clear()
            flash('Tài khoản không tồn tại', 'error')
            return redirect(url_for('auth. login_page'))
        
        if not user.is_active:
            session.clear()
            flash('Tài khoản đã bị vô hiệu hóa', 'error')
            return redirect(url_for('auth.login_page'))

        if user.role != UserRole.ADMIN:
            flash('Bạn không có quyền truy cập trang này', 'error')
            return redirect(url_for('auth.login_page'))
        
        return fn(*args, **kwargs)
    
    return wrapper
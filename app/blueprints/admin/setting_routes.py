# app/blueprints/admin/setting_routes.py
from flask import render_template, request, flash, redirect, url_for, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import setting_service
from app.models import User
from app.extensions import db


@admin_bp.route('/settings')
@admin_required
def settings_page():
    """Settings page"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Initialize settings if not exist
        setting_service.initialize_default_settings()
        
        # Get all settings
        settings = setting_service.get_all_settings()
        
        return render_template('admin/settings/index.html', user=user, settings=settings)
    except Exception as e:
        flash(f'Lỗi tải cài đặt: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/settings/update', methods=['POST'])
@admin_required
def update_settings():
    """Update settings"""
    try:
        user_id = session.get('user_id')
        
        # Get form data
        settings_to_update = [
            'tuition_fee_monthly',
            'meal_price_daily',
            'default_classroom_capacity',
            'school_name',
            'school_address',
            'school_phone',
            'school_email'
        ]
        
        # Update each setting
        for key in settings_to_update:
            value = request.form.get(key)
            if value is not None:
                success, message = setting_service.update_setting(key, value, user_id)
                if not success:
                    flash(message, 'error')
                    return redirect(url_for('admin.settings_page'))
        
        flash('Cập nhật cài đặt thành công!', 'success')
        return redirect(url_for('admin.settings_page'))
        
    except Exception as e:
        flash(f'Lỗi cập nhật cài đặt: {str(e)}', 'error')
        return redirect(url_for('admin.settings_page'))

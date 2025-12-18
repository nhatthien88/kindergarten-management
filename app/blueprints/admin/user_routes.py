# app/blueprints/admin/user_routes.py
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import user_service
from app.models import User
from app.extensions import db


@admin_bp.route('/users')
@admin_required
def list_users():
    """List all users with filters"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get filters
        role = request.args.get('role')
        status = request.args.get('status')
        
        # Get users
        users = user_service.get_all_users(role=role, status=status)
        
        # Get pending teachers count
        pending_teachers = user_service.get_pending_teachers()
        
        return render_template('admin/users/list.html', 
                             user=user, 
                             users=users,
                             pending_count=len(pending_teachers),
                             current_role=role,
                             current_status=status)
    except Exception as e:
        flash(f'Lỗi tải danh sách người dùng: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """User detail page"""
    try:
        current_user_id = session.get('user_id')
        current_user = db.session.get(User, current_user_id)
        
        # Get user detail
        detail = user_service.get_user_detail(user_id)
        if not detail:
            flash('Người dùng không tồn tại', 'error')
            return redirect(url_for('admin.list_users'))
        
        return render_template('admin/users/detail.html', 
                             user=current_user,
                             target_user=detail['user'],
                             profile=detail['profile'],
                             stats=detail['stats'])
    except Exception as e:
        flash(f'Lỗi tải thông tin người dùng: {str(e)}', 'error')
        return redirect(url_for('admin.list_users'))


@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    """Approve teacher account"""
    try:
        success, message = user_service.approve_teacher(user_id)
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'message': message}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id):
    """Toggle user active status"""
    try:
        success, message = user_service.toggle_user_status(user_id)
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'message': message}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

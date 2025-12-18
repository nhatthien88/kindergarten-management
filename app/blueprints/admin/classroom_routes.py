# app/blueprints/admin/classroom_routes.py
from flask import render_template, request, flash, redirect, url_for, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import classroom_service
from app.models import User
from app.extensions import db


@admin_bp.route('/classrooms')
@admin_required
def list_classrooms():
    """List all classrooms"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get filter
        school_year = request.args.get('school_year')
        
        # Get classrooms
        classrooms = classroom_service.get_classrooms(school_year=school_year)
        school_years = classroom_service.get_school_years()
        
        return render_template('admin/classrooms/list.html',
                             user=user,
                             classrooms=classrooms,
                             school_years=school_years,
                             current_year=school_year)
    except Exception as e:
        flash(f'Lỗi tải danh sách lớp học: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/classrooms/add')
@admin_required
def add_classroom_form():
    """Add classroom form"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get available teachers
        teachers = classroom_service.get_available_teachers()
        
        return render_template('admin/classrooms/form.html',
                             user=user,
                             classroom=None,
                             teachers=teachers)
    except Exception as e:
        flash(f'Lỗi tải form: {str(e)}', 'error')
        return redirect(url_for('admin.list_classrooms'))


@admin_bp.route('/classrooms', methods=['POST'])
@admin_required
def create_classroom():
    """Create new classroom"""
    try:
        data = {
            'name': request.form.get('name'),
            'school_year': request.form.get('school_year'),
            'capacity': int(request.form.get('capacity', 25)),
            'room_number': request.form.get('room_number'),
            'teacher_id': int(request.form.get('teacher_id')) if request.form.get('teacher_id') else None
        }
        
        success, message = classroom_service.create_classroom(data)
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.list_classrooms'))
        else:
            flash(message, 'error')
            return redirect(url_for('admin.add_classroom_form'))
    except Exception as e:
        flash(f'Lỗi tạo lớp học: {str(e)}', 'error')
        return redirect(url_for('admin.add_classroom_form'))


@admin_bp.route('/classrooms/<int:classroom_id>')
@admin_required
def classroom_detail(classroom_id):
    """Classroom detail with students"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        detail = classroom_service.get_classroom_detail(classroom_id)
        if not detail:
            flash('Lớp học không tồn tại', 'error')
            return redirect(url_for('admin.list_classrooms'))
        
        return render_template('admin/classrooms/detail.html',
                             user=user,
                             classroom=detail['classroom'],
                             students=detail['students'],
                             teacher=detail['teacher'])
    except Exception as e:
        flash(f'Lỗi tải thông tin lớp học: {str(e)}', 'error')
        return redirect(url_for('admin.list_classrooms'))


@admin_bp.route('/classrooms/<int:classroom_id>/edit')
@admin_required
def edit_classroom_form(classroom_id):
    """Edit classroom form"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        detail = classroom_service.get_classroom_detail(classroom_id)
        if not detail:
            flash('Lớp học không tồn tại', 'error')
            return redirect(url_for('admin.list_classrooms'))
        
        teachers = classroom_service.get_available_teachers()
        
        return render_template('admin/classrooms/form.html',
                             user=user,
                             classroom=detail['classroom'],
                             teachers=teachers)
    except Exception as e:
        flash(f'Lỗi tải form: {str(e)}', 'error')
        return redirect(url_for('admin.list_classrooms'))


@admin_bp.route('/classrooms/<int:classroom_id>/update', methods=['POST'])
@admin_required
def update_classroom(classroom_id):
    """Update classroom"""
    try:
        data = {
            'name': request.form.get('name'),
            'school_year': request.form.get('school_year'),
            'capacity': int(request.form.get('capacity', 25)),
            'room_number': request.form.get('room_number'),
            'teacher_id': int(request.form.get('teacher_id')) if request.form.get('teacher_id') else None
        }
        
        success, message = classroom_service.update_classroom(classroom_id, data)
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.classroom_detail', classroom_id=classroom_id))
        else:
            flash(message, 'error')
            return redirect(url_for('admin.edit_classroom_form', classroom_id=classroom_id))
    except Exception as e:
        flash(f'Lỗi cập nhật lớp học: {str(e)}', 'error')
        return redirect(url_for('admin.edit_classroom_form', classroom_id=classroom_id))


@admin_bp.route('/classrooms/<int:classroom_id>/assign-teacher', methods=['POST'])
@admin_required
def assign_teacher(classroom_id):
    """Assign teacher to classroom"""
    try:
        teacher_id = int(request.form.get('teacher_id')) if request.form.get('teacher_id') else None
        
        success, message = classroom_service.assign_teacher(classroom_id, teacher_id)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('admin.classroom_detail', classroom_id=classroom_id))
    except Exception as e:
        flash(f'Lỗi phân công giáo viên: {str(e)}', 'error')
        return redirect(url_for('admin.classroom_detail', classroom_id=classroom_id))


@admin_bp.route('/classrooms/<int:classroom_id>/delete', methods=['POST'])
@admin_required
def delete_classroom(classroom_id):
    """Delete classroom"""
    try:
        success, message = classroom_service.delete_classroom(classroom_id)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('admin.list_classrooms'))
    except Exception as e:
        flash(f'Lỗi xóa lớp học: {str(e)}', 'error')
        return redirect(url_for('admin.list_classrooms'))

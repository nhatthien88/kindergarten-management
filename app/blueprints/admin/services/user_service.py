# app/blueprints/admin/services/user_service.py
"""Service for user management"""
from app.extensions import db
from app.models import User, Teacher, Parent, UserRole
from sqlalchemy import or_


def get_all_users(role=None, status=None):
    """Get users with optional filters"""
    query = User.query
    
    if role:
        query = query.filter_by(role=UserRole(role))
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    return query.order_by(User.created_at.desc()).all()


def get_pending_teachers():
    """Get teachers waiting for approval (is_active=False)"""
    return User.query.filter_by(
        role=UserRole.TEACHER,
        is_active=False
    ).order_by(User.created_at.desc()).all()


def get_unlinked_parents():
    """Get parents without students"""
    parents_with_students = db.session.query(Parent.id).join(
        Parent.students
    ).distinct()
    
    return User.query.join(User.parent_profile).filter(
        User.role == UserRole.PARENT,
        ~Parent.id.in_(parents_with_students)
    ).all()


def approve_teacher(user_id):
    """Approve teacher account (set is_active=True)"""
    try:
        user = db.session.get(User, user_id)
        if not user:
            return False, "Người dùng không tồn tại"
        
        if user.role != UserRole.TEACHER:
            return False, "Chỉ có thể duyệt giáo viên"
        
        if user.is_active:
            return False, "Giáo viên đã được duyệt"
        
        user.is_active = True
        db.session.commit()
        return True, "Duyệt giáo viên thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi duyệt giáo viên: {str(e)}"


def toggle_user_status(user_id):
    """Toggle user active status"""
    try:
        user = db.session.get(User, user_id)
        if not user:
            return False, "Người dùng không tồn tại"
        
        if user.role == UserRole.ADMIN:
            return False, "Không thể thay đổi trạng thái admin"
        
        user.is_active = not user.is_active
        status_text = "kích hoạt" if user.is_active else "vô hiệu hóa"
        db.session.commit()
        return True, f"Đã {status_text} tài khoản thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi thay đổi trạng thái: {str(e)}"


def get_user_detail(user_id):
    """Get detailed user information"""
    user = db.session.get(User, user_id)
    if not user:
        return None
    
    result = {
        'user': user,
        'profile': None,
        'stats': {}
    }
    
    if user.role == UserRole.TEACHER and user.teacher_profile:
        result['profile'] = user.teacher_profile
        result['stats']['classrooms'] = user.teacher_profile.classrooms.count()
    elif user.role == UserRole.PARENT and user.parent_profile:
        result['profile'] = user.parent_profile
        result['stats']['students'] = user.parent_profile.students.count()
    
    return result

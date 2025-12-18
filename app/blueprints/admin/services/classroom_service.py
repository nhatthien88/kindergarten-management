# app/blueprints/admin/services/classroom_service.py
"""Service for classroom management"""
from app.extensions import db
from app.models import Classroom, Teacher, User, UserRole


def get_classrooms(school_year=None):
    """Get classrooms optionally filtered by school year"""
    query = Classroom.query
    if school_year:
        query = query.filter_by(school_year=school_year)
    return query.order_by(Classroom.name).all()


def get_classroom_detail(classroom_id):
    """Get classroom with students"""
    classroom = db.session.get(Classroom, classroom_id)
    if not classroom:
        return None
    
    return {
        'classroom': classroom,
        'students': classroom.students.filter_by(is_active=True).all(),
        'teacher': classroom.teacher
    }


def create_classroom(data):
    """Create new classroom with validation"""
    try:
        # Validate required fields
        if not data.get('name') or not data.get('school_year'):
            return False, "Tên lớp và năm học là bắt buộc"
        
        # Check duplicate
        existing = Classroom.query.filter_by(
            name=data['name'],
            school_year=data['school_year']
        ).first()
        if existing:
            return False, f"Lớp {data['name']} năm học {data['school_year']} đã tồn tại"
        
        # Create classroom
        classroom = Classroom(
            name=data['name'],
            school_year=data['school_year'],
            capacity=data.get('capacity', 25),
            room_number=data.get('room_number'),
            teacher_id=data.get('teacher_id')
        )
        
        db.session.add(classroom)
        db.session.commit()
        return True, "Tạo lớp học thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi tạo lớp học: {str(e)}"


def update_classroom(classroom_id, data):
    """Update classroom information"""
    try:
        classroom = db.session.get(Classroom, classroom_id)
        if not classroom:
            return False, "Lớp học không tồn tại"
        
        # Update fields
        if 'name' in data:
            classroom.name = data['name']
        if 'school_year' in data:
            classroom.school_year = data['school_year']
        if 'capacity' in data:
            classroom.capacity = data['capacity']
        if 'room_number' in data:
            classroom.room_number = data['room_number']
        if 'teacher_id' in data:
            classroom.teacher_id = data['teacher_id'] if data['teacher_id'] else None
        
        db.session.commit()
        return True, "Cập nhật lớp học thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi cập nhật lớp học: {str(e)}"


def assign_teacher(classroom_id, teacher_id):
    """Assign homeroom teacher to classroom"""
    try:
        classroom = db.session.get(Classroom, classroom_id)
        if not classroom:
            return False, "Lớp học không tồn tại"
        
        if teacher_id:
            teacher = db.session.get(Teacher, teacher_id)
            if not teacher:
                return False, "Giáo viên không tồn tại"
            classroom.teacher_id = teacher_id
        else:
            classroom.teacher_id = None
        
        db.session.commit()
        return True, "Phân công giáo viên thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi phân công giáo viên: {str(e)}"


def get_available_teachers():
    """Get teachers without assigned classroom or all active teachers"""
    # Get all active teachers
    teachers = Teacher.query.join(Teacher.user).filter(
        User.is_active == True,
        User.role == UserRole.TEACHER
    ).all()
    return teachers


def check_classroom_capacity(classroom_id):
    """Check if classroom is at or over capacity"""
    classroom = db.session.get(Classroom, classroom_id)
    if not classroom:
        return None
    
    current_count = classroom.current_student_count
    return {
        'current': current_count,
        'capacity': classroom.capacity,
        'is_full': classroom.is_full,
        'available': classroom.capacity - current_count
    }


def delete_classroom(classroom_id):
    """Delete classroom if no students"""
    try:
        classroom = db.session.get(Classroom, classroom_id)
        if not classroom:
            return False, "Lớp học không tồn tại"
        
        if classroom.current_student_count > 0:
            return False, "Không thể xóa lớp học có học sinh"
        
        db.session.delete(classroom)
        db.session.commit()
        return True, "Xóa lớp học thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi xóa lớp học: {str(e)}"


def get_school_years():
    """Get list of distinct school years"""
    years = db.session.query(Classroom.school_year).distinct().order_by(Classroom.school_year.desc()).all()
    return [y[0] for y in years]

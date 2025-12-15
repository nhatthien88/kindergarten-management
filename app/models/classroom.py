
from app.models.base import BaseModel, TimestampMixin
from app.extensions import db


class Classroom(BaseModel, TimestampMixin):
 
    __tablename__ = 'classrooms'
    
    # thong tin classroom
    name = db.Column(
        db.String(50), 
        nullable=False,
        comment='Tên lớp (Lớp Chồi, Lớp Lá... )'
    )
    school_year = db.Column(
        db.String(20), 
        nullable=False,
        index=True,
        comment='Năm học (2024-2025)'
    )
    capacity = db.Column(
        db.Integer, 
        default=25,
        comment='Sức chứa tối đa (YC5:  có thể thay đổi)'
    )
    room_number = db.Column(
        db.String(20),
        comment='Số phòng'
    )
    
    # Foreign Key
    teacher_id = db.Column(
        db.Integer, 
        db.ForeignKey('teachers.id', ondelete='SET NULL'),
        comment='Giáo viên chủ nhiệm'
    )
    
    # Relationships
    teacher = db.relationship(
        'Teacher', 
        back_populates='classrooms'
    )
    students = db.relationship(
        'Student', 
        back_populates='classroom',
        lazy='dynamic'
    )
    
    @property
    def current_student_count(self):
        """Sốo hoc sinh hien tai trong lop"""
        return self.students.filter_by(is_active=True).count()
    
    @property
    def is_full(self):
        """Lớop full chua"""
        return self.current_student_count >= self.capacity
    
    def __repr__(self):
        return f'<Classroom {self.name} - {self.school_year}>'
from app.models.base import BaseModel, TimestampMixin
from app.extensions import db


class Teacher(BaseModel, TimestampMixin):

    __tablename__ = 'teachers'
    
    # foreign key
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False,
        unique=True,
        comment='Liên kết với User (1-1)'
    )
    
    # thong tin teacher
    employee_id = db.Column(
        db.String(20), 
        unique=True,
        comment='Mã nhân viên'
    )
    qualification = db.Column(
        db.String(200),
        comment='Trình độ chuyên môn'
    )
    specialization = db.Column(
        db.String(100),
        comment='Chuyên môn (Mầm non, Nhà trẻ... )'
    )
    
    # Relationships
    user = db.relationship(
        'User', 
        back_populates='teacher_profile'
    )
    classrooms = db.relationship(
        'Classroom', 
        back_populates='teacher',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Teacher {self.employee_id}>'
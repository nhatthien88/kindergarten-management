"""
Student model - Học sinh
"""
from app.models.base import BaseModel, TimestampMixin
from app.extensions import db
from datetime import date


class Student(BaseModel, TimestampMixin):
 
    __tablename__ = 'students'
    
    # thong tin student
    full_name = db.Column(
        db.String(100), 
        nullable=False,
        comment='Họ tên trẻ (YC1)'
    )
    date_of_birth = db.Column(
        db.Date, 
        nullable=False,
        index=True,
        comment='Ngày sinh (YC1)'
    )
    gender = db.Column(
        db. Enum('Nam', 'Nữ', name='gender_enum'), 
        nullable=False,
        index=True,
        comment='Giới tính (YC1, YC4:  để thống kê)'
    )
    avatar_url = db.Column(
        db.String(255),
        comment='Ảnh đại diện'
    )
    birth_certificate_number = db.Column(
        db.String(50),
        comment='Số giấy khai sinh'
    )
    
    # Foreign Keys
    parent_id = db.Column(
        db.Integer, 
        db.ForeignKey('parents.id', ondelete='RESTRICT'), 
        nullable=False,
        index=True,
        comment='Phụ huynh (YC1)'
    )
    classroom_id = db.Column(
        db.Integer, 
        db.ForeignKey('classrooms.id', ondelete='SET NULL'),
        index=True,
        comment='Lớp học hiện tại'
    )
    
    # Status
    is_active = db.Column(
        db.Boolean, 
        default=True,
        comment='Còn học không (nghỉ học = False)'
    )
    enrollment_date = db.Column(
        db.Date,
        default=date.today,
        comment='Ngày nhập học'
    )
    
    # Relationships
    parent = db.relationship(
        'Parent', 
        back_populates='students'
    )
    classroom = db.relationship(
        'Classroom', 
        back_populates='students'
    )
    health_records = db.relationship(
        'HealthRecord', 
        back_populates='student',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    fees = db.relationship(
        'Fee', 
        back_populates='student',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    meal_charges = db.relationship(
        'MealCharge', 
        back_populates='student',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    @property
    def age(self):
        """Tinh tuoi"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def __repr__(self):
        return f'<Student {self. full_name}>'
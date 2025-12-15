from app.models.base import BaseModel, TimestampMixin
from app.extensions import db
from datetime import date


class HealthRecord(BaseModel, TimestampMixin):
    
    __tablename__ = 'health_records'
    
    # Foreign Key
    student_id = db.Column(
        db.Integer, 
        db.ForeignKey('students.id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment='Học sinh'
    )
    
    # Health Data
    record_date = db.Column(
        db.Date, 
        nullable=False, 
        default=date.today,
        index=True,
        comment='Ngày ghi nhận (YC2)'
    )
    weight = db.Column(
        db.Numeric(5, 2),
        comment='Cân nặng (kg) - YC2'
    )
    temperature = db.Column(
        db.Numeric(4, 2),
        comment='Nhiệt độ (°C) - YC2'
    )
    note = db.Column(
        db.Text,
        comment='Ghi chú - YC2 (Bình thường, Ốm... )'
    )
    
    # Metadata
    recorded_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='SET NULL'),
        comment='Giáo viên ghi nhận'
    )
    
    # Relationships
    student = db.relationship(
        'Student', 
        back_populates='health_records'
    )
    recorder = db.relationship(
        'User',
        foreign_keys=[recorded_by]
    )
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('student_id', 'record_date', name='unique_student_health_date'),
        db.CheckConstraint('weight > 0 AND weight < 100', name='check_weight_range'),
        db.CheckConstraint('temperature > 30 AND temperature < 45', name='check_temperature_range'),
    )
    
    def __repr__(self):
        return f'<HealthRecord {self.student_id} - {self.record_date}>'
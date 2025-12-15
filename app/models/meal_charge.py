from app.models.base import BaseModel, TimestampMixin
from app.extensions import db
from datetime import date


class MealCharge(BaseModel, TimestampMixin):
   
    __tablename__ = 'meal_charges'
    
    # Foreign Key
    student_id = db.Column(
        db.Integer, 
        db.ForeignKey('students.id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment='Học sinh'
    )
    
    # Meal Information
    charge_date = db.Column(
        db.Date, 
        nullable=False,
        default=date.today,
        index=True,
        comment='Ngày ăn'
    )
    has_meal = db.Column(
        db.Boolean, 
        default=True,
        comment='Có ăn không?  (False = nghỉ/không ăn)'
    )
    meal_price = db.Column(
        db.Numeric(10, 2),
        comment='Giá tiền ăn/ngày - YC3 (25,000đ)'
    )
    note = db.Column(
        db.Text,
        comment='Ghi chú (VD: Dị ứng...)'
    )
    
    # Relationships
    student = db.relationship(
        'Student', 
        back_populates='meal_charges'
    )
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('student_id', 'charge_date', name='unique_student_meal_date'),
        db.CheckConstraint('meal_price >= 0', name='check_positive_meal_price'),
    )
    
    def __repr__(self):
        return f'<MealCharge {self.student_id} - {self.charge_date}>'
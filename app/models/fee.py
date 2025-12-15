
from app. models.base import BaseModel, TimestampMixin
from app. extensions import db
from datetime import date
from enum import Enum


class FeeStatus(str, Enum):
    """trang thai hoc phi"""
    PENDING = "pending"      # cho thanh toan
    PAID = "paid"            # da thanh toan
    OVERDUE = "overdue"      # qua han thanh toan
    PARTIAL = "partial"      # thanh toan 1 phan


class Fee(BaseModel, TimestampMixin):
   
    __tablename__ = 'fees'
    
    # Foreign Key
    student_id = db.Column(
        db.Integer, 
        db.ForeignKey('students.id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment='Học sinh'
    )
    
    # Time Period
    month = db.Column(
        db.Integer, 
        nullable=False,
        comment='Tháng (1-12)'
    )
    year = db.Column(
        db.Integer, 
        nullable=False,
        comment='Năm'
    )
    
    # Fee Breakdown
    tuition_fee = db.Column(
        db.Numeric(10, 2), 
        nullable=False,
        comment='Học phí cơ bản - YC3 (1,500,000đ)'
    )
    meal_fee = db.Column(
        db.Numeric(10, 2), 
        default=0,
        comment='Tổng tiền ăn trong tháng - YC3 (25,000đ x số ngày)'
    )
    extra_fee = db.Column(
        db.Numeric(10, 2), 
        default=0,
        comment='Phí khác (đồng phục, sách vở... )'
    )
    discount = db.Column(
        db.Numeric(10, 2), 
        default=0,
        comment='Giảm giá'
    )
    total_fee = db.Column(
        db.Numeric(10, 2), 
        nullable=False,
        comment='Tổng cộng phải thanh toán'
    )
    paid_amount = db.Column(
        db.Numeric(10, 2), 
        default=0,
        comment='Số tiền đã thanh toán'
    )
    
    # Status
    status = db.Column(
        db.Enum(FeeStatus), 
        default=FeeStatus.PENDING,
        index=True,
        comment='Trạng thái thanh toán'
    )
    due_date = db.Column(
        db.Date,
        comment='Hạn thanh toán'
    )
    
    # Relationships
    student = db.relationship(
        'Student', 
        back_populates='fees'
    )
    payments = db.relationship(
        'Payment', 
        back_populates='fee',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    invoice = db.relationship(
        'Invoice', 
        back_populates='fee',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('student_id', 'month', 'year', name='unique_student_fee_month'),
        db.CheckConstraint('month >= 1 AND month <= 12', name='check_valid_month'),
        db.CheckConstraint('total_fee >= 0', name='check_positive_total'),
    )
    
    @property
    def remaining_amount(self):
        """so tien con no"""
        return float(self.total_fee) - float(self.paid_amount)
    
    @property
    def is_fully_paid(self):
        """Đa thanh toan du chua"""
        return self.paid_amount >= self.total_fee
    
    def __repr__(self):
        return f'<Fee {self.student_id} - {self.month}/{self.year}>'
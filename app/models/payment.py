
from app. models.base import BaseModel
from app.extensions import db
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    """method"""
    CASH = "cash"                  
    BANK_TRANSFER = "bank_transfer" 
    CARD = "card"                  
    MOMO = "momo"                   
    ZALOPAY = "zalopay"             


class Payment(BaseModel):

    __tablename__ = 'payments'
    
    # Foreign Key
    fee_id = db.Column(
        db.Integer, 
        db.ForeignKey('fees.id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment='Học phí được thanh toán'
    )
    
    # Payment Information
    amount = db.Column(
        db.Numeric(10, 2), 
        nullable=False,
        comment='Số tiền thanh toán'
    )
    payment_method = db.Column(
        db.Enum(PaymentMethod), 
        default=PaymentMethod.CASH,
        comment='Phương thức thanh toán'
    )
    payment_date = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        index=True,
        comment='Thời gian thanh toán'
    )
    reference_number = db.Column(
        db.String(50),
        comment='Mã giao dịch (nếu chuyển khoản)'
    )
    note = db.Column(
        db.Text,
        comment='Ghi chú'
    )
    
    # Metadata
    collected_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='SET NULL'),
        comment='Người thu tiền'
    )
    
    # Relationships
    fee = db.relationship(
        'Fee', 
        back_populates='payments'
    )
    collector = db.relationship(
        'User',
        foreign_keys=[collected_by]
    )
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='check_positive_amount'),
    )
    
    def __repr__(self):
        return f'<Payment {self.amount} - {self.payment_date}>'
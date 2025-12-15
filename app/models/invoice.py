
from app.models.base import BaseModel
from app.extensions import db
from datetime import datetime


class Invoice(BaseModel):

    __tablename__ = 'invoices'
    
    # Foreign Key
    fee_id = db.Column(
        db.Integer, 
        db.ForeignKey('fees.id', ondelete='CASCADE'), 
        nullable=False,
        unique=True,
        comment='Học phí (1 fee = 1 invoice)'
    )
    
    # Invoice Information
    invoice_number = db.Column(
        db.String(50), 
        unique=True, 
        nullable=False,
        index=True,
        comment='Số hóa đơn (VD: INV-2024-001)'
    )
    issue_date = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        comment='Ngày xuất hóa đơn'
    )
    pdf_url = db.Column(
        db.String(255),
        comment='Link file PDF hóa đơn'
    )
    
    # Relationships
    fee = db.relationship(
        'Fee', 
        back_populates='invoice'
    )
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'
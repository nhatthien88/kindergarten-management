from app.models.base import BaseModel, TimestampMixin
from app.extensions import db


class Parent(BaseModel, TimestampMixin):

    __tablename__ = 'parents'
    
    # Foreign Key
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False,
        unique=True,
        comment='Liên kết với User (1-1)'
    )
    
    # thong tin parent
    address = db.Column(
        db.Text,
        comment='Địa chỉ nhà'
    )
    emergency_contact = db.Column(
        db.String(20),
        comment='Số điện thoại khẩn cấp'
    )
    relationship = db.Column(
        db.String(50),
        comment='Quan hệ với trẻ (Bố/Mẹ/Ông/Bà)'
    )
    occupation = db.Column(
        db.String(100),
        comment='Nghề nghiệp'
    )
    
    # Relationships
    user = db.relationship(
        'User', 
        back_populates='parent_profile'
    )
    students = db.relationship(
        'Student', 
        back_populates='parent',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Parent {self.user. full_name if self.user else "Unknown"}>'
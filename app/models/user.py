from enum import Enum
from app.models.base import BaseModel, TimestampMixin
from app.extensions import db
from flask_bcrypt import generate_password_hash, check_password_hash

class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    PARENT = "parent"


class User(BaseModel, TimestampMixin):
     __tablename__ = 'users'
     email = db.Column(
        db.String(120), 
        unique=True, 
        nullable=False, 
        index=True,
        comment='Email đăng nhập (unique)'
    )
     password_hash = db.Column(
        db.String(255), 
        nullable=False,
        comment='Mật khẩu đã mã hóa (bcrypt)'
    )
     full_name = db.Column(
        db.String(100), 
        nullable=False,
        comment='Họ và tên đầy đủ'
    )
     phone = db.Column(
        db.String(20),
        comment='Số điện thoại'
    )
     
     role= db.Column(
        db.Enum(UserRole), 
        nullable=False, 
        index=True,
        comment='Vai trò:  admin/teacher/parent'
     )
     is_active = db.Column(
        db.Boolean, 
        default=True,
        comment='Tài khoản có hoạt động không'
    )
     parent_profile = db.relationship(
        'Parent', 
        back_populates='user', 
        uselist=False,
        cascade='all, delete-orphan'
    )
     teacher_profile = db.relationship(
        'Teacher', 
        back_populates='user', 
        uselist=False,
        cascade='all, delete-orphan'
    )
     def set_password(self, password):
        """Ma hoa va save password"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
     def check_password(self, password):
        """KKiem tra password"""
        return check_password_hash(self.password_hash, password)
    
     def to_dict(self):
        data = super().to_dict()
        data.pop('password_hash', None)  # khong tra ve password
        data['role'] = self.role.value if self.role else None
        return data
    
     def __repr__(self):
        return f'<User {self.email} - {self.role}>'
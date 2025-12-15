
from app.models.base import BaseModel
from app.extensions import db
from datetime import datetime


class Setting(BaseModel):

    __tablename__ = 'settings'
    
    # Setting Key-Value
    setting_key = db.Column(
        db.String(100), 
        unique=True, 
        nullable=False,
        index=True,
        comment='Khóa cấu hình (VD: tuition_fee_monthly)'
    )
    setting_value = db.Column(
        db.Text, 
        nullable=False,
        comment='Giá trị (VD: 1500000)'
    )
    description = db.Column(
        db.Text,
        comment='Mô tả cấu hình'
    )
    data_type = db.Column(
        db.String(20),
        default='string',
        comment='Loại dữ liệu (string, integer, float, boolean)'
    )
    
    # Metadata
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='Lần cập nhật cuối'
    )
    updated_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='SET NULL'),
        comment='Admin thay đổi'
    )
    
    # Relationships
    updater = db.relationship(
        'User',
        foreign_keys=[updated_by]
    )
    
    def get_value(self):
        """Parse value theo data_type"""
        if self.data_type == 'integer':
            return int(self.setting_value)
        elif self.data_type == 'float':
            return float(self.setting_value)
        elif self.data_type == 'boolean':
            return self.setting_value.lower() in ('true', '1', 'yes')
        return self.setting_value
    
    def __repr__(self):
        return f'<Setting {self.setting_key}={self.setting_value}>'
from datetime import datetime, timezone
from app.extensions import db

class TimestampMixin:
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment='Thời gian tạo'
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        comment='Thời gian cập nhật'
    )
class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True,
        comment='ID tự động tăng'
    )
    
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    """tra ve doi tuong, gia tri cua doi tuong"""
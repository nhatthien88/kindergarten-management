# app/blueprints/admin/services/setting_service.py
"""Service for system settings management"""
from app.extensions import db
from app.models import Setting


def get_setting(key):
    """Get one setting value by key"""
    setting = Setting.query.filter_by(setting_key=key).first()
    if setting:
        return setting.get_value()
    return None


def get_all_settings():
    """Get all settings as a dictionary"""
    settings = Setting.query.all()
    return {s.setting_key: s.get_value() for s in settings}


def update_setting(key, value, updated_by):
    """Update a setting value"""
    try:
        setting = Setting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = str(value)
            setting.updated_by = updated_by
        else:
            # Create new setting if not exists
            setting = Setting(
                setting_key=key,
                setting_value=str(value),
                updated_by=updated_by
            )
            db.session.add(setting)
        
        db.session.commit()
        return True, "Cập nhật cài đặt thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi cập nhật cài đặt: {str(e)}"


def initialize_default_settings():
    """Initialize default settings if not exist"""
    default_settings = [
        {
            'setting_key': 'tuition_fee_monthly',
            'setting_value': '1500000',
            'description': 'Học phí hàng tháng (VND)',
            'data_type': 'integer'
        },
        {
            'setting_key': 'meal_price_daily',
            'setting_value': '25000',
            'description': 'Giá tiền ăn mỗi ngày (VND)',
            'data_type': 'integer'
        },
        {
            'setting_key': 'default_classroom_capacity',
            'setting_value': '25',
            'description': 'Sức chứa mặc định của lớp học',
            'data_type': 'integer'
        },
        {
            'setting_key': 'school_name',
            'setting_value': 'Trường Mầm Non ABC',
            'description': 'Tên trường',
            'data_type': 'string'
        },
        {
            'setting_key': 'school_address',
            'setting_value': '',
            'description': 'Địa chỉ trường',
            'data_type': 'string'
        },
        {
            'setting_key': 'school_phone',
            'setting_value': '',
            'description': 'Số điện thoại trường',
            'data_type': 'string'
        },
        {
            'setting_key': 'school_email',
            'setting_value': '',
            'description': 'Email trường',
            'data_type': 'string'
        }
    ]
    
    try:
        for setting_data in default_settings:
            existing = Setting.query.filter_by(setting_key=setting_data['setting_key']).first()
            if not existing:
                setting = Setting(**setting_data)
                db.session.add(setting)
        
        db.session.commit()
        return True, "Khởi tạo cài đặt mặc định thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi khởi tạo cài đặt: {str(e)}"

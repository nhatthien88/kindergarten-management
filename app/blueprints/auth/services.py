# app/blueprints/auth/services.py
from app.extensions import db
from app.models import User, UserRole, Parent, Teacher
from sqlalchemy.exc import IntegrityError


def create_user(email, password, full_name, role, phone=None, **extra_data):
    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user: 
            raise ValueError('Email đã tồn tại trong hệ thống')
        

        if role == 'teacher' and extra_data.get('employee_id'):
            existing_teacher = Teacher.query.filter_by(
                employee_id=extra_data['employee_id']
            ).first()
            if existing_teacher:
                raise ValueError('Mã giáo viên đã tồn tại trong hệ thống')
        

        if role not in ['admin', 'teacher', 'parent']: 
            raise ValueError('Vai trò không hợp lệ')
        

        user = User(
            email=email,
            full_name=full_name,
            role=UserRole[role.upper()],
            phone=phone,
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  
        

        if role == 'parent':
            parent = Parent(
                user_id=user.id,
                address=extra_data.get('address'),
                emergency_contact=extra_data.get('emergency_contact'),
                relationship=extra_data.get('relationship'),
                occupation=extra_data.get('occupation')
            )
            db.session.add(parent)
            
        elif role == 'teacher': 
            teacher = Teacher(
                user_id=user.id,
                employee_id=extra_data.get('employee_id'),
                qualification=extra_data.get('qualification'),
                specialization=extra_data.get('specialization')
            )
            db.session.add(teacher)
        
        db.session.commit()
        return user
        
    except IntegrityError as e:
        db.session.rollback()
        error_message = str(e.orig)
        if 'Duplicate entry' in error_message:
            if 'email' in error_message: 
                raise ValueError('Email đã tồn tại trong hệ thống')
            elif 'employee_id' in error_message: 
                raise ValueError('Mã giáo viên đã tồn tại trong hệ thống')
        raise ValueError('Thông tin đã tồn tại trong hệ thống')
        
    except Exception as e: 
        db.session.rollback()
        raise


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    
    if not user: 
        return None
    
    if not user.check_password(password):
        return None
    
    if not user.is_active:
        return None
    
    return user
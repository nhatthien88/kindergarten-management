"""
Authentication business logic
"""
from app.models import User, UserRole, Parent, Teacher
from app.extensions import db


def create_user(email, password, full_name, role, phone=None, **extra_data):
 
    if role not in ['parent', 'teacher']: 
        raise ValueError('Only parent or teacher roles allowed for public registration')
    
    if User.query.filter_by(email=email).first():
        raise ValueError('Email already exists')
    
    user = User(
        email=email,
        full_name=full_name,
        role=UserRole(role),
        phone=phone
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.flush()  
    
    if role == 'parent':
        parent = Parent(
            user_id=user. id,
            address=extra_data.get('address'),
            emergency_contact=extra_data.get('emergency_contact'),
            relationship=extra_data.get('relationship', 'Phụ huynh'),
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


def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()
    
    if not user: 
        return None
    
    if not user.check_password(password):
        return None
    
    if not user.is_active:
        return None
    
    return user
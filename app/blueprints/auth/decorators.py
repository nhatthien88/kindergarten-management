from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User

def role_required(*roles):
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
        
            verify_jwt_in_request()
            
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403
            
            if user.role. value not in roles:
                return jsonify({
                    'error': 'Access denied',
                    'message':  f'This endpoint requires one of these roles: {", ".join(roles)}',
                    'your_role': user.role.value
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

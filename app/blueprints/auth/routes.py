from flask import request, jsonify, render_template 
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app.blueprints.auth import auth_bp
from app.blueprints.auth.services import create_user, authenticate_user
from app.models import User
from datetime import timedelta


@auth_bp.route('/register', methods=['POST'])
def register():

    try:
        data = request.json
        
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        role = data.get('role')
        
        if not all([email, password, full_name, role]):
            return jsonify({
                'error': 'Missing required fields',
                'required': ['email', 'password', 'full_name', 'role']
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'error': 'Password must be at least 6 characters'
            }), 400
        
        phone = data.get('phone')
        
        extra_data = {
            'address': data.get('address'),
            'emergency_contact': data. get('emergency_contact'),
            'relationship': data.get('relationship'),
            'occupation': data.get('occupation'),
            'employee_id': data.get('employee_id'),
            'qualification':  data.get('qualification'),
            'specialization': data.get('specialization')
        }
        
        user = create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            phone=phone,
            **extra_data
        )
        
        return jsonify({
            'message':  'Registration successful',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e: 
        return jsonify({'error':  f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
   
    try:
        data = request.json
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'error': 'Email and password are required'
            }), 400
        
        user = authenticate_user(email, password)
        
        if not user:
            return jsonify({
                'error': 'Invalid email or password'
            }), 401

        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token':  refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed:  {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
   
    try:
        current_user_id = get_jwt_identity()
        
        new_access_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
   
    try: 
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        
        return jsonify({
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Logout failed:  {str(e)}'}), 500
    

@auth_bp.route('/login-page')
def login_page():
    """Render login page"""
    return render_template('auth/login.html')


@auth_bp.route('/register-page')
def register_page():
    """Render register page"""
    return render_template('auth/register.html')


@auth_bp.route('/dashboard-page')
def dashboard_page():
    """Render dashboard page"""
    return render_template('dashboard.html')
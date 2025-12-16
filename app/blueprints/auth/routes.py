# app/blueprints/auth/routes.py
from flask import request, jsonify, render_template, redirect, url_for, flash, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.blueprints.auth import auth_bp
from app.blueprints.auth.services import create_user, authenticate_user
from app.models import User, UserRole
from datetime import timedelta



@auth_bp.route('/login-page', methods=['GET'])
def login_page():
    """Trang đăng nhập"""
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:  
            if user.role == UserRole.ADMIN:
                return redirect(url_for('admin.dashboard'))
            elif user.role == UserRole.TEACHER:
                return redirect(url_for('teacher.dashboard'))
            elif user.role == UserRole.PARENT:
                return redirect(url_for('parent.dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/login-submit', methods=['POST'])
def login_submit():
    try: 
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:  
            flash('Vui lòng nhập đầy đủ email và mật khẩu', 'error')
            return redirect(url_for('auth.login_page'))
        
        user = authenticate_user(email, password)
        
        if not user:
            flash('Email hoặc mật khẩu không đúng', 'error')
            return redirect(url_for('auth.login_page'))
        
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_role'] = user.role.value
        session['user_name'] = user.full_name
        session.permanent = True
        
        flash(f'Chào mừng {user.full_name}! ', 'success')
        
        if user.role == UserRole.ADMIN:
            return redirect(url_for('admin.dashboard'))
        elif user.role == UserRole.TEACHER:
            return redirect(url_for('teacher.dashboard'))
        elif user.role == UserRole.PARENT:
            return redirect(url_for('parent.dashboard'))
        else:
            flash('Vai trò không hợp lệ', 'error')
            return redirect(url_for('auth.login_page'))
        
    except Exception as e: 
        flash(f'Có lỗi xảy ra: {str(e)}', 'error')
        return redirect(url_for('auth.login_page'))


@auth_bp.route('/register-page', methods=['GET'])
def register_page():
    return render_template('auth/register.html')


@auth_bp.route('/register-submit', methods=['POST'])
def register_submit():
    """Xử lý đăng ký từ form HTML"""
    try:  
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        role = request.form.get('role')
        
        if not all([email, password, full_name, role]):
            flash('Vui lòng nhập đầy đủ thông tin bắt buộc', 'error')
            return redirect(url_for('auth.register_page'))
        
        if len(password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự', 'error')
            return redirect(url_for('auth.register_page'))
        
        extra_data = {}
        if role == 'parent':
            extra_data['address'] = request.form.get('address')
            extra_data['relationship'] = request.form.get('relationship', 'Phụ huynh')
            extra_data['emergency_contact'] = request.form.get('phone')
            extra_data['occupation'] = request.form.get('occupation')
        elif role == 'teacher':
            extra_data['employee_id'] = request.form.get('employee_id')
            extra_data['qualification'] = request.form.get('qualification')
            extra_data['specialization'] = request.form.get('specialization')
        
        user = create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            phone=phone,
            **extra_data
        )
        
        flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')
        return redirect(url_for('auth.login_page'))
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('auth.register_page'))
        
    except Exception as e: 
        error_message = str(e)
        
        if 'Duplicate entry' in error_message: 
            if 'email' in error_message.lower():
                flash('Email đã tồn tại trong hệ thống', 'error')
            elif 'employee_id' in error_message.lower():
                flash('Mã giáo viên đã tồn tại trong hệ thống', 'error')
            else:
                flash('Thông tin đã tồn tại trong hệ thống', 'error')
        else:
            flash(f'Đăng ký thất bại:  {error_message}', 'error')
        
        return redirect(url_for('auth.register_page'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công', 'success')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/dashboard-page')
def dashboard_page():
    user_id = session.get('user_id')
    
    if not user_id:  
        flash('Vui lòng đăng nhập', 'warning')
        return redirect(url_for('auth.login_page'))
    
    user = User.query.get(user_id)
    
    if not user: 
        session.clear()
        flash('Tài khoản không tồn tại', 'error')
        return redirect(url_for('auth.login_page'))
    
    if user.role == UserRole.ADMIN:
        return redirect(url_for('admin.dashboard'))
    elif user.role == UserRole.TEACHER:
        return redirect(url_for('teacher.dashboard'))
    elif user.role == UserRole.PARENT:
        return redirect(url_for('parent.dashboard'))
    
    flash('Vai trò không xác định', 'error')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/register', methods=['POST'])
def register_api():
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
                'error':  'Password must be at least 6 characters'
            }), 400
        
        phone = data.get('phone')
        
        extra_data = {
            'address': data.get('address'),
            'emergency_contact': data.get('emergency_contact'),
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
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login_api():
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
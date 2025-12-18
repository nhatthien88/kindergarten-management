# app/blueprints/admin/fee_routes.py
from flask import render_template, request, flash, redirect, url_for, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import fee_service
from app.models import User, Classroom
from app.extensions import db


@admin_bp.route('/fees')
@admin_required
def list_fees():
    """List all fees with filters"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get filters
        filters = {}
        if request.args.get('month'):
            filters['month'] = int(request.args.get('month'))
        if request.args.get('year'):
            filters['year'] = int(request.args.get('year'))
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('classroom_id'):
            filters['classroom_id'] = int(request.args.get('classroom_id'))
        
        # Get fees
        fees = fee_service.get_fees(filters=filters if filters else None)
        
        # Get classrooms for filter
        classrooms = Classroom.query.order_by(Classroom.name).all()
        
        return render_template('admin/fees/list.html',
                             user=user,
                             fees=fees,
                             classrooms=classrooms,
                             filters=filters)
    except Exception as e:
        flash(f'Lỗi tải danh sách học phí: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/fees/generate', methods=['GET'])
@admin_required
def generate_fees_form():
    """Generate monthly fees form"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        return render_template('admin/fees/generate.html', user=user)
    except Exception as e:
        flash(f'Lỗi tải form: {str(e)}', 'error')
        return redirect(url_for('admin.list_fees'))


@admin_bp.route('/fees/generate', methods=['POST'])
@admin_required
def generate_fees():
    """Generate fees for all students"""
    try:
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        
        success, message = fee_service.generate_monthly_fees(month, year)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('admin.list_fees'))
    except Exception as e:
        flash(f'Lỗi tạo học phí: {str(e)}', 'error')
        return redirect(url_for('admin.generate_fees_form'))


@admin_bp.route('/fees/<int:fee_id>')
@admin_required
def fee_detail(fee_id):
    """Fee detail with breakdown and payments"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        detail = fee_service.get_fee_detail(fee_id)
        if not detail:
            flash('Học phí không tồn tại', 'error')
            return redirect(url_for('admin.list_fees'))
        
        return render_template('admin/fees/detail.html',
                             user=user,
                             fee=detail['fee'],
                             student=detail['student'],
                             payments=detail['payments'],
                             remaining=detail['remaining'])
    except Exception as e:
        flash(f'Lỗi tải thông tin học phí: {str(e)}', 'error')
        return redirect(url_for('admin.list_fees'))


@admin_bp.route('/fees/<int:fee_id>/payment', methods=['GET'])
@admin_required
def payment_form(fee_id):
    """Payment recording form"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        detail = fee_service.get_fee_detail(fee_id)
        if not detail:
            flash('Học phí không tồn tại', 'error')
            return redirect(url_for('admin.list_fees'))
        
        return render_template('admin/fees/payment_form.html',
                             user=user,
                             fee=detail['fee'],
                             student=detail['student'],
                             remaining=detail['remaining'])
    except Exception as e:
        flash(f'Lỗi tải form thanh toán: {str(e)}', 'error')
        return redirect(url_for('admin.list_fees'))


@admin_bp.route('/fees/<int:fee_id>/payment', methods=['POST'])
@admin_required
def record_payment(fee_id):
    """Record payment"""
    try:
        user_id = session.get('user_id')
        
        amount = float(request.form.get('amount'))
        method = request.form.get('method', 'cash')
        reference = request.form.get('reference_number', '')
        note = request.form.get('note', '')
        
        success, message = fee_service.record_payment(
            fee_id, amount, method, reference, note, user_id
        )
        
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('admin.fee_detail', fee_id=fee_id))
        else:
            return redirect(url_for('admin.payment_form', fee_id=fee_id))
    except Exception as e:
        flash(f'Lỗi ghi nhận thanh toán: {str(e)}', 'error')
        return redirect(url_for('admin.payment_form', fee_id=fee_id))

# app/blueprints/admin/services/fee_service.py
"""Service for fee management"""
from app.extensions import db
from app.models import Fee, Payment, Student, MealCharge, FeeStatus, PaymentMethod
from app.blueprints.admin.services import setting_service
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlalchemy import extract


def calculate_fee(student_id, month, year):
    """Calculate fee for a student in a month"""
    try:
        # Get settings
        tuition_fee = setting_service.get_setting('tuition_fee_monthly') or 1500000
        meal_price = setting_service.get_setting('meal_price_daily') or 25000
        
        # Count meal charges for the month
        meal_count = MealCharge.query.filter(
            MealCharge.student_id == student_id,
            extract('month', MealCharge.charge_date) == month,
            extract('year', MealCharge.charge_date) == year,
            MealCharge.has_meal == True
        ).count()
        
        meal_fee = meal_count * meal_price
        total = Decimal(tuition_fee) + Decimal(meal_fee)
        
        return {
            'tuition_fee': Decimal(tuition_fee),
            'meal_fee': Decimal(meal_fee),
            'meal_count': meal_count,
            'extra_fee': Decimal(0),
            'discount': Decimal(0),
            'total_fee': total
        }
    except Exception as e:
        return None


def generate_monthly_fees(month, year):
    """Generate fees for ALL active students in a month"""
    try:
        # Get all active students
        students = Student.query.filter_by(is_active=True).all()
        if not students:
            return False, "Không có học sinh nào đang hoạt động"
        
        created_count = 0
        skipped_count = 0
        
        for student in students:
            # Check if fee already exists
            existing_fee = Fee.query.filter_by(
                student_id=student.id,
                month=month,
                year=year
            ).first()
            
            if existing_fee:
                skipped_count += 1
                continue
            
            # Calculate fee
            fee_data = calculate_fee(student.id, month, year)
            if not fee_data:
                continue
            
            # Create fee
            due_date = date(year, month, 10) if month <= 12 else date(year + 1, 1, 10)
            
            fee = Fee(
                student_id=student.id,
                month=month,
                year=year,
                tuition_fee=fee_data['tuition_fee'],
                meal_fee=fee_data['meal_fee'],
                extra_fee=fee_data['extra_fee'],
                discount=fee_data['discount'],
                total_fee=fee_data['total_fee'],
                paid_amount=Decimal(0),
                status=FeeStatus.PENDING,
                due_date=due_date
            )
            db.session.add(fee)
            created_count += 1
        
        db.session.commit()
        message = f"Tạo {created_count} học phí thành công"
        if skipped_count > 0:
            message += f", bỏ qua {skipped_count} học phí đã tồn tại"
        return True, message
        
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi tạo học phí: {str(e)}"


def record_payment(fee_id, amount, method, reference, note, collected_by):
    """Record payment and update fee status"""
    try:
        fee = db.session.get(Fee, fee_id)
        if not fee:
            return False, "Học phí không tồn tại"
        
        # Create payment record
        payment = Payment(
            fee_id=fee_id,
            amount=Decimal(amount),
            payment_method=PaymentMethod(method),
            payment_date=datetime.utcnow(),
            reference_number=reference,
            note=note,
            collected_by=collected_by
        )
        db.session.add(payment)
        
        # Update fee paid amount
        fee.paid_amount += Decimal(amount)
        
        # Update fee status
        update_fee_status(fee)
        
        db.session.commit()
        return True, "Ghi nhận thanh toán thành công"
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi ghi nhận thanh toán: {str(e)}"


def update_fee_status(fee):
    """Auto-update fee status based on paid_amount and due_date"""
    if fee.paid_amount >= fee.total_fee:
        fee.status = FeeStatus.PAID
    elif fee.paid_amount > 0:
        fee.status = FeeStatus.PARTIAL
    elif fee.due_date and fee.due_date < date.today():
        fee.status = FeeStatus.OVERDUE
    else:
        fee.status = FeeStatus.PENDING


def get_fees(filters=None):
    """Get fees with optional filters"""
    query = Fee.query.join(Fee.student)
    
    if filters:
        if filters.get('month'):
            query = query.filter(Fee.month == filters['month'])
        if filters.get('year'):
            query = query.filter(Fee.year == filters['year'])
        if filters.get('status'):
            query = query.filter(Fee.status == FeeStatus(filters['status']))
        if filters.get('classroom_id'):
            query = query.filter(Student.classroom_id == filters['classroom_id'])
    
    return query.order_by(Fee.year.desc(), Fee.month.desc()).all()


def get_overdue_fees():
    """Get fees past due_date and not fully paid"""
    return Fee.query.filter(
        Fee.due_date < date.today(),
        Fee.paid_amount < Fee.total_fee
    ).order_by(Fee.due_date).all()


def get_fee_detail(fee_id):
    """Get detailed fee information with payments"""
    fee = db.session.get(Fee, fee_id)
    if not fee:
        return None
    
    return {
        'fee': fee,
        'student': fee.student,
        'payments': fee.payments.order_by(Payment.payment_date.desc()).all(),
        'remaining': fee.remaining_amount
    }

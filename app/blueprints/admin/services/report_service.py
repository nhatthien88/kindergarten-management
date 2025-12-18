# app/blueprints/admin/services/report_service.py
"""Service for reports and statistics"""
from app.extensions import db
from app.models import User, Student, Teacher, Parent, Fee, Payment, Classroom, FeeStatus, UserRole
from sqlalchemy import func, extract
from datetime import datetime, date
from decimal import Decimal


def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Count active users
        total_students = Student.query.filter_by(is_active=True).count()
        total_teachers = User.query.filter_by(role=UserRole.TEACHER, is_active=True).count()
        total_parents = User.query.filter_by(role=UserRole.PARENT, is_active=True).count()
        
        # Revenue this month
        current_month = date.today().month
        current_year = date.today().year
        
        revenue_query = db.session.query(func.sum(Payment.amount)).join(Payment.fee).filter(
            extract('month', Payment.payment_date) == current_month,
            extract('year', Payment.payment_date) == current_year
        ).scalar()
        
        revenue_this_month = float(revenue_query) if revenue_query else 0
        
        # Pending and overdue fees
        pending_fees = Fee.query.filter(
            Fee.status == FeeStatus.PENDING
        ).count()
        
        overdue_fees = Fee.query.filter(
            Fee.status == FeeStatus.OVERDUE
        ).count()
        
        return {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_parents': total_parents,
            'revenue_this_month': revenue_this_month,
            'pending_fees': pending_fees,
            'overdue_fees': overdue_fees
        }
    except Exception as e:
        return {
            'total_students': 0,
            'total_teachers': 0,
            'total_parents': 0,
            'revenue_this_month': 0,
            'pending_fees': 0,
            'overdue_fees': 0
        }


def get_student_statistics(school_year=None):
    """Get student statistics by class and gender"""
    try:
        query = Student.query.filter_by(is_active=True)
        
        # Group by classroom
        classroom_stats = db.session.query(
            Classroom.name,
            func.count(Student.id).label('count')
        ).join(Student.classroom).filter(
            Student.is_active == True
        )
        
        if school_year:
            classroom_stats = classroom_stats.filter(Classroom.school_year == school_year)
        
        classroom_stats = classroom_stats.group_by(Classroom.name).all()
        
        # Get gender distribution
        gender_stats = db.session.query(
            Student.gender,
            func.count(Student.id).label('count')
        ).filter(Student.is_active == True)
        
        if school_year:
            gender_stats = gender_stats.join(Student.classroom).filter(
                Classroom.school_year == school_year
            )
        
        gender_stats = gender_stats.group_by(Student.gender).all()
        
        return {
            'by_classroom': {name: count for name, count in classroom_stats},
            'by_gender': {gender: count for gender, count in gender_stats}
        }
    except Exception as e:
        return {
            'by_classroom': {},
            'by_gender': {}
        }


def get_gender_distribution():
    """Get gender distribution for pie chart"""
    try:
        stats = db.session.query(
            Student.gender,
            func.count(Student.id).label('count')
        ).filter(Student.is_active == True).group_by(Student.gender).all()
        
        return {gender: count for gender, count in stats}
    except Exception as e:
        return {}


def get_revenue_by_month(start_date, end_date):
    """Get revenue trend by month"""
    try:
        revenue_data = db.session.query(
            extract('year', Payment.payment_date).label('year'),
            extract('month', Payment.payment_date).label('month'),
            func.sum(Payment.amount).label('total')
        ).filter(
            Payment.payment_date >= start_date,
            Payment.payment_date <= end_date
        ).group_by('year', 'month').order_by('year', 'month').all()
        
        result = []
        for year, month, total in revenue_data:
            result.append({
                'label': f"{int(month)}/{int(year)}",
                'value': float(total) if total else 0
            })
        
        return result
    except Exception as e:
        return []


def get_revenue_by_class(month, year):
    """Get revenue by classroom for bar chart"""
    try:
        revenue_data = db.session.query(
            Classroom.name,
            func.sum(Payment.amount).label('total')
        ).join(Payment.fee).join(Fee.student).join(Student.classroom).filter(
            extract('month', Payment.payment_date) == month,
            extract('year', Payment.payment_date) == year
        ).group_by(Classroom.name).all()
        
        return {name: float(total) if total else 0 for name, total in revenue_data}
    except Exception as e:
        return {}

# app/blueprints/admin/report_routes.py
from flask import render_template, request, flash, redirect, url_for, session
from app.blueprints.admin import admin_bp
from app.blueprints.admin.decorators import admin_required
from app.blueprints.admin.services import report_service, fee_service, classroom_service
from app.models import User
from app.extensions import db
from datetime import datetime, date, timedelta


@admin_bp.route('/reports/dashboard')
@admin_required
def report_dashboard():
    """Dashboard with charts and statistics"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get dashboard stats
        stats = report_service.get_dashboard_stats()
        
        # Get recent overdue fees
        recent_fees = fee_service.get_overdue_fees()[:5]
        
        # Get revenue by month (last 6 months)
        end_date = date.today()
        start_date = end_date - timedelta(days=180)
        revenue_trend = report_service.get_revenue_by_month(start_date, end_date)
        
        # Get student gender distribution
        gender_dist = report_service.get_gender_distribution()
        
        return render_template('admin/reports/dashboard.html',
                             user=user,
                             stats=stats,
                             recent_fees=recent_fees,
                             revenue_trend=revenue_trend,
                             gender_dist=gender_dist)
    except Exception as e:
        flash(f'Lỗi tải dashboard: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/reports/students')
@admin_required
def student_report():
    """Student statistics report (YC4)"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get school year filter
        school_year = request.args.get('school_year')
        
        # Get statistics
        stats = report_service.get_student_statistics(school_year=school_year)
        
        # Get available school years
        school_years = classroom_service.get_school_years()
        
        return render_template('admin/reports/students.html',
                             user=user,
                             stats=stats,
                             school_years=school_years,
                             current_year=school_year)
    except Exception as e:
        flash(f'Lỗi tải báo cáo học sinh: {str(e)}', 'error')
        return redirect(url_for('admin.report_dashboard'))


@admin_bp.route('/reports/revenue')
@admin_required
def revenue_report():
    """Revenue report with charts"""
    try:
        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        
        # Get month/year from query params or use current
        month = int(request.args.get('month', date.today().month))
        year = int(request.args.get('year', date.today().year))
        
        # Get revenue by classroom
        revenue_by_class = report_service.get_revenue_by_class(month, year)
        
        # Get revenue trend (last 12 months)
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        revenue_trend = report_service.get_revenue_by_month(start_date, end_date)
        
        return render_template('admin/reports/revenue.html',
                             user=user,
                             month=month,
                             year=year,
                             revenue_by_class=revenue_by_class,
                             revenue_trend=revenue_trend)
    except Exception as e:
        flash(f'Lỗi tải báo cáo doanh thu: {str(e)}', 'error')
        return redirect(url_for('admin.report_dashboard'))

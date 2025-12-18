# Admin Features Documentation

## Overview
This document describes the complete admin features implementation for the Kindergarten Management System.

## Features Implemented

### 1. User Management (Quản lý Users)
**Location:** `app/blueprints/admin/user_routes.py`

**Routes:**
- `GET /api/admin/users` - List all users with filters (role, status)
- `GET /api/admin/users/<id>` - User detail page
- `POST /api/admin/users/<id>/approve` - Approve teacher (AJAX)
- `POST /api/admin/users/<id>/toggle` - Toggle user active status (AJAX)

**Features:**
- Filter users by role (teacher/parent) and status (active/inactive)
- Display pending teachers count (teachers with is_active=False)
- Show teacher status: ✅ Đã duyệt / ⏳ Chờ duyệt
- Show parent status: ✅ Có X con / ⚠️ Chưa liên kết
- AJAX approve/toggle functionality

---

### 2. Classroom Management (Quản lý Lớp học)
**Location:** `app/blueprints/admin/classroom_routes.py`

**Routes:**
- `GET /api/admin/classrooms` - List all classrooms
- `GET /api/admin/classrooms/add` - Add classroom form
- `POST /api/admin/classrooms` - Create classroom
- `GET /api/admin/classrooms/<id>` - Classroom detail with students
- `GET /api/admin/classrooms/<id>/edit` - Edit classroom form
- `POST /api/admin/classrooms/<id>/update` - Update classroom
- `POST /api/admin/classrooms/<id>/assign-teacher` - Assign teacher
- `POST /api/admin/classrooms/<id>/delete` - Delete classroom (if no students)

**Features:**
- Filter classrooms by school year
- Display classroom capacity status (current/max, full indicator)
- Assign homeroom teacher to classroom
- View student list in each classroom
- Only allow deletion if classroom has no students

---

### 3. System Settings (Cấu hình Hệ thống - YC5)
**Location:** `app/blueprints/admin/setting_routes.py`

**Routes:**
- `GET /api/admin/settings` - Settings page with tabs
- `POST /api/admin/settings/update` - Update all settings

**Default Settings:**
```python
tuition_fee_monthly: 1,500,000 VND   # YC3
meal_price_daily: 25,000 VND         # YC3
default_classroom_capacity: 25       # YC5
school_name: 'Trường Mầm Non ABC'
school_address: ''
school_phone: ''
school_email: ''
```

**Features:**
- Tab-based interface for different setting categories
- Settings automatically initialized on first access
- Updates tracked with updated_by and updated_at

---

### 4. Fee Management (Quản lý Học phí - YC3)
**Location:** `app/blueprints/admin/fee_routes.py`

**Routes:**
- `GET /api/admin/fees` - List all fees with filters
- `GET /api/admin/fees/generate` - Generate monthly fees form
- `POST /api/admin/fees/generate` - Generate fees for all students
- `GET /api/admin/fees/<id>` - Fee detail with breakdown
- `GET /api/admin/fees/<id>/payment` - Payment form
- `POST /api/admin/fees/<id>/payment` - Record payment

**Fee Calculation (YC3):**
```
Học phí cơ bản:    1,500,000đ  (from settings)
Tiền ăn:           meal_count × 25,000đ  (from MealCharge records)
Phí khác:          0đ
Giảm giá:          -0đ
----------------------
Tổng cộng:         1,500,000đ + meal_fee
```

**Features:**
- Generate fees for all active students in a month
- Filter fees by month, year, status, classroom
- Status badges: pending, paid, overdue, partial
- Detailed fee breakdown display
- Payment recording with multiple methods (cash, bank_transfer, card, momo, zalopay)
- Auto-update fee status after payment

---

### 5. Reports & Statistics (Thống kê & Báo cáo - YC4)
**Location:** `app/blueprints/admin/report_routes.py`

**Routes:**
- `GET /api/admin/reports/dashboard` - Dashboard with charts
- `GET /api/admin/reports/students` - Student statistics (YC4)
- `GET /api/admin/reports/revenue` - Revenue report

**Dashboard Metrics:**
- Total students, teachers, parents
- Revenue this month
- Pending fees count
- Overdue fees count

**Student Statistics (YC4):**
- Table: Number of students per classroom
- Pie Chart: Gender distribution (Nam/Nữ) using Chart.js
- Filter by school year

**Revenue Reports:**
- Line Chart: Revenue trend (last 6-12 months)
- Bar Chart: Revenue by classroom
- Detailed revenue table by classroom

---

## Technical Implementation

### Service Layer
All business logic is in service files:
- `user_service.py` - User management operations
- `classroom_service.py` - Classroom CRUD operations
- `fee_service.py` - Fee calculation and payment handling
- `setting_service.py` - Settings management
- `report_service.py` - Statistics and analytics

### Security
- All routes protected by `@admin_required` decorator
- Session-based authentication (existing pattern)
- No breaking changes to existing auth/teacher/parent modules

### UI/UX
- **Layout:** Sidebar navigation with admin base template
- **Styling:** Custom admin.css with responsive design
- **JavaScript:** admin.js with AJAX functionality
- **Charts:** Chart.js CDN for YC4 visualizations
- **Colors:** Status badges (green/yellow/red/blue)
- **Responsiveness:** Mobile-friendly design

### Database Models Used
All existing models from `app/models/`:
- User, Teacher, Parent (user management)
- Classroom, Student (classroom management)
- Fee, Payment, MealCharge (fee management)
- Setting (system settings)

---

## Requirements Fulfilled

### ✅ YC3: Fee Management
- Tuition fee: 1,500,000 VND (configurable)
- Meal price: 25,000 VND/day (configurable)
- Automatic fee calculation based on meal records

### ✅ YC4: Student Statistics
- Table showing student count by classroom
- Pie chart for gender distribution (Nam/Nữ)
- Implemented using Chart.js

### ✅ YC5: Configurable Classroom Capacity
- Default capacity setting in system settings
- Capacity configurable per classroom
- Visual indicators when classroom is full

---

## Testing Checklist

### User Management
- [ ] List users with filters
- [ ] View user details
- [ ] Approve pending teachers (AJAX)
- [ ] Toggle user status (AJAX)

### Classroom Management
- [ ] Create new classroom
- [ ] Edit classroom details
- [ ] Assign teacher to classroom
- [ ] View classroom with student list
- [ ] Delete empty classroom
- [ ] Filter by school year

### Fee Management
- [ ] Generate monthly fees for all students
- [ ] Filter fees by month/year/status/classroom
- [ ] View fee detail with breakdown
- [ ] Record payment
- [ ] Verify automatic status update

### Settings
- [ ] View settings page
- [ ] Update fee settings
- [ ] Update classroom settings
- [ ] Update school info

### Reports
- [ ] View dashboard with metrics
- [ ] View student statistics with pie chart (YC4)
- [ ] View revenue reports with charts
- [ ] Filter reports by date/school year

---

## File Structure

```
app/
├── blueprints/admin/
│   ├── __init__.py (imports all routes)
│   ├── routes.py (main dashboard)
│   ├── user_routes.py
│   ├── classroom_routes.py
│   ├── fee_routes.py
│   ├── report_routes.py
│   ├── setting_routes.py
│   ├── decorators.py
│   └── services/
│       ├── user_service.py
│       ├── classroom_service.py
│       ├── fee_service.py
│       ├── report_service.py
│       └── setting_service.py
├── static/
│   ├── css/admin.css
│   └── js/admin.js
└── templates/admin/
    ├── base.html (sidebar layout)
    ├── dashboard.html
    ├── users/ (list.html, detail.html)
    ├── classrooms/ (list.html, form.html, detail.html)
    ├── fees/ (list.html, generate.html, detail.html, payment_form.html)
    ├── reports/ (dashboard.html, students.html, revenue.html)
    └── settings/ (index.html)
```

---

## Usage Examples

### Approving Teachers
1. Navigate to `/api/admin/users?role=teacher&status=inactive`
2. View pending teachers (⏳ Chờ duyệt)
3. Click "Chi tiết" to view teacher details
4. Click "✅ Duyệt giáo viên" button
5. AJAX request approves teacher (sets is_active=True)

### Generating Monthly Fees
1. Navigate to `/api/admin/fees/generate`
2. Select month and year
3. Click "✅ Tạo học phí"
4. System creates fees for all active students
5. Fees calculated: tuition + (meal_count × meal_price)

### Viewing Statistics (YC4)
1. Navigate to `/api/admin/reports/students`
2. View table of student count by classroom
3. View pie chart of gender distribution
4. Filter by school year to see specific data

---

## Notes

- All Vietnamese text preserved in UI
- No external dependencies added except Chart.js (CDN)
- Follows existing project structure and patterns
- Compatible with existing authentication system
- No database migrations needed (uses existing models)

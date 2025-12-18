# run: python scripts/seed_students.py

import sys
import os
import random
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import User, UserRole, Teacher, Parent, Classroom, Student, Setting


# Vietnamese names data
FIRST_NAMES = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Phan', 'Vũ', 'Võ', 'Đặng', 'Bùi']
MIDDLE_NAMES = ['Văn', 'Thị', 'Minh', 'Hữu', 'Đức', 'Anh', 'Thanh', 'Hoàng', 'Ngọc', 'Công']
LAST_NAMES_MALE = ['An', 'Bình', 'Cường', 'Dũng', 'Hùng', 'Khang', 'Long', 'Nam', 'Phong', 'Quân', 'Sơn', 'Tuấn', 'Vinh', 'Tú', 'Đạt']
LAST_NAMES_FEMALE = ['Anh', 'Chi', 'Hoa', 'Lan', 'Mai', 'Nga', 'Phương', 'Thu', 'Trang', 'Uyên', 'Vân', 'Xuân', 'Yến', 'Linh', 'Hương']
LAST_NAMES_CHILDREN_MALE = ['An', 'Bảo', 'Duy', 'Khang', 'Minh', 'Nam', 'Phúc', 'Quân', 'Tài', 'Tuấn', 'Vũ', 'Khôi', 'Đạt', 'Hưng', 'Long']
LAST_NAMES_CHILDREN_FEMALE = ['An', 'Anh', 'Chi', 'Hà', 'Khánh', 'Linh', 'My', 'Ngọc', 'Phương', 'Quỳnh', 'Trang', 'Uyên', 'Vi', 'Vy', 'Yến']

DISTRICTS = ['Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 7', 'Quận 10', 'Bình Thạnh', 'Tân Bình', 'Phú Nhuận']
STREETS = ['Lê Lợi', 'Nguyễn Huệ', 'Trần Hưng Đạo', 'Hai Bà Trưng', 'Võ Văn Tần', 'Pasteur', 'Cách Mạng Tháng 8', 'Điện Biên Phủ', 'Phan Xích Long', 'Hoàng Văn Thụ']

OCCUPATIONS = ['Giáo viên', 'Kỹ sư', 'Bác sĩ', 'Kinh doanh', 'Nhân viên văn phòng']
RELATIONSHIPS = ['Bố', 'Mẹ']


def generate_vietnamese_name(gender='male', for_child=False):
    """Generate random Vietnamese name"""
    first = random.choice(FIRST_NAMES)
    middle = random.choice(MIDDLE_NAMES)
    
    if for_child:
        last = random.choice(LAST_NAMES_CHILDREN_MALE if gender == 'male' else LAST_NAMES_CHILDREN_FEMALE)
    else:
        last = random.choice(LAST_NAMES_MALE if gender == 'male' else LAST_NAMES_FEMALE)
    
    return f"{first} {middle} {last}"


def generate_address():
    """Generate random address in HCM"""
    number = random.randint(1, 999)
    street = random.choice(STREETS)
    district = random.choice(DISTRICTS)
    return f"Số {number}, Đường {street}, {district}, TP. HCM"


def generate_random_date(start_year, end_year):
    """Generate random date between years"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def seed_settings():
    """Seed system settings"""
    print("\n1️⃣  Seeding Settings...")
    
    settings_data = [
        {
            'setting_key': 'tuition_fee_monthly',
            'setting_value': '1500000',
            'description': 'Học phí tháng (VNĐ)',
            'data_type': 'float'
        },
        {
            'setting_key': 'meal_price_daily',
            'setting_value': '25000',
            'description': 'Giá tiền ăn/ngày (VNĐ)',
            'data_type': 'float'
        },
        {
            'setting_key': 'default_classroom_capacity',
            'setting_value': '25',
            'description': 'Sức chứa lớp',
            'data_type': 'integer'
        }
    ]
    
    for data in settings_data:
        existing = Setting.query.filter_by(setting_key=data['setting_key']).first()
        if not existing:
            setting = Setting(**data)
            db.session.add(setting)
    
    db.session.commit()
    print("✅ Created settings")


def seed_teachers():
    """Seed 5 teachers"""
    print("\n2️⃣  Seeding Teachers...")
    
    teachers_data = [
        ('teacher1@kindergarten.com', 'Nguyễn Thị Hoa', 'GV001', '0901234561'),
        ('teacher2@kindergarten.com', 'Trần Văn An', 'GV002', '0901234562'),
        ('teacher3@kindergarten.com', 'Lê Thị Mai', 'GV003', '0901234563'),
        ('teacher4@kindergarten.com', 'Phạm Minh Tuấn', 'GV004', '0901234564'),
        ('teacher5@kindergarten.com', 'Hoàng Thị Lan', 'GV005', '0901234565'),
    ]
    
    teachers = []
    
    for email, full_name, employee_id, phone in teachers_data:
        # Check if teacher already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            teachers.append(existing_user.teacher_profile)
            continue
        
        # Create user account
        user = User(
            email=email,
            full_name=full_name,
            phone=phone,
            role=UserRole.TEACHER,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.flush()  # Get user.id
        
        # Create teacher profile
        teacher = Teacher(
            user_id=user.id,
            employee_id=employee_id,
            qualification=random.choice(['Cử nhân Sư phạm Mầm non', 'Thạc sĩ Sư phạm Mầm non'])
        )
        db.session.add(teacher)
        teachers.append(teacher)
    
    db.session.commit()
    print(f"✅ Created {len(teachers)} teachers")
    return teachers


def seed_parents():
    """Seed 20 parents"""
    print("\n3️⃣  Seeding Parents...")
    
    parents = []
    
    for i in range(1, 21):
        email = f"parent{i}@example.com"
        
        # Check if parent already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            parents.append(existing_user.parent_profile)
            continue
        
        # Generate random data
        relationship = random.choice(RELATIONSHIPS)
        gender = 'male' if relationship == 'Bố' else 'female'
        full_name = generate_vietnamese_name(gender)
        
        # Create user account
        user = User(
            email=email,
            full_name=full_name,
            phone=f"090123{i:02d}",
            role=UserRole.PARENT,
            is_active=True
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.flush()  # Get user.id
        
        # Create parent profile
        parent = Parent(
            user_id=user.id,
            address=generate_address(),
            emergency_contact=f"091234{i:02d}",
            relationship=relationship,
            occupation=random.choice(OCCUPATIONS)
        )
        db.session.add(parent)
        parents.append(parent)
    
    db.session.commit()
    print(f"✅ Created {len(parents)} parents")
    return parents


def seed_classrooms(teachers):
    """Seed 5 classrooms"""
    print("\n4️⃣  Seeding Classrooms...")
    
    classrooms_data = [
        ('Lớp Chồi', 'P101'),
        ('Lớp Lá', 'P102'),
        ('Lớp Búp', 'P103'),
        ('Lớp Hoa', 'P104'),
        ('Lớp Trái', 'P105'),
    ]
    
    classrooms = []
    
    for idx, (name, room_number) in enumerate(classrooms_data):
        # Check if classroom already exists
        existing = Classroom.query.filter_by(name=name, school_year='2024-2025').first()
        if existing:
            classrooms.append(existing)
            continue
        
        teacher = teachers[idx % len(teachers)]
        
        classroom = Classroom(
            name=name,
            school_year='2024-2025',
            capacity=25,
            room_number=room_number,
            teacher_id=teacher.id
        )
        db.session.add(classroom)
        classrooms.append(classroom)
    
    db.session.commit()
    print(f"✅ Created {len(classrooms)} classrooms")
    return classrooms


def seed_students(parents, classrooms):
    """Seed 50 students"""
    print("\n5️⃣  Seeding Students...")
    
    # Count existing students to avoid duplicates
    existing_count = Student.query.count()
    students = []
    
    for i in range(50):
        gender = random.choice(['Nam', 'Nữ'])
        full_name = generate_vietnamese_name('male' if gender == 'Nam' else 'female', for_child=True)
        date_of_birth = generate_random_date(2018, 2021)
        
        # Generate birth certificate number
        year = date_of_birth.year
        birth_cert = f"GKS{year}{(existing_count + i + 1):05d}"
        
        # Check if student with this birth certificate already exists
        existing_student = Student.query.filter_by(birth_certificate_number=birth_cert).first()
        if existing_student:
            students.append(existing_student)
            continue
        
        parent = random.choice(parents)
        classroom = random.choice(classrooms)
        
        student = Student(
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            birth_certificate_number=birth_cert,
            parent_id=parent.id,
            classroom_id=classroom.id,
            enrollment_date=date(2024, 9, 1),
            is_active=True
        )
        db.session.add(student)
        students.append(student)
    
    db.session.commit()
    print(f"✅ Created {len(students)} students")
    return students


def main():
    """Main function to run seed script"""
    app = create_app()
    
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        
        print("=" * 62)
        print("  KINDERGARTEN MANAGEMENT - SEED DATA SCRIPT")
        print("=" * 62)
        print()
        
        # Check if data already exists
        teacher_count = Teacher.query.count()
        parent_count = Parent.query.count()
        student_count = Student.query.count()
        
        if teacher_count > 0 or parent_count > 0 or student_count > 0:
            print("⚠️  WARNING: Data already exists in the database!")
            print(f"   Teachers:  {teacher_count}")
            print(f"   Parents:   {parent_count}")
            print(f"   Students:  {student_count}")
            print()
            print("   Existing data will be skipped, but new students may be added.")
            print()
        
        # Confirmation prompt
        choice = input("⚠️  This will create sample data. Continue? (y/N): ").strip().lower()
        if choice != 'y':
            print("\n❌ Cancelled.")
            return
        
        print("\n🚀 Starting seed process...")
        
        try:
            # Seed data in order
            seed_settings()
            teachers = seed_teachers()
            parents = seed_parents()
            classrooms = seed_classrooms(teachers)
            students = seed_students(parents, classrooms)
            
            # Print summary
            print()
            print("=" * 62)
            print("  ✅ SEED COMPLETED!")
            print("=" * 62)
            print(f"  📊 Teachers:    {len(teachers)}")
            print(f"  👪 Parents:     {len(parents)}")
            print(f"  🏫 Classrooms:  {len(classrooms)}")
            print(f"  🎓 Students:    {len(students)}")
            print("=" * 62)
            print()
            print("💡 Login credentials:")
            print("  Teachers: teacher1@kindergarten.com / 123456")
            print("  Parents:  parent1@example.com / 123456")
            print()
            
        except Exception as e:
            db.session.rollback()
            print()
            print(f"❌ ERROR: Failed to seed data!")
            print(f"   {str(e)}")
            print()
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

#run: python scripts/seed_admin.py

# admin@gmail.vn 123456

import sys
import os


sys.path. insert(0, os.path. abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import User, UserRole


def seed_admin():

    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("  KINDERGARTEN MANAGEMENT - ADMIN SEED SCRIPT")
        print("=" * 60)
        print()
        

        existing_admin = User.query.filter_by(role=UserRole.ADMIN).first()
        
        if existing_admin:
            print("⚠️  ADMIN ALREADY EXISTS!")
            print(f"   Email: {existing_admin.email}")
            print(f"   Name: {existing_admin.full_name}")
            print(f"   Created: {existing_admin.created_at}")
            print()
            
            choice = input("Do you want to create another admin? (y/N): ").strip().lower()
            if choice != 'y':
                print("\n✅ Exiting...")
                return
            print()
        

        print("📝 Enter Admin Information:")
        print("-" * 60)
        
        while True:
            email = input("Email: ").strip()
            if not email: 
                print("❌ Email cannot be empty!")
                continue
            

            if User.query.filter_by(email=email).first():
                print(f"❌ Email '{email}' already exists!")
                continue
            
            break
        
        while True:
            password = input("Password (min 6 characters): ").strip()
            if len(password) < 6:
                print("❌ Password must be at least 6 characters!")
                continue
            break
        
        while True: 
            full_name = input("Full Name:  ").strip()
            if not full_name:
                print("❌ Full name cannot be empty!")
                continue
            break
        
        phone = input("Phone (optional): ").strip() or None
        
        print()
        print("=" * 60)
        print("  CONFIRM ADMIN INFORMATION")
        print("=" * 60)
        print(f"Email:      {email}")
        print(f"Password:  {'*' * len(password)}")
        print(f"Full Name:  {full_name}")
        print(f"Phone:     {phone or 'N/A'}")
        print(f"Role:      ADMIN")
        print("=" * 60)
        print()
        
        confirm = input("Create this admin account? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("\n❌ Cancelled.")
            return
        
        try:
            admin = User(
                email=email,
                full_name=full_name,
                role=UserRole.ADMIN,
                phone=phone,
                is_active=True
            )
            admin.set_password(password)
            
            db.session.add(admin)
            db.session.commit()
            
            print()
            print("=" * 60)
            print("  ✅ ADMIN CREATED SUCCESSFULLY!")
            print("=" * 60)
            print(f"ID:         {admin.id}")
            print(f"Email:     {admin.email}")
            print(f"Full Name: {admin. full_name}")
            print(f"Role:      {admin.role. value}")
            print(f"Created:   {admin.created_at}")
            print("=" * 60)
            print()
            print("🔐 You can now login with these credentials:")
            print(f"   POST http://127.0.0.1:5000/api/auth/login")
            print(f"   Body: {{'email': '{email}', 'password': '***'}}")
            print()
            
        except Exception as e:
            db.session.rollback()
            print()
            print(f"❌ ERROR: Failed to create admin!")
            print(f"   {str(e)}")
            print()


if __name__ == '__main__':
    try:
        seed_admin()
    except KeyboardInterrupt: 
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
# kindergarten-management
Hệ thống quản lý trường mầm non

## Setup

1. Clone repository
```bash
git clone https://github.com/nhatthien88/kindergarten-management.git
cd kindergarten-management

2. Activate venv
.\venv\Scripts\Activate.ps1

3.Install dependencies
pip install -r requirements.txt

4. Create . env file
cp .env.example .env(doi secret va DATABASE_URL cua .env.example di)


5. khoi tao migration
flask db init

6. tao migration file
flask db migrate -m "tao database schema voi 11 model"

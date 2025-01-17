from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # 检查管理员是否已存在
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print("Admin already exists!")
            return
        
        # 创建新管理员
        admin = User(
            email='admin@example.com',
            name='Admin',
            is_admin=True
        )
        admin.set_password('admin123')  # 设置默认密码
        
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully!")

if __name__ == '__main__':
    create_admin() 
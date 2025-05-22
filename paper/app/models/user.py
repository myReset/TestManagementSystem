from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager, bcrypt

class User(db.Model, UserMixin):
    """教师信息表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(20), unique=True, nullable=False, comment='工号')
    name = db.Column(db.String(50), nullable=False, comment='员工姓名')
    gender = db.Column(db.String(10), nullable=False, comment='性别')
    department = db.Column(db.String(50), nullable=False, comment='所在教研室')
    position = db.Column(db.String(50), nullable=False, comment='职务')
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='teacher', comment='权限角色：admin/teacher')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    papers = db.relationship('Paper', backref='teacher', lazy='dynamic')
    borrowings = db.relationship('Borrowing', backref='borrower', lazy='dynamic')

    @property
    def password(self):
        """禁止访问密码属性"""
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        """设置密码"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """验证密码"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        """是否为管理员"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.name}>'


@login_manager.user_loader
def load_user(user_id):
    """加载用户的回调函数"""
    return User.query.get(int(user_id)) 
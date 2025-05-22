#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User

# 加载环境变量
load_dotenv()

# 创建Flask应用上下文
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app_ctx = app.app_context()
app_ctx.push()

def init_db():
    """初始化数据库"""
    # 创建所有表
    db.create_all()
    
    # 删除可能存在的管理员和教师账户以确保密码哈希正确
    existing_admin = User.query.filter_by(staff_id='admin').first()
    if existing_admin:
        db.session.delete(existing_admin)
        print('已删除现有管理员账户，将重新创建...')
    
    existing_teacher = User.query.filter_by(staff_id='teacher').first()
    if existing_teacher:
        db.session.delete(existing_teacher)
        print('已删除现有教师账户，将重新创建...')
    
    db.session.commit()
    
    # 创建管理员账户
    print('创建管理员账户...')
    admin = User(
        staff_id='admin',
        name='管理员',
        gender='男',
        department='系统管理',
        position='管理员',
        role='admin'
    )
    admin.password = 'admin123'
    db.session.add(admin)
    
    # 添加测试教师账户
    teacher = User(
        staff_id='teacher',
        name='测试教师',
        gender='女',
        department='计算机科学与技术',
        position='讲师',
        role='teacher'
    )
    teacher.password = 'teacher123'
    db.session.add(teacher)
    
    db.session.commit()
    print('初始用户创建成功!')

if __name__ == '__main__':
    try:
        init_db()
        print('数据库初始化成功!')
    except Exception as e:
        print(f'初始化数据库时出错: {e}')
    finally:
        app_ctx.pop() 
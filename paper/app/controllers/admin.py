from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.forms import UserForm
from app.utils.permissions import admin_required

# 创建蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def index():
    """管理员首页"""
    users = User.query.all()
    return render_template('admin/index.html', users=users)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """用户列表"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """新建用户"""
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            staff_id=form.staff_id.data,
            name=form.name.data,
            gender=form.gender.data,
            department=form.department.data,
            position=form.position.data,
            role=form.role.data
        )
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, title='新建用户')


@admin_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    """编辑用户"""
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.staff_id = form.staff_id.data
        user.name = form.name.data
        user.gender = form.gender.data
        user.department = form.department.data
        user.position = form.position.data
        user.role = form.role.data
        
        if form.password.data:
            user.password = form.password.data
            
        db.session.commit()
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, user=user, title='编辑用户')


@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    """删除用户"""
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('不能删除自己的账户', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users')) 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from app import db
from app.models.forms import LoginForm
from app.models.user import User

# 创建蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录视图"""
    if current_user.is_authenticated:
        return redirect(url_for('paper.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(staff_id=form.staff_id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # 通知Principal用户身份已改变
            identity_changed.send(
                request.application, identity=Identity(user.id)
            )
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('paper.index')
            return redirect(next_page)
        flash('无效的工号或密码', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """登出视图"""
    logout_user()
    # 通知Principal用户身份已改变
    identity_changed.send(
        request.application, identity=AnonymousIdentity()
    )
    flash('您已成功登出', 'info')
    return redirect(url_for('auth.login')) 
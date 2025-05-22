from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user
from flask_principal import Permission, RoleNeed


# 定义权限
admin_permission = Permission(RoleNeed('admin'))


def admin_required(f):
    """检查是否为管理员的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function 
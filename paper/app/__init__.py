import os
import redis
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_principal import Principal

from config import config

# 创建扩展实例，但不初始化
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
principal = Principal()

def create_app(config_name=None):
    """创建Flask应用实例"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    principal.init_app(app)

    # 配置登录视图
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'warning'

    # 创建Redis连接
    app.redis = redis.from_url(app.config['REDIS_URL'])

    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 添加上下文处理器，提供now变量给所有模板
    @app.context_processor
    def inject_now():
        return {'now': datetime.datetime.now()}

    # 注册蓝图
    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp
    from app.controllers.paper import paper_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(paper_bp)

    # 注册错误处理器
    from app.controllers.errors import register_error_handlers
    register_error_handlers(app)

    return app 
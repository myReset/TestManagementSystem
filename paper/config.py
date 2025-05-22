import os
from datetime import timedelta

class Config:
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:591121@localhost:3308/paper_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis配置
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 上传文件配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf'}


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/paper_management_test'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # 在生产环境中，应该使用环境变量设置SECRET_KEY和DATABASE_URL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 
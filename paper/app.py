import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Paper, Borrowing
from flask.cli import FlaskGroup

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli = FlaskGroup(app)

@app.shell_context_processor
def make_shell_context():
    """为Flask shell创建上下文"""
    return dict(app=app, db=db, User=User, Paper=Paper, Borrowing=Borrowing)

if __name__ == '__main__':
    cli() 
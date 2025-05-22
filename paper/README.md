# 试卷管理系统

试卷管理系统是一个基于Flask的Web应用，用于管理和归档试卷。系统提供了试卷管理、借阅、归还以及统计分析等功能。


## 页面预览
### 首页
![img.png](img.png)

### 试卷管理
![img_1.png](img_1.png)

### 试卷借阅
![img_2.png](img_2.png)

### 试卷归还
![img_3.png](img_3.png)

### 借阅记录
![img_4.png](img_4.png)

### 统计分析
![img_5.png](img_5.png)

### 用户管理
![img_6.png](img_6.png)
## 功能特点

- 用户认证：管理员和教师角色，基于Flask-Login和Flask-Principal实现
- 试卷管理：提交、编辑、删除试卷
- 试卷归档：支持纸质试卷存储位置记录和PDF文件上传
- 试卷借阅与归还：教师可以借阅和归还试卷
- 统计分析：以可视化方式展示试卷归档状态和每月归档数量
- 响应式界面：基于Bootstrap 5构建的现代化界面

## 技术栈

- 后端：Python 3.8 + Flask 2.2.3
- 数据库：MariaDB（使用SQLAlchemy ORM）
- 缓存：Redis
- 前端：Bootstrap 5 + FontAwesome + jQuery
- 可视化：Matplotlib
- 认证：Flask-Login + Flask-Principal + Flask-Bcrypt
- 部署：支持Docker部署

## 数据库设计

系统使用MariaDB数据库，包含以下主要表：

1. users（教师信息表）：存储教师和管理员信息
2. papers（试卷信息表）：存储试卷的基本信息
3. borrowings（借阅记录表）：记录试卷借阅和归还情况

详细的数据库设计请查看 [database/README.md](database/README.md) 文件。

## 安装与运行

### 前提条件

- Python 3.8或更高版本
- MariaDB / MySQL
- Redis
- 可选：用于生成PDF缩略图的工具包（如wkhtmltopdf）

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/paper-management-system.git
cd paper-management-system
```

2. 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 初始化数据库

```bash
# Windows
cd database
install.bat

# Linux/Mac
cd database
chmod +x install.sh
./install.sh
```

或者手动创建数据库：

```sql
CREATE DATABASE paper_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后导入SQL文件：

```bash
mysql -u username -p paper_management < database/paper_management.sql
mysql -u username -p paper_management < database/init_data.sql
```

5. 创建环境变量文件

创建一个名为`.env`的文件，包含以下内容：

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/paper_management
REDIS_URL=redis://localhost:6379/0
```

6. 初始化Flask应用

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

7. 创建初始管理员账户（如果没有使用初始数据）

```bash
python init_db.py
```

8. 运行应用

```bash
python run.py
```

现在，应用应该正在运行于 http://127.0.0.1:5000/

## 项目结构

```
paper-management-system/
├── app/                      # 应用主目录
│   ├── controllers/          # 控制器（视图函数）
│   ├── models/               # 数据模型
│   ├── static/               # 静态文件（CSS、JS、图片等）
│   ├── templates/            # HTML模板
│   ├── utils/                # 工具函数和辅助模块
│   └── __init__.py           # 应用工厂
├── database/                 # 数据库相关文件
│   ├── paper_management.sql  # 数据库结构
│   ├── init_data.sql         # 示例数据
│   ├── install.bat           # Windows安装脚本
│   ├── install.sh            # Linux/Mac安装脚本
│   └── README.md             # 数据库说明
├── migrations/               # 数据库迁移文件
├── .env                      # 环境变量（不应提交到版本控制）
├── app.py                    # 应用入口点
├── config.py                 # 配置文件
├── init_db.py                # 数据库初始化脚本
├── run.py                    # 运行脚本
└── requirements.txt          # 项目依赖
```

## 数据库表结构

系统包含三个主要数据表：

1. 教师信息表（users）：存储教师信息，包括工号、姓名、性别、教研室、职务等
2. 试卷信息表（papers）：存储试卷信息，包括学期、课程名称、班级、考试类型等
3. 借阅信息表（borrowings）：记录试卷借阅和归还信息

## 使用示例

1. 登录系统（使用教师工号和密码）
2. 在首页查看试卷统计和最近操作
3. 通过"提交试卷"功能提交新试卷
4. 使用"试卷管理"功能查看和管理试卷
5. 使用"借阅试卷"和"归还试卷"功能操作试卷借阅和归还
6. 通过"统计分析"功能查看试卷归档情况

## 默认账户信息

安装示例数据后，系统会自动创建以下账户：

- 管理员：admin（需要在应用中设置密码）
- 教师：teacher1, teacher2, teacher3, teacher4（需要在应用中设置密码）

## 许可证

本项目基于MIT许可证。详见LICENSE文件。 
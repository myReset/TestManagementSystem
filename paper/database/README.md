# 数据库设计说明

本项目使用MariaDB作为关系型数据库，以下是数据库的设计说明。

## 数据库表结构

### 1. users（教师信息表）

存储系统用户信息，包括教师和管理员。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| id | INT | 主键，自增 |
| staff_id | VARCHAR(20) | 工号，唯一索引 |
| name | VARCHAR(50) | 员工姓名 |
| gender | VARCHAR(10) | 性别 |
| department | VARCHAR(50) | 所在教研室 |
| position | VARCHAR(50) | 职务 |
| password_hash | VARCHAR(128) | 密码哈希值 |
| role | VARCHAR(20) | 角色：admin/teacher，默认teacher |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 2. papers（试卷信息表）

存储试卷的基本信息。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| id | INT | 主键，自增 |
| semester | VARCHAR(20) | 所属学期 |
| course_name | VARCHAR(100) | 课程名称 |
| class_name | VARCHAR(50) | 班级 |
| count | INT | 份数 |
| exam_type | VARCHAR(20) | 考试类型：考试/考查 |
| storage_location | VARCHAR(100) | 试卷存储位置，可为NULL |
| pdf_path | VARCHAR(255) | PDF文件路径，可为NULL |
| archived | BOOLEAN | 是否已归档，默认FALSE |
| archive_date | DATETIME | 归档日期，可为NULL |
| teacher_id | INT | 关联教师ID，外键 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 3. borrowings（借阅记录表）

记录试卷的借阅和归还情况。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| id | INT | 主键，自增 |
| paper_id | INT | 关联试卷ID，外键 |
| borrower_id | INT | 借阅人ID，外键 |
| borrow_date | DATETIME | 借阅日期 |
| return_date | DATETIME | 归还日期，可为NULL |
| status | VARCHAR(20) | 状态：borrowed/returned |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 视图设计

### 1. monthly_archive_stats（按月归档统计）

按月统计归档的试卷数量。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| month | VARCHAR | 月份（格式：YYYY-MM） |
| archive_count | INT | 归档数量 |

### 2. exam_type_stats（考试类型统计）

统计不同考试类型的试卷数量。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| exam_type | VARCHAR(20) | 考试类型 |
| paper_count | INT | 试卷数量 |

### 3. teacher_archive_stats（按教师归档统计）

按教师统计试卷的归档情况。

| 字段名 | 类型 | 说明 |
|-------|------|------|
| teacher_id | INT | 教师ID |
| teacher_name | VARCHAR(50) | 教师姓名 |
| total_papers | INT | 总试卷数 |
| archived_papers | INT | 已归档试卷数 |
| unarchived_papers | INT | 未归档试卷数 |

## 索引设计

为了提高查询性能，在以下字段上建立了索引：

1. users表：staff_id, role
2. papers表：semester, course_name, class_name, archived, teacher_id
3. borrowings表：paper_id, borrower_id, status

## 外键关系

1. papers.teacher_id -> users.id：试卷关联到教师
2. borrowings.paper_id -> papers.id：借阅记录关联到试卷
3. borrowings.borrower_id -> users.id：借阅记录关联到借阅人

## 初始化数据

数据库初始化时，会自动创建以下用户：

1. 管理员账户：
   - 工号：admin
   - 姓名：管理员
   - 角色：admin

2. 测试教师账户：
   - 工号：teacher
   - 姓名：测试教师
   - 角色：teacher

> 注意：实际密码需要通过应用程序中的bcrypt工具生成哈希值。 
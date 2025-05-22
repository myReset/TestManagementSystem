-- 创建数据库
CREATE DATABASE IF NOT EXISTS paper_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE paper_management;

-- 创建用户（教师）表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(20) NOT NULL UNIQUE COMMENT '工号',
    name VARCHAR(50) NOT NULL COMMENT '员工姓名',
    gender VARCHAR(10) NOT NULL COMMENT '性别',
    department VARCHAR(50) NOT NULL COMMENT '所在教研室',
    position VARCHAR(50) NOT NULL COMMENT '职务',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希',
    role VARCHAR(20) NOT NULL DEFAULT 'teacher' COMMENT '权限角色：admin/teacher',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_staff_id (staff_id),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教师信息表';

-- 创建试卷表
CREATE TABLE IF NOT EXISTS papers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    semester VARCHAR(20) NOT NULL COMMENT '所属学期',
    course_name VARCHAR(100) NOT NULL COMMENT '试卷名称/课程名称',
    class_name VARCHAR(50) NOT NULL COMMENT '班级',
    count INT NOT NULL COMMENT '份数',
    exam_type VARCHAR(20) NOT NULL COMMENT '考试或考查',
    storage_location VARCHAR(100) NULL COMMENT '纸质试卷储存位置',
    pdf_path VARCHAR(255) NULL COMMENT 'PDF文件路径',
    archived BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否已归档',
    archive_date DATETIME NULL COMMENT '归档日期',
    teacher_id INT NOT NULL COMMENT '关联教师ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_semester (semester),
    INDEX idx_course_name (course_name),
    INDEX idx_class_name (class_name),
    INDEX idx_archived (archived),
    INDEX idx_teacher_id (teacher_id),
    CONSTRAINT fk_papers_teacher FOREIGN KEY (teacher_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试卷信息表';

-- 创建借阅表
CREATE TABLE IF NOT EXISTS borrowings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL COMMENT '关联试卷ID',
    borrower_id INT NOT NULL COMMENT '借阅人ID',
    borrow_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '借阅日期',
    return_date DATETIME NULL COMMENT '归还日期',
    status VARCHAR(20) NOT NULL DEFAULT 'borrowed' COMMENT '状态：borrowed/returned',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_paper_id (paper_id),
    INDEX idx_borrower_id (borrower_id),
    INDEX idx_status (status),
    CONSTRAINT fk_borrowings_paper FOREIGN KEY (paper_id) REFERENCES papers (id) ON DELETE CASCADE,
    CONSTRAINT fk_borrowings_borrower FOREIGN KEY (borrower_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试卷借阅表';

-- 初始数据：添加管理员用户（密码需要在应用中通过bcrypt生成）
-- 注意：这里的密码哈希值只是示例，实际应用中应该通过应用程序生成
INSERT INTO users (staff_id, name, gender, department, position, password_hash, role) 
VALUES ('admin', '管理员', '男', '系统管理', '管理员', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'admin');

-- 初始数据：添加测试教师
INSERT INTO users (staff_id, name, gender, department, position, password_hash, role) 
VALUES ('teacher', '测试教师', '女', '计算机科学与技术', '讲师', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'teacher');

-- 创建统计视图：按月份归档试卷统计
CREATE OR REPLACE VIEW monthly_archive_stats AS
SELECT 
    DATE_FORMAT(archive_date, '%Y-%m') AS month,
    COUNT(*) AS archive_count
FROM 
    papers
WHERE 
    archived = TRUE AND archive_date IS NOT NULL
GROUP BY 
    DATE_FORMAT(archive_date, '%Y-%m')
ORDER BY 
    month;

-- 创建统计视图：考试类型统计
CREATE OR REPLACE VIEW exam_type_stats AS
SELECT 
    exam_type,
    COUNT(*) AS paper_count
FROM 
    papers
GROUP BY 
    exam_type;

-- 创建统计视图：按教师归档统计
CREATE OR REPLACE VIEW teacher_archive_stats AS
SELECT 
    u.id AS teacher_id,
    u.name AS teacher_name,
    COUNT(p.id) AS total_papers,
    SUM(CASE WHEN p.archived = TRUE THEN 1 ELSE 0 END) AS archived_papers,
    SUM(CASE WHEN p.archived = FALSE THEN 1 ELSE 0 END) AS unarchived_papers
FROM 
    users u
LEFT JOIN 
    papers p ON u.id = p.teacher_id
GROUP BY 
    u.id, u.name; 
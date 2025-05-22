-- 使用数据库
USE paper_management;

-- 清空现有数据（谨慎使用）
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE borrowings;
-- TRUNCATE TABLE papers;
-- TRUNCATE TABLE users;
-- SET FOREIGN_KEY_CHECKS = 1;

-- 添加用户数据
INSERT INTO users (staff_id, name, gender, department, position, password_hash, role) VALUES
('admin', '管理员', '男', '系统管理', '管理员', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'admin'),
('teacher1', '张三', '男', '计算机科学与技术', '教授', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'teacher'),
('teacher2', '李四', '女', '软件工程', '副教授', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'teacher'),
('teacher3', '王五', '男', '信息安全', '讲师', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'teacher'),
('teacher4', '赵六', '女', '人工智能', '助教', '$2b$12$example_hash_here_would_be_replaced_by_actual_hash', 'teacher');

-- 添加试卷数据
INSERT INTO papers (semester, course_name, class_name, count, exam_type, storage_location, pdf_path, archived, archive_date, teacher_id) VALUES
('2023-2024-1', 'Python程序设计', '计算机2301', 50, '考试', 'A区-01柜', 'uploads/python_2301_20231220.pdf', TRUE, '2023-12-20 10:30:00', 2),
('2023-2024-1', 'Java程序设计', '软件2302', 45, '考试', 'A区-02柜', 'uploads/java_2302_20231221.pdf', TRUE, '2023-12-21 14:20:00', 2),
('2023-2024-1', '数据结构', '计算机2301', 50, '考试', 'B区-01柜', 'uploads/datastructure_2301_20231222.pdf', TRUE, '2023-12-22 09:15:00', 3),
('2023-2024-1', '操作系统', '软件2301', 48, '考试', 'B区-02柜', 'uploads/os_2301_20231223.pdf', TRUE, '2023-12-23 16:40:00', 3),
('2023-2024-1', '计算机网络', '网络2301', 42, '考查', 'C区-01柜', 'uploads/network_2301_20231224.pdf', TRUE, '2023-12-24 11:10:00', 4),
('2023-2024-1', '软件工程', '软件2301', 46, '考查', 'C区-02柜', 'uploads/se_2301_20231225.pdf', TRUE, '2023-12-25 13:50:00', 4),
('2023-2024-1', '高等数学', '计算机2302', 52, '考试', 'D区-01柜', 'uploads/math_2302_20231226.pdf', TRUE, '2023-12-26 10:00:00', 5),
('2023-2024-1', '线性代数', '软件2302', 44, '考试', 'D区-02柜', NULL, TRUE, '2023-12-27 15:30:00', 5),
('2023-2024-2', 'C++程序设计', '计算机2301', 50, '考试', 'A区-03柜', NULL, TRUE, '2024-05-20 09:00:00', 2),
('2023-2024-2', '数据库原理', '软件2301', 48, '考试', 'A区-04柜', NULL, FALSE, NULL, 2),
('2023-2024-2', '编译原理', '计算机2301', 50, '考试', NULL, NULL, FALSE, NULL, 3),
('2023-2024-2', '人工智能导论', '人工智能2301', 40, '考查', NULL, NULL, FALSE, NULL, 5);

-- 添加借阅数据
INSERT INTO borrowings (paper_id, borrower_id, borrow_date, return_date, status) VALUES
(1, 3, '2024-01-05 10:15:00', '2024-01-10 14:30:00', 'returned'),
(2, 4, '2024-01-08 09:20:00', '2024-01-12 16:40:00', 'returned'),
(3, 2, '2024-01-15 13:45:00', '2024-01-20 11:30:00', 'returned'),
(4, 5, '2024-02-01 10:00:00', '2024-02-05 15:20:00', 'returned'),
(5, 2, '2024-02-10 14:10:00', '2024-02-15 09:50:00', 'returned'),
(6, 3, '2024-03-01 11:30:00', '2024-03-05 16:45:00', 'returned'),
(7, 4, '2024-03-10 09:15:00', NULL, 'borrowed'),
(8, 5, '2024-03-15 13:40:00', NULL, 'borrowed'),
(9, 2, '2024-03-20 15:30:00', NULL, 'borrowed'); 
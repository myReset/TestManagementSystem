#!/bin/bash

echo "试卷管理系统数据库安装脚本"
echo "============================"

read -p "请输入MariaDB用户名（默认root）: " user
user=${user:-root}

read -s -p "请输入MariaDB密码: " pass
echo

echo
echo "正在创建数据库结构..."
mysql -u "$user" -p"$pass" < paper_management.sql

echo
echo "正在导入示例数据..."
mysql -u "$user" -p"$pass" < init_data.sql

echo
echo "数据库初始化完成！"
echo "默认管理员账号: admin"
echo "默认教师账号: teacher1, teacher2, teacher3, teacher4"
echo "密码: 请在应用程序中设置"

read -p "按回车键继续..." 
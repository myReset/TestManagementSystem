#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from app import create_app

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # 从环境变量获取主机和端口，如果不存在则使用默认值
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f'启动应用: http://{host}:{port}')
    print(f'调试模式: {"开启" if debug else "关闭"}')
    
    app.run(host=host, port=port, debug=debug) 
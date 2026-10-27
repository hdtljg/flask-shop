"""Windows / 内网部署启动脚本：用 Waitress 代替 Flask 自带的开发服务器。

用法：
    python serve.py
    # 或指定端口
    set PORT=8080 && python serve.py

环境变量：
    HOST     监听地址，默认 0.0.0.0（局域网可访问）
    PORT     监听端口，默认 8000
    THREADS  工作线程数，默认 8
"""
import os

from waitress import serve

from app import app


def main():
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '8000'))
    threads = int(os.environ.get('THREADS', '8'))

    print(' * Flask 服务已启动：http://%s:%s （Ctrl+C 停止）' % (host, port))
    print(' * 上传目录：%s' % app.config['UPLOAD_FOLDER'])
    serve(app, host=host, port=port, threads=threads, ident='flask-shop')


if __name__ == '__main__':
    main()

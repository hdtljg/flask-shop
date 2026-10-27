"""生产环境 WSGI 入口。

- Linux + Gunicorn：gunicorn -w 4 -b 127.0.0.1:8000 wsgi:application
- Windows + Waitress：python serve.py
- 其他平台（如 Azure App Service）也可以识别 application 变量
"""
from app import app
from werkzeug.middleware.proxy_fix import ProxyFix

# 仅当应用确实运行在 Nginx 等反向代理之后时才启用，
# 这样 request.remote_addr / url_for(_external=True) 才能拿到真实协议和 IP。
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

application = app

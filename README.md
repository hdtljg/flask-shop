# Flask 商城（校园特产）

一个基于 Flask + MySQL 的校园特产商城课程项目，包含商品展示、搜索、购物车、用户注册登录、个人中心和管理员后台。

## 技术栈

- Python 3.12 / Flask 3.1
- Flask-Login、Flask-SQLAlchemy
- MySQL 8 + PyMySQL
- 原生 HTML / CSS / JavaScript
- 部署：Waitress（Windows）、Gunicorn + Nginx + systemd（Linux）、Docker Compose

## 功能

- 首页商品列表、轮播图、商品详情
- 商品关键词搜索
- 用户注册、登录、退出
- 个人资料与头像上传、修改密码
- 购物车添加、删除、结算
- 管理员后台：商品增删改、用户管理
- 数据统计页面（ECharts）

## 本地运行

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# 编辑 .env，填写 DATABASE_URL 和 SECRET_KEY
.\.venv\Scripts\python.exe app.py
```

默认访问 <http://127.0.0.1:5000>。

> `app.py` 使用 Flask 开发服务器，只适合本地开发。

## Docker 部署

```powershell
Copy-Item .env.example .env
# 编辑 .env，至少修改 SECRET_KEY、MYSQL_ROOT_PASSWORD、MYSQL_PASSWORD
docker compose up -d --build
```

访问 <http://127.0.0.1:8000/login>。

仓库包含 `deploy/00-schema.sql`（表结构）和 `deploy/flask_data.sql`（演示数据），首次启动会自动建表并导入数据。完整部署步骤见 [DEPLOY.md](DEPLOY.md)。

创建管理员：

```powershell
docker compose exec web python deploy/create_admin.py --username admin
```

## 目录结构

```
app.py                 开发入口
wsgi.py                WSGI 入口（Gunicorn）
serve.py               Waitress 启动脚本
config.py              配置（支持 .env）
routes/                路由
controllers/           业务逻辑
models/                数据模型
templates/             Jinja2 模板
static/                静态资源
deploy/                部署脚本与配置
DEPLOY.md              部署指南
```

## 数据说明

仓库包含演示数据库 `deploy/flask_data.sql` 和示例图片。其中用户姓名、学号、手机号均为虚构，仅用于课程演示。

`.env` 不包含在仓库中（里面是数据库密码和 `SECRET_KEY`），克隆后请复制 `.env.example` 并修改。若要在真实环境使用，请替换演示数据，不要把真实用户信息提交到公开仓库。部署步骤见 [DEPLOY.md](DEPLOY.md)。

## License

仅用于课程学习与演示。

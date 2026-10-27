# Flask 商城项目部署指南

> 项目目录：`E:\python node\flask - 副本`
> 技术栈：Flask 3.1 + Flask-Login + Flask-SQLAlchemy + MySQL 8 + 原生 HTML/CSS/JS
> 已在本机验证：Python 3.12.5、MySQL 8.0.42、9 个商品、4 个用户

---

## 0. 先选部署方案

| 场景 | 推荐方案 | 启动方式 |
| --- | --- | --- |
| 本机演示、教室/宿舍局域网访问 | A. Windows + Waitress | `deploy\start_windows.ps1` |
| 有公网 Linux 云服务器（阿里云/腾讯云等） | B. Gunicorn + Nginx + systemd | `systemctl start flask-shop` |
| 有 Docker，希望环境可复现 | C. Docker Compose | `docker compose up -d --build` |

三种方案使用同一份代码和同一个数据库导出文件 `deploy/flask_data.sql`。

---

## 1. 部署到底在部署什么

一个 Flask 项目上线，不只是“把代码放到服务器上”，而是四件事：

```
浏览器
  │
  ▼
Nginx（80/443，处理 HTTPS、静态文件、反向代理）
  │
  ▼
Gunicorn / Waitress（WSGI 服务器，运行 Flask 应用，127.0.0.1:8000）
  │
  ├── MySQL 8（业务数据：users / goods / cart / user_info）
  └── static/img/upload（用户上传的图片，必须持久化并备份）
```

对应到本项目：

1. **代码**：`app.py`、`routes/`、`controllers/`、`models/`、`templates/`、`static/`。
2. **数据库**：MySQL 库 `flask_data`，表结构和初始数据在 `deploy/flask_data.sql`。
3. **上传目录**：`static/img/upload/`，数据库里只存文件名，**文件丢了图片就会 404**。
4. **配置**：`.env` 中的 `SECRET_KEY`、`DATABASE_URL`，不要硬编码在代码里。

> 为什么不能直接 `python app.py` 对外提供服务？
> `app.py` 里是 `app.run(debug=True)`，用的是 Flask 自带的开发服务器：单进程、性能低、调试器可能泄露源码，**只能本机开发用**。生产必须换成 Waitress（Windows）或 Gunicorn（Linux），并用 Nginx 挡在前面。

---

## 2. 三种方案共同的准备

### 2.1 安装依赖

```powershell
Set-Location "E:\python node\flask - 副本"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

新机器上没有 `.venv` 时先创建：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` 已包含：Flask、Flask-Login、Flask-SQLAlchemy、SQLAlchemy、PyMySQL、Werkzeug、Waitress、python-dotenv、cryptography（连接 MySQL 8 默认认证方式时需要）。

### 2.2 准备数据库

本项目**不会自动建表**，必须导入 `deploy/flask_data.sql`（结构 + 初始数据），或者连接一个已经存在的 `flask_data` 库。

> 如果是刚从 GitHub 克隆的仓库：`deploy/flask_data.sql` 出于隐私原因不在仓库里，可先执行 `deploy/00-schema.sql` 创建空表，再用 `deploy/create_admin.py` 创建管理员。

在 Windows 上导入：

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" `
  -uroot -p --default-character-set=utf8mb4 `
  -e "source deploy/flask_data.sql"
```

> ⚠️ 这个 SQL 文件里包含 `DROP TABLE`，会覆盖目标库中同名的表。**不要**在没有备份的生产库上直接执行。

导入后验证：

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -uroot -p `
  -e "USE flask_data; SELECT COUNT(*) AS goods FROM goods; SELECT COUNT(*) AS users FROM users;"
```

### 2.3 复制上传图片

数据库迁移过去之后，还要把图片文件一起复制：

- `static/img/upload/`：用户头像、后台上传的商品图。
- `static/img/`：项目自带的商品图和轮播图，例如 `北流凉亭鸡.webp`。

Linux 上复制后要改权限（见方案 B）。Windows 上直接用资源管理器或 `scp` 复制即可。

### 2.4 配置 `.env`

```powershell
Copy-Item .env.example .env
notepad .env
```

至少修改：

```dotenv
SECRET_KEY=用随机字符串替换
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/flask_data?charset=utf8mb4
```

生成随机 `SECRET_KEY`：

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

> `SECRET_KEY` 用来签名登录 session。用默认值上线，别人可以伪造管理员登录。
>
> 一般不要改 `UPLOAD_FOLDER`。如果改成外部目录，Nginx 必须额外把 `/static/img/upload/` alias 到该目录，否则页面图片会 404。

---

## 3. 方案 A：Windows 本机 / 局域网（最快）

适合：课程演示、答辩、同一 Wi-Fi 下手机/同学访问。

### 3.1 确认 MySQL 正在运行

```powershell
Get-Service MySQL80
```

状态应为 `Running`。

### 3.2 启动生产服务器

```powershell
Set-Location "E:\python node\flask - 副本"
powershell -ExecutionPolicy Bypass -File deploy\start_windows.ps1
```

或者直接：

```powershell
$env:HOST = "0.0.0.0"
$env:PORT = "8000"
.\.venv\Scripts\python.exe serve.py
```

看到类似输出后，浏览器访问：

- 本机：<http://127.0.0.1:8000/login>
- 首页：<http://127.0.0.1:8000/index>

### 3.3 让局域网其他设备访问

1. 查本机 IP：

```powershell
ipconfig | Select-String "IPv4"
```

2. 手机/其他电脑访问 `http://192.168.x.x:8000/login`。
3. 如果访问不了，用**管理员** PowerShell 放行防火墙：

```powershell
New-NetFirewallRule -DisplayName "Flask Shop 8000" `
  -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

> 不建议把家里的电脑直接通过路由器端口映射暴露到公网。公网访问请用方案 B 的云服务器。

### 3.4 创建/重置管理员

项目里已有用户 `zhangsan` 是管理员，但密码未知。可以新建一个管理员：

```powershell
.\.venv\Scripts\python.exe deploy\create_admin.py --username admin
```

按提示输入密码；也可以直接传参：

```powershell
.\.venv\Scripts\python.exe deploy\create_admin.py --username admin --password "你的强密码"
```

### 3.5 开机自启（可选）

以**管理员**身份打开 PowerShell：

```powershell
$action = New-ScheduledTaskAction `
  -Execute "E:\python node\flask - 副本\.venv\Scripts\python.exe" `
  -Argument "serve.py" `
  -WorkingDirectory "E:\python node\flask - 副本"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "FlaskShop" -Action $action -Trigger $trigger `
  -RunLevel Highest -User "SYSTEM" -Force
```

`serve.py` 默认监听 `0.0.0.0:8000`，无需额外设置环境变量。

---

## 4. 方案 B：Linux 云服务器（公网正式部署）

以 Ubuntu 22.04/24.04 为例，服务器 IP 用 `SERVER_IP` 代替，域名用 `example.com` 代替。

### 4.1 安装系统软件

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip mysql-server nginx unzip
```

> 可选：`sudo mysql_secure_installation`。注意它可能把 MySQL root 改成密码登录，之后本文所有 `sudo mysql` 命令要改成 `sudo mysql -uroot -p`。

### 4.2 创建数据库和专用账号

```bash
sudo mysql
```

在 MySQL 提示符中执行（把密码换掉）：

```sql
CREATE DATABASE IF NOT EXISTS flask_data
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'flask_user'@'localhost'
  IDENTIFIED BY 'ReplaceWithStrongPassword';
GRANT ALL PRIVILEGES ON flask_data.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

> 不要让应用用 `root` 连数据库；密码里如果包含 `@ : / ? #`，写进 `DATABASE_URL` 时需要 URL 编码，最简单是只用字母数字。

### 4.3 上传代码

在 Windows 上打包（排除 `.venv`、`.idea`、`__pycache__`）：

```powershell
Set-Location "E:\python node\flask - 副本"
Compress-Archive -Path app.py,config.py,requirements.txt,wsgi.py,serve.py,.env.example,routes,models,controllers,templates,static,deploy `
  -DestinationPath "$env:TEMP\flask-shop.zip" -Force
scp "$env:TEMP\flask-shop.zip" root@SERVER_IP:/tmp/
```

服务器上解压：

```bash
sudo mkdir -p /opt/flask-shop
sudo unzip -o /tmp/flask-shop.zip -d /opt/flask-shop
cd /opt/flask-shop
```

> 上传后建议检查中文图片文件名是否正常：`ls static/img | grep 北流`。
> 如果担心压缩包导致中文名乱码，可以不走 zip：直接执行
> `scp -r "E:\python node\flask - 副本" root@SERVER_IP:/opt/flask-shop`
> （目标目录不存在时会整体复制），然后在服务器上删除 `.venv`、`.idea`、`__pycache__`。

### 4.4 导入数据库

```bash
cd /opt/flask-shop
sudo mysql --default-character-set=utf8mb4 -e "source deploy/flask_data.sql"
```

验证中文没有乱码：

```bash
mysql -u flask_user -p -e "USE flask_data; SELECT id,name FROM goods LIMIT 3;"
```

### 4.5 创建虚拟环境并安装依赖

```bash
cd /opt/flask-shop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt gunicorn==23.0.0
```

### 4.6 写生产配置

```bash
cd /opt/flask-shop
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
nano .env
```

修改为：

```dotenv
SECRET_KEY=上一步生成的长随机字符串
DATABASE_URL=mysql+pymysql://flask_user:ReplaceWithStrongPassword@127.0.0.1:3306/flask_data?charset=utf8mb4
MAX_CONTENT_LENGTH_MB=16
```

然后收紧权限：

```bash
sudo chown -R www-data:www-data /opt/flask-shop
sudo chmod 600 /opt/flask-shop/.env
sudo -u www-data mkdir -p /opt/flask-shop/static/img/upload
```

### 4.7 先手动试跑 Gunicorn

```bash
cd /opt/flask-shop
sudo -u www-data .venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:application
```

另开一个终端验证：

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/login
```

返回 `200` 后按 `Ctrl+C` 停止，继续配置 systemd。

### 4.8 用 systemd 守护进程

```bash
cd /opt/flask-shop
sudo cp deploy/flask-shop.service /etc/systemd/system/flask-shop.service
sudo systemctl daemon-reload
sudo systemctl enable --now flask-shop
sudo systemctl status flask-shop --no-pager
```

看日志：

```bash
sudo journalctl -u flask-shop -f
```

创建或重置管理员（可选）：

```bash
cd /opt/flask-shop
sudo -u www-data .venv/bin/python deploy/create_admin.py --username admin
```

> service 文件里的路径默认是 `/opt/flask-shop`、用户是 `www-data`。如果你改了目录或用户，记得同步修改。

### 4.9 配置 Nginx 反向代理

```bash
cd /opt/flask-shop
sudo cp deploy/nginx-flask-shop.conf /etc/nginx/sites-available/flask-shop
sudo ln -sf /etc/nginx/sites-available/flask-shop /etc/nginx/sites-enabled/flask-shop
sudo rm -f /etc/nginx/sites-enabled/default
sudo sed -i 's/server_name example.com;/server_name _;/' /etc/nginx/sites-available/flask-shop
sudo nginx -t
sudo systemctl reload nginx
```

- 有域名：把 `server_name _;` 改成 `server_name example.com www.example.com;`，并在域名解析里添加 A 记录指向服务器 IP。
- 暂时用 IP 访问：保持 `server_name _;`。

浏览器访问 `http://SERVER_IP/`。

### 4.10 HTTPS（有域名时强烈建议）

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

Certbot 会自动改 Nginx 配置并续期。

### 4.11 防火墙

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

云服务器还要在控制台“安全组”放行 80/443/22，**不要**放行 8000（Gunicorn 只监听 127.0.0.1）。

---

## 5. 方案 C：Docker Compose

适合：本机/服务器已安装 Docker，想一条命令拉起 Web + MySQL。

### 5.1 准备配置

```powershell
Set-Location "E:\python node\flask - 副本"
Copy-Item .env.example .env
notepad .env
```

至少修改：

```dotenv
SECRET_KEY=随机长字符串
MYSQL_ROOT_PASSWORD=数据库root密码
MYSQL_PASSWORD=应用账号密码
WEB_PORT=8000
```

`MYSQL_PASSWORD` 建议只用字母数字，因为它会被拼进 `DATABASE_URL`。

### 5.2 启动

```powershell
docker compose up -d --build
docker compose ps
docker compose logs -f web
```

首次启动时 MySQL 初始化需要 20–40 秒，`web` 会等数据库健康检查通过后再启动。

访问 <http://localhost:8000/login>。

### 5.3 常用命令

```powershell
docker compose logs -f db          # 看数据库日志
docker compose restart web         # 重启应用
docker compose down                # 停止，保留数据库和上传图片
docker compose down -v             # 停止并删除数据库卷（数据会丢！）
docker compose up -d --build       # 改代码后重新构建
```

说明：

- 数据库数据在 Docker 命名卷 `flask-shop_mysql_data` 中。
- 上传图片通过 `./static/img/upload` 挂载到宿主机，重建容器不丢。
- `deploy` 目录下的 SQL 只在**数据库卷为空**时自动执行：`00-schema.sql` 先建空表；如果本机存在 `flask_data.sql`，再导入完整数据。如果之前已经启动过，想重新导入，先 `docker compose down -v`。
- Linux 上如果上传图片提示无权限，执行 `sudo chown -R 1000:1000 static/img/upload`。

---

## 6. 把当前电脑的数据迁到服务器

部署到新环境时，代码之外最重要的是**数据库 + 上传图片**。

### 6.1 导出数据库（当前电脑执行）

```powershell
Set-Location "E:\python node\flask - 副本"
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -uroot -p `
  --databases flask_data --single-transaction --default-character-set=utf8mb4 `
  --result-file="deploy\flask_data.sql"
```

如果数据有更新，重新执行上面命令即可。当前仓库里的导出文件使用的是 `utf8mb4_unicode_ci`；如果目标库是 MySQL 5.7，重新导出后请把文件中的 `utf8mb4_0900_ai_ci` 替换为 `utf8mb4_unicode_ci`（MySQL 8 则不用处理）。

### 6.2 复制上传图片

```powershell
scp -r "E:\python node\flask - 副本\static\img\upload" root@SERVER_IP:/opt/flask-shop/static/img/
```

项目自带的 `static/img` 里也有商品图，如果服务器上的代码是完整打包上传的，就不用单独复制；只传了代码没传 `static` 时才需要。

### 6.3 服务器上导入

```bash
sudo mysql --default-character-set=utf8mb4 -e "source /opt/flask-shop/deploy/flask_data.sql"
sudo chown -R www-data:www-data /opt/flask-shop/static/img/upload
```

### 6.4 验证

```bash
mysql -u flask_user -p -e "USE flask_data; SELECT COUNT(*) FROM goods; SELECT COUNT(*) FROM users;"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/index
```

---

## 7. 上线检查清单

- [ ] `.env` 里的 `SECRET_KEY` 已换成随机值，不是示例值。
- [ ] `DATABASE_URL` 指向生产库，使用专用账号，不是 `root`。
- [ ] `deploy/flask_data.sql` 已导入，`goods`、`users` 数量正确。
- [ ] `static/img/upload/` 已复制，目录对运行用户可写。
- [ ] 生产环境没有运行 `python app.py`，也没有开着 `debug=True`。
- [ ] Nginx `client_max_body_size` ≥ `MAX_CONTENT_LENGTH_MB`（默认 16MB）。
- [ ] 公网只开放 22/80/443，8000 端口不对外。
- [ ] HTTPS 已配置（有域名时）。
- [ ] 数据库和上传目录有定时备份。
- [ ] 日志能看到访问记录和错误。

---

## 8. 这个项目上线前建议修的问题

这些不影响“能跑”，但影响安全和稳定性，按需处理。

1. **`/delete`、`/change_data` 没有管理员校验**
   任何人只要知道 URL，就能删用户、改资料。建议加上 `@admin_required`：

   ```python
   @app.route('/delete')
   @admin_required
   def delete():
       ...
   ```

2. **`/admin` 把所有用户塞进 session cookie**
   `session['users'] = items` 会把全部用户数据写进浏览器 cookie，用户一多就超过 4KB，导致 session 丢失、编辑/删除报错。建议改成按 id 查库：

   ```python
   def get_session_data(user_id):
       user = user_c.get_user_by_id(user_id)
       return user.to_json() if user else None
   ```

   同时删除 `admin()` 里的 `session['users'] = items`。

3. **没有 CSRF 防护**
   登录、改密码、删除等操作可被跨站伪造。生产建议引入 Flask-WTF 的 `CSRFProtect`。

4. **上传只校验扩展名，没有校验文件内容**
   已限制常见图片后缀，但生产还应校验 MIME、限制大小，并确保上传目录不能执行脚本（Nginx 已按静态文件处理，不要配 PHP）。

5. **默认密钥和默认数据库密码**
   `config.py` 保留了开发默认值，方便本地跑；生产必须通过 `.env` 覆盖。

6. **模型和实际表结构不完全一致**
   例如模型里 `goods.price` 是 `Float`，实际库里是 `varchar(50)`；`users.img`、`role` 的可空性也不同。**不要**在已有库上随便跑 `db.create_all()`，以 `deploy/flask_data.sql` 为准。

7. **时区**
   `cart.created_at` 用 `datetime.utcnow`，Docker 默认 UTC。如果要显示北京时间，查询/展示时做 +8 小时转换。

8. **Linux 文件名区分大小写**
   `static/img/` 里的中文文件名、大小写必须和数据库 `img` 字段完全一致，否则图片 404。

---

## 9. 日常运维

### 9.1 更新代码

```bash
cd /opt/flask-shop
sudo systemctl stop flask-shop
# 上传/拉取新代码，保留 .env 和 static/img/upload
sudo -u www-data .venv/bin/pip install -r requirements.txt
sudo systemctl start flask-shop
sudo systemctl status flask-shop --no-pager
```

### 9.2 备份

```bash
sudo mysqldump --single-transaction --default-character-set=utf8mb4 flask_data \
  | gzip | sudo tee /var/backups/flask_data_$(date +%F).sql.gz > /dev/null

sudo tar czf /var/backups/flask_upload_$(date +%F).tar.gz \
  -C /opt/flask-shop static/img/upload
```

### 9.3 恢复

```bash
gunzip < /var/backups/flask_data_2026-01-01.sql.gz | sudo mysql flask_data
sudo tar xzf /var/backups/flask_upload_2026-01-01.tar.gz -C /opt/flask-shop
sudo chown -R www-data:www-data /opt/flask-shop/static/img/upload
```

### 9.4 看日志

```bash
sudo journalctl -u flask-shop -n 200 --no-pager
sudo tail -f /var/log/nginx/flask-shop.error.log
sudo tail -f /var/log/nginx/flask-shop.access.log
```

---

## 10. 常见报错排查

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'flask'` | 用了系统 Python，不是 `.venv` | 用 `.venv\Scripts\python.exe` 或先激活虚拟环境 |
| `Access denied for user ...` | `.env` 数据库账号/密码错误 | 核对 `DATABASE_URL`，确认 MySQL 用户授权 |
| `Unknown database 'flask_data'` | 没建库/没导入 | 执行 `deploy/flask_data.sql` |
| `Table 'flask_data.goods' doesn't exist` | 只建库没导表 | 导入 `deploy/flask_data.sql` |
| `413 Request Entity Too Large` | 上传超过限制 | 调整 `MAX_CONTENT_LENGTH_MB` 和 Nginx `client_max_body_size` |
| `502 Bad Gateway` | Gunicorn 没起来/端口不一致 | `systemctl status flask-shop`、`journalctl -u flask-shop` |
| 图片 404 | 上传目录没复制/权限不对/大小写不一致 | 检查 `static/img/upload`、`chown`、文件名 |
| 中文乱码 | 数据库/连接字符集不是 utf8mb4 | 库、表、`DATABASE_URL` 都确认 `utf8mb4` |
| `cryptography package is required` | MySQL 8 认证方式 | `pip install cryptography`（已在 requirements 中） |
| `Address already in use` | 端口被占用 | 换 `PORT`，或结束占用进程 |
| Docker 启动后没有数据 | `mysql_data` 卷已存在，初始化脚本没执行 | `docker compose down -v` 后重新启动（会清空数据） |

---

## 11. 最短路径（现在就在这台电脑上跑起来）

```powershell
Set-Location "E:\python node\flask - 副本"
Copy-Item .env.example .env
# 编辑 .env，把 SECRET_KEY 换成随机值
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File deploy\start_windows.ps1
```

然后访问 <http://127.0.0.1:8000/login>。

本机 MySQL 里已经有 `flask_data` 和现有数据，不需要再导入 SQL；只有换电脑/换服务器时才需要执行第 2.2 节。

# 云服务器 + 域名长期部署指南

> 方案：云服务器（Ubuntu）+ Docker Compose + Caddy 自动 HTTPS
> 适用：让互联网上的其他人通过自己的域名访问商城
> 配套文件：[docker-compose.prod.yml](docker-compose.prod.yml)、[deploy/Caddyfile](deploy/Caddyfile)

---

## 0. 先做两个决定

### 0.1 服务器放在哪里？

| 选择 | 是否需要 ICP 备案 | 适合 | 注意 |
| --- | --- | --- | --- |
| 中国大陆（阿里云/腾讯云/华为云） | **需要** | 主要访问者在中国大陆，追求低延迟 | 备案通常 7–20 个工作日；未备案时 80/443 可能被服务商拦截 |
| 中国香港 / 新加坡 / 日本 | 不需要 | 想快速上线、不想备案 | 中国大陆访问延迟略高，线路质量看服务商 |

> 备案是工信部对网站域名的要求，不是技术配置。买大陆服务器前先确认服务商的备案流程；个人也可以备案，需要身份证、域名、服务器等资料。备案通过后还可能需要做公安联网备案，以服务商提示为准。

### 0.2 买什么配置？

| 项目 | 建议 |
| --- | --- |
| 服务器 | 2 核 2G 起步；建议 **2 核 4G**，40GB 系统盘 |
| 系统 | Ubuntu 22.04 / 24.04 LTS |
| 带宽 | 3–5 Mbps 足够课程项目；图片多可配对象存储 |
| 域名 | `.com` / `.cn`，在阿里云、腾讯云等注册并完成实名认证 |
| HTTPS | Caddy 自动申请 Let's Encrypt，免费 |
| 数据库 | MySQL 跑在 Docker 内，不暴露 3306 |

2G 内存的机器建议加 2GB swap，否则 Docker 构建可能偏慢：

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 1. 最终架构

```
互联网
  │ 80 / 443
  ▼
Caddy（自动 HTTPS、反向代理）
  │ 内网 8000
  ▼
Flask / Gunicorn（web 容器）
  │ 内网 3306
  ▼
MySQL 8（db 容器）

持久化：
  mysql_data 卷        → 数据库
  ./static/img/upload  → 上传图片
  caddy_data 卷        → HTTPS 证书
```

公网只开放 **22、80、443**；`8000` 和 `3306` 不映射到宿主机。

---

## 2. 购买服务器和域名

### 2.1 服务器

在阿里云/腾讯云购买“轻量应用服务器”或 ECS：

- 地域：按 0.1 的选择
- 镜像：Ubuntu 24.04 LTS
- 公网 IP：必须分配
- 安全组/防火墙：放行 `22`、`80`、`443`

> 22 端口建议只允许你的常用 IP，不要对全网开放。

### 2.2 域名

1. 购买域名并完成实名认证。
2. 进入域名解析，添加记录：

| 记录类型 | 主机记录 | 记录值 |
| --- | --- | --- |
| A | `@` | 服务器公网 IP |

> 先只配置裸域名（如 `shop.example.com`）。需要 `www` 时，再额外加一条 `www` 的 A 记录，并在 `deploy/Caddyfile` 里增加对应的站点块和跳转，否则证书可能申请失败。

3. 等待 DNS 生效，验证：

```bash
dig +short your-domain.com
```

应该返回你的服务器 IP。

4. 大陆服务器：在服务商控制台提交 **ICP 备案**，备案通过前不要指望域名能正常访问 80/443。

---

## 3. 登录服务器并做基础配置

```bash
ssh root@SERVER_IP
```

更新系统：

```bash
apt update && apt upgrade -y
apt install -y curl git unzip ufw
```

防火墙：

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status
```

> 云厂商的“安全组”和服务器内的 `ufw` 是两层，两个都要放行 80/443。

设置时区（可选）：

```bash
timedatectl set-timezone Asia/Shanghai
```

---

## 4. 安装 Docker

推荐用 Docker 官方脚本：

```bash
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
docker version
docker compose version
```

如果 `get.docker.com` 访问慢，可以：

- 在云厂商控制台选择“Docker”应用镜像；或
- 使用系统包：

```bash
apt install -y docker.io docker-compose-v2
systemctl enable --now docker
```

### Docker 拉镜像慢

如果 `docker pull` 超时，在阿里云控制台进入 **容器镜像服务 → 镜像工具 → 镜像加速器**，拿到专属地址，然后：

```bash
mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": ["https://你的专属地址.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker
```

---

## 5. 把代码放到服务器

### 方式 A：直接 clone（服务器能访问 GitHub 时）

```bash
mkdir -p /opt
git clone https://github.com/hdtljg/flask-shop.git /opt/flask-shop
cd /opt/flask-shop
```

### 方式 B：本地打包上传（GitHub 访问慢时推荐）

在本地项目目录执行：

```powershell
Set-Location "E:\python node\flask - 副本"
git archive --format=zip -o "$env:TEMP\flask-shop.zip" HEAD
scp "$env:TEMP\flask-shop.zip" root@SERVER_IP:/tmp/
```

`git archive` 只打包已提交文件，不会带 `.env`、`.venv`、`.git`。

服务器上解压：

```bash
apt install -y unzip
mkdir -p /opt/flask-shop
unzip -o /tmp/flask-shop.zip -d /opt/flask-shop
cd /opt/flask-shop
```

---

## 6. 配置生产环境变量

```bash
cd /opt/flask-shop
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"
nano .env
chmod 600 .env
```

至少修改：

```dotenv
DOMAIN=shop.example.com

SECRET_KEY=上一步生成的长随机字符串
MYSQL_ROOT_PASSWORD=数据库root密码
MYSQL_PASSWORD=应用数据库密码
MAX_CONTENT_LENGTH_MB=16
```

说明：

- `DOMAIN` 只写域名，不要带 `https://`。
- 数据库密码建议用字母数字，避免 `@ : / ? # $` 等字符影响连接串。
- `DATABASE_URL` 在 `docker-compose.prod.yml` 中会被覆盖，保留示例值也不影响。
- **首次启动后不要随意改 `MYSQL_PASSWORD`**：数据库里的用户密码不会自动跟着变。要改必须进 MySQL 执行 `ALTER USER`。

---

## 7. 启动生产服务

```bash
cd /opt/flask-shop
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f caddy
```

第一次会：

1. 拉取 `mysql:8.0`、`caddy:2-alpine`，构建 `flask-shop-web` 镜像
2. 初始化 MySQL，依次执行 `deploy/00-schema.sql` 和 `deploy/flask_data.sql`
3. 启动 Gunicorn（3 个 worker）
4. Caddy 向 Let's Encrypt 申请证书

Caddy 日志里看到类似内容即成功：

```text
certificate obtained successfully
```

按 `Ctrl+C` 退出日志（不会停止容器）。

访问：

```text
https://your-domain.com/login
```

如果浏览器显示证书有效、页面正常，说明部署成功。

验证：

```bash
curl -I https://your-domain.com/login
curl -I http://your-domain.com
```

`http` 应该 308 跳转到 `https`。

---

## 8. 创建管理员、导入数据

### 8.1 创建管理员

```bash
cd /opt/flask-shop
docker compose -f docker-compose.prod.yml exec web python deploy/create_admin.py --username admin
```

按提示输入密码。也可以：

```bash
docker compose -f docker-compose.prod.yml exec web python deploy/create_admin.py --username admin --password "你的强密码"
```

### 8.2 使用当前电脑的最新数据

GitHub 仓库里的 `deploy/flask_data.sql` 是之前导出的演示数据。如果你本地又加了商品/用户，按下面步骤导出并替换。

在本地 Windows：

```powershell
Set-Location "E:\python node\flask - 副本"
docker compose exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysqldump -uroot --single-transaction --default-character-set=utf8mb4 --databases flask_data --result-file=/tmp/flask_data_current.sql'
docker cp flask-shop-db-1:/tmp/flask_data_current.sql .\deploy\flask_data.sql
scp .\deploy\flask_data.sql root@SERVER_IP:/opt/flask-shop/deploy/
```

> 容器名以 `docker compose ps` 显示的为准，通常是 `flask-shop-db-1`。

如果服务器**还没首次启动**，替换 `deploy/flask_data.sql` 后直接启动即可自动导入。

如果服务器**已经启动过**，需要手动导入（会 DROP 现有表，先备份）：

```bash
cd /opt/flask-shop
docker cp deploy/flask_data.sql flask-shop-prod-db-1:/tmp/import.sql
docker compose -f docker-compose.prod.yml exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot --default-character-set=utf8mb4 -e "source /tmp/import.sql"'
```

### 8.3 上传图片权限

仓库里已包含现有示例图片。以后从本地上传新图片到服务器时：

```powershell
scp -r "E:\python node\flask - 副本\static\img\upload" root@SERVER_IP:/opt/flask-shop/static/img/
```

服务器上修正权限（容器内应用用户 UID 是 1000）：

```bash
chown -R 1000:1000 /opt/flask-shop/static/img/upload
chmod -R u+rwX /opt/flask-shop/static/img/upload
```

否则后台新上传的图片可能写入失败。

---

## 9. 备份

创建每日备份脚本：

```bash
mkdir -p /var/backups/flask-shop
cat >/etc/cron.daily/flask-shop-backup <<'EOF'
#!/bin/sh
set -e
cd /opt/flask-shop
TS=$(date +%F)

docker compose -f docker-compose.prod.yml exec -T db sh -c \
  'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysqldump -uroot --single-transaction --default-character-set=utf8mb4 flask_data' \
  | gzip > /var/backups/flask-shop/db-$TS.sql.gz

tar czf /var/backups/flask-shop/upload-$TS.tar.gz \
  -C /opt/flask-shop static/img/upload

find /var/backups/flask-shop -type f -mtime +14 -delete
EOF

chmod +x /etc/cron.daily/flask-shop-backup
```

手动测试一次：

```bash
/etc/cron.daily/flask-shop-backup
ls -lh /var/backups/flask-shop/
```

> 备份只放在同一台服务器上不够安全。建议定期把 `/var/backups/flask-shop` 同步到对象存储（阿里云 OSS、腾讯云 COS）或另一台机器。

### 恢复数据库

```bash
gunzip < /var/backups/flask-shop/db-2026-01-01.sql.gz \
  | docker compose -f docker-compose.prod.yml exec -T db \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot flask_data'
```

### 恢复上传图片

```bash
tar xzf /var/backups/flask-shop/upload-2026-01-01.tar.gz -C /opt/flask-shop
chown -R 1000:1000 /opt/flask-shop/static/img/upload
```

---

## 10. 更新代码

```bash
cd /opt/flask-shop
/etc/cron.daily/flask-shop-backup      # 先备份

git pull
docker compose -f docker-compose.prod.yml up -d --build
docker image prune -f
```

如果服务器不能访问 GitHub，就用本地 `git archive` 打包上传，覆盖代码；**保留 `.env` 和 `static/img/upload`**。

更新后检查：

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs --tail=100 web
docker compose -f docker-compose.prod.yml logs --tail=100 caddy
```

---

## 11. 安全与运维清单

- [ ] 安全组只开放 22、80、443，`3306`、`8000` 不对外开放
- [ ] SSH 使用密钥登录，禁用密码登录（`PermitRootLogin prohibit-password`）
- [ ] `.env` 权限 600，不提交 Git
- [ ] 修改默认管理员密码
- [ ] HTTPS 证书正常，Caddy 自动续期
- [ ] 每日备份数据库和上传目录，并定期验证恢复
- [ ] 监控磁盘：`df -h`；图片多了会占空间
- [ ] 定期 `apt upgrade`、更新 Docker 镜像

> 这个项目是课程演示级别，公网长期运行时建议再补：CSRF 防护、`/delete` 与 `/change_data` 的管理员校验、上传文件内容校验、登录限流。

---

## 12. 常见问题

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| 域名打不开，IP 能访问 | DNS 未生效 / 备案未通过 | `dig +short 域名`；大陆服务器先完成 ICP 备案 |
| Caddy 日志一直证书失败 | 80/443 未放行、DNS 不对、备案未通过、Cloudflare 代理 | 检查安全组和 `ufw`；先关闭 Cloudflare 小黄云，证书签发后再开 |
| `502 Bad Gateway` | web 容器未启动或数据库连不上 | `docker compose -f docker-compose.prod.yml ps`、`logs web`、`logs db` |
| `413 Request Entity Too Large` | 上传超过 16MB | 改 `.env` 的 `MAX_CONTENT_LENGTH_MB`，重启 web |
| `docker pull` 超时 | Docker Hub 网络问题 | 配置阿里云镜像加速器，或使用云厂商 Docker 镜像 |
| `git clone` 很慢/失败 | 服务器访问 GitHub 不稳定 | 用第 5 节 `git archive` + `scp` 方式 |
| MySQL `Access denied` | `.env` 密码和数据库初始化时的密码不一致 | 首次启动后不要改密码；改了就进 MySQL `ALTER USER` |
| 80 端口被占用 | 服务器预装了 Nginx/Apache | `ss -lntp | grep ':80'`，停掉占用服务，只保留 Caddy |
| `down -v` 后数据没了 | 删除了 `mysql_data` 卷 | 从备份恢复；不要把 `down -v` 当重启命令 |
| 上传图片失败 | 上传目录权限不对 | `chown -R 1000:1000 /opt/flask-shop/static/img/upload` |

---

## 13. 费用和时间预估

| 项目 | 大致费用 |
| --- | --- |
| 2 核 2G 云服务器 | 约 ¥60–120/月（活动价差异大） |
| 2 核 4G 云服务器 | 约 ¥100–200/月 |
| 域名 | 约 ¥60–100/年 |
| HTTPS 证书 | 免费（Let's Encrypt） |
| 备案 | 免费，时间 7–20 个工作日 |

技术部署本身约 1–2 小时；大陆服务器的主要等待时间是 ICP 备案。

---

## 14. 最短执行顺序

```text
1. 买服务器（Ubuntu 24.04，2C4G，公网 IP）
2. 买域名，实名认证，A 记录指向服务器 IP
3. 大陆服务器：提交 ICP 备案，等待通过
4. 安全组放行 22/80/443，SSH 登录，配置 ufw
5. 安装 Docker 和 compose 插件
6. 上传代码到 /opt/flask-shop
7. cp .env.example .env，填写 DOMAIN、SECRET_KEY、两个数据库密码
8. docker compose -f docker-compose.prod.yml up -d --build
9. 看 Caddy 日志，确认证书签发
10. 创建管理员，导入最新数据，配置每日备份
11. 浏览器访问 https://你的域名/login
```

如果卡在某一步，把该步骤的命令输出或报错发我，我可以按你的服务器系统继续排查。

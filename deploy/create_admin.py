"""创建管理员账号，或把已有账号重置为管理员。

用法（在项目根目录执行）：
    .venv\\Scripts\\python.exe deploy\\create_admin.py --username admin
    .venv\\Scripts\\python.exe deploy\\create_admin.py --username admin --password 新密码

注意：密码会使用 Werkzeug 的哈希算法写入数据库，不会明文保存。
"""
import argparse
import getpass
import sys
from pathlib import Path

# 让脚本无论从哪个目录执行都能导入项目根目录下的模块
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from werkzeug.security import generate_password_hash

from app import app
from models.user_model import User
from routes import db


def main():
    parser = argparse.ArgumentParser(description='创建管理员账号或重置管理员密码')
    parser.add_argument('--username', help='管理员用户名')
    parser.add_argument('--password', help='管理员密码（不传则交互输入）')
    parser.add_argument('--telephone', default='00000000000', help='手机号（仅新建时使用）')
    args = parser.parse_args()

    username = args.username or input('管理员用户名: ').strip()
    password = args.password or getpass.getpass('管理员密码: ')

    if not username or not password:
        print('用户名和密码不能为空')
        return 1

    with app.app_context():
        user = User.query.filter_by(username=username).first()

        if user:
            user.password = generate_password_hash(password)
            user.role = 'admin'
            db.session.commit()
            print('已重置密码并设为管理员: %s' % username)
        else:
            user = User(username, password, args.telephone, None, role='admin')
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            print('管理员创建成功: %s' % username)

    return 0


if __name__ == '__main__':
    sys.exit(main())

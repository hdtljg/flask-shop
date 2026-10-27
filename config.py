import os
from pathlib import Path

from dotenv import load_dotenv

# 项目根目录（不依赖启动时的工作目录）
BASE_DIR = Path(__file__).resolve().parent

# 本地开发读取项目根目录下的 .env；生产环境可用系统环境变量覆盖
load_dotenv(BASE_DIR / '.env')

# 数据库连接：优先 DATABASE_URL，未设置时使用本地开发库
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://root:123456@localhost/flask_data?charset=utf8mb4'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 生产环境务必通过环境变量设置一个足够长的随机值
SECRET_KEY = os.environ.get('SECRET_KEY', '!@#qwer$%^')

# 上传目录：默认项目内 static/img/upload。
# 如果改成外部目录，Web 服务器必须把 /static/img/upload/ 映射到该目录，否则图片会 404。
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or str(
    BASE_DIR / 'static' / 'img' / 'upload'
)

# 单次请求最大上传大小（MB），防止超大文件打满磁盘
MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH_MB', '16')) * 1024 * 1024

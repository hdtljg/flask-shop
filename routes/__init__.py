import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder='../templates',static_folder='../static')

#配置数据库

app.config.from_object('config')
db = SQLAlchemy(app)

# 确保上传目录存在（新服务器/首次部署时该目录可能不存在）
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#登录管理
login_manager = LoginManager()
login_manager.init_app(app)

from  routes import  views,login_route,user_route,goods_route

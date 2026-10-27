from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from routes import db

# def add_user(user):
#     # 对密码进行加密
#     user.password = generate_password_hash(user.password)
#     db.session.add(user)
#     db.session.commit()

# def get_user_by_username_pwd(username,password):
#     return User.query.filter_by(username=username,password=password).first()

def get_user_by_username_pwd(username, password):
    # 修改为使用哈希验证
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None



def get_user_by_id(id):
    return User.query.get(id)


def add_user(user):
    # 对密码进行加密
    user.password = generate_password_hash(user.password)
    db.session.add(user)
    db.session.commit()

def select_all_users():
    return User.query.all()

def delete_user_by_id(user_id):
    db.session.delete(get_user_by_id(user_id))
    db.session.commit()

def update_user(user_id, username,telephone,img):
    user=get_user_by_id(user_id)

    user.username=username
    user.telephone=telephone
    if img:
        user.img=img
    db.session.commit()

# 新增修改密码方法
def update_password(user_id, old_password, new_password):
    user = get_user_by_id(user_id)
    # 验证旧密码是否正确
    if not check_password_hash(user.password, old_password):
        return False
    # 更新密码
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return True

import time
import os

from models.UserInfo import UserInfo
from models.user_model import User
from routes import app
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user, logout_user
import controllers.user_controller as user_c
from routes.views import admin_required


#注册
@app.route('/pai/register',methods=['POST'])
def pai_register():
    #1.接收用户注册数据（非文件域数据）
    username = request.form['username']
    password = request.form['pwd']
    telephone = request.form['tel']

    #2.若有文件数据，保存文件数据到项目目录
    files = request.files['img']

    file_name = saveImg(files)

    #3.封装用户model实体类，默认角色为user
    user=User(username,password,telephone,file_name, role='user')

    #4.添加到数据库
    #5.返回结果
    try:
        user_c.add_user(user)
        return redirect('/login')
    except Exception as e:

        flash('注册失败','error')
        return redirect('/register')

@app.route('/admin')
@admin_required
def admin():
    #读取数据表所有数据
    users=user_c.select_all_users()
    #把users转换成json
    items=[obj.to_json() for obj in users]
    session['users']=items
    return render_template("edit.html",users=users)

@app.route('/delete')
def delete():
    #获取被删除记录的id
    user_id=request.args.get('id')
    # 获取旧的头像
    user = get_session_data(user_id)

    if user and user['img']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user['img'])

        try:
            os.remove(file_path)
        except Exception as e:
            print("删除失败")

    try:
        user_c.delete_user_by_id(user_id)
    except Exception as e:
        print(e)

    return redirect('/admin')

@app.route('/get_user_session')
def get_user_session():
    user_id=request.args.get('id')
    return get_session_data(user_id)
    # users = session.get('users')
    # for user in users:
    #     if user['id'] == int(user_id):
    #         return user

@app.route('/change_data',methods=['POST'])
def change_data():
    user_id=request.args.get('id')
    username=request.form.get('username')
    telephone=request.form.get('tel')
    files=request.files['img']

    #获取旧的头像
    user=get_session_data(user_id)

    if user and user['img']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user['img'])

        try:
            os.remove(file_path)
        except Exception as e:
            print("删除失败")

    file_name = ""
    if files:
        file_name=saveImg(files)

    #更新数据库：
    try:
        user_c.update_user(user_id,username,telephone,file_name)
    except Exception as e:
        print('更新失败')
        print(e)

    return redirect('/admin')

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

def saveImg(files):
    """保存上传的头像，返回存入数据库的文件名。"""
    original_name = files.filename or ''
    ext = os.path.splitext(original_name)[1].lower()

    # 只允许常见图片格式，避免上传任意文件
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError('不支持的图片格式: %s' % ext)

    # 时间戳命名，避免同名覆盖；扩展名必须保留
    file_name = str(int(time.time())) + ext

    upload_dir = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    files.save(os.path.join(upload_dir, file_name))

    return file_name

def get_session_data(user_id):
    users=session.get('users')
    for user in users:
        if user['id'] == int(user_id):
            return user


@app.route('/user_info',methods=['post'])
def user_info():

    users = UserInfo.query.all()

    items=[obj.to_json() for obj in users]

    return jsonify(items)


# 个人信息页面
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


# 新增修改密码路由
@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # 验证新密码和确认密码是否一致
    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': '新密码和确认密码不一致'})

    # 调用控制器方法修改密码
    if user_c.update_password(current_user.id, old_password, new_password):
        return jsonify({'status': 'success', 'message': '密码修改成功'})
    else:
        return jsonify({'status': 'error', 'message': '原密码错误'})


# 新增修改个人信息路由
@app.route('/api/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    username = request.form.get('username')
    telephone = request.form.get('telephone')
    files = request.files['img']

    # 处理头像上传
    file_name = ""
    if files and files.filename:
        # 保存新头像
        file_type = files.filename.split('.')[-1]
        times = int(time.time())
        file_name = str(times) + "." + file_type
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        files.save(file_path)

        # 删除旧头像
        if current_user.img:
            old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.img)
            try:
                os.remove(old_file_path)
            except Exception as e:
                print("删除旧头像失败:", e)

    # 更新用户信息
    try:
        user_c.update_user(current_user.id, username, telephone, file_name)
        return jsonify({'status': 'success', 'message': '个人信息修改成功'})
    except Exception as e:
        print('更新失败:', e)
        return jsonify({'status': 'error', 'message': '个人信息修改失败'})




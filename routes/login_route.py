from routes import app, login_manager
from flask import redirect, request, flash, session, jsonify
import  controllers.user_controller as user_c
from flask_login import login_user, logout_user


@app.route('/api/login', methods=['POST'])
def api_login():
    # 1.获取请求数据
    # username = request.form['username']
    # password = request.form['pwd']
    username = request.form.get('username')
    password = request.form.get('password')

    # 2.访问数据库
    user = user_c.get_user_by_username_pwd(username, password)
    # 3.验证
    # 4.返回结果
    if user is None:
        # flash('无效用户名或密码','error')
        # return redirect('/login')
        return jsonify({'status': 'error'})

        # return 'error'


    login_user(user)

    session['user_id'] = user.id
    # return redirect('/index')
    session['user_role'] = user.role  # 保存用户角色到session

    # return 'success'
    return jsonify({
        'status': 'success',
        'role': user.role
    })
@login_manager.user_loader
def load_user(id):
    return user_c.get_user_by_id(id)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/login')
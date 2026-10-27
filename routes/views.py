from flask import render_template,send_from_directory, redirect, url_for, flash, request
from flask_login import current_user
from functools import wraps
from routes import app
# 导入商品控制器
from controllers.goods_controller import select_all_goods
# 管理员权限检查装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.role != 'admin':
            flash('您没有权限访问此页面')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
# 路径映射

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../static/css', path)
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../static/js', path)
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('../static/img', path)

@app.route('/index')
def index():
    # 获取所有商品数据
    goods_list = select_all_goods()
    if current_user.is_authenticated:#验证是否有用户登录
        return render_template('index.html',user=current_user, goods=goods_list)

    return render_template('index.html', goods=goods_list)

@app.route('/register')
def register():
    return render_template('register.html')



# 添加管理员仪表板路由
@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html', user=current_user)



@app.route('/showData')
def showData():
    return render_template('echart.html')

@app.route('/login')
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/random_page')
def random_page():
    return render_template('selectjq.html')

# 在文件末尾添加商品管理页面路由

# 商品管理页面
@app.route('/admin/manage_goods')
@admin_required
def manage_goods():
    goods_list = select_all_goods()
    message = request.args.get('message')
    return render_template('manage_goods.html', goods=goods_list, message=message, user=current_user)
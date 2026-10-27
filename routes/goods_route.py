from flask import jsonify, render_template, request, redirect, url_for
from models.goods_model import Goods
from routes import db
from routes import app
from flask_login import current_user
import controllers.goods_controller as goods_controller
import controllers.cart_controller as cart_controller
from routes.views import admin_required
import time
import os

# 添加搜索路由
@app.route('/search')
def search():
    # 获取搜索关键词
    keyword = request.args.get('keyword', '').strip()
    # 调用搜索函数
    results = goods_controller.search_goods(keyword)
    # 渲染搜索结果页面
    return render_template('search_results.html',
                          goods=results,
                          keyword=keyword,
                          result_count=len(results))

@app.route('/goods', methods=['post'])
def goods():
    goods = goods_controller.select_all_goods()
    items = [obj.to_dict() for obj in goods]
    return jsonify(items)

# 商品详情页
@app.route('/goods/<int:goods_id>')
def goods_detail(goods_id):
    good = goods_controller.select_goods_by_id(goods_id)
    if not good:
        return render_template('error.html', message='商品不存在')
    return render_template('goods_detail.html', good=good)

# 购买商品的API
@app.route('/api/buy_goods/<int:goods_id>', methods=['POST'])
def buy_goods(goods_id):
    try:
        quantity = request.args.get('quantity', 1, type=int)

        # 查询商品
        goods = Goods.query.get(goods_id)
        if not goods:
            return jsonify({'success': False, 'message': '商品不存在'})

        # 增加销量
        goods.sales += quantity
        db.session.commit()

        # 这里可以添加创建订单等其他购买逻辑
        return jsonify({'success': True, 'message': '购买成功！', 'new_sales': goods.sales})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'购买失败：{str(e)}'})


# 检查用户登录状态
@app.route('/api/check_login', methods=['GET'])
def check_login():
    return jsonify({'is_logged_in': current_user.is_authenticated})


# 添加到购物车
@app.route('/api/add_to_cart/<int:goods_id>', methods=['POST'])
def add_to_cart(goods_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '请先登录'})

    quantity = request.args.get('quantity', 1, type=int)
    result = cart_controller.add_to_cart(goods_id, quantity)
    return jsonify(result)


# 购物车页面
@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return render_template('error.html', message='请先登录')

    cart_data = cart_controller.get_user_cart()
    return render_template('cart.html', cart_items=cart_data['items'], total_price=cart_data['total_price'])


# 从购物车移除商品
@app.route('/api/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '请先登录'})

    result = cart_controller.remove_from_cart(cart_id)
    return jsonify(result)


@app.route('/api/checkout_cart', methods=['POST'])
def checkout_cart():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '请先登录'})

    result = cart_controller.checkout_cart()
    return jsonify(result)


# 保存图片的辅助函数
def save_goods_image(file):
    if not file or not file.filename:
        return None

    # 确保上传目录存在（使用配置中的绝对路径，避免依赖启动目录）
    upload_dir = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    # 生成唯一文件名
    file_type = file.filename.split('.')[-1]
    times = int(time.time())
    file_name = f"goods_{times}.{file_type}"
    file_path = os.path.join(upload_dir, file_name)

    # 保存文件
    file.save(file_path)
    return file_name


# 添加商品页面路由
@app.route('/admin/add_goods')
@admin_required
def add_goods_page():
    return render_template('add_goods.html')


# 添加商品处理路由
@app.route('/admin/add_goods_process', methods=['POST'])
@admin_required
def add_goods_process():
    try:
        # 获取表单数据
        name = request.form.get('name')
        price = request.form.get('price')
        detail = request.form.get('detail')
        sales = request.form.get('sales', 0)
        file = request.files['img']

        # 验证必填字段
        if not name or not price or not detail:
            return render_template('add_goods.html', error='商品名称、价格和详情不能为空')

        # 处理图片上传
        img_name = None
        if file and file.filename:
            img_name = save_goods_image(file)

        # 调用控制器添加商品
        success, result = goods_controller.add_goods(name, price, detail, img_name, int(sales))

        if success:
            return redirect(url_for('admin_dashboard', message='商品添加成功'))
        else:
            return render_template('add_goods.html', error=f'添加失败: {result}')

    except Exception as e:
        return render_template('add_goods.html', error=f'添加过程中出错: {str(e)}')

# 删除商品API路由
@app.route('/admin/delete_goods/<int:goods_id>', methods=['POST'])
@admin_required
def delete_goods_route(goods_id):
    success, message = goods_controller.delete_goods(goods_id)
    return jsonify({'success': success, 'message': message})


# 编辑商品页面路由
@app.route('/admin/edit_goods/<int:goods_id>')
@admin_required
def edit_goods_page(goods_id):
    goods = goods_controller.select_goods_by_id(goods_id)
    if not goods:
        return render_template('error.html', message='商品不存在')
    return render_template('edit_goods.html', goods=goods)


# 更新商品处理路由
@app.route('/admin/update_goods/<int:goods_id>', methods=['POST'])
@admin_required
def update_goods_process(goods_id):
    try:
        # 获取表单数据
        name = request.form.get('name')
        price = request.form.get('price')
        sales = request.form.get('sales')
        detail = request.form.get('detail')
        file = request.files.get('img')

        # 验证必填字段
        if not name or not price or not detail or sales is None:
            goods = goods_controller.select_goods_by_id(goods_id)
            return render_template('edit_goods.html', goods=goods, error='请填写所有必填字段')

        # 处理图片上传（如果有新图片）
        img_name = None
        if file and file.filename:
            img_name = save_goods_image(file)

        # 调用控制器更新商品
        success, message = goods_controller.update_goods(
            goods_id=goods_id,
            name=name,
            price=price,
            detail=detail,
            img=img_name if img_name else None,
            sales=sales
        )

        if success:
            return redirect(url_for('manage_goods', message='商品更新成功'))
        else:
            goods = goods_controller.select_goods_by_id(goods_id)
            return render_template('edit_goods.html', goods=goods, error=message)

    except Exception as e:
        goods = goods_controller.select_goods_by_id(goods_id)
        return render_template('edit_goods.html', goods=goods, error=f'更新过程中出错: {str(e)}')
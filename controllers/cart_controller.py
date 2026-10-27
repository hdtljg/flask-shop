from models.cart_model import Cart
from models.goods_model import Goods
from routes import db
from flask_login import current_user


def add_to_cart(goods_id, quantity=1):
    """添加商品到购物车"""
    try:
        # 检查商品是否存在
        goods = Goods.query.get(goods_id)
        if not goods:
            return {'success': False, 'message': '商品不存在'}

        # 检查购物车中是否已存在该商品
        cart_item = Cart.query.filter_by(user_id=current_user.id, goods_id=goods_id).first()

        if cart_item:
            # 如果已存在，更新数量
            cart_item.quantity += quantity
        else:
            # 如果不存在，创建新购物车项
            cart_item = Cart(current_user.id, goods_id, quantity)
            db.session.add(cart_item)

        db.session.commit()
        return {'success': True, 'message': '添加成功'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'添加失败：{str(e)}'}


# 修改后
def get_user_cart():
    """获取用户购物车并计算总价"""
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        # 计算总价
        total_price = sum(item.goods.price * item.quantity for item in cart_items)
        return {'items': cart_items, 'total_price': total_price}
    except Exception as e:
        print(f'获取购物车失败：{str(e)}')
        return {'items': [], 'total_price': 0}


def remove_from_cart(cart_id):
    """从购物车移除商品"""
    try:
        cart_item = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first()
        if not cart_item:
            return {'success': False, 'message': '购物车商品不存在'}

        db.session.delete(cart_item)
        db.session.commit()
        return {'success': True, 'message': '移除成功'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'移除失败：{str(e)}'}


def checkout_cart():
    """结算购物车，确认购买并删除购物车商品"""
    try:
        # 获取用户的所有购物车商品
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            return {'success': False, 'message': '购物车为空'}

        # 遍历购物车商品，更新商品销量
        for item in cart_items:
            # 获取对应的商品
            goods = Goods.query.get(item.goods_id)
            if goods:
                # 增加销量
                goods.sales += item.quantity

        # 删除用户的所有购物车商品
        Cart.query.filter_by(user_id=current_user.id).delete()

        # 提交所有更改
        db.session.commit()

        return {'success': True, 'message': '购买成功，购物车已清空'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'结算失败：{str(e)}'}
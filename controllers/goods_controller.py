from sqlalchemy import or_

from models.goods_model import Goods
from routes import db
def select_all_goods():
    return Goods.query.all()

def select_goods_by_id(goods_id):
    """根据ID获取商品详情"""
    return Goods.query.get(goods_id)
# 添加搜索商品函数
def search_goods(keyword):
    """根据关键词搜索商品，在名称和详情中模糊匹配"""
    if not keyword:
        return []
    # 使用or_实现多字段搜索，在商品名称和商品详情中模糊匹配
    goods = Goods.query.filter(
        or_(
            Goods.name.like(f'%{keyword}%'),
            Goods.detail.like(f'%{keyword}%')
        )
    ).all()
    return goods

# 添加商品函数
def add_goods(name, price, detail, img=None, sales=0):
    """添加新商品"""
    try:
        # 创建商品实例
        new_goods = Goods(
            name=name,
            price=float(price),
            detail=detail,
            sales=sales,
            img=img
        )
        # 添加到数据库
        db.session.add(new_goods)
        db.session.commit()
        return True, new_goods
    except Exception as e:
        db.session.rollback()
        print(f"添加商品失败: {str(e)}")
        return False, str(e)


# 删除商品函数
def delete_goods(goods_id):
    """根据ID删除商品"""
    try:
        # 查询商品是否存在
        goods = Goods.query.get(goods_id)
        if not goods:
            return False, "商品不存在"

        # 删除商品
        db.session.delete(goods)
        db.session.commit()
        return True, "删除成功"
    except Exception as e:
        db.session.rollback()
        print(f"删除商品失败: {str(e)}")
        return False, str(e)


# 更新商品函数
def update_goods(goods_id, name=None, price=None, detail=None, img=None, sales=None):
    """更新商品信息"""
    try:
        # 查询商品是否存在
        goods = Goods.query.get(goods_id)
        if not goods:
            return False, "商品不存在"

        # 更新字段，只更新提供的值
        if name is not None:
            goods.name = name
        if price is not None:
            goods.price = float(price)
        if detail is not None:
            goods.detail = detail
        if img is not None:
            goods.img = img
        if sales is not None:
            goods.sales = int(sales)

        # 提交更改
        db.session.commit()
        return True, "更新成功"
    except Exception as e:
        db.session.rollback()
        print(f"更新商品失败: {str(e)}")
        return False, str(e)
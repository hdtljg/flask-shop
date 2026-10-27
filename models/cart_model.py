from routes import db
from datetime import datetime
from models.goods_model import Goods  # 添加导入

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加与Goods模型的关联关系
    goods = db.relationship('Goods', backref=db.backref('cart_items', lazy=True))

    def __init__(self, user_id, goods_id, quantity=1):
        self.user_id = user_id
        self.goods_id = goods_id
        self.quantity = quantity

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goods_id': self.goods_id,
            'quantity': self.quantity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
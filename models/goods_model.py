from routes import db

class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.Integer, default=0, nullable=False)  # 修改为整数类型
    img = db.Column(db.String(200), nullable=True)  # 添加图片字段

    def __init__(self, name, price, detail, sales, img=None):
        self.name = name
        self.price = price
        self.detail = detail
        self.sales = sales
        # self.id=None
        self.img = img

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'detail': self.detail,
            'sales': self.sales,
            'img': self.img
        }
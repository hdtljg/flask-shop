from routes import db

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tel = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String(80), nullable=False)


    def __init__(self, name, tel, img):
        self.name = name
        self.tel = tel
        self.img = img
        self.id=None

    def to_json(self):
        return {'id':self.id, 'name':self.name, 'tel':self.tel, 'img':self.img}

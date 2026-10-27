from flask_login import UserMixin

from routes import db

class User(db.Model,UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(64), nullable=False)
    img=db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 添加角色字段，默认为普通用户

    def __init__(self,username,password,telephone,img, role='user'):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.img=img
        self.role = role  # 初始化角色
        if img and img[-1]=='.':
            self.img=None
        # self.id = None


    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        return {
                'id':self.id,
                'username':self.username,
                'telephone':self.telephone,
                'img':self.img,
                'role': self.role  # 包含角色信息
        }
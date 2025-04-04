from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location = db.Column(db.String)
    timezone = db.Column(db.String)
    style = db.Column(db.String, default='default')

    def set_password(self, password):
        # 生成盐值并对密码进行哈希处理
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        # 验证密码是否匹配
        return bcrypt.checkpw(password.encode('utf-8'), self.password)


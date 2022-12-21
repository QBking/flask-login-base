from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from RealProject import db, login_manager
from app.my_utils import verifyToken


class BaseModel(db.Model):
    """
    基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 更新时间


class User(UserMixin, BaseModel):
    """
    用户模型
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.request_loader
def login_user_from_request(request):
    token = request.headers.get('Authorization')
    if token is None:
        return None
    payload = verifyToken(token)
    if payload is not None:
        user = User.query.get(int(payload['data']['userid']))
    else:
        user = None
    return user

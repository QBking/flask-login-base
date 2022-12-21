import json

from flask import Blueprint, request
from flask_login import login_required, current_user

from RealProject import db
from ..models import User
from app.my_utils import api_return, genToken

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    # 登录
    req = json.loads(request.get_data().decode('utf-8'))
    email = req.get('email')
    password = req.get('password')

    user = User.query.filter_by(email=email).first()
    if user is not None:
        if user.check_password(password):
            # login_user(user)
            token = genToken({"userid": user.id})
            return api_return("OK", data={"token": token})  # 登录成功
        else:
            return api_return("USER_PWD_ERROR")  # 密码错误
    else:
        return api_return("USER_NOT_FOUND")  # 没有此用户


@bp.route('/register', methods=['POST'])
def register():
    # 注册
    req = json.loads(request.get_data().decode('utf-8'))
    username = req.get('username')
    password = req.get('password')
    email = req.get('email')
    if User.query.filter_by(email=email).first() is not None:
        print('register')
        return api_return("USER_EXIST")  # 用户已存在
    user = User()
    user.username = username
    user.password = password
    user.email = email
    db.session.add(user)
    db.session.commit()
    return api_return("OK")  # 注册成功


@bp.route("/getInfoBase", methods=["GET"])
@login_required
def getInfoBase():
    # 返回基本信息
    return api_return("OK", data={
        "username": current_user.username,
        "email": current_user.email
    })

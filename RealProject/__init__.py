from flask import Flask
from flask_cors import CORS

from .extensions import db, login_manager
from app.auth import views as auth
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    # 允许跨域
    CORS(app, resources=r'/*')
    # 初始化login_manager
    login_manager.init_app(app)
    # 绑定配置文件
    app.config.from_pyfile('config.py', silent=True)
    # 初始化数据库
    db.init_app(app)
    # 数据库迁移
    migrate = Migrate(app, db)
    # 注册蓝图
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return 'hello!'

    return app

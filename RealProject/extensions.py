from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
"""防止循环调用"""
db = SQLAlchemy()
login_manager = LoginManager()

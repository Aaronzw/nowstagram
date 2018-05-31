from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
#jinja语言拓展
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
#flash消息需要
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)
#登录模块初始化
login_manager=LoginManager(app)
login_manager.login_view='/regloginpage/'
from nowstagram import views, models

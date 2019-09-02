import os

from flask import Flask
from .views import blog, admin
from .exts import init_exts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)
    # 配置静态文件
    static_path = os.path.join(BASE_DIR,'static')
    template_path = os.path.join(BASE_DIR,'templates')
    print(static_path)

    #添加静态文件路径、和模板路径
    app = Flask(__name__,static_folder=static_path,template_folder=template_path)

    # 配置数据库
    db_uri = 'mysql+pymysql://root:rock1204@localhost:3306/blogdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 注册路由
    # 【前缀，命令空间】
    # app.register_blueprint(blueprint=blog,url_prefix='/blog')  # 注册蓝图
    # app.register_blueprint(blueprint=admin,url_prefix='/admin')  # 注册蓝图
    # 【注册路由】
    app.register_blueprint(blueprint=blog)
    app.register_blueprint(blueprint=admin)

    init_exts(app)  # 初始化插件

    return app


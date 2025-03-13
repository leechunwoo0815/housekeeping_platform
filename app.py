from flask import Flask
from config import Config  # 导入配置
from extensions import db, migrate, jwt  # 导入扩展
# 导入蓝图
from views.users import users_bp
from views.services import services_bp
from views.orders import orders_bp
from views.payments import payments_bp
from views.notifications import notifications_bp
from views.admin import admin_bp, admin, admin_index_view  # 修改，导入 admin_index_view
from views.support import support_bp
from views.marketing import marketing_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    admin.init_app(app)  # 初始化 flask-admin 实例，**注意这里不再注册 admin 实例为蓝图**

    # 注册蓝图
    app.register_blueprint(users_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp, name='admin_module')  # 注册我们自定义的 admin_bp 蓝图, 并指定 name='admin_module'
    app.register_blueprint(marketing_bp)
    app.register_blueprint(support_bp)
    # 添加这行代码
    app.add_url_rule('/', view_func=admin_index_view, methods=['GET'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # 开启调试模式 (仅限开发环境)

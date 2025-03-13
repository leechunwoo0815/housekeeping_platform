from flask import Blueprint, redirect, url_for, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from extensions import db
from models.user import User
from models.service import ServiceCategory, ServiceItem, ServiceProvider
from models.order import Order, OrderReview
from models.marketing import Coupon, UserCoupon
from models.support import FAQ
from flask_jwt_extended import  get_jwt_identity  # 移除 jwt_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 自定义Admin主页视图
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    #@jwt_required()  # 移除 JWT 认证
    def index(self):
        # 简单权限控制示例: 只有管理员可以访问
        #current_user_id = get_jwt_identity() #移除
        #user = User.query.get(current_user_id)  # 移除

        # 修改权限控制逻辑，直接查询 admin@example.com 用户
        user = User.query.filter_by(email="admin@example.com").first()

        if not user : #假设管理员邮箱是这个
             return redirect(url_for('users.login'))
        return self.render('admin/index.html')

# 创建Admin实例
admin = Admin(name='家政服务平台管理后台', template_mode='bootstrap4', index_view=MyAdminIndexView())

# 获取视图函数
admin_index_view = admin.index_view.index # 添加这行代码

# 自定义ModelView (可选)
class MyModelView(ModelView):
    # can_create = False  # 禁止创建
    # can_edit = False  # 禁止编辑
    # can_delete = False  # 禁止删除
    # column_list = [...]  # 显示的列
    # form_excluded_columns = [...]  # 表单中排除的列
    def is_accessible(self):  # 4 个空格缩进
        user = User.query.filter_by(email="admin@example.com").first()  # 8 个空格缩进
        # 超级管理员
        return user is not None  # 8 个空格缩进

    def inaccessible_callback(self, name, **kwargs):  # 4 个空格缩进
        # 无权限访问时重定向到登录
        return redirect(url_for('users.login', next=request.url))  # 8 个空格缩进



# 添加模型视图
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(ServiceCategory, db.session))
admin.add_view(MyModelView(ServiceItem, db.session))
admin.add_view(MyModelView(ServiceProvider, db.session))
admin.add_view(MyModelView(Order, db.session))
admin.add_view(MyModelView(OrderReview, db.session))
admin.add_view(MyModelView(Coupon, db.session))
admin.add_view(MyModelView(UserCoupon, db.session))
admin.add_view(MyModelView(FAQ, db.session))

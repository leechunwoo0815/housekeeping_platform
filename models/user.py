from extensions import db
from datetime import datetime

class User(db.Model):
    """用户模型类
    用于存储和管理系统用户的基本信息
    """
    # 用户ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，唯一且不能为空
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 电子邮箱，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 密码，不能为空
    password = db.Column(db.String(255), nullable=False)
    # 手机号码，唯一
    phone = db.Column(db.String(20), unique=True)
    # 用户头像URL
    avatar = db.Column(db.String(255))
    # 账户是否激活，默认为True
    is_active = db.Column(db.Boolean, default=True)
    # 账户创建时间，默认为当前UTC时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 与地址模型建立一对多关系
    addresses = db.relationship('Address', backref='user', lazy=True)

    def __repr__(self):
        """返回用户对象的字符串表示"""
        return f'<User {self.username}>'

class Address(db.Model):
    """地址模型类
    用于存储用户的收货地址信息
    """
    # 地址ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 关联的用户ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 省份
    province = db.Column(db.String(50), nullable=False)
    # 城市
    city = db.Column(db.String(50), nullable=False)
    # 区/县
    district = db.Column(db.String(50), nullable=False)
    # 详细地址
    detail_address = db.Column(db.String(255), nullable=False)
    # 联系电话
    phone = db.Column(db.String(20), nullable=False)
    # 收货人姓名
    name = db.Column(db.String(100))

from extensions import db
from datetime import datetime
import random

class Order(db.Model):
    """订单模型类
    用于存储和管理用户的服务订单信息
    """
    # 订单ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 订单号，唯一且不能为空
    order_no = db.Column(db.String(255), unique=True, nullable=False)
    # 关联的用户ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 关联的服务项目ID，外键
    service_item_id = db.Column(db.Integer, db.ForeignKey('service_item.id'), nullable=False)
    # 关联的服务提供者ID，外键
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'), nullable=False)
    # 订单总金额
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    # 实际支付金额
    paid_amount = db.Column(db.Numeric(10, 2))
    # 订单状态
    status = db.Column(db.String(50), nullable=False)
    # 预约服务时间
    appointment_time = db.Column(db.DateTime, nullable=False)
    # 服务地址
    address = db.Column(db.String(255), nullable=False)
    # 订单备注
    remark = db.Column(db.Text)
    # 订单创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 订单更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 支付方式
    pay_method = db.Column(db.String(50))
    # 支付时间
    paid_at = db.Column(db.DateTime)

    # 建立与用户、服务项目、服务提供者的关系
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    service_item = db.relationship('ServiceItem', backref=db.backref('orders', lazy=True))
    service_provider = db.relationship('ServiceProvider', backref=db.backref('orders', lazy=True))

    def generate_order_no(self):
        """生成订单号
        使用时间戳+用户ID+随机数的方式生成唯一订单号
        """
        self.order_no = f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}{self.user_id:04d}{str(random.randint(1000, 9999))}'

    def __repr__(self):
        return f'<Order {self.order_no}>'

class OrderReview(db.Model):
    """订单评价模型类
    用于存储用户对服务的评价信息
    """
    # 评价ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 关联的订单ID，外键
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    # 评价用户ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 被评价的服务提供者ID，外键
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'), nullable=False)
    # 评分（1-5分）
    rating = db.Column(db.Integer, nullable=False)
    # 评价内容
    comment = db.Column(db.Text)
    # 评价图片，多个URL用逗号分隔
    images = db.Column(db.Text)
    # 评价创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 建立与订单、用户、服务提供者的关系
    order = db.relationship('Order', backref=db.backref('review', uselist=False))
    user = db.relationship('User')
    service_provider = db.relationship('ServiceProvider')


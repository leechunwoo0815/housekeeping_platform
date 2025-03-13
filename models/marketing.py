from extensions import db
from datetime import datetime, timedelta

class Coupon(db.Model):
    """优惠券模型类
    用于管理系统中的优惠券信息，包括折扣类型、使用条件等
    """
    # 优惠券ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 优惠券码，唯一且不能为空
    code = db.Column(db.String(50), unique=True, nullable=False)
    # 折扣类型：'percentage'（百分比）或'fixed'（固定金额）
    discount_type = db.Column(db.String(20), nullable=False)
    # 折扣值：百分比折扣时为1-100的数字，固定金额时为具体金额
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    # 优惠券生效开始时间
    start_date = db.Column(db.DateTime, nullable=False)
    # 优惠券失效结束时间
    end_date = db.Column(db.DateTime, nullable=False)
    # 优惠券是否激活，默认为True
    is_active = db.Column(db.Boolean, default=True)
    # 使用优惠券需要的最低消费金额
    min_spend = db.Column(db.Numeric(10, 2))
    # 最大折扣金额，防止百分比折扣时优惠金额过大
    max_discount = db.Column(db.Numeric(10, 2))
    # 每个用户的使用次数限制
    usage_limit = db.Column(db.Integer)

    def is_valid(self):
        """检查优惠券是否有效
        
        Returns:
            bool: 优惠券在有效期内且处于激活状态返回True，否则返回False
        """
        now = datetime.utcnow()
        return self.is_active and self.start_date <= now <= self.end_date

class UserCoupon(db.Model):
    """用户优惠券关联模型类
    用于记录用户领取和使用优惠券的情况
    """
    # 记录ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 关联的用户ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 关联的优惠券ID，外键
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=False)
    # 优惠券使用时间，未使用时为空
    used_at = db.Column(db.DateTime)
    
    # 建立与用户和优惠券的关系
    user = db.relationship('User', backref=db.backref('coupons', lazy=True))
    coupon = db.relationship('Coupon')

from marshmallow import Schema, fields
from datetime import datetime

class CouponSchema(Schema):
    """优惠券序列化模式类
    用于将优惠券模型实例序列化为JSON格式，或将JSON数据反序列化为优惠券模型实例
    """
    # 优惠券ID，仅用于序列化输出
    id = fields.Integer(dump_only=True)
    # 优惠券码，必填字段
    code = fields.String(required=True)
    # 折扣类型，必填字段
    discount_type = fields.String(required=True)
    # 折扣值，必填字段
    discount_value = fields.Decimal(required=True)
    # 生效开始时间，必填字段
    start_date = fields.DateTime(required=True)
    # 失效结束时间，必填字段
    end_date = fields.DateTime(required=True)
    # 是否激活
    is_active = fields.Boolean()
    # 最低消费金额
    min_spend = fields.Decimal()
    # 最大折扣金额
    max_discount = fields.Decimal()
    # 使用次数限制
    usage_limit = fields.Integer()

class UserCouponSchema(Schema):
    """用户优惠券关联序列化模式类
    用于将用户优惠券关联模型实例序列化为JSON格式，或将JSON数据反序列化为用户优惠券关联模型实例
    """
    # 记录ID，仅用于序列化输出
    id = fields.Integer(dump_only=True)
    # 用户ID，必填字段
    user_id = fields.Integer(required=True)
    # 优惠券ID，必填字段
    coupon_id = fields.Integer(required=True)
    # 使用时间
    used_at = fields.DateTime()
    # 嵌套优惠券信息
    coupon = fields.Nested(CouponSchema)

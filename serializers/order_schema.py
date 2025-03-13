from marshmallow import Schema, fields
from .service_schema import ServiceItemSchema, ServiceProviderSchema
from .user_schema import UserSchema

class OrderSchema(Schema):
    """订单序列化模式类
    用于将订单模型实例序列化为JSON格式，或将JSON数据反序列化为订单模型实例
    """
    # 订单ID，仅用于序列化输出
    id = fields.Int(dump_only=True)
    # 订单号，仅用于序列化输出
    order_no = fields.Str(dump_only=True)
    # 用户ID，必填字段
    user_id = fields.Int(required=True)
    # 服务项目ID，必填字段
    service_item_id = fields.Int(required=True)
    # 订单总金额，必填字段
    total_amount = fields.Decimal(required=True)
    # 实际支付金额
    paid_amount = fields.Decimal()
    # 订单状态，必填字段
    status = fields.Str(required=True)
    # 预约服务时间，必填字段
    appointment_time = fields.DateTime(required=True)
    # 服务地址
    address = fields.Str()
    # 订单备注
    remark = fields.Str()
    # 创建时间，仅用于序列化输出
    created_at = fields.DateTime(dump_only=True)
    # 更新时间，仅用于序列化输出
    updated_at = fields.DateTime(dump_only=True)
    # 支付方式
    pay_method = fields.String()
    # 支付时间
    paid_at = fields.DateTime()
    # 嵌套用户信息，仅用于序列化输出
    user = fields.Nested(UserSchema, dump_only=True)
    # 嵌套服务项目信息，仅用于序列化输出
    service_item = fields.Nested(ServiceItemSchema, dump_only=True)
    # 服务提供者ID，必填字段
    service_provider_id = fields.Integer(required=True)

class OrderReviewSchema(Schema):
    """订单评价序列化模式类
    用于将订单评价模型实例序列化为JSON格式，或将JSON数据反序列化为订单评价模型实例
    """
    # 评价ID，仅用于序列化输出
    id = fields.Integer(dump_only=True)
    # 关联的订单ID，必填字段
    order_id = fields.Integer(required=True)
    # 评价用户ID，必填字段
    user_id = fields.Integer(required=True)
    # 被评价的服务提供者ID，必填字段
    service_provider_id = fields.Integer(required=True)
    # 评分（1-5分），必填字段
    rating = fields.Integer(required=True, validate=lambda n: 1 <= n <= 5)
    # 评价内容
    comment = fields.String()
    # 评价图片，多个URL用逗号分隔
    images = fields.String()
    # 评价创建时间，仅用于序列化输出
    created_at = fields.DateTime(dump_only=True)
    # 嵌套订单信息，仅用于序列化输出
    order = fields.Nested(OrderSchema, dump_only=True)
    # 嵌套用户信息，仅用于序列化输出
    user = fields.Nested(UserSchema, dump_only = True)
    # 嵌套服务提供者信息，仅用于序列化输出
    service_provider = fields.Nested(ServiceProviderSchema, dump_only = True)

from marshmallow import Schema, fields

class ServiceCategorySchema(Schema):
    """服务类别序列化模式类
    用于将服务类别模型实例序列化为JSON格式，或将JSON数据反序列化为服务类别模型实例
    """
    # 类别ID，仅用于序列化输出
    id = fields.Int(dump_only=True)
    # 类别名称，必填字段
    name = fields.Str(required=True)
    # 父类别ID，允许为空
    parent_id = fields.Int(allow_none=True)
    # 类别图标URL
    icon = fields.Str()
    # 子类别列表，仅用于序列化输出
    children = fields.List(fields.Nested('ServiceCategorySchema'), dump_only=True)

class ServiceItemSchema(Schema):
    """服务项目序列化模式类
    用于将服务项目模型实例序列化为JSON格式，或将JSON数据反序列化为服务项目模型实例
    """
    # 服务项目ID，仅用于序列化输出
    id = fields.Int(dump_only=True)
    # 所属类别ID，必填字段
    category_id = fields.Int(required=True)
    # 服务项目标题，必填字段
    title = fields.Str(required=True)
    # 服务项目描述
    description = fields.Str()
    # 服务价格，必填字段
    price = fields.Decimal(required=True)
    # 计价单位
    unit = fields.Str()
    # 服务项目图片，多个URL用逗号分隔
    images = fields.Str()
    # 是否在售
    is_on_sale = fields.Bool()
    # 创建时间，仅用于序列化输出
    created_at = fields.DateTime(dump_only=True)
    # 更新时间，仅用于序列化输出
    updated_at = fields.DateTime(dump_only=True)
    # 嵌套服务类别信息，仅用于序列化输出
    category = fields.Nested(ServiceCategorySchema, dump_only=True)
    # 关联的服务提供者ID
    service_provider_id = fields.Integer()

class ServiceProviderSchema(Schema):
    """服务提供者序列化模式类
    用于将服务提供者模型实例序列化为JSON格式，或将JSON数据反序列化为服务提供者模型实例
    """
    # 服务提供者ID，仅用于序列化输出
    id = fields.Integer(dump_only=True)
    # 关联的用户ID，必填字段
    user_id = fields.Integer(required=True)
    # 真实姓名，必填字段
    real_name = fields.String(required=True)
    # 身份证号，必填字段
    id_card = fields.String(required=True)
    # 联系电话，必填字段
    phone = fields.String(required=True)
    # 居住地址
    address = fields.String()
    # 工作经验描述
    experience = fields.String()
    # 资质证书，多个URL用逗号分隔
    certificates = fields.String()
    # 是否已通过验证
    is_verified = fields.Boolean()
    # 审核状态
    status = fields.String()
    # 创建时间，仅用于序列化输出
    created_at = fields.DateTime(dump_only=True)
    # 更新时间，仅用于序列化输出
    updated_at = fields.DateTime(dump_only=True)

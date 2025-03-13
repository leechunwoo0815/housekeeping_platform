from marshmallow import Schema, fields

class FAQSchema(Schema):
    """FAQ序列化模式类
    用于将FAQ模型实例序列化为JSON格式，或将JSON数据反序列化为FAQ模型实例
    """
    # FAQ记录的唯一标识符
    id = fields.Integer()
    # FAQ问题字段，必填
    question = fields.String(required = True)
    # FAQ答案字段，必填
    answer = fields.String(required = True)

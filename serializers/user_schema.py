from marshmallow import Schema, fields, validate

class AddressSchema(Schema):
    id = fields.Int(dump_only=True)
    province = fields.Str(required=True)
    city = fields.Str(required=True)
    district = fields.Str(required=True)
    detail_address = fields.Str(required=True)
    phone = fields.Str(required=True)
    name = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # 只在序列化时包含
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    avatar = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    addresses = fields.List(fields.Nested(AddressSchema))
    # 密码不应该被序列化


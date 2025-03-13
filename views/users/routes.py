"""用户管理模块，提供用户注册、登录和地址管理等功能

主要功能：
1. 用户注册：新用户注册账号
2. 用户登录：账号登录并获取访问令牌
3. 个人信息：获取用户个人信息
4. 地址管理：添加和查询用户地址
"""

from flask import request, jsonify
from . import users_bp
from models.user import User, Address
from serializers.user_schema import UserSchema, AddressSchema
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.helpers import is_valid_email, is_valid_phone

@users_bp.route('/register', methods=['POST'])
def register():
    """用户注册
    
    新用户注册账号，需提供用户名、邮箱、手机号和密码
    
    请求参数：
        username: 用户名（至少3个字符）
        email: 邮箱地址
        phone: 手机号
        password: 密码（至少6个字符）
        
    返回值：
        成功：返回新创建的用户信息，状态码201
        失败：返回错误信息和对应状态码
    """
    data = request.get_json()

    # 1. 数据验证 (更全面的验证)
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if not is_valid_email(data.get('email')):
        return jsonify({'message': 'Invalid email format'}), 400

    if not is_valid_phone(data.get('phone')):
        return jsonify({'message': 'Invalid phone number format'}), 400

    if not data.get('username') or len(data.get('username')) < 3:
         return jsonify({'message':'username at least 3 characters'}),400

    if not data.get('password') or len(data.get('password')) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400

    # 2. 检查邮箱是否已注册
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    # 3. 检查电话是否已注册
    existing_phone = User.query.filter_by(phone=data['phone']).first()
    if existing_phone:
        return jsonify({'message':'Phone number already registered'}), 400

    # 4. 创建用户
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()
    return jsonify(user_schema.dump(new_user)), 201

@users_bp.route('/login', methods=['POST'])
def login():
    """用户登录
    
    用户使用邮箱和密码登录，成功后返回访问令牌
    
    请求参数：
        email: 邮箱地址
        password: 密码
        
    返回值：
        成功：返回访问令牌，状态码200
        失败：返回错误信息，状态码401
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """获取用户个人信息
    
    获取当前登录用户的详细信息
    
    返回值：
        成功：返回用户个人信息，状态码200
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/address', methods=['POST'])
@jwt_required()
def add_address():
    """添加收货地址
    
    为当前登录用户添加新的收货地址
    
    请求参数：
        province: 省份
        city: 城市
        district: 区县
        detail_address: 详细地址
        phone: 联系电话
        name: 收货人姓名（可选）
        
    返回值：
        成功：返回新创建的地址信息，状态码201
        失败：返回错误信息和对应状态码
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    #数据验证
    if not is_valid_phone(data.get('phone')):
        return jsonify({'message': 'Invalid phone format'}),400
    # 创建地址
    new_address = Address(
        user_id=current_user_id,
        province=data['province'],
        city=data['city'],
        district=data['district'],
        detail_address=data['detail_address'],
        phone=data['phone'],
        name = data.get('name')
    )
    db.session.add(new_address)
    db.session.commit()

    address_schema = AddressSchema()
    return jsonify(address_schema.dump(new_address)), 201

@users_bp.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    """获取用户地址列表
    
    获取当前登录用户的所有收货地址
    
    返回值：
        成功：返回用户的地址列表，状态码200
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    address_schema = AddressSchema(many=True)
    return jsonify(address_schema.dump(user.addresses)),200

# 其他用户相关视图函数... (修改密码、获取用户信息等)


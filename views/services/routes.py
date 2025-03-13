"""服务管理模块，提供服务类别、服务项目和服务人员相关功能

主要功能：
1. 服务类别：获取所有服务类别
2. 服务项目：查询和添加服务项目
3. 服务人员：服务人员注册
"""

from flask import request, jsonify
from . import services_bp
from models.service import ServiceCategory, ServiceItem, ServiceProvider
from serializers.service_schema import ServiceCategorySchema, ServiceItemSchema, ServiceProviderSchema
from extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity

@services_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有服务类别
    
    返回值：
        成功：返回所有服务类别列表，状态码200
    """
    categories = ServiceCategory.query.all()
    category_schema = ServiceCategorySchema(many=True)
    return jsonify(category_schema.dump(categories)), 200

@services_bp.route('/items', methods=['GET'])
def get_items():
    """获取服务项目列表
    
    支持按类别筛选和分页查询
    
    查询参数：
        category_id: 服务类别ID（可选）
        page: 页码（可选，默认1）
        per_page: 每页数量（可选，默认10）
        
    返回值：
        成功：返回分页的服务项目列表，状态码200
    """
    # 获取查询参数 (例如: category_id, page, per_page)
    category_id = request.args.get('category_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = ServiceItem.query
    if category_id:
        query = query.filter_by(category_id=category_id)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    item_schema = ServiceItemSchema(many=True)
    return jsonify({
        'items': item_schema.dump(items.items),
        'page': items.page,
        'per_page': items.per_page,
        'total': items.total
    }), 200

#添加服务（服务人员专属）
@services_bp.route('/items', methods=['POST'])
@jwt_required()
def add_service_item():
    """添加服务项目
    
    仅限服务人员添加自己提供的服务项目
    
    请求参数：
        category_id: 服务类别ID
        title: 服务标题
        description: 服务描述（可选）
        price: 服务价格
        unit: 计价单位
        images: 服务图片URL列表（可选）
        is_on_sale: 是否上架（可选，默认True）
        
    返回值：
        成功：返回新创建的服务项目信息，状态码201
        失败：返回错误信息和对应状态码
    """
    current_user_id = get_jwt_identity()

    # 1. 检查当前用户是否是服务人员
    service_provider = ServiceProvider.query.filter_by(user_id=current_user_id).first()
    if not service_provider:
        return jsonify({'message': 'Only service providers can add service items'}), 403

    data = request.get_json()
    # 2. 数据验证
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    # 必填字段
    required_fields = ['category_id', 'title', 'price', 'unit']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f"Missing required field: {field}"}), 400

    # 3. 创建服务项目
    new_item = ServiceItem(
        category_id=data['category_id'],
        title=data['title'],
        description=data.get('description'),
        price=data['price'],
        unit=data['unit'],
        images=data.get('images'),  # 假设前端上传图片URL，多个用逗号分隔
        is_on_sale=data.get('is_on_sale', True),  # 默认上架
        service_provider_id = service_provider.id #关联服务人员
    )
    db.session.add(new_item)
    db.session.commit()

    item_schema = ServiceItemSchema()
    return jsonify(item_schema.dump(new_item)),201

#服务人员注册
@services_bp.route('/providers/register', methods=['POST'])
@jwt_required()
def register_service_provider():
    """服务人员注册
    
    用户注册成为服务人员，提供个人信息和资质证明
    
    请求参数：
        real_name: 真实姓名
        id_card: 身份证号
        phone: 联系电话
        address: 联系地址
        experience: 工作经验（可选）
        certificates: 资质证书URL列表（可选）
        
    返回值：
        成功：返回新创建的服务人员信息，状态码201
        失败：返回错误信息和对应状态码
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # 1. 检查用户是否已经注册过服务人员
    existing_provider = ServiceProvider.query.filter_by(user_id=current_user_id).first()
    if existing_provider:
        return jsonify({'message': 'User already registered as a service provider'}), 400

    # 2. 数据验证 (简化示例，根据实际需求添加更多验证)
    required_fields = ['real_name', 'id_card', 'phone', 'address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400

    # 3. 创建服务人员记录
    new_provider = ServiceProvider(
        user_id=current_user_id,
        real_name=data['real_name'],
        id_card=data['id_card'],
        phone=data['phone'],
        address=data['address'],
        experience=data.get('experience'),
        certificates=data.get('certificates'),  # 假设前端上传证书URL，多个用逗号分隔
        # is_verified 和 status 默认值已在模型中定义
    )
    db.session.add(new_provider)
    db.session.commit()
    provider_schema = ServiceProviderSchema()
    return jsonify(provider_schema.dump(new_provider)), 201

# 其他服务相关视图函数... (创建、编辑、删除服务等)


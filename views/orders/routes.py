"""订单管理模块，提供订单的创建、查询、取消和评价等功能

主要功能：
1. 创建订单：用户选择服务项目并提交订单
2. 查询订单：获取订单详细信息
3. 取消订单：允许用户在特定条件下取消订单
4. 订单评价：用户对已完成的订单进行评价
"""

from flask import request, jsonify
from . import orders_bp
from models.order import Order, OrderReview
from models.service import ServiceItem
from serializers.order_schema import OrderSchema, OrderReviewSchema
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from utils.helpers import format_datetime

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """创建新订单
    
    用户选择服务项目并提交订单信息，系统验证后创建新订单
    
    请求参数：
        service_item_id: 服务项目ID
        appointment_time: 预约时间
        address: 服务地址
        
    返回值：
        成功：返回新创建的订单信息，状态码201
        失败：返回错误信息和对应的状态码
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # 1. 数据验证
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    required_fields = ['service_item_id', 'appointment_time','address']
    for field in required_fields:
        if field not in data:
            return jsonify({'message':f'Missing required field:{field}'}),400

    # 2. 检查服务项目是否存在
    service_item = ServiceItem.query.get(data['service_item_id'])
    if not service_item:
        return jsonify({'message': 'Service item not found'}), 404
    # 3. 服务是否下架
    if not service_item.is_on_sale:
        return jsonify({'message':'Service item is currently not on sale'}),400

    # 4. 创建订单
    new_order = Order(
        user_id=current_user_id,
        service_item_id=data['service_item_id'],
        service_provider_id = service_item.service_provider_id, # 从服务中获取服务提供者ID
        total_amount=service_item.price,  # 简化处理，假设总价等于服务单价
        appointment_time=data['appointment_time'],
        address = data['address'],
        status='pending' # 新订单状态为待支付
    )
    # 生成订单号
    new_order.generate_order_no()

    db.session.add(new_order)
    db.session.commit()

    order_schema = OrderSchema()
    return jsonify(order_schema.dump(new_order)), 201

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """获取订单详情
    
    根据订单ID获取订单的详细信息，只能获取属于当前用户的订单
    
    参数：
        order_id: 订单ID
        
    返回值：
        成功：返回订单详细信息
        失败：返回错误信息和404状态码
    """
    current_user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order_schema = OrderSchema()
    return jsonify(order_schema.dump(order)), 200

@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """取消订单
    
    允许用户取消未支付或未完成的订单
    
    参数：
        order_id: 要取消的订单ID
        
    返回值：
        成功：返回成功消息
        失败：返回错误信息和对应状态码
    """
    current_user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id = current_user_id).first()

    # 1. 订单是否存在
    if not order:
        return jsonify({'message':'Order not found'}), 404

    # 2. 订单是否可以取消 (例如，已完成或已支付的订单可能不能取消)
    if order.status in ('completed', 'paid'):
        return jsonify({'message':'Order cannot be cancelled'}), 400
    
    # 3. 取消订单
    order.status = 'cancelled'
    db.session.commit()

    return jsonify({'message':'Order cancelled successfully'}),200

@orders_bp.route('/<int:order_id>/review', methods=['POST'])
@jwt_required()
def create_review(order_id):
    """创建订单评价
    
    允许用户对已完成的订单进行评价，包括评分和评论
    
    参数：
        order_id: 要评价的订单ID
    请求数据：
        rating: 评分（必填）
        comment: 评价内容（必填）
        images: 评价图片URL列表（可选）
        
    返回值：
        成功：返回创建的评价信息，状态码201
        失败：返回错误信息和对应状态码
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # 1. 检查订单是否存在且属于当前用户
    order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # 2. 检查订单是否已完成 (只有已完成的订单才能评价)
    if order.status != 'completed':
        return jsonify({'message': 'Only completed orders can be reviewed'}), 400
    
    # 3. 检查是否已经评价过
    existing_review = OrderReview.query.filter_by(order_id = order_id).first()
    if existing_review:
        return jsonify({'message':'Order already reviewed'}), 400

    # 4. 数据验证 (简化，根据需要添加更多验证)
    required_fields = ['rating', 'comment']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400

    # 5. 创建评价
    new_review = OrderReview(
        order_id=order_id,
        user_id=current_user_id,
        service_provider_id = order.service_provider_id,
        rating=data['rating'],
        comment=data['comment'],
        images=data.get('images')  # 假设前端上传图片URL，多个用逗号分隔
    )
    db.session.add(new_review)
    db.session.commit()

    review_schema = OrderReviewSchema()
    return jsonify(review_schema.dump(new_review)), 201

# 其他订单相关视图函数... (获取订单列表、取消订单、订单支付回调等)


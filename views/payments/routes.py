"""支付模块，提供订单支付和支付回调处理等功能

主要功能：
1. 创建支付：生成订单支付请求
2. 支付回调：处理第三方支付平台的支付结果
"""

from flask import request, jsonify
from . import payments_bp
from models.order import Order
from extensions import db
# 假设的支付工具函数
from utils.pay_utils import create_payment, handle_payment_callback
from flask_jwt_extended import jwt_required, get_jwt_identity

@payments_bp.route('/create', methods=['POST'])
@jwt_required()
def create_payment_request():
    """创建支付请求
    
    为指定订单创建支付请求，生成支付URL
    
    请求参数：
        order_id: 订单ID
        
    返回值：
        成功：返回支付URL，状态码200
        失败：返回错误信息和对应状态码
    """
    # 获取请求数据
    data = request.get_json()
    order_id = data['order_id']
    # 获取当前登录用户ID
    current_user_id = get_jwt_identity()
    # 查询订单，确保订单属于当前用户
    order = Order.query.filter_by(id=order_id, user_id = current_user_id).first()

    # 检查订单是否存在
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    
    # 检查订单状态是否为待支付
    if order.status != 'pending':
        return jsonify({'message':'Order is not in pending state'}),400

    # 创建支付请求（这里只是模拟，实际应调用第三方支付SDK）
    # pay_url = create_payment(order.order_no, order.total_amount)
    pay_url = "https://example.com/pay" #模拟

    return jsonify({'pay_url': pay_url}), 200

@payments_bp.route('/callback', methods=['POST'])
def payment_callback():
    """支付回调处理
    
    处理第三方支付平台的支付结果回调，更新订单状态
    
    请求参数：
        order_no: 订单号
        status: 支付状态（success/failed）
        pay_method: 支付方式（可选）
        
    返回值：
        成功：返回处理成功消息，状态码200
        失败：返回错误信息和对应状态码
    """
    # 处理支付回调（这里只是模拟，实际应验证签名、处理支付结果）
    data = request.get_json()
    order_no = data['order_no']
    status = data['status']  # 'success' 或 'failed'

    # 查找对应的订单
    order = Order.query.filter_by(order_no=order_no).first()
    if order:
        if status == 'success':
            # 支付成功，更新订单状态
            order.status = 'paid'
            # 假设全额支付
            order.paid_amount = order.total_amount
            # 记录支付方式
            order.pay_method = data.get('pay_method','unknown')
            # 记录支付时间
            order.paid_at = datetime.datetime.now()
        # 提交数据库更改
        db.session.commit()

    # 实际的回调处理
    # handle_payment_callback(data)

    return jsonify({'message': 'Callback received'}), 200

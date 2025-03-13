"""营销模块，提供优惠券的创建和领取等功能

主要功能：
1. 创建优惠券：管理员创建各类优惠券
2. 领取优惠券：用户领取可用的优惠券
"""

from flask import jsonify, request
from . import marketing_bp
from models.marketing import Coupon, UserCoupon
from serializers.marketing_schema import CouponSchema, UserCouponSchema
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

@marketing_bp.route('/coupons', methods=['POST'])
@jwt_required()
def create_coupon():
    """创建优惠券
    
    管理员创建新的优惠券，设置优惠券的基本信息和使用规则
    
    请求参数：
        code: 优惠券码
        discount_type: 折扣类型
        discount_value: 折扣值
        start_date: 生效开始时间
        end_date: 失效结束时间
        is_active: 是否激活（可选，默认True）
        min_spend: 最低消费金额（可选）
        max_discount: 最大折扣金额（可选）
        usage_limit: 使用次数限制（可选）
        
    返回值：
        成功：返回新创建的优惠券信息，状态码201
        失败：返回错误信息和对应状态码
    """
    # 获取当前登录用户ID
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    # 权限验证（仅管理员可创建优惠券）
    if not user or user.email != "admin@example.com":
        return jsonify({'message':'Unauthorized'}), 403
    
    # 获取请求数据
    data = request.get_json()
    # 验证必填字段
    required = ['code', 'discount_type', 'discount_value', 'start_date', 'end_date']
    for r in required:
        if not data.get(r):
            return jsonify({'message':f'Missing required field: {r}'}), 400

    # 创建新的优惠券实例
    new_coupon = Coupon(
        code=data['code'],  # 优惠券码
        discount_type=data['discount_type'],  # 折扣类型
        discount_value=data['discount_value'],  # 折扣值
        start_date=data['start_date'],  # 生效开始时间
        end_date=data['end_date'],  # 失效结束时间
        is_active=data.get('is_active', True),  # 是否激活，默认为True
        min_spend=data.get('min_spend'),  # 最低消费金额
        max_discount=data.get('max_discount'),  # 最大折扣金额
        usage_limit=data.get('usage_limit')  # 使用次数限制
    )
    # 保存到数据库
    db.session.add(new_coupon)
    db.session.commit()

    # 序列化优惠券数据并返回
    coupon_schema = CouponSchema()
    return jsonify(coupon_schema.dump(new_coupon)), 201

@marketing_bp.route('/coupons/claim', methods=['POST'])
@jwt_required()
def claim_coupon():
    """领取优惠券
    
    用户领取系统中可用的优惠券
    
    请求参数：
        code: 优惠券码
        
    返回值：
        成功：返回用户领取的优惠券信息，状态码201
        失败：返回错误信息和对应状态码
    """
    # 获取当前登录用户ID
    current_user_id = get_jwt_identity()
    # 获取请求数据
    data = request.get_json()
    coupon_code = data.get('code')

    # 查找优惠券并验证是否存在且激活
    coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
    if not coupon:
        return jsonify({'message': 'Invalid or expired coupon code'}), 404

    # 检查优惠券是否在有效期内
    if not coupon.is_valid():
        return jsonify({'message': 'Coupon is expired or not active'}), 400

    # 检查用户是否已经领取过该优惠券
    existing_user_coupon = UserCoupon.query.filter_by(user_id=current_user_id, coupon_id=coupon.id).first()
    if existing_user_coupon:
        return jsonify({'message': 'User has already claimed this coupon'}), 400

    # 创建用户优惠券关联记录
    user_coupon = UserCoupon(user_id=current_user_id, coupon_id=coupon.id)
    db.session.add(user_coupon)
    db.session.commit()

    # 序列化用户优惠券数据并返回
    user_coupon_schema = UserCouponSchema()
    return jsonify(user_coupon_schema.dump(user_coupon)), 201


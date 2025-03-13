"""通知模块，提供短信验证码发送等功能

主要功能：
1. 短信验证码：发送手机验证码
"""

from flask import request, jsonify
from . import notifications_bp
# 假设的短信发送工具函数
from utils.sms_utils import send_sms
from utils.helpers import generate_random_code

@notifications_bp.route('/send_sms', methods=['POST'])
def send_sms_route():
    """发送短信验证码
    
    向指定手机号发送随机生成的验证码
    
    请求参数：
        phone: 接收验证码的手机号
        
    返回值：
        成功：返回发送成功消息，状态码200
        失败：返回错误信息，状态码500
    """
    # 获取请求数据
    data = request.get_json()
    # 获取手机号
    phone = data['phone']
    # 生成随机验证码
    code = generate_random_code()

    # 发送短信（这里只是模拟）
    # 实际应用中需要调用真实的短信服务提供商API
    result = send_sms(phone, code)
    
    # 根据发送结果返回相应的响应
    if result:
        return jsonify({'message': 'SMS sent successfully'}), 200
    else:
        return jsonify({'message': 'Failed to send SMS'}), 500

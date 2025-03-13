from flask import jsonify
from . import support_bp
from models.support import FAQ
from serializers.support_schema import FAQSchema
from extensions import db

@support_bp.route('/faq', methods = ['GET'])
def get_faq():
    """获取所有常见问题列表的API端点
    
    Returns:
        tuple: 包含FAQ列表的JSON响应和HTTP状态码
    """
    # 查询数据库中的所有FAQ记录
    faqs = FAQ.query.all()
    # 创建FAQ序列化器实例，设置many=True表示序列化多个对象
    faq_schema = FAQSchema(many = True)
    # 将FAQ对象列表序列化为JSON格式并返回，状态码200表示成功
    return jsonify(faq_schema.dump(faqs)), 200

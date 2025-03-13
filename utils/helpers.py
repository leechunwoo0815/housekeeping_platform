import re
from datetime import datetime
import random

def is_valid_email(email):
    """验证邮箱格式
    
    Args:
        email: 需要验证的邮箱地址
        
    Returns:
        bool: 邮箱格式正确返回True，否则返回False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """验证手机号格式（简单示例，根据实际需求修改）
    
    Args:
        phone: 需要验证的手机号
        
    Returns:
        bool: 手机号格式正确返回True，否则返回False
    """
    pattern = r'^1[3456789]\d{9}$'
    return re.match(pattern, phone) is not None

def generate_random_code(length=6):
    """生成指定长度的随机验证码（数字）
    
    Args:
        length: 验证码长度，默认为6位
        
    Returns:
        str: 生成的随机验证码
    """
    return ''.join(random.choices('0123456789', k=length))

def format_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间
    
    Args:
        dt: 要格式化的datetime对象
        format: 格式化模板，默认为'%Y-%m-%d %H:%M:%S'
        
    Returns:
        str: 格式化后的日期时间字符串，如果输入不是datetime对象则返回None
    """
    if isinstance(dt, datetime):
        return dt.strftime(format)
    return None

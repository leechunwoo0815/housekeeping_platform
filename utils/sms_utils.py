# 模拟发送
def send_sms(phone, code):
    """发送短信验证码（模拟）
    
    Args:
        phone: 接收短信的手机号
        code: 要发送的验证码
        
    Returns:
        bool: 发送成功返回True，否则返回False
        
    Note:
        这是一个模拟函数，实际应用中需要集成真实的短信服务提供商API
    """
    print(f"Sending SMS to {phone}: Code is {code}")
    return True

import datetime

def create_payment(order_no, amount, subject):
    """创建支付请求（模拟）
    
    Args:
        order_no: 订单号
        amount: 支付金额
        subject: 支付主题
        
    Returns:
        str: 支付URL，实际应用中应返回第三方支付平台的支付链接
    """
    print(f"Create payment request: order_no={order_no}, amount={amount}, subject={subject}")
    return "https://example.com/pay"

def handle_payment_callback(data):
    """处理支付回调（模拟）
    
    Args:
        data: 支付回调数据
        
    Returns:
        bool: 处理成功返回True，否则返回False
    """
    print(f"Handle payment callback: {data}")
    return True

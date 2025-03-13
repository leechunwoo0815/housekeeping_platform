import pytest
from datetime import datetime
from models import Order, User, Service

def test_create_order(db_session):
    """测试创建订单"""
    user = User(username='test_user', email='test@example.com')
    service = Service(name='测试服务', price=100.0)
    
    db_session.session.add(user)
    db_session.session.add(service)
    db_session.session.commit()

    order = Order(
        user_id=user.id,
        service_id=service.id,
        status='pending',
        scheduled_time=datetime.utcnow(),
        address='测试地址',
        total_price=100.0
    )
    db_session.session.add(order)
    db_session.session.commit()

    assert order.id is not None
    assert order.user_id == user.id
    assert order.service_id == service.id
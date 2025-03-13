import pytest
from models import User

def test_create_user(db_session):
    """测试创建用户"""
    user = User(
        username='test_user',
        email='test@example.com',
        phone='1234567890'
    )
    db_session.session.add(user)
    db_session.session.commit()

    assert user.id is not None
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.phone == '1234567890'
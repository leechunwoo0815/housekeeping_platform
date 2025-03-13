import pytest
from models import Service

def test_create_service(db_session):
    """测试创建服务"""
    service = Service(
        name='家庭保洁',
        description='专业的家庭保洁服务',
        price=100.0,
        duration=120,
        category='清洁'
    )
    db_session.session.add(service)
    db_session.session.commit()

    assert service.id is not None
    assert service.name == '家庭保洁'
    assert service.price == 100.0
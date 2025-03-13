from extensions import db
from datetime import datetime

class ServiceCategory(db.Model):
    """服务类别模型
    用于管理服务项目的分类信息，支持多级分类
    """
    # 类别ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 类别名称，唯一且不能为空
    name = db.Column(db.String(255), unique=True, nullable=False)
    # 父类别ID，外键，可以为空（顶级类别）
    parent_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=True)
    # 类别图标URL
    icon = db.Column(db.String(255))
    # 与子类别建立自引用关系
    children = db.relationship("ServiceCategory", backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<ServiceCategory {self.name}>'

class ServiceItem(db.Model):
    """服务项目模型
    用于存储具体服务项目的详细信息
    """
    # 服务项目ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 所属类别ID，外键
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    # 服务项目标题
    title = db.Column(db.String(255), nullable=False)
    # 服务项目描述
    description = db.Column(db.Text)
    # 服务价格
    price = db.Column(db.Numeric(10, 2), nullable=False)
    # 计价单位（如：次、小时等）
    unit = db.Column(db.String(50))
    # 服务项目图片，多个URL用逗号分隔
    images = db.Column(db.Text)
    # 是否在售，默认为True
    is_on_sale = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 与服务类别建立关系
    category = db.relationship('ServiceCategory', backref=db.backref('items', lazy=True))

    # 关联的服务提供者ID，外键
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'))
    # 与服务提供者建立关系
    service_provider = db.relationship('ServiceProvider', backref='services')

    def __repr__(self):
        return f'<ServiceItem {self.title}>'
    
class ServiceProvider(db.Model):
    """服务提供者模型
    用于存储家政服务人员的详细信息
    """
    # 服务提供者ID，主键
    id = db.Column(db.Integer, primary_key=True)
    # 关联的用户ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 真实姓名
    real_name = db.Column(db.String(255), nullable=False)
    # 身份证号，唯一且不能为空
    id_card = db.Column(db.String(18), unique=True, nullable=False)
    # 联系电话
    phone = db.Column(db.String(20), nullable=False)
    # 居住地址
    address = db.Column(db.String(255))
    # 工作经验描述
    experience = db.Column(db.Text)
    # 资质证书，多个URL用逗号分隔
    certificates = db.Column(db.Text)
    # 是否已通过验证
    is_verified = db.Column(db.Boolean, default=False)
    # 审核状态：pending（待审核）, approved（已通过）, rejected（已拒绝）
    status = db.Column(db.String(50), default='pending')
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 与用户建立一对一关系
    user = db.relationship('User', backref=db.backref('provider_info', uselist=False))


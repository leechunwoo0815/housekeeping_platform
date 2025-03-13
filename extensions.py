# 导入所需的Flask扩展
from flask_sqlalchemy import SQLAlchemy  # 用于数据库ORM
from flask_migrate import Migrate  # 用于数据库迁移
from flask_jwt_extended import JWTManager  # 用于JWT认证

# 创建数据库实例，但不初始化它（在工厂函数中进行初始化）
db = SQLAlchemy()

# 创建数据库迁移工具实例，用于处理数据库版本控制
migrate = Migrate()

# 创建JWT管理器实例，用于处理用户认证和token管理
jwt = JWTManager()


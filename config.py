import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# .env文件用于存储敏感配置信息，如数据库连接串、密钥等
load_dotenv()

class Config:
    # 应用密钥，用于会话签名等安全相关功能
    # 优先从环境变量获取，如果没有则使用默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    
    # 数据库连接URI
    # 优先使用环境变量中的配置，否则默认使用SQLite数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'  # 使用SQLite
    
    # 关闭SQLAlchemy的修改跟踪功能，提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT（JSON Web Token）密钥，用于用户认证
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'

    # Flask-Admin配置
    FLASK_ADMIN_SWATCH = 'cerulean'  # 设置Flask-Admin的界面主题为cerulean

class DevelopmentConfig(Config):
    # 开发环境配置类，继承基础配置
    DEBUG = True  # 启用调试模式，显示详细的错误信息

class TestingConfig(Config):
    # 测试环境配置类，用于单元测试等场景
    TESTING = True  # 启用测试模式
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用SQLite内存数据库进行测试

class ProductionConfig(Config):
    # 生产环境配置类，用于实际部署
    # 必须从环境变量获取数据库连接信息，确保安全性
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # 在此处添加其他生产环境特定的配置项


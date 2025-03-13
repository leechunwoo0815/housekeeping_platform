from extensions import db

class FAQ(db.Model):
    """常见问题模型类
    用于存储和管理网站的常见问题及其答案
    """
    # 主键ID字段
    id = db.Column(db.Integer, primary_key=True)
    # 问题字段，不允许为空，最大长度255字符
    question = db.Column(db.String(255), nullable=False)
    # 答案字段，使用Text类型存储长文本，不允许为空
    answer = db.Column(db.Text, nullable=False)

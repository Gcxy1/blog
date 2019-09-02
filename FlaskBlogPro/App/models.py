# 模型

from .exts import db


class User(db.Model):
    # 表名
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.Integer, default=1)
    phone = db.Column(db.String(30))


#文章分类表
class Articletype(db.Model):
    __tablename__ = 'articletype'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    alias = db.Column(db.String(100))  #别名
    keyword = db.Column(db.String(50))  #标签
    parentnode = db.Column(db.String(50)) # 父级节点
    describe = db.Column(db.Text) #描述
    #     # 单：声明， 关联表的字段
    articles= db.relationship('Article',backref = 'my_article',lazy = True)


# 文章表
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(30),unique=True)
    text = db.Column(db.Text)  #文本内容
    comment= db.Column(db.Integer,default=0)
    keyword = db.Column(db.String(50))
    describe = db.Column(db.Text)  #描述
    label = db.Column(db.String(50),default='') #标签
    img = db.Column(db.String(255))
    data = db.Column(db.DateTime)  # 时间

    # 多：设外键
    articletypeid = db.Column(db.Integer,db.ForeignKey(Articletype.id))

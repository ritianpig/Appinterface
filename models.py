from APP import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    article_name = db.Column(db.String(200))
    appid = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    column_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    countcollect = db.Column(db.Integer)
    countbrowse = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    url = db.Column(db.String(500))


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    path = db.Column(db.String(200))
    picture_name = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    head_url = db.Column(db.String(200), comment="用户头像地址")
    user_name = db.Column(db.String(100), comment="用户名称")
    sign = db.Column(db.String(100), comment="用户签名")


class Collect(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    article_id = db.Column(db.Integer, comment="文章id")


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    article_id = db.Column(db.Integer, comment="文章id")
from App import db


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
    countup = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    url = db.Column(db.String(500))


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appid = db.Column(db.Integer)
    article_id = db.Column(db.Integer)
    path = db.Column(db.String(200))
    picture_name = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appid = db.Column(db.Integer)
    user_id = db.Column(db.String(200), comment="用户id")
    other_name = db.Column(db.String(200), default="暂无昵称", comment="昵称")
    head_url = db.Column(db.String(200), comment="用户头像地址")
    user_name = db.Column(db.String(100), comment="用户名称")
    sign = db.Column(db.String(100), default="暂无签名", comment="用户签名")
    password = db.Column(db.String(200), comment="密码")


class Collect(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    article_id = db.Column(db.Integer, comment="文章id")


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    article_id = db.Column(db.Integer, comment="文章id")


class Up(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), comment="用户id")
    article_id = db.Column(db.Integer, comment="文章id")


class Hotkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.Integer)
    hotkey = db.Column(db.String(100), comment="搜索热词")


class ColumnClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column_id = db.Column(db.Integer, comment="栏目id")
    class_id = db.Column(db.Integer, comment="分类id")
    appid = db.Column(db.Integer, comment="appid")
    column_name = db.Column(db.String(50), comment="栏目名")
    class_name = db.Column(db.String(50), comment="分类名")
    class_pic = db.Column(db.String(200), comment="分类图片地址")


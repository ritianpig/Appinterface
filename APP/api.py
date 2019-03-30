import json
import random

from flask import request, jsonify
from . import app, db
from models import Article, Pictures, User, Collect, History


def getresult(datalist):
    articlelist = []
    for data in datalist:

        res_pictures = Pictures.query.filter_by(article_id
                                                =data.article_id).all()
        pictures = []
        for pic in res_pictures:
            pic_dic = {
                "article_id": pic.article_id,
                "picture_name": pic.picture_name,
                "path": pic.path
            }
            pictures.append(pic_dic)

        article = {
            'appid': data.appid,
            'article_id': data.article_id,
            'article_name': data.article_name,
            'class_id': data.class_id,
            'column_id': data.column_id,
            'content': data.content,
            'countcollect': data.countcollect,
            'countlike': data.countlike,
            'create_date': str(data.create_date),
            'create_idate': int(str(data.create_date.
                                    date()).replace('-', '')),
            'url': data.url,
            "contentPictures": pictures
        }

        articlelist.append(article)
    result = {
        "articlelist": articlelist
    }

    return result


@app.route('/appinterface1', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        get_data = request.get_data()
        isclass = request.headers.get("isclass")
        iscollect = request.headers.get("iscollect")
        isbrowse = request.headers.get("isbrowse")
        edituser = request.headers.get("edituser")

        data_dic = json.loads(get_data)

        if isclass:
            if data_dic["class_id"] == 0:
                res_data = Article.query.filter_by(appid=data_dic["appid"]).all()
                if res_data:
                    randomdata_list = random.sample(res_data, 8)
                    result = getresult(randomdata_list)

                    return jsonify(result)
                else:
                    return "class0暂无数据"

            elif data_dic["class_id"] == 1:
                res_data1 = Article.query.filter_by(
                    appid=data_dic["appid"], class_id=1)\
                    .order_by(Article.id.desc()).all()
                if res_data1:
                    index1 = data_dic["page"] * 8
                    index2 = (data_dic["page"] + 1) * 8
                    descdata_list = res_data1[index1:index2]

                    result = getresult(descdata_list)
                    return jsonify(result)
                else:
                    return "class1没有数据"

            elif data_dic["class_id"] == 2:
                res_data2 = Article.query.filter_by(
                    appid=data_dic["appid"], class_id=1) \
                    .order_by(Article.id.desc()).all()
                if res_data2:
                    index1 = data_dic["page"] * 8
                    index2 = (data_dic["page"] + 1) * 8
                    descdata_list = res_data2[index1:index2]

                    result = getresult(descdata_list)
                    return jsonify(result)
                else:
                    return "class2没有数据"

            elif data_dic["class_id"] == 3:
                res_data3 = Article.query.filter_by(
                    appid=data_dic["appid"], class_id=1) \
                    .order_by(Article.id.desc()).all()
                if res_data3:
                    index1 = data_dic["page"] * 8
                    index2 = (data_dic["page"] + 1) * 8
                    descdata_list = res_data3[index1:index2]

                    result = getresult(descdata_list)
                    return jsonify(result)
                else:
                    return "class3没有数据"

            elif data_dic["class_id"] == 4:
                res_data4 = Article.query.filter_by(
                    appid=data_dic["appid"], class_id=1) \
                    .order_by(Article.id.desc()).all()
                if res_data4:
                    index1 = data_dic["page"] * 8
                    index2 = (data_dic["page"] + 1) * 8
                    descdata_list = res_data4[index1:index2]

                    result = getresult(descdata_list)
                    return jsonify(result)
                else:
                    return "class4没有数据"

            else:
                return "分类大于四个需要重新添加接口"

        if iscollect:
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            res_collect = Collect.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            if res_collect:
                return "文章已经被用户收藏过了"
            else:
                res_article = Article.query(article_id=article_id).first()
                res_article.countcollect += 1
                add_collect = Collect(user_id=user_id, article_id=article_id)
                db.session.add(add_collect)
                db.session.commit()
                return "ok"

        if isbrowse:
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            res_history = History.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            res_article = Article.query.filter_by(article_id=article_id).first()
            res_article.countbrowse += 1
            db.session.commit()

            if res_history:
                db.session.delete(res_history)
                db.session.commit()

            add_history = History(user_id=user_id, article_id=article_id)
            db.session.add(add_history)
            db.session.commit()
            return "ok"

        if edituser:
            user_id = data_dic["user_id"]
            user_name = data_dic["user_name"]
            sign = data_dic["sign"]
            res_user = User.query.filter_by(user_id=user_id).first()
            if res_user:
                res_user.user_name = user_name
                res_user.sign = sign
                db.session.commit()
                return "修改用户信息ok"
            else:
                add_user = User(user_id=user_id, user_name=user_name, sign=sign)
                db.session.add(add_user)
                db.session.commit()
                return "添加用户信息ok"

    else:
        return "不支持GET请求"






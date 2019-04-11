import json
import os
import random
import time
import string

from flask import request, jsonify
from . import app, db
from models import Article, Pictures, User, Collect, History, Up, Hotkey, \
    ColumnClass


def getresult(user_id, datalist):
    base_url = "https://hudong-app.oss-cn-beijing.aliyuncs.com"
    articlelist = []
    for data in datalist:

        res_pictures = Pictures.query.filter_by(
            article_id=data.article_id).all()
        res_collect = Collect.query.filter_by(
            user_id=user_id, article_id=data.article_id).first()
        res_article = Article.query.filter_by(article_id=data.article_id)\
            .first()

        if res_collect:
            iscollect = "1"
        else:
            iscollect = "0"
        pictures = []
        for pic in res_pictures:
            pic_dic = {
                "article_id": pic.article_id,
                "picture_name": pic.picture_name,
                "pic_url": base_url + pic.path
            }
            pictures.append(pic_dic)

        article = {
            'appid': res_article.appid,
            'iscollect': iscollect,
            'article_id': res_article.article_id,
            'article_name': res_article.article_name,
            'class_id': res_article.class_id,
            'column_id': res_article.column_id,
            'content': res_article.content,
            'countcollect': res_article.countcollect,
            'countbrowse': res_article.countbrowse,
            'countup': res_article.countup,
            'create_date': str(res_article.create_date),
            'create_idate': int(str(res_article.create_date.
                                    date()).replace('-', '')),
            'url': res_article.url,
            "contentPictures": pictures
        }

        articlelist.append(article)
    result = {
        "articlelist": articlelist
    }
    return result


@app.route('/appinterface1', methods=["GET", "POST"])
def index():
    """
    App资讯类接口，根据请求头信息的异同来区分处理逻辑，请求头为isclass,iscollect,isbrowse
    ,edituser,showhistory,showcollect分别对应的是处理分类显示信息逻辑，收藏逻辑，历史记录
    逻辑，编辑用户信息逻辑，展示历史记录逻辑，展示收藏信息逻辑。当需要对应的处理逻辑时需要post
    过来的json，包含该字段信息即可，值可以随意指定，但是不可为空.
    """
    if request.method == "POST":

        get_data = request.get_data()
        showcolumn = request.headers.get("showcolumn")
        iscolumn = request.headers.get("iscolumn")
        iscollect = request.headers.get("iscollect")
        isbrowse = request.headers.get("isbrowse")
        edituser1 = request.headers.get("edituser1")
        edituser2 = request.headers.get("picname")
        showhistory = request.headers.get("showhistory")
        showcollect = request.headers.get("showcollect")
        showuser = request.headers.get("showuser")
        register = request.headers.get("register")
        login = request.headers.get("login")
        isup = request.headers.get("isup")
        showup = request.headers.get("showup")
        cancelcollect = request.headers.get("cancelcollect")
        search = request.headers.get("search")
        hotkey = request.headers.get("hotkey")
        deletehistory = request.headers.get("deletehistory")
        cleanhistory = request.headers.get("cleanhistory")
        cleancollect = request.headers.get("cleancollect")
        cleanup = request.headers.get("cleanup")
        cancelup = request.headers.get("cancelup")
        isarticle = request.headers.get("isarticle")

        # 用户注册
        if register:
            data_dic = json.loads(get_data)
            path_time = str(time.time()).replace('.', '')
            user_id = ''.join(random.sample(string.ascii_letters +
                                            string.digits, 8)) + path_time
            appid = data_dic["appid"]
            user_name = data_dic["user_name"]
            password = data_dic["password"]

            check_user = User.query.filter_by(appid=appid,
                                              user_name=user_name).first()
            if check_user:
                return "用户已存在"
            else:
                add_user = User(user_id=user_id, user_name=user_name,
                                appid=appid, password=password)
                db.session.add(add_user)
                db.session.commit()
            return "ok"

        # 用户登录
        if login:
            data_dic = json.loads(get_data)
            user_name = data_dic["user_name"]
            password = data_dic["password"]
            appid = data_dic["appid"]
            check_user = User.query.filter_by(user_name=user_name, appid=appid,
                                              password=password).first()
            if check_user:
                return jsonify({"user_id": check_user.user_id})
            else:
                return "用户名或密码错误"

        # 用户编辑信息
        if edituser1:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            user_name = data_dic["user_name"]
            pic_name = data_dic["picname"]
            sign = data_dic["sign"],
            other_name = data_dic["other_name"]
            res_user = User.query.filter_by(user_id=user_id).first()
            pic_path = "https://xcx.51babyapp.com/App/static/head/"
            if res_user:
                res_user.user_name = user_name
                res_user.sign = sign
                res_user.head_url = pic_path + pic_name
                res_user.other_name = other_name
                db.session.commit()
                return "ok"
            else:
                return "用户未登录不能修改信息"

        # 用户更改头像信息
        if edituser2:
            if get_data:
                path = os.path.dirname(os.path.abspath(__file__))
                name = path + "/static/head/" + edituser2
                with open(name, "wb") as f:
                    f.write(get_data)
                return "ok"
            return "没有检测到图片信息"

        # 返回用户资料信息
        if showuser:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            appid = data_dic["appid"]
            show_user = User.query.filter_by(
                user_id=user_id, appid=appid).first()
            if show_user:
                user = {
                    "user_id": show_user.user_id,
                    "user_name": show_user.user_name,
                    "head_url": show_user.head_url,
                    "sign": show_user.sign,
                    "other_name": show_user.other_name
                }
                return jsonify(user)
            else:
                return "没有用户信息"

        # 返回栏目分类信息
        if showcolumn:
            data_dic = json.loads(get_data)
            appid = data_dic["appid"]
            column_id = data_dic["column_id"]
            res_columns = ColumnClass.query.filter_by(appid=appid,
                                                      column_id=column_id).all()
            class_list = []
            if res_columns:
                for data in res_columns:
                    class_dic = {
                        "appid": data.appid,
                        "column_id": data.column_id,
                        "class_id": data.class_id,
                        "column_name": data.column_name,
                        "class_name": data.class_name,
                        "class_pic": data.class_pic
                    }
                    class_list.append(class_dic)
            else:
                pass
            return jsonify({"classlist": class_list})

        # 根据栏目返回分类数据
        if iscolumn:
            data_dic = json.loads(get_data)
            appid = data_dic["appid"]
            column_id = data_dic["column_id"]
            class_id = data_dic["class_id"]
            user_id = data_dic["user_id"]

            if class_id == 0:
                res_data = Article.query.filter_by(appid=appid,
                                                   column_id=column_id).all()
                if res_data:
                    try:
                        randomdata_list = random.sample(res_data, 8)
                    except:
                        randomdata_list = res_data
                    result = getresult(user_id, randomdata_list)
                    return jsonify(result)
                else:
                    return "class%s没有数据" % class_id

            else:
                res_data = Article.query.filter_by(appid=appid,
                                                   column_id=column_id,
                                                   class_id=class_id).all()
                if res_data:
                    try:
                        randomdata_list = random.sample(res_data, 8)
                    except:
                        randomdata_list = res_data
                    result = getresult(user_id, randomdata_list)
                    return jsonify(result)
                else:
                    return "class%s没有数据" % class_id

        if isarticle:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            only_article = Article.query.filter_by(article_id=article_id).all()

        # 用户收藏逻辑
        if iscollect:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            res_collect = Collect.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            if res_collect:
                return "文章已经被用户收藏过了"
            else:
                res_article = Article.query.filter_by(
                    article_id=article_id).first()
                res_article.countcollect += 1
                add_collect = Collect(user_id=user_id, article_id=article_id)
                db.session.add(add_collect)
                db.session.commit()
                return "ok"

        # 用户浏览逻辑
        if isbrowse:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            res_history = History.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            res_article = Article.query.filter_by(
                article_id=article_id).first()
            res_article.countbrowse += 1
            db.session.commit()

            if res_history:
                db.session.delete(res_history)
                db.session.commit()

            add_history = History(user_id=user_id, article_id=article_id)
            db.session.add(add_history)
            db.session.commit()
            return "ok"

        # 用户点赞逻辑
        if isup:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            res_up = Up.query.filter_by(user_id=user_id,
                                        article_id=article_id).first()
            res_article = Article.query.filter_by(
                article_id=article_id).first()
            try:
                res_article.countup += 1
            except:
                res_article.countup = 1
            db.session.commit()

            if res_up:
                return "已赞过"
            else:
                add_up = Up(user_id=user_id, article_id=article_id)
                db.session.add(add_up)
                db.session.commit()
            return "ok"

        # 用户取消收藏逻辑
        if cancelcollect:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            get_collect = Collect.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            if get_collect:
                db.session.delete(get_collect)
                db.session.commit()
                return "ok"
            else:
                return "用户还没收藏该文章"

        # 用户删除历史记录
        if deletehistory:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            get_history = History.query.filter_by(user_id=user_id,
                                                  article_id=article_id).first()
            if get_history:
                db.session.delete(get_history)
                db.session.commit()
                return "ok"
            else:
                return "用户还没浏览该文章"

        # 取消点赞
        if cancelup:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            article_id = data_dic["article_id"]
            get_up = Up.query.filter_by(user_id=user_id,
                                        article_id=article_id).first()
            if get_up:
                db.session.delete(get_up)
                db.session.commit()
                return "ok"
            else:
                return "用户还没有赞这篇文章"

        # 用户清空历史记录(多条)
        if cleanhistory:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            res_history = History.query.filter_by(user_id=user_id).all()
            [db.session.delete(i) for i in res_history]
            db.session.commit()
            return "ok"

        # 用户清空收藏记录(多条)
        if cleancollect:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            res_collect = Collect.query.filter_by(user_id=user_id).all()
            [db.session.delete(i) for i in res_collect]
            db.session.commit()
            return "ok"

        # 用户清空点赞记录(多条)
        if cleanup:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            res_up = Up.query.filter_by(user_id=user_id).all()
            [db.session.delete(i) for i in res_up]
            db.session.commit()
            return "ok"

        # 返回用户浏览历史记录
        if showhistory:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            page = data_dic["page"]
            show_history = History.query.filter_by(user_id=user_id).\
                order_by(History.id.desc()).all()
            if show_history:
                index1 = page * 8
                index2 = (page + 1) * 8
                part_history = show_history[index1:index2]
                result = getresult(user_id, part_history)
                return jsonify(result)
            else:
                return "暂无浏览记录"

        # 返回用户收藏列表
        if showcollect:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            page = data_dic["page"]
            show_collect = Collect.query.filter_by(user_id=user_id).\
                order_by(Collect.id.desc()).all()
            if show_collect:
                index1 = page * 8
                index2 = (page + 1) * 8
                part_collect = show_collect[index1:index2]
                result = getresult(user_id, part_collect)
                return jsonify(result)
            else:
                return "暂无收藏记录"

        # 返回用户点赞列表
        if showup:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            page = data_dic["page"]
            show_up = Up.query.filter_by(user_id=user_id).\
                order_by(Up.id.desc()).all()
            if show_up:
                index1 = page * 8
                index2 = (page + 1) * 8
                part_up = show_up[index1:index2]
                result = getresult(user_id, part_up)
                return jsonify(result)
            else:
                return "暂无点赞记录"

        # 用户搜索逻辑,精准匹配
        if search:
            data_dic = json.loads(get_data)
            user_id = data_dic["user_id"]
            key = data_dic["key"]
            appid = data_dic["appid"]
            page = data_dic["page"]
            get_articles = Article.query.filter_by(appid=appid).all()
            articles = []
            for data in get_articles:
                if key in data.article_name:
                    articles.append(data)
                else:
                    pass

            if articles:
                index1 = page * 8
                index2 = (page + 1) * 8
                part_article = articles[index1:index2]
                result = getresult(user_id, part_article)
                return jsonify(result)
            else:
                return "没有相关文章"

        if hotkey:
            data_dic = json.loads(get_data)
            appid = data_dic["appid"]
            res_hotkey = Hotkey.query.filter_by(appid=appid).all()
            if res_hotkey:
                keys = []
                for data in res_hotkey:
                    keys.append(data.hotkey)
                result = {"hotkey": keys}
                return jsonify(result)
            else:
                return jsonify([])

    else:
        return "不支持GET请求"

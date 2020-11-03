# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

from flask import (
    views,

    current_app, render_template, request
)
from sqlalchemy import or_, and_

from models import WechatTag, Announcement, WechatAccount, WechatArticleList
from utils import field, tools


def anaysis(articless, flag=None):
    '''
    in查询文章的信息，falg不存在默认返回阅读量，查询的次数多一次。若flag存在只返回一个articles数据库中的信息
    :param articless:
    :param flag:
    :return:
    '''
    article_data = []
    if flag:
        for i in articless:
            article = {}
            article['title'] = i.title
            article['biz'] = getattr(i,'__biz')
            article['account_name'] = i.account
            article['id'] = i.sn
            article['publish_time'] = str(i.publish_time)
            article['url'] = tools.url_remove_info(i.url)
            article_data.append(article)
    else:
        for i in articless:
            article = {}
            if i.title == '' or i.title == None:
                article['title'] = '分享的图片、视频、链接'
            else:
                article['title'] = i.title
            if i.author == '' or i.author == None:
                article['author'] = '匿名'
            else:
                article['author'] = i.author
            if i.digest == '' or i.digest == None:
                article['digest'] = '&nbsp; &nbsp;'
            else:
                article['digest'] = i.digest
            article['biz'] = getattr(i,'__biz')
            article['cover'] = i.cover
            article['url'] = tools.url_remove_info(i.url)
            article['publish_time'] = str(i.publish_time)
            article['account_name'] = (WechatAccount.query.filter_by(__biz=i.__biz).first()).account
            article['id'] = i.sn
            article['like'] = 0
            article['read'] = 0
            article_data.append(article)
    return article_data



class IndexView(views.MethodView):

    def get(self):
        tag = WechatTag.query.all()
        account_num = WechatAccount.query.count()
        article_num = WechatArticleList.query.count()
        announcement = Announcement.query.filter(Announcement.flag == 1).order_by(Announcement.time.desc()).first()
        tag_style = ['layui-badge layui-bg-blue', 'layui-badge', 'layui-badge layui-bg-orange',
                     'layui-badge layui-bg-green', 'layui-badge layui-bg-cyan', 'layui-badge layui-bg-black']
        context = {
            'tags': tag,
            'tag_style': tag_style,
            'account_num': account_num,
            'article_num': article_num,
            'announcement': announcement,
        }
        return render_template('front/front_index.html', **context)


# 公众号下的所有文章 articles

class ArticlesView(views.MethodView):

    def get(self):

        id = request.args.get('id')
        flag = request.args.get('flag')

        if id:
            article_obj = WechatArticleList.query.filter_by(__biz=id).order_by(
                WechatArticleList.publish_time.desc())
        else:
            article_obj = WechatArticleList.query.order_by(
                WechatArticleList.publish_time.desc())

        page = int(request.args.get('page'))
        limit = current_app.config['FRONT_ARTICLES']
        start = (page - 1) * limit
        end = start + limit
        articles = article_obj.slice(start, end)
        pages = int(article_obj.count() / limit) + 1
        if flag:
            article_data = anaysis(articles, flag=flag)
        else:
            article_data = anaysis(articles)
        return field.layui_success(message='', data=article_data, count=pages)


# 类型标签 tags
class TagsView(views.MethodView):

    def get(self):
        cat_id = request.args.get('cat_id')

        cat = WechatTag.query.get(cat_id)
        article = WechatArticleList.query.filter(
            getattr(WechatArticleList,'__biz').in_(set([i.account_id for i in cat.accounts]))).order_by(
            WechatArticleList.publish_time.desc())
        page = int(request.args.get('page'))
        limit = current_app.config['FRONT_ARTICLES']
        start = (page - 1) * limit
        end = start + limit
        data = article.slice(start, end)  # 切片查询
        pages = int(article.count() / limit) + 1
        article_data = anaysis(data)
        return field.layui_success(message='', data=article_data, count=pages)


# 获取指定ID文章的内容 article_id

class ArticleIDView(views.MethodView):

    def get(self):
        id = request.args.get('id')
        if id:
            article = WechatArticleList.query.filter_by(sn=id).first()
            if article:
                article_dict = {}
                article_dict['title'] = article.title
                if article.author == '':
                    article_dict['author'] = '匿名'
                else:
                    article_dict['author'] = article.author
                article_dict['publish_time'] = str(article.publish_time)
                article_dict['account_name'] = article.account
                article_dict['url'] = article.url
                article_dict['content_html'] = tools.filter_html(article.content_html)
                article_dict['id'] = getattr(article,'__biz')
                return field.success(message='', data=article_dict)
            else:
                return field.params_error(message='没有该文章！')
        return field.params_error(message='参数错误！')





# 前台搜索
class SearchView(views.MethodView):

    def get(self):
        # 不在使用GET的请求方式
        keyword = request.args.get('keyword')

        if keyword:
            if "amp" in keyword:
                # 将查找关键字变为多条件合并查找；&分割关键字
                keyword_list = (keyword.strip()).split('amp')
                article_obj = WechatArticleList.query
                for per_keyword in keyword_list:
                    find_filter = []
                    per_keyword = per_keyword
                    find_filter.append(WechatArticleList.title.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.author.like("%" + per_keyword + "%"))
                    # find_filter.append(WechatArticleList.account.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.digest.like("%" + per_keyword + "%"))
                article_obj = article_obj.filter(WechatArticleList.title.like("%" + "聚合" + "%"))
                # article_obj = article_obj.filter(or_(*find_filter)).filter(WechatArticleList.title.like("%" + "聚合" + "%"))
                article_obj = article_obj.order_by(WechatArticleList.publish_time.desc())
            else:

                # 将查找关键字变为多条件或查找；|分割关键字
                keyword_list = (keyword.strip()).split('|')
                find_filter = []
                for per_keyword in keyword_list:
                    per_keyword = per_keyword
                    find_filter.append(WechatArticleList.title.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.author.like("%" + per_keyword + "%"))
                    # find_filter.append(WechatArticleList.account.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.digest.like("%" + per_keyword + "%"))

                article_obj = WechatArticleList.query.filter(or_(*find_filter
                                                                 )).order_by(WechatArticleList.publish_time.desc())

            page = int(request.args.get('page'))
            limit = current_app.config['FRONT_ARTICLES']
            start = (page - 1) * limit
            end = start + limit
            articles = article_obj.slice(start, end)
            count = article_obj.count()
            pages = int(count / limit) + 1
            if count > 0:
                article_data = anaysis(articles)
                return field.layui_success(message='共查询到 {} 条相关信息'.format(count), data=article_data, count=pages)
            else:
                return field.layui_success(message='没有找到相关信息！', count=0)

    def post(self):
        # 由于get的传参方式会将&隐藏所以我们尝试该传输参数的方式
        data = request.values
        keyword = data.get('keyword')
        page = int(data.get('page'))

        if keyword:
            if "&" in keyword:
                # 将查找关键字变为多条件合并查找；&分割关键字
                keyword_list = keyword.split('&')
                article_obj = WechatArticleList.query
                article_obj = article_obj
                all_filter = []
                for per_keyword in keyword_list:
                    find_filter = []
                    per_keyword = per_keyword.strip()
                    find_filter.append(WechatArticleList.title.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.author.like("%" + per_keyword + "%"))
                    # find_filter.append(WechatArticleList.account.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.digest.like("%" + per_keyword + "%"))
                    all_filter.append(or_(*find_filter))
                article_obj = article_obj.filter(and_(*all_filter))
                article_obj = article_obj.order_by(WechatArticleList.publish_time.desc())
            else:

                # 将查找关键字变为多条件或查找；|分割关键字
                keyword_list = keyword.split('|')
                find_filter = []
                for per_keyword in keyword_list:
                    per_keyword = per_keyword.strip()
                    find_filter.append(WechatArticleList.title.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.author.like("%" + per_keyword + "%"))
                    # find_filter.append(WechatArticleList.account.like("%" + per_keyword + "%"))
                    find_filter.append(WechatArticleList.digest.like("%" + per_keyword + "%"))

                article_obj = WechatArticleList.query.filter(or_(*find_filter
                                                                 )).order_by(
                    WechatArticleList.publish_time.desc())
            limit = current_app.config['FRONT_ARTICLES']
            start = (page - 1) * limit
            end = start + limit
            articles = article_obj.slice(start, end)
            count = article_obj.count()
            pages = int(count / limit) + 1
            if count > 0:
                article_data = anaysis(articles)
                return field.layui_success(message='共查询到 {} 条相关信息'.format(count), data=article_data, count=pages)
            else:
                return field.layui_success(message='没有找到相关信息！', count=0)


class GetImgView(views.MethodView):

    def get(self):
        account_id = request.args.get('account_id')
        if account_id:
            account = WechatAccount.query.filter_by(__biz=account_id.strip()).first()
            if account:
                img = account.qr_code
                return field.success(message='查询成功', data={'img': img})
            else:
                return field.params_error('')
        return field.params_error('参数错误')



# 公告内容
class AnnouncementView(views.MethodView):

    def get(self):
        tag = WechatTag.query.all()
        annocuncements = Announcement.query.filter(Announcement.flag == 1).order_by(Announcement.time.desc()).all()
        return render_template('front/front_announcement.html', annocuncements=annocuncements, tags=tag)

    def post(self):
        pass


# 快速关注公众号 wechat_github
class WechatGithubView(views.MethodView):

    def get(self):
        tag = WechatTag.query.all()
        content = tools.follow_wechat()

        return render_template('front/front_wechat_github.html', content=content, tags=tag)


# 年报总结 year_report
class YearReportView(views.MethodView):

    def get(self):
        return render_template('front/2019.html')


# 公众号展示 account_list

class AccountListView(views.MethodView):
    '''
    [ {'tag':'asd','accounts':[{'name':'xx','img':'img'}]}]
    '''

    def get(self):
        tags = WechatTag.query.all()
        new_tags = []
        for tag in tags:
            tag_dict = dict()
            account_list = list()
            account = WechatAccount.query.filter(
                getattr(WechatAccount, '__biz').in_(set([i.account_id for i in tag.accounts])))
            for i in account:
                account_dict = dict()
                account_dict['account'] = i.account
                account_dict['head_url'] = i.head_url
                account_dict['summary'] = i.summary
                account_dict['qr_code'] = i.qr_code
                account_dict['verify'] = i.verify
                account_dict['spider_time'] = i.spider_time
                account_list.append(account_dict)
            tag_dict['tag_name'] = tag.tag_name
            tag_dict['accounts'] = account_list
            new_tags.append(tag_dict)
        return render_template('front/front_account_list.html', tags=new_tags)




# -*- coding: utf-8 -*-
"""
@project ： src
@Time ： 2020/11/1 15:34
@Auth ： AJay13
@File ：urls.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
from flask import Blueprint,render_template

from utils import tools
from .views import AccountListView, YearReportView, AnnouncementView, WechatGithubView, IndexView, ArticleIDView, \
    ArticlesView, GetImgView, SearchView, TagsView

bp = Blueprint('front', __name__, url_prefix='/')

bp.add_url_rule('/', view_func=IndexView.as_view('index'))  # 首页展示
bp.add_url_rule('article_id/', view_func=ArticleIDView.as_view('article_id'))  # 获取指定ID文章的内容
bp.add_url_rule('articles/', view_func=ArticlesView.as_view('articles'))  # 公告展示

bp.add_url_rule('get_img/', view_func=GetImgView.as_view('get_img'))  # 公告展示
bp.add_url_rule('search/', view_func=SearchView.as_view('search'))  # 公告展示
bp.add_url_rule('tags/', view_func=TagsView.as_view('tags'))  # 公告展示

# 公告模块
bp.add_url_rule('announcement/', view_func=AnnouncementView.as_view('announcement'))  # 公告展示

# 快速关注公众号（彩蛋 ）
bp.add_url_rule('wechat_github/', view_func=WechatGithubView.as_view('wechat_github'))  # 快速关注公众号

# 2019年报（公众号图表总结 ）
bp.add_url_rule('year_report/', view_func=YearReportView.as_view('year_report'))  # 年报总结

# 公众号展示
bp.add_url_rule('account_list/', view_func=AccountListView.as_view('account_list'))  # 公众号展示

# 前端过滤器
bp.add_app_template_filter(tools.filter_html, 'Html')
bp.add_app_template_filter(tools.url_remove_info, 'url_remove_info')
bp.add_app_template_filter(tools.markdown2html, 'markdown2html')

@bp.app_errorhandler(404)
def page_not_found(error):

    return render_template('front/front_404.html'), 404

# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import datetime

from exts import db


class WechatTag(db.Model):
    __tablename__ = 't_wechat_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(30), nullable=False, unique=True)
    tag_en = db.Column(db.String(30), nullable=False, unique=True)
    tag_summary = db.Column(db.String(100), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    accounts = db.relationship('TWechatAccount', backref='tags', lazy=True)



class TWechatAccount(db.Model):
    __tablename__ = 't_wechat_account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.String(50), nullable=False, unique=True)
    account_name = db.Column(db.String(30), nullable=False)
    tag = db.Column(db.Integer, db.ForeignKey('t_wechat_tag.id'))
    status = db.Column(db.String(50), nullable=False, default='forbid',
                       comment='监控的状态 默认 禁用 forbid  开始监控 start')  # 规则的状态 默认active 1 禁用 为0
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


class Announcement(db.Model):
    __tablename__ = 't_announcement'  # 公告
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    context = db.Column(db.Text, nullable=False)
    flag = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.datetime.now)


class WechatAccount(db.Model):
    '''
        爬取的微信公众号信息
    '''
    __tablename__ = 'wechat_account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(255), nullable=True, comment='公众号中文名')
    head_url = db.Column(db.String(255), nullable=True, comment='公众号头像链接')
    summary = db.Column(db.String(500), nullable=True, comment='公众号描述')
    qr_code = db.Column(db.String(255), nullable=True, comment='公众号二维码')
    verify = db.Column(db.String(255), nullable=True, comment='公众号认证')
    spider_time = db.Column(db.DateTime, comment='上次爬取时间')

    @classmethod
    @property
    def get_biz(self):
        return WechatAccount.__biz


WechatAccount.__biz = db.Column(db.String(50), nullable=True, unique=True, comment='公众号id')


class WechatArticleList(db.Model):
    '''
        公众号中微信文章列表
    '''
    __tablename__ = 'wechat_article_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment='标题')
    digest = db.Column(db.String(2000), nullable=False, comment='描述')
    url = db.Column(db.String(500), nullable=False, comment='文章链接')
    source_url = db.Column(db.String(1000), nullable=False, comment='源地址')
    cover = db.Column(db.String(255), nullable=False, comment='封面地址')
    subtype = db.Column(db.Integer, nullable=False, comment='')
    is_multi = db.Column(db.Integer, nullable=False, comment='')
    author = db.Column(db.String(255), nullable=False, comment='作者')
    copyright_stat = db.Column(db.Integer, nullable=False, comment='')
    duration = db.Column(db.Integer, nullable=False, comment='')
    del_flag = db.Column(db.Integer, nullable=False, comment='删除标志')
    type = db.Column(db.Integer, nullable=False, comment='')
    sn = db.Column(db.String(50), nullable=False, comment='')
    re_spider = db.Column(db.Integer, nullable=True, default=0, comment='是否回采文章，0默认、1失败、2完成')
    publish_time = db.Column(db.DateTime, nullable=True, comment='文章发布时间，做文章增量采集用')
    spider_time = db.Column(db.DateTime, nullable=True, comment='上次抓取时间，')


WechatArticleList.__biz = db.Column(db.String(50), nullable=False, comment='公众号id')

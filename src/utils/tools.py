#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/10/11 0011'

"""
import re
from models import WechatAccount,WechatTag
import markdown


def markdown2html(text):
    return markdown.markdown(text, extensions=['extra'])

# 过滤html
def filter_html(content_html):
    no_n_html = content_html.replace("\\n", '').replace('xa0', '').replace('\\', '')
    no_style_html = no_n_html.replace("style=\"visibility: hidden;\"", "")  #: 修复bug。微信改版爬取的数据被隐藏。
    new_html = no_style_html.replace('data-src=\\', 'src=').replace('data-src="',
                                                                    'src="http://img04.sogoucdn.com/net/a/04/link?appid=100520033&url=')
    return '<div style="margin: 20px">' + new_html + '</div>'  # 改变弹窗样式


def is_Linux_which_sys():
    # 判断系统是不是linux系统，一般软件只能在linux上运行，windows上只是开发环境。目前时对黑名单做判断操作nginx
    import platform
    if (platform.system() == 'Windows'):
        print('Windows系统')
        return False
    elif (platform.system() == 'Linux'):
        print('Linux系统')
        return True
    else:
        return False
# 快速关注公众号排版
def follow_wechat():
    accounts_dict = {}
    accounts_obj = WechatAccount.query
    accounts = accounts_obj.all()
    accounts_num = accounts_obj.count()  # 公众号数量


    for account in accounts:
        accounts_info = {}
        accounts_info['account'] = account.account
        accounts_info['head_url'] = account.head_url
        accounts_info['summary'] = account.summary
        accounts_info['qr_code'] = account.qr_code
        accounts_info['account'] = account.account
        accounts_info['__biz'] = account.__biz
        accounts_dict[account.__biz] = accounts_info

    tags_obj = WechatTag.query  # 获取所有tags obj
    tags = tags_obj.all()  # 获取所有tags
    tags_num = tags_obj.count()  # 获取所有tags 数量

    # README.md的编写
    header_accound = ''
    body_accound = ''
    foot_accound = ''
    all_accound = ''

    header_accound = '''
# [awesome-security-weixin-official-accounts](https://github.com/DropsOfZut/awesome-security-weixin-official-accounts/)
网络安全类公众号推荐，点击名称可快速关注微信公众号

本项目共分为{tag_num}大类，收集公众号{account_num}个。
收集优质文章在[微信聚合平台](http://wechat.doonsec.com)展示。

- [目录分类]()\n'''.format(tag_num=tags_num, account_num=accounts_num)

    for tag in tags:
        tag_name = tag.tag_name
        tag_summary = tag.tag_summary
        header_accound += '	- [{tag_name}](#{tag_name})\n'.format(tag_name=tag_name)
        body_accound += '''

---

## [{tag_name}]({tag_name})\n
{tag_summary}


|公众号||公众号||公众号||公众号|
|:--|:--|:--|:--|:--|:--|:--|
'''.format(tag_name=tag_name, tag_summary=tag_summary)
        for account_list in split_list_average_n(tag.accounts,4):
            for account in account_list:
                accounts_info = accounts_dict.get(account.account_id)
                if accounts_info:
                    body_accound += '|<div style="width: 150pt"><img align="right" width="80" src="{qr_code}" alt="" />**[{account_name}](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={account_biz}#wechat_redirect)**<details><summary>*{summary_short}*</summary> {summary}</details></div>|<img width=1/>'.format(
                        account_name=accounts_info.get('account'), summary_short=accounts_info.get('summary').replace('|','')[0:6],account_biz=accounts_info.get('__biz'),
                        summary=accounts_info.get('summary').replace('|','')[6:],  qr_code=accounts_info.get('qr_code'))
            body_accound+='|\n'

    foot_accound = '''
## Coder
感谢洞见研发工程师参与此项目设计

* [@AJay13](https://github.com/Hatcat123)
* [@Joynice](https://github.com/Joynice)

## Thanks
感谢[@neargle](https://github.com/neargle)对本项目提供无私的帮助

## License
GNU GENERAL PUBLIC LICENSE'''

    all_accound = header_accound + body_accound + foot_accound  # 仓库readme组成部分为头、身体、脚
    with open('wechat.md','w',encoding='utf-8')as f:
        f.write(all_accound)
    return all_accound


# 过滤原链接，清除个人链接的信息
def url_remove_info(wechat_url):
    '''
    chksm\scene\sessionid\key 去除这个可能代表个人的信息
    :param wechat_url: https://mp.weixin.qq.com/s?__biz=MzU4ODQ3NTM2OA==&mid=2247486203&idx=1&sn=3f48ca14c061ea44aac924eb8e6786f1&chksm=fddd747ccaaafd6ad0889cbf80d22e7cf1e4692a118cae776c46b803130353f993c95125ace8&scene=126&sessionid=1598928777&key=1fb38d1ad08361bbdf714d126c3e54
    :return: https://mp.weixin.qq.com/s?__biz=MzU4ODQ3NTM2OA==&mid=2247486203&idx=1&sn=3f48ca14c061ea44aac924eb8e6786f1
    '''
    pattern = '&chksm=.*&scene=\d+&sessionid=\d+&key=.*'
    no_info_url = re.sub(pattern=pattern, repl='', string=wechat_url)
    return no_info_url


# 过滤原链接，清除个人链接的信息
def url_remove_session(wechat_url):
    '''
    chksm\scene\sessionid\key 去除这个可能代表个人的信息
    :param wechat_url: https://mp.weixin.qq.com/s?__biz=MzU4ODQ3NTM2OA==&mid=2247486203&idx=1&sn=3f48ca14c061ea44aac924eb8e6786f1&chksm=fddd747ccaaafd6ad0889cbf80d22e7cf1e4692a118cae776c46b803130353f993c95125ace8&scene=126&sessionid=1598928777&key=1fb38d1ad08361bbdf714d126c3e54
    :return: https://mp.weixin.qq.com/s?__biz=MzU4ODQ3NTM2OA==&mid=2247486203&idx=1&sn=3f48ca14c061ea44aac924eb8e6786f1
    '''
    pattern = '&scene=\d+&sessionid=\d+&key=.*'
    no_info_url = re.sub(pattern=pattern, repl='', string=wechat_url)
    return no_info_url + '&scene=27#wechat_redirect'

## 将一个列表,分成若干个大小为n的列表
def split_list_average_n(origin_list, n):
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]
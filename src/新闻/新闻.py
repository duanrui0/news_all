# ********************************************************************
# Author: deep as sea
# Create by: 2023/12/20
# Description: 
# Update: Task Update Description
# ********************************************************************
# -*- coding: utf-8 -*-
# 
#                     _ooOoo_
#                    o8888888o
#                    88" . "88
#                    (| -_- |)
#                     O\ = /O
#                 ____/`---'\____
#               .   ' \\| |// `.
#                / \\||| : |||// \
#              / _||||| -:- |||||- \
#                | | \\\ - /// | |
#              | \_| ''\---/'' | |
#               \ .-\__ `-` ___/-. /
#            ___`. .' /--.--\ `. . __
#         ."" '< `.___\_<|>_/___.' >'"".
#        | | : `- \`.;`\ _ /`;.`/ - ` : | |
#          \ \ `-. \_ __\ /__ _/ .-` / /
#  ======`-.____`-.___\_____/___.-`____.-'======
#                     `=---='
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#          佛祖保佑       永无BUG
import re
import json
from datetime import datetime
import lunar
import jsonpath
from scrapy import Selector
'''自动提取：标题、作者、发布时间、正文'''


class ExtractAuto:
    def __init__(self):
        self.html = ''
        self.title_re = [
            re.compile(r'<title>(.*)</title>'),
            r'-[\u4e00-\u9fa5 ]|_[\u4e00-\u9fa5 ]'
        ]
        self.publish_time_re = [
            re.compile(r'[：:"]?(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)[T\s]?(\d{2}:\d{2}:?\d{0,2})?["\s+<\+]?'),
            re.compile(r'>([今昨前\d]?天前?)(\s?\d{1,2}:\d{2})?')
        ]
        self.content_path = '//p[last()>2]//text()'

        self.author_re = [
            re.compile(r'作者[：:]([^\n\t&<\$\{]{2,8})[\s+]?')
        ]

    def init_html(self, html):
        self.html = html

    # 自动提取新闻 标题、发布时间、正文
    def get_news(self, html=None):
        html = html if html else self.html
        title, publish_time, content = self.get_title(html), self.get_publish_time(html), self.get_content(html)
        obj = {
            'title': title if title else '',
            'publish_time': publish_time if publish_time else '',
            'content': content if content else ''
        }
        return obj

    # 标题
    def get_title(self, html=None):
        html = html if html else self.html
        date_list = []
        result = self.title_re[0].findall(html)
        # print(f'html_title:{result}')
        if len(result) > 0:
            date_list.append(''.join(re.split(self.title_re[1], result[0])[:1]))
        result = date_list[0] if len(date_list) > 0 else ''
        return result

    # 发布时间
    def get_publish_time(self, html=None):
        html = html if html else self.html
        date_list = []
        result = self.publish_time_re[0].findall(html)
        if len(result) > 0:
            date_list.append(' '.join(result[0]))
        result = self.publish_time_re[1].findall(html)
        if len(result) > 0:
            date_list.append(' '.join(result[0]))
            # print(date_list)
        result = date_list[0] if len(date_list) > 0 else ''
        return result

    # 正文
    def get_content(self, html=None):
        html = html if html else self.html
        date_list = []
        selector = Selector(text=html)
        result = selector.xpath(self.content_path).extract()
        # print(len(result), result)
        if len(result) > 0:
            date_list.append('\n'.join(result).replace('\u3000', '').strip())
        result = date_list[0] if len(date_list) > 0 else ''
        return result

    # 作者
    def get_author(self, html=None):
        html = html if html else self.html
        date_list = []
        result = self.author_re[0].findall(html)
        # print(f'html_author:{result}')
        if len(result) > 0:
            date_list.append(''.join(re.split(self.title_re[1], result[0])[:1]))
        result = date_list[0] if len(date_list) > 0 else ''
        return result


if __name__ == '__main__':
    import requests
    auto = ExtractAuto()
    url_list =[
        # 'https://www.dcdapp.com/article/6853790625674822155'
        'https://k.sina.com.cn/article_5974491597_1641b81cd00100zmex.html?from=auto',
        'https://www.pcauto.com.cn/qcbj/bozhou/znbj/2007/21426798.html'
        # 'https://chejiahao.autohome.com.cn/info/6573119#pvareaid=28086821202',
        # 'https://www.bilibili.com/read/cv6150098?from=search',
        # 'http://news.cheshi.com/dujia/20200721/3262814.shtml',
        # 'http://www.laixinews.com/epaper/Html/2020-7-28/59056.html',
        # 'https://hj.pcauto.com.cn/article/451489.html',
        # 'https://www.autohome.com.cn/culture/202007/1018313.html#pvareaid=102624',
        # 'https://k.sina.com.cn/article_1912222221_p71fa320d02700mhkn.html?from=auto&subch=oauto#p=1'
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
               "Content-Type": "application/json"}
    current_time = datetime.now()
    current_lunar = lunar.Lunar(year=current_time.year, month=current_time.month, day=current_time.day)
    formatted_time = current_time.strftime("%Y年 %m月 %d日 星期%A,农历%d月%d日")
    formatted_time = formatted_time % (
    current_time.year, current_time.month, current_time.day, current_time.weekday(), current_lunar.month,
    current_lunar.day)

    # print(formatted_time)

    for i, v in enumerate(url_list):
        res = requests.get(v, headers=headers)
        res.encoding = res.apparent_encoding
        if res.status_code != 200:
            print(f'code:{res.status_code}, history:{res.history}')
        html = res.text
        auto.init_html(html=html)
        title = ''
        publish_time = ''
        content = ''
        title = auto.get_title()
        publish_time = auto.get_publish_time()
        content = auto.get_content()
        author = auto.get_author()
        # print(html)
        print(f'{i},作者：【{author}】 标题：【{title}】  发布时间：【{publish_time}】  正文：【{content[:30]}...{content[-30:]}】')
        print(formatted_time)

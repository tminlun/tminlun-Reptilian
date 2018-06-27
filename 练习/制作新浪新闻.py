"""
    爬取时间、链接和内容
    2018/5/16
"""

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def get_page_index(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
               }
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            res.encoding = 'gzip'
            return res.text
        return None
    except RequestException:
        return None



def parse_all_page(html):
    soup = BeautifulSoup(html,"html.parser")
    title = soup.select('.main-title')
    dt = soup.select('.date')
    newssource  =soup.select('#top_bar > div > div.date-source > a')[0].get_text()
    join = soup.select('#top_bar > div > div.date-source > a')[0]['href']
    article =' '.join([p.get_text().rstrip('\n\n点击进入专题：\n政要·新浪新闻|聚焦政要 关注人事 汇聚新政责任编辑：张玉') for p in soup.select('.article')])

    for title,dt in zip(title,dt):
        data = {
            'title':title.get_text(),
            'dt':dt.get_text().strip(' '),
            'newssource':newssource,
            'join':join,
            'article':article.strip(),
        }
        print(data)

def getResulTtotal(url):
    m = re.search('doc-i(.*?).shtml',url)
    newsid = m.group(1)
    comments = requests.get(newsURL.format(newsid)) #取得评论的网址
    print(type(comments))


if __name__ == '__main__':
    newsURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=0&compress=0&ie=gbk&oe=gbk&page=1&page_size=20'
    url = 'http://news.sina.com.cn/c/2018-05-27/doc-ihcaqueu7685091.shtml'
    html = get_page_index(url)
    parse_all_page(html)
    getResulTtotal(url)





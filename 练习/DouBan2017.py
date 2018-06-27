"""
    爬取豆瓣读书2017top
    2018/6/3
"""
import requests
from requests.exceptions import RequestException
import json
import time

def get_page_url(url):
    headers={
        'User - Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            return res
        return None
    except RequestException:
        return None

def parse_page_html(html):
    try:
        jd = html.json()['res']['subjects']
        for i in jd:
            images = i.get('cover')
            url = i.get('url')
            score = i.get('rating')
            title = i.get('title')
            yield {
                'title': title,
                'images':images,
                'score':score,
                'url':url,
            }
    except KeyError:
        pass


def main(url):
    html = get_page_url(url)
    for ent in parse_page_html(html):
        print(ent)


if __name__ == '__main__':
    urls = ['https://book.douban.com/ithil_j/activity/book_annual2017/widget/{}'.format(str(i)) for i in range(1,47)]
    for url in urls:
        main(url)
        time.sleep(1)
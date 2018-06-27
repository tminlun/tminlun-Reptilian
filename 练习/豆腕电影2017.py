"""
    爬取豆腕2017度电影
    2018/5/31
"""
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import json
import time



def get_url(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res
        return None
    except RequestException:
        return None


def parse_page(html):
    try:
        jd = html.json()['res']['subject']
        rating = jd.get('rating')
        url =  jd.get('url')
        name = jd.get('title')
        type = jd.get('type')

        yield {
            '类型':type,
            '名字': name,
            '评分': rating,
            '网址': url,
        }
    except:
        pass

def write_to_movie(content):
    with open('movie.text','a') as f:
        f.write(json.dumps(content)+'\n')
        f.close()

def main(url):
    html = get_url(url)
    for i in parse_page(html):
        print(i)
        write_to_movie(i)

if __name__ == '__main__':
    urls = ['https://movie.douban.com/ithil_j/activity/movie_annual2017/widget/{}'.format(str(i)) for i in range(2,89)]
    #url = 'https://movie.douban.com/ithil_j/activity/movie_annual2017/widget/88'
    for url in urls:
        main(url)
        time.sleep(1)

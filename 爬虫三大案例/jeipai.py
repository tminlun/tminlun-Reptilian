"""
    爬取今日头条的街怕图片
    2018/5/25
    parse.urlencode(data) 功能：将字典形式的数据转化成查询字符串
    yield就对应每一次的单步调试，并获取当前的变量值
"""
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import re


def get_page_index(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    try:
        response = requests.get(url,headers=headers)#获取网址
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        print('请求网页异常')
        return None

def parse_page_index(html):
        jd = html.json()['data']#将网址转换成字典对象
        for item in jd:
            url = item.get('article_url')  # 把所有的article_url提取出来
            title = item.get('title')
            image = item.get('image_list')

            yield {
                    'url':url,
                    'title':title,
                    'image':image,
                }

"""
#得到详细的url，除去没用的网页
def get_page_detail(url):
    try:
        response = requests.get(url)#获取网址
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求页面出错")
        return None
#解析详细的url，得到里面的照片
def parse_page_detail(url):
    try:
        res = get_page_detail(url)
        soup = BeautifulSoup(res,'html.parser')
        title = soup.select('.title')
        print(title)
    except TypeError:
        pass
"""
def main(url):
    html = get_page_index(url)#网址
    for url in parse_page_index(html):
        print(url)
        # parse_page_detail(url)

if __name__ == '__main__':
    urls = ['https://www.toutiao.com/search_content/?offset=20&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab'.format(str(i)) for i in range(0,140,20)]
    for url in urls:
        main(url)

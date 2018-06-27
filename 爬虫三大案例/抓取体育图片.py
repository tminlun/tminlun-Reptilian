"""
    抓取体育图片
    2018/5/25

"""
import requests
from requests.exceptions import RequestException
from urllib import parse

def get_page_tiyu(offset,keyword):
    data = {
        'offset': 'offset',
        'format': 'json',
        'keyword': 'keyword',
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?' + parse.urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200: #如果获取网址成功
            return response.text
        return None
    except RequestException:
        print("获取网址失败")
        return None

def main():
    html = get_page_tiyu(0,'体育')
    print(html)

if __name__ == '__main__':
    main()
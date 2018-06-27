"""
    爬取美团广州的酒店
    2018/6/1
"""
import requests
from requests.exceptions import RequestException
import json
import pandas
import openpyxl
import time
import xlwt
from xlrd import open_workbook


def get_url(url):
    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res
        return None
    except RequestException:
        return None

def parse_all_page_(html):
    try:
        jd = html.json()['data']['searchresult']
        for i in jd:
            addr = i.get('addr')
            commentsCountDesc = i.get('commentsCountDesc')
            poiLastOrderTime = i.get('poiLastOrderTime')
            scoreIntro = i.get('scoreIntro')
            name = i.get('name')
            lowestPrice = i.get('lowestPrice')
            yield {
                '名字':name,
                '最低价格':lowestPrice,
                '评分': scoreIntro,
                '具体地址':addr,
                '评论数':commentsCountDesc,
                '订货时间':poiLastOrderTime,
            }
    except:
        pass

def write_meituan_Hotel(ent):
    with open('meituan_Hotel.text','a') as f:
        f.write(json.dumps(ent)+'\n')
        f.close()




def main(url):
    html = get_url(url)
    for ent in parse_all_page_(html):
        print(ent)
    #     newsary = ent
    #     new_total.extend(newsary)#extend() 函数用于在列表末尾一次性追加另一个列表
    # df = pandas.DataFrame(new_total)
    # df.to_excel('meituan_Hotel.xlsx')




if __name__ == '__main__':
    #time.strftime('%Y%m%d)格式化时间，time.localtime(time.time())获取当前时间
    time_day = time.strftime('%Y%m%d',time.localtime(time.time()))
    urls = ['https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=A78BEA191031084B7AA48663918205B6153FAA3F76DB7FA6DD0BAB2526A7319C%401529079245650&cityId=20&offset={}&limit=20&startDay={}&endDay={}&q=&sort=defaults&X-FOR-WITH=VWN5sf8%2Fp55TlZotLZddLPdi%2Fdc7FIxH5q%2BbvHUQvcUXw5%2FuOw1e2oyG9b5g7HC88W9R28JqQMPjdkmXVudRk4DOg'.format(str(i),time_day,time_day) for i in range(20,580,20)]
    for url in urls:
        main(url)




"""
    爬取美团
    2018/5/19
    修改：
    1.追写电子表格
    2.优化爬虫速度
    by：pig
"""

import requests
from requests.exceptions import RequestException
import json
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import time

COUNT = 1  # 计数器


def get_html(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 53.0.2785.104Safari / 537.36Core / 1.53.5006.400QQBrowser / 9.7.13114.400'
    }
    try:
        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            html.encoding = 'uft-8'
            return html
        return None
    except RequestException:
        return None


def get_info(url):
    dict_list = []
    html = get_html(url)
    c = html.json()['data']['searchresult']
    for i in c:
        name = i.get('name')
        price = i.get('originalPrice')
        posdescr = i.get('posdescr')
        addr = i.get('addr')
        scoreIntro = i.get('scoreIntro')
        yield {
            'name': name,
            'price': price,
            'posdescr': posdescr,
            'addr': addr,
            'scoreIntro': scoreIntro
        }


def write_excel(write_dict):
    rexcel = open_workbook("OK.xls")  # 打开excel文件
    rows = rexcel.sheets()[0].nrows  # 获取最后一行
    excel = copy(rexcel)  # 复制excel
    table = excel.get_sheet(0)  # 写对象
    for key, value in write_dict.items():
        if key == "name":
            table.write(rows, 0, value)
        elif key == "price":
            table.write(rows, 1, value)
        elif key == "posdescr":
            table.write(rows, 2, value)

        elif key == "addr":
            table.write(rows, 3, value)

        elif key == "scoreIntro":
            table.write(rows, 4, value)

        else:
            pass
    # 保存
    excel.save('OK.xls')


def write_header(excel_name):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(str(excel_name))

    # 设置表头
    worksheet.write(0, 0, label='name')
    worksheet.write(0, 1, label='price')
    worksheet.write(0, 2, label='posdescr')
    worksheet.write(0, 3, label='addr')
    worksheet.write(0, 4, label='scoreIntro')
    workbook.save('ok.xls')


def main(page):
    global COUNT  # 全局变量计数器
    time_day = time.strftime('%Y%m%d', time.localtime(time.time()))
    url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=A78BEA191031084B7AA48663918205B6153FAA3F76DB7FA6DD0BAB2526A7319C%401527839102863&cityId=20&offset={}&limit=20&startDay={}&endDay={}&q=& ort=defaults' \
        .format(str(page), time_day, time_day)
    #https: // ihotel.meituan.com / hbsearch / HotelSearch?utm_medium = pc & version_name = 999.9 & cateId = 20 & attr_28 = 129 & uuid = A78BEA191031084B7AA48663918205B6153FAA3F76DB7FA6DD0BAB2526A7319C % 401527839102863 & cityId = 20 & offset = {} & limit = 20 & startDay = {} & endDay = {}& q = & sort = defaults
    for i in get_info(url):
        write_excel(i)
        COUNT += 1
        if COUNT % 10 == 0:
            print('已经完成%s条数据爬取' % COUNT)


if __name__ == '__main__':
    write_header('酒店')
    for i in range(0, 200, 20):
        main(i)
    print("by_pig")
    time.sleep(5)
"""
    多进程爬虫
    pool = Pool(processes=4)python进程时
     pool.map(func,iterable)  func:运行爬虫的参数, iterable:迭代参数，传入url
    2018/5/31
"""
import requests
import time
from multiprocessing import Pool#导入多进程
import re


def re_scraper(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    names = re.findall('<h2>(.*?)</h2>',res.text,re.S)#名字
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>',res.text,re.S)#内容
    laughs = re.findall('<span class="stats-vote">.*?<i class="number">(\d+)</i> 好笑',res.text,re.S)#好笑
    comments = re.findall('<i class="number">(\d+)</i> 评论',res.text,re.S)#评论
    for names,contents,laughs,comments in zip(names,contents,laughs,comments):
        yield {
            '用户名':names.strip(),
            '内文':contents.strip(),
            '好笑':laughs,
            '评论':comments,
        }

def main(url):#记得定义main方法遍历爬虫参数
    for i in re_scraper(url):
        print(i)

if __name__ == "__main__":
    urls = ['https://www.qiushibaike.com/hot/page/{}/'.format(str(i)) for i in range(1,14)]
    start_1 = time.time()
    for url in urls:
        main(url)
        time.sleep(1)
    end_1 = time.time()
    print('耗时：',end_1 - start_1)
    #多进程
    start_2 = time.time()
    pool = Pool(processes=4)
    pool.map(re_scraper,urls)
    end_2 = time.time()
    print('4进制爬虫耗时：',end_2 - start_2)



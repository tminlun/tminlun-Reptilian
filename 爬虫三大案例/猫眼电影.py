"""
    爬取猫眼电影
    2018/5/26
    re.search(pattern, string) 扫描整个字符串并返回第一个成功的匹配
    compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，
    供 findall() 和 search() 这两个函数使用
    re.findall: 在字符串中找到正则表达式所匹配的 所有 子串，并返回一个列表
    yield：获取当前的变量值
"""
import requests
from requests.exceptions import RequestException
import re#正则表达式
import json
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
def get_one_page(url):
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html): #对网页进行解析
    # .*?任意字符串,\d+代表数字,注意提取每一个元素都要加 结束符
    #re.S表示任意的字符，如果不加re.S  点（.）就无法匹配换行符
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name">'
                          +'.*?">(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                          +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)

    items = re.findall(pattern,html)#在字符串找到正则表达式所有的字符，返回一个列表
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'name':item[2].strip(),
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6],
        }
#保存进文件
def write_to_file(content):
    with open('result.text','a') as f:
        f.write(json.dumps(content)+'\n') #将字典转换为字符串，每一个电影内容记得换行
        f.close()


def main(url): #功能用于调用其他函数给主函数调用

    html = get_one_page(url)
    for item in parse_one_page(html):#遍历出每一个字典，有很多电影，要遍历全部电影的内容
        print(item)#输出字典
        write_to_file(item)



if __name__ == '__main__':
    #列表出所有的电影网址
    urls = ['http://maoyan.com/board/4?offset={}'.format(str(i)) for i in range(0, 100)]
    for url in urls:
            main(url)
            time.sleep(1)





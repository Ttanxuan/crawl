# encoding  = utf-8
import requests as re
from lxml import etree

#获得页面内容
url = "https://movie.douban.com/chart"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
resp = re.get(url, headers=headers)
resp.encoding = 'utf-8'

#xpath解析
html = etree.HTML(resp.text)
'''
/html/body/div[3]/div[1]/div/div[1]/div/div
/html/body/div[3]/div[1]/div/div[1]/div/div/table/tbody/tr/td[2]/div/a/text() 
页面检查时发现有tbody，而页面源代码中没有tbody，所以正确的xpath路径为：
/html/body/div[3]/div[1]/div/div[1]/div/div/table/tr/td[2]/div/a/text()
'''
divs = html.xpath("/html/body/div[3]/div[1]/div/div[1]/div/div")
name = []
for div in divs:
    name1 = div.xpath("./table/tr/td[2]/div/a/text()")

#去除空白
for i in name1:
    if i !=  '\n                    ':
        name.append(i[25:-27])

print(name)

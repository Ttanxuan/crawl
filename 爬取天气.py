# encoding  = utf-8
import requests as re
from bs4 import BeautifulSoup

url = "http://weather.cma.cn/web/weather/57678.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
resp = re.get(url, headers=headers)
resp.encoding = 'utf-8'

# 获取全部的天气信息
bfs = BeautifulSoup(resp.text, "html.parser")
divs = bfs.find("div", class_="row hb days")

'''one_day = divs.find_all("div", class_="pull-left day actived")
week_1 = divs.find("div", class_="day-item").text    #find得到的type结果为bs4.element.Tag，.text后得到的结果为str类型
other_days = divs.find_all("div", class_="pull-left day")    #find_all得到的结果为bs4.element.ResultSet类型
weather_1 = other_days[1]'''

#创建列表储存数据
week = []
date = []
high_weather = []
low_weather = []
high_temp = []
low_temp = []

data = divs.find_all("div", class_="day-item")    #得到星期、日期、天气变化
high = divs.find_all("div", class_="high")    #得到最高温度
low = divs.find_all("div", class_="low")    #得到最低温度
for i in range(7):
    date1 = data[i*10].text
    week1 = date1[10:13]
    date2 = date1[23:28]
    week.append(week1)
    date.append(date2)
    high_weather.append(data[i*10+2].text[10:12])
    high_temp.append(high[i].text[12:15])
    low_weather.append(data[i*10+7].text[10:12])
    low_temp.append(low[i].text[12:15])
    print(week[i], date[i], low_weather[i], high_weather[i], low_temp[i], high_temp[i])

#print(high_weather)
